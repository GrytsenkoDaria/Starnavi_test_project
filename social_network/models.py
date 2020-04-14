from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(unique=True)
    last_activity = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    liked = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)
