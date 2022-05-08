from calendar import c
from django.shortcuts import render, redirect
from .models import User, Restaurant, Meal
from .serializers import UserFriendSerializer, UserSerializer, RestaurantSerializer, MealSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from .permissions import IsOwnerOrReadOnly
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic.list import ListView
from rest_framework.generics import ListAPIView, GenericAPIView
from django.conf import settings
import responses
import googlemaps
import requests
from findDining.settings import GOOGLE_MAPS_API_KEY as google_api_key
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from djoser.conf import django_settings
from djoser.views import UserViewSet

User = get_user_model()


class TokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        custom_response = {
            'token': token.key,
            'user_id': user.id
        }
        return Response(custom_response)


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

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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
        friend_username = self.request.query_params.get('q')
        if friend_username is not None:
            queryset = queryset.filter(username__icontains=friend_username)
        return queryset


class SaveFriendView(APIView):
    '''
    This view will follow a friend
    '''

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(request, self, pk, format=None):
        current_profile = self.user
        other_profile = pk
        current_profile.friends.add(other_profile)

        return Response({"Requested": "Save request has been sent!!"}, status=status.HTTP_200_OK)


class DeleteFriendView(APIView):
    '''
    This view will unfollow a friend
    '''

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

        return User.objects.annotate(search=SearchVector("username", "first_name", "last_name")).filter(search=query)


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
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants%20in%20{this_meal.location}&key={google_api_key}"
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
                    meal=this_meal,
                    photo_reference=i['photos'][0]["photo_reference"],
                    lat=i['geometry']['location']['lat'],
                    lon=i['geometry']['location']['lng']
                )
                restaurant_data.save()

        get_restaurants()

        return Response({"Requested": "Restaurants Added"}, status=status.HTTP_200_OK)


class UserFriendsList(generics.ListAPIView):
    '''
    Return a list of all of a users friends 
    '''
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

    def post(request, self, pk, format=None):
        current_user = self.user
        current_restaurant = Restaurant.objects.get(id=pk)
        current_restaurant.yes.add(current_user)

        return Response({"Requested": "You have said YES to this restaurant!"}, status=status.HTTP_200_OK)


class No(APIView):
    '''
    This view will post the current users name to the restaurants list of 'no's'
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(request, self, pk, format=None):
        current_user = self.user
        current_restaurant = Restaurant.objects.get(id=pk)
        current_restaurant.no.add(current_user)

        return Response({"Requested": "You have said NO to this restaurant!"}, status=status.HTTP_200_OK)


# *****************************************************************************************************
# Making a List of Safe Restaurant Choices
# *****************************************************************************************************

class MatchedRestaurantList(generics.ListAPIView):
    '''
    This list is made up of the places a group of users in a meal 
    has agreed upon as restaurants they would like to eat at.
    '''
    serializer_class = RestaurantSerializer
    model = Restaurant

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        restaurants = Restaurant.objects.filter(meal_id=self.kwargs['pk'])
        meal = Meal.objects.get(id=self.kwargs['pk'])
        number_diners = meal.invitee.all().count()

        greenzone_queryset = restaurants.annotate(restaurant_yes_count=Count(
            'yes')).filter(restaurant_yes_count=number_diners)

        return greenzone_queryset


class RestaurantMatchView(generics.ListAPIView):
    '''
    This view retrieves a queryset with a single value for the matched restaurant
    '''
    serializer_class = RestaurantSerializer
    model = Restaurant

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        restaurants = Restaurant.objects.filter(meal_id=self.kwargs['pk'])
        meal = Meal.objects.get(id=self.kwargs['pk'])
        number_diners = meal.invitee.all().count()
        selected_count = meal.all_users_have_selected.count()

        greenzone_queryset = restaurants.annotate(restaurant_yes_count=Count(
            'yes')).filter(restaurant_yes_count=selected_count)

        # logic for selecting a restaurant from the GreenZone list
        # get pk of first matched restaurant
        match_pk = greenzone_queryset[0].id

        # filter greenzone list by the pk of the first match
        match_queryset = greenzone_queryset.filter(id=match_pk)

        return match_queryset


class MealRestaurantList(generics.ListAPIView):
    '''
    Get a list of all the restaurants associated with a meal
    '''
    serializer_class = RestaurantSerializer
    model = Restaurant

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user

        filter_parameters = Restaurant.objects.filter(
            Q(meal_id=self.kwargs['pk']))

        return filter_parameters


class UserSelectedView(APIView):
    '''
    This view will post the current users name to the restaurants list of 'yes's'
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(request, self, pk, format=None):
        current_user = self.user
        current_meal = Meal.objects.get(id=pk)
        current_meal.yes.add(current_user)

        return Response({"Requested": "You have updated your selection status for this meal"}, status=status.HTTP_200_OK)


