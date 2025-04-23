from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .models import Post , Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CreatePostForm, PostUpdateForm , CommentCreateForm


# Create your views here.
# def index(request):
#     return render(request , 'home/index.html' , {})

class HomeView(View):
    def get(self, request):
        post = Post.objects.all()
        return render(request, 'home/index.html', {'post': post})


class PostDetailView(View):
    form_class = CommentCreateForm
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        comments = post.p_comments.filter(is_reply=False)
        return render(request, 'home/details.html', {'post': post , 'comments': comments , 'form':self.form_class})

    def post(self, request, post_id, post_slug):
        form = self.form_class(request.POST)
        post1 = get_object_or_404(Post, pk=post_id, slug=post_slug)
        if form.is_valid():
            cd = form.cleaned_data
            Comment.objects.create(body=cd['body'], user=request.user , post=post1)
            messages.success(request, 'comment created!', 'success')
        return redirect('home:post_detail', post_id, post_slug )

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'deleted!', 'success')
        else:
            messages.error(request, 'error', 'danger')
        return redirect('home:index')


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        create = CreatePostForm()
        return render(request, 'home/create.html', {'create': create})

    def post(self, request):
        form = CreatePostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Post.objects.create(body=cd['body'], user=request.user)
            messages.success(request, 'created!', 'success')
            return redirect('home:index')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'you cant update this post!', 'danger')
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            messages.success(request, 'updated!', 'success')
        return redirect('home:post_detail', post.id, post.slug)
