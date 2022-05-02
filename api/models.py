from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import django_filters


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
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name="meal")
    yes_count = models.IntegerField(default=0)
    yes= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voted_yes', blank=True)
    no= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voted_no', blank=True)
    photo_reference = models.CharField(blank=True, max_length=1000)
    user_has_selected = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_has_selected', blank=True)

    def __str__(self):
        return self.name

    def yes_count(self):
        restaurant_id_from_obj = self.id
        restaurant = Restaurant.objects.get(id=restaurant_id_from_obj)
        yes_count = restaurant.yes.all().count()
        # breakpoint()
        return yes_count
        

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

    @property
    def num_of_diners(self):
        
        number_of_creators = 1
        # num_invitees = 1     # get count by querying M2M table 'api_meal_invitee'
        meal_id_from_self = self.id
        meal = Meal.objects.get(id=meal_id_from_self)
        number_of_people_invited = meal.invitee.all().count()
        total_number_people_going_to_eat = number_of_people_invited + number_of_creators

        return total_number_people_going_to_eat