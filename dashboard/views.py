import os
import time
import calendar
from rest_framework.views import APIView
from utils.common import *
from .serializer import *
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.


class RegisterRestaurant(APIView):
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            data = request.data
            image = data["image"]
            gmt = time.gmtime()
            ts = calendar.timegm(gmt)
            path = "/".join(["public", "images", str(ts)])
            os.makedirs(path, exist_ok=True)
            image_path = path+"/"+image.name
            with open(image_path, "wb") as file:
                for chunk in image.chunks():
                    file.write(chunk)
            data["restaurant_logo"] = image_path
            data["user_id"] = request.user.pk
            del data["image"]
            restaurant_serializer = self.serializer_class(data=data)
            if restaurant_serializer.is_valid():
                restaurant_serializer.save()
                return success_response(message="Data inserted successfully")
            return error_response(message="Invalid data")
        except Exception as e:
            return error_response(message=str(e))


class RegisterSeat(APIView):
    def post(self, request):
        try:
            seat_am_ls = []
            seat_pm_ls = []
            user_id = request.user.pk
            restaurant = RestaurantInformation.objects.filter(user_id=user_id)
            restaurant_date = {
                "date": request.data.get("date"),
                "restaurant_id": restaurant.get().id,
                "user_id":user_id
            }
            date_serializer = DateSerializer(data=restaurant_date)
            if date_serializer.is_valid():
                date_serializer.save()
                for am in request.data.get("seat_am"):
                    seat_am_ls.append({
                        "date_id": date_serializer.data["id"],
                        "restaurant_id": restaurant.get().id,
                        "seat_slot_am": am
                    })
                seat_am_serializer = SeatAMSerializer(data=seat_am_ls, many=True)
                if seat_am_serializer.is_valid():
                    seat_am_serializer.save()
                    for pm in request.data.get("seat_pm"):
                       seat_pm_ls.append({
                            "date_id": date_serializer.data["id"],
                            "restaurant_id": restaurant.get().id,
                            "seat_slot_pm": pm
                        })
                    seat_pm_serializer = SeatPmSerializer(data=seat_pm_ls, many=True)
                    if seat_pm_serializer.is_valid():
                        seat_pm_serializer.save()
                        return success_response(message="Seating added successfully")
                return error_response(message="Something went wrong")
            else:
                return error_response(message=str(date_serializer.error_messages))
        except Exception as e:
            return error_response(message=str(e))


class RestaurantList(APIView):
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            restaurant_info = RestaurantInformation.objects.filter(user_id = request.user.pk)
            user_data = self.serializer_class(restaurant_info, many=True).data
            return success_response(data=user_data)
        except Exception as e:
            return error_response(message=str(e))
