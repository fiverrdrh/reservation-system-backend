from rest_framework.serializers import ModelSerializer, SerializerMethodField
from dashboard.models import *


class RestaurantSerializer(ModelSerializer):
    user_name = SerializerMethodField("get_user_name")

    class Meta:
        fields = "__all__"
        model = RestaurantInformation

    def get_user_name(self, obj):
        return obj.user_id.first_name + obj.user_id.last_name


class DateSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = RestaurantDate


class SeatAMSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = RestaurantSeatAM


class SeatPmSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = RestaurantSeatPM