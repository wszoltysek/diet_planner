from django.db import models
import datetime


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateField(datetime.datetime.now)
    updated = models.DateField(datetime.datetime.now)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)


