from django.shortcuts import render
from .models import User, Restaurant, Meal
from .serializers import UserSerializer, RestaurantSerializer, MealSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from .permissions import IsOwnerOrReadOnly


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
    permission_class = [AllowAny]

# Searching
# class UserSearchView(generics.ListAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         queryset = User.objects.all()
#         friend_username = self.request.query_params.get('username')
#         if friend_username is not None:
#             queryset = queryset.filter(friend_username__icontains=friend_username)
#         return queryset

# Follow/Unfollow
class SaveFriendView(APIView):
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                
        def post(request, self, pk,format=None):    
            current_profile = self.user
            other_profile = pk
            current_profile.friends.add(other_profile)

            return Response({"Requested" : "Save request has been sent!!"},status=status.HTTP_200_OK)

class DeleteFriendView(APIView):
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                
        def delete(request, self, pk,format=None):    
            current_profile = self.user
            other_profile = pk
            current_profile.friends.remove(other_profile)

            return Response({"Requested" : "Deleted!"},status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    '''
    Return a list of all the users registered to use the application
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

