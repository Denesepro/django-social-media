from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation


# Create your views here.
class UserRegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'successfully created!', 'success')
            user = authenticate(request, username=cd['username'], password=cd['password1'])
            login(request, user)
            return redirect('home:index')
        return render(request, 'account/register.html', {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.next = request.GET.get('next')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'successfully Logged in!', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:index')
            else:
                messages.error(request, 'wrong info!', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'successfully logged out!', 'success')
        return redirect('home:index')


class UserProfileView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        post = user.posts.all()
        is_following = None
        if request.user.is_authenticated:
            relation = Relation.objects.filter(from_user=request.user, to_user=user)
            if relation.exists():
                is_following = True
        return render(request, 'account/profile.html', {'user': user, 'post': post, 'is_following': is_following})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'You Already Followed!', 'warning')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'You Followed Successfully!', 'success')

            return redirect('account:user_profile', user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'You Unfollowed Successfully!', 'success')
        else:
            messages.error(request, 'You are not Following this User!', 'warning')
        return redirect('account:user_profile', user.id)
