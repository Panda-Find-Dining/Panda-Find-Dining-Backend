from calendar import c
from django.shortcuts import render
from .models import User, Restaurant, Meal
from .serializers import UserFriendSerializer, UserSerializer, RestaurantSerializer, MealSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from .permissions import IsOwnerOrReadOnly
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic.list import ListView
from rest_framework.generics import ListAPIView
from django.conf import settings
import responses
import googlemaps
import requests
from findDining.settings import GOOGLE_MAPS_API_KEY as google_api_key
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend


class MealViewSet(ModelViewSet):
    '''
    This ViewSet creates the following endpoints:

    List all meals with answers:      GET / meals /
    Retrieve a specific meal:         GET / meals / {id}
    Add a new meal:                   POST / meals /
    Update an existing meal:          PUT / meals / {id}
    Update part of an existing meal:  PATCH / meals / {id}
    Remove a meal:                    DELETE / meals / {id} /
    '''
    # breakpoint()
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RestaurantViewSet(ModelViewSet):
    '''
    This ViewSet creates the following endpoints:

    List all restaurants with answers:      GET / restaurants /
    Retrieve a specific restaurant:         GET / restaurants / {id}
    Add a new restaurant:                   POST / restaurants /
    Update an existing restaurant:          PUT / restaurants / {id}
    Update part of an existing restaurant:  PATCH / restaurants / {id}
    Remove a restaurant:                    DELETE / restaurants / {id} /
    '''
    # breakpoint()
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Searching
class UserSearchView(generics.ListAPIView):
    '''
    This view will search all usernames for the query parameter
    passed in by the URL.

    ex: Lookup Input Field [john wick]
    url would look like:
    /api/search/?q=john+wick
    '''
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = User.objects.all()
        # breakpoint()
        friend_username = self.request.query_params.get('q')
        if friend_username is not None:
            queryset = queryset.filter(username__icontains=friend_username)
        return queryset


# Follow/Unfollow
class SaveFriendView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(request, self, pk, format=None):
        current_profile = self.user
        other_profile = pk
        current_profile.friends.add(other_profile)

        return Response({"Requested": "Save request has been sent!!"}, status=status.HTTP_200_OK)


class DeleteFriendView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(request, self, pk, format=None):
        current_profile = self.user
        other_profile = pk
        current_profile.friends.remove(other_profile)

        return Response({"Requested": "Deleted!"}, status=status.HTTP_200_OK)


class UserSearchResultsView(ListView):
    '''
    This view utilizes a PostGres Full Text Search in order to return a
    list of users based on the string input in the UI form.

    This will search username, first name and last name of all users

    ex: Lookup Input Field [john wick]
    url would look like:
    /api/search/?q=john+wick
    '''
    model = User
    context_object_name = "user"

    def get_queryset(self):
        query = self.request.GET.get("q")

        return User.objects.annotate(search=SearchVector("username", "first_name", "last_name")).filter(
            search=query
        )


class UserList(generics.ListAPIView):
    '''
    Return a list of all the users registered to use the application
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Update or delete details for a single user
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserMealList(generics.ListAPIView):
    '''
    Get a list of all the users Meals
    '''
    serializer_class = MealSerializer
    model = Meal
    
    def get_queryset(self):
        user = self.request.user
        return Meal.objects.filter(Q(invitee=user) | Q(creator_id=user)).order_by('-created_date')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserFriendsList(generics.ListAPIView):
    '''
    Return a list of all a users friends as a slug
    '''
    # queryset = User.objects.all()
    serializer_class = UserFriendSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        filters = Q(id=self.request.user.pk)
        return User.objects.filter(filters)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoogleAPICall(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(request, self, pk, format=None):
        this_meal = Meal.objects.get(id=pk)

        def get_restaurants():
            print(this_meal)
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants%20in%20{this_meal.location}%20NorthCarolina&key={google_api_key}"
            response = requests.get(url)
            data = response.json()
            restaurants = data['results']
            for i in restaurants:
                restaurant_data = Restaurant(
                    name=i['name'],
                    formatted_address=i['formatted_address'],
                    place_id=i['place_id'],
                    business_status=i['business_status'],
                    icon=i['icon'],
                    meal=this_meal
                )
                restaurant_data.save()

        get_restaurants()
        
        return Response({"Requested": "Restaurants Added"}, status=status.HTTP_200_OK)


class UserFriendsList(generics.ListAPIView):
    '''
    Return a list of all a users friends as a slug
    '''
    # queryset = User.objects.all()
    serializer_class = UserFriendSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        filters = Q(id=self.request.user.pk)
        return User.objects.filter(filters)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class Yes(APIView):
    '''
    This view will post the current users name to the restaurants list of 'yes's'
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(request, self, pk,format=None):    
            current_user = self.user
            current_restaurant = Restaurant.objects.get(id=pk)
            current_restaurant.yes.add(current_user)

            return Response({"Requested" : "You have said YES to this restaurant!"},status=status.HTTP_200_OK)
            


class No(APIView):
    '''
    This view will post the current users name to the restaurants list of 'no's'
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(request, self, pk,format=None):    
            current_user = self.user
            current_restaurant = Restaurant.objects.get(id=pk)
            current_restaurant.no.add(current_user)

            return Response({"Requested" : "You have said NO to this restaurant!"},status=status.HTTP_200_OK)