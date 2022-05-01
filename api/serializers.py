from .models import Restaurant, Meal, User
from rest_framework import serializers


class UserFriendSerializer(serializers.ModelSerializer):
    '''
    Serialize Data for the User model
    '''

    friends = serializers.SlugRelatedField(slug_field="username", read_only=True, many=True)
    friends_pk = serializers.PrimaryKeyRelatedField(source='friends', many=True, read_only=True)

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
    # friends = serializers.SlugRelatedField(slug_field="username", read_only=True, many=True)
    friends = serializers.SlugRelatedField(slug_field="username", read_only=True, many=True)
    friends_pk = serializers.PrimaryKeyRelatedField(source='friends', many=True, read_only=True)

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
            'yes',
            'no',
        )        


class MealSerializer(serializers.ModelSerializer):
    '''
    Serialize Data for the Meal model
    '''

    class Meta:
        model = Meal
        fields = (
            'id',
            'creator',
            'created_date',
            'invitee',
            'location',
            'radius',
            'lat',
            'lon',
            # 'restaurant',
        )        





