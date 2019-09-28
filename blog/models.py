from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class SurveyHistory(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    record = models.BooleanField()
    recorded_date = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.post.title
