import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings


class Farmer(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username


class Crop(models.Model):
    cropname = models.CharField(max_length=200)
    crop_id = models.CharField(max_length=200)
    def __str__(self):
        return self.cropname
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)s
class SelectedCrop(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    cropname = models.CharField(max_length=200)
    date = models.DateField() 
    