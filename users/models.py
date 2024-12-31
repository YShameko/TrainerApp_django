from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Rating(models.Model):
    rate =models.IntegerField(default=0)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
