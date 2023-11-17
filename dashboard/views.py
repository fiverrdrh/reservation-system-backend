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
            if request.user.username == "superadmin":
                restaurant_info = RestaurantInformation.objects.all()
            else:
                restaurant_info = RestaurantInformation.objects.filter(user_id=request.user.pk)
            user_data = self.serializer_class(restaurant_info, many=True).data
            return success_response(data=user_data)
        except Exception as e:
            return error_response(message=str(e))


class SeatingList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_id = request.user.pk
            restaurant_information = RestaurantInformation.objects.filter(user_id=user_id)

        except Exception as e:
            return error_response(message=str(e))


class RestaurantNameList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            restaurant_ls = []
            restaurant_information = RestaurantInformation.objects.all()
            serializer_data = RestaurantSerializer(restaurant_information, many=True).data
            for data in serializer_data:
                restaurant_ls.append({
                    "id" : data["id"],
                    "restaurant_name": data["restaurant_name"]
                })
            return success_response(data=restaurant_ls)
        except Exception as e:
            return error_response(message=str(e))


class RestaurantFullRecord(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            id = request.GET["id"]
            date = request.GET["date"]
            restaurant_info = RestaurantInformation.objects.filter(id=id)
            restaurant_info_serializer = RestaurantSerializer(restaurant_info, many=True).data
            restaurant_date = RestaurantDate.objects.filter(restaurant_id=id, date=date)
            restaurant_seat_am = RestaurantSeatAM.objects.filter(restaurant_id=id, date_id=restaurant_date.get().id)
            seat_am = SeatAMSerializer(restaurant_seat_am, many=True).data
            restaurant_seat_pm = RestaurantSeatPM.objects.filter(restaurant_id=id,
                                                                 date_id=restaurant_date.get().id)
            seat_pm = SeatPmSerializer(restaurant_seat_pm, many=True).data
            resultset = {"restaurant_info":restaurant_info_serializer, "seat_am": seat_am, "seat_pm": seat_pm}
            return success_response(data=resultset)
        except Exception as e:
            return error_response(message=str(e))
