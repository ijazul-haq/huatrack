from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.CharField(max_length=255, null=True, blank=True)
    private_key = models.CharField(max_length=255, null=True, blank=True)
    dp = models.ImageField(verbose_name='dp', upload_to='dp', blank=True, null=True)


class Artwork(models.Model):
    title = models.CharField(max_length=255)
    created = models.CharField(max_length=255)
    timestamp = models.DateTimeField(max_length=255)
    artist = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    path = models.ImageField(verbose_name='path', upload_to='artwork', blank=True, null=True)
    txid = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