class Pending(generics.ListAPIView):
    '''
    This view will show you a list of pending meals 
    '''
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        filters = (Q(creator=self.request.user) | Q(
            invitee__pk=self.request.user.pk)) & Q(match=False)
        pending = Meal.objects.filter(filters).distinct()
        return pending

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Match(generics.ListAPIView):
    '''
    This view will show you a list of matched meals 
    '''
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        filters = (Q(creator=self.request.user) | Q(
            invitee__pk=self.request.user.pk)) & Q(match=True)
        match = Meal.objects.filter(filters).distinct()
        return match

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeclineMeal(APIView):
    '''
    This view will Decline your meal 
    '''

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(request, self, pk, format=None):
        current_user = self.user
        current_meal_creator = self.user.pk
        current_meal = Meal.objects.get(id=pk)
        current_user.invitee.remove(current_meal)

        if current_meal.creator.pk == current_meal_creator:
            current_meal.archive = True
            current_meal.save()

        return Response({"Requested": "You have declined the meal!"}, status=status.HTTP_200_OK)


class UndoYes(APIView):
    '''
    This view will undo your option YES if you accidently hit the yes
    '''

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(request, self, pk, format=None):
        current_user = self.user
        current_restaurant = Restaurant.objects.get(id=pk)
        current_user.voted_yes.remove(current_restaurant)

        return Response({"Requested": "You have changed your mind from yes!"}, status=status.HTTP_200_OK)


class UndoNo(APIView):
    '''
    This view will undo your option NO if you accidently hit the no
    '''

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(request, self, pk, format=None):
        current_user = self.user
        current_restaurant = Restaurant.objects.get(id=pk)
        current_user.voted_no.remove(current_restaurant)

        return Response({"Requested": "You have changed your mind from no!"}, status=status.HTTP_200_OK)

    def post(request, self, pk, format=None):
        current_user = self.user
        current_restaurant = Restaurant.objects.get(id=pk)
        current_restaurant.yes.add(current_user)

        return Response({"Requested": "You have said YES to this restaurant!"}, status=status.HTTP_200_OK)


class SelectedAndMatch(APIView):
    '''
    This view will give you a  match after selecting restaurants
    '''
    def get(request, self, pk, format=None):
        current_user = self.user
        current_meal = Meal.objects.get(id=pk)
        current_meal.all_users_have_selected.add(current_user)
        current_meal.save()
        select_count = current_meal.all_users_have_selected.count()
        if select_count == (current_meal.invitee.count() + 1):
            current_meal.match = True
            current_meal.save()

        return Response({"Requested": "You selected and done a match check!"}, status=status.HTTP_200_OK)


def reset_user_password(request, uid, token):
    if request.POST:
        password = request.POST.get('password1')
        payload = {'uid': uid, 'token': token, 'new_password': password}

        url = 'https://find-dining-panda.herokuapp.com/api/auth/users/reset_password_confirm/'

        response = requests.post(url, data=payload)
        if response.status_code == 204:
            # Give some feedback to the user. For instance:
            # https://docs.djangoproject.com/en/2.2/ref/contrib/messages/
            return render(request, 'success.html')
        else:
            return render(request, 'error.html')
    else:
        return render(request, 'reset_password.html')


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # this line is the only change from the base implementation.
        kwargs['data'] = {"uid": self.kwargs['uid'],
                          "token": self.kwargs['token']}

        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
