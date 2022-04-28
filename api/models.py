from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        REQUIRED_FIELDS = ['username', 'password']
        return user


class User(AbstractUser):
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='User', blank=True)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User username={self.username} pk={self.pk}>"


class Restaurant(models.Model):
    name = models.CharField(blank=False, max_length=100)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    formatted_address = models.CharField(max_length=300)
    place_id = models.CharField(max_length=300)
    hours = models.CharField(max_length=200, blank=True)
    business_status = models.CharField(max_length=200, blank=True)
    icon = models.URLField(blank=True)
    meal = models.ForeignKey(
        'Meal', on_delete=models.CASCADE, related_name="meal")

    def __str__(self):
        return self.name


class Meal(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator")
    created_date = models.DateTimeField(auto_now_add=datetime.now)
    invitee = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='invitee')
    location = models.CharField(blank=True, null=True, max_length=100)
    radius = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    # restaurant = models.ForeignKey(Restaurant, blank=True, null=True, on_delete=models.CASCADE, related_name="restaurant")

    def __str__(self):
        return self.location
