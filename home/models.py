from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  #pak shodan abshari
    body = models.TextField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', 'body']

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('home:post_detail', kwargs={self.id, self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.body[:30])
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='p_comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='r_comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}--->{self.body[:30]}'

    class Meta:
        ordering = ['-created', 'body']