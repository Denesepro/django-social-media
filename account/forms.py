from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter Your Email:','class':'form-control'}))
    password1 = forms.CharField(label='Enter Your Password:' , widget=forms.PasswordInput(attrs={'placeholder':'Enter Your Password','class':'form-control'}))
    password2 = forms.CharField(label='Enter Your Password again:' ,  widget=forms.PasswordInput(attrs={'placeholder':'Enter Your Password again','class':'form-control'}))
    
    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('email exists!')
        return email
    def clean(self):
            cd=super().clean()
            p1 = cd.get('password1')
            p2 = cd.get('password2')
            if p1 and p2 and p1 != p2:
                raise ValidationError('password must match!')
    def clean_username(self):
        username=self.cleaned_data['username']
        user=User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('username exists!')
        return username
    
class UserLoginForm(forms.Form):
    username = forms.CharField( label= 'Username or Email:' ,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Enter Your Password:' , widget=forms.PasswordInput(attrs={'placeholder':'Enter Your Password','class':'form-control'}))