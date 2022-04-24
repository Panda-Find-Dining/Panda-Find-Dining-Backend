from django.shortcuts import render
from .models import User, Restaurant, Meal
from .serializers import UserSerializer, RestaurantSerializer, MealSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics


class MealViewSet(ModelViewSet):
    '''
    List all meals with answers:      GET / meals /
    Retrieve a specific meal:         GET / meals / {id}
    Add a new meal:                   POST / meals /
    Update an existing meal:          PUT / meals / {id}
    Update part of an existing meal:  PATCH / meals / {id}
    Remove a meal:                    DELETE / meals / {id} /
    '''
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_class = [AllowAny]
