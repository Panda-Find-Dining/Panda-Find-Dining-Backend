from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='User')

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User username={self.username} pk={self.pk}>"


class Restaurant(models.Model):
    name = models.CharField(blank=False, max_length=100)
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)
    formatted_address = models.CharField(max_length=300)
    place_id = models.CharField(max_length=300)
    hours = models.CharField(max_length=200, blank=True)
    business_status = models.BooleanField(default=True)
    icon = models.URLField(blank=True)
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name="meal")

    def __str__(self):
        return self.name


class Meal(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    created_date = models.DateTimeField(auto_now_add=datetime.now)
    invitee = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='invitee')
    location = models.CharField(blank=False, max_length=100)
    radius = models.IntegerField(blank=True)
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)
    restaurant = models.ForeignKey(Restaurant, blank=True, null=True, on_delete=models.CASCADE, related_name="restaurant")
    

    def __str__(self):
        return self.name