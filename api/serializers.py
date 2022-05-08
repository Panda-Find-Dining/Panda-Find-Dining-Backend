from .models import Restaurant, Meal, User, UserManager
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class UserFriendSerializer(serializers.ModelSerializer):
    '''
    Serialize Data for the User model
    '''

    friends = serializers.SlugRelatedField(
        slug_field="username", read_only=True, many=True)
    friends_pk = serializers.PrimaryKeyRelatedField(
        source='friends', many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "friends",
            "friends_pk",
        )


class UserSerializer(serializers.ModelSerializer):
    '''
    Serialize Data for the User model
    '''
    friends = serializers.SlugRelatedField(
        slug_field="username", read_only=True, many=True)
    friends_pk = serializers.PrimaryKeyRelatedField(
        source='friends', many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "friends",
            "friends_pk"
        )


class RestaurantSerializer(serializers.ModelSerializer):
    '''
    Serialize Data for the Restaurant model
    '''
    yes_count = serializers.ReadOnlyField()

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'lat',
            'lon',
            'formatted_address',
            'place_id',
            'hours',
            'business_status',
            'icon',
            'meal',
            'yes_count',
            'yes',
            'no',
            'photo_reference',
        )


class MealSerializer(serializers.ModelSerializer):
    '''
    Serialize Data for the Meal model
    '''
    num_of_diners = serializers.ReadOnlyField()

    class Meta:
        model = Meal
        fields = (
            'id',
            'num_of_diners',
            'creator',
            'invitee',
            'created_date',
            'location',
            'radius',
            'lat',
            'lon',
            'match',
            'user_has_selected',
            'friends_have_selected',
            'archive',
            'all_users_have_selected',
        )


class UserManagerSerializer(serializers.ModelSerializer):
    '''
    Serialize Data to use for email
    '''
    class Meta:
        model = UserManager
        fields = (
            "id",
            "email",
            "username",
            "user",
        )


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'username', 'password')
