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
    # num_of_diners = serializers.Field(source='num_of_diners')
    # num_of_diners = 5

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            # "num_of_diners",
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
    num_of_diners = serializers.SerializerMethodField()

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
            # 'restaurant',
        )        

    def get_num_of_diners(self, obj):
        
        num_creators = 1
        num_invitees = 1     # get count by querying M2M table 'api_meal_invitee'
        
        # meal = Meal.objects.get(id=17)
        # num_invitees = meal.invitee.all()

        # breakpoint()
        return num_invitees + num_creators




