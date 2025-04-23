from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from home.models import Post


class CreatePostForm(forms.Form):
    body = forms.CharField()


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
