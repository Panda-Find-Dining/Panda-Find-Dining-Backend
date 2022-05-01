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
        
        number_of_creators = 1
        # num_invitees = 1     # get count by querying M2M table 'api_meal_invitee'
        
        meal_id_from_obj = obj.id
        meal = Meal.objects.get(id=meal_id_from_obj)
        
        number_of_people_invited = meal.invitee.all().count()
        
        total_number_people_going_to_eat = number_of_people_invited + number_of_creators

        # breakpoint()
        
        return total_number_people_going_to_eat




