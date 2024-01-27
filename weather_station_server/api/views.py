from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from time import sleep
from .serializers import *


class CheckEmployeeCardView(APIView):
    """Checks if the card is active and saves the log entry."""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["card_number"],
            properties={
                "card_number": openapi.Schema(type=openapi.TYPE_STRING),
                "weather_station": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Weather station ID"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="OK - card is active",
                examples={
                    "application/json": {
                        "status": "OK",
                    }
                },
            ),
            400: openapi.Response(
                description="Bad Request - missing card_number parameter",
                examples={
                    "application/json": {
                        "status": "ERROR",
                    }
                },
            ),
            401: openapi.Response(
                description="Unauthorized - card is not active or does not exist",
                examples={
                    "application/json": {
                        "status": "ERROR",
                    }
                },
            ),
        },
    )
    def post(self, request):
        try:
            card_number = request.data["card_number"]
        except:
            print("ERROR - missing card_number parameter")
            return Response({"status": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        weather_station = None
        if "weather_station" in request.data:
            weather_station = request.data["weather_station"]
            try:
                weather_station = get_object_or_404(
                    WeatherStation, id=weather_station, is_active=True
                )
                print(weather_station)
            except:
                return Response(
                    {"status": "ERROR"}, status=status.HTTP_401_UNAUTHORIZED
                )
        employee_card = get_object_or_404(
            EmployeeCard, card_number=card_number
        )
        if employee_card.is_active:
            employee_card_log = EmployeeCardLog(
                employee_card=employee_card,
                date=timezone.now(),
                weather_station=weather_station,
            )
            employee_card_log.save()
            return Response({"status": "OK"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "ERROR - card is inactive"}, status=status.HTTP_403_FORBIDDEN)

class NewEmployeeCardView(APIView):
    """Checks if the card is active, otherwise creates a new one."""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["card_number"],
            properties={
                "card_number": openapi.Schema(type=openapi.TYPE_STRING),
                "weather_station": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Weather station ID"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="OK - card is active",
                examples={
                    "application/json": {
                        "status": "OK",
                    }
                },
            ),
            201: openapi.Response(
                description="OK - new card created",
                examples={
                    "application/json": {
                        "status": "OK",
                    }
                },
            ),
            400: openapi.Response(
                description="Bad Request - missing card_number parameter",
                examples={
                    "application/json": {
                        "status": "ERROR",
                    }
                },
            ),
            401: openapi.Response(
                description="Unauthorized - card is not active or does not exist",
                examples={
                    "application/json": {
                        "status": "ERROR",
                    }
                },
            ),
        },
    )
    def post(self, request):
        try:
            card_number = request.data["card_number"]
        except:
            print("ERROR - missing card_number parameter")
            return Response({"status": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        weather_station = None
        if "weather_station" in request.data:
            weather_station = request.data["weather_station"]
            try:
                weather_station = get_object_or_404(
                    WeatherStation, id=weather_station, is_active=True
                )
                print(weather_station)
            except:
                return Response(
                    {"status": "ERROR"}, status=status.HTTP_401_UNAUTHORIZED
                )
        if not EmployeeCard.objects.filter(card_number=card_number).exists():
            EmployeeCard.objects.create(card_number=card_number, is_active=False)
            return Response({"status": "New card created"}, status=status.HTTP_201_CREATED)
        employee_card = get_object_or_404(
            EmployeeCard, card_number=card_number
        )
        if employee_card.is_active:
            return Response({"status": "OK"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "ERROR - card is inactive"}, status=status.HTTP_403_FORBIDDEN)
                

class HandleWorkTimeView(APIView):
    """Handles work time."""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["card_number", "weather_station"],
            properties={
                "card_number": openapi.Schema(type=openapi.TYPE_STRING),
                "weather_station": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Weather station ID"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="OK - WorkTime started or ended",
                examples={
                    "application/json": {
                        "status": "OK",
                    }
                },
            ),
            400: openapi.Response(
                description="Bad Request - missing card_number parameter",
                examples={
                    "application/json": {
                        "status": "ERROR",
                    }
                },
            ),
            401: openapi.Response(
                description="Unauthorized - card is not active or does not exist",
                examples={
                    "application/json": {
                        "status": "ERROR",
                    }
                },
            ),
        },
    )
    def post(self, request):
        try:
            card_number = request.data["card_number"]
        except:
            return Response({"status": "ERROR - Provide card_number"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            weather_station = request.data["weather_station"]
            weather_station = get_object_or_404(
                WeatherStation, id=weather_station, is_active=True
            )
        except:
            return Response(
                {"status": "ERROR - Invalid work_station id"}, status=status.HTTP_401_UNAUTHORIZED
            )
        employee_card = get_object_or_404(
            EmployeeCard, card_number=card_number
        )
        if employee_card.is_active:
            if WorkTime.objects.filter(employee=employee_card.employee, end_date=None).exists():
                work_time = WorkTime.objects.get(employee=employee_card.employee, end_date=None)
                if work_time.work_space.end_station != weather_station:
                    return Response({"status": "ERROR - Can't end WorkTime at this station!"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    work_time.end_date = timezone.now()
                    work_time.end_station = weather_station
                    work_time.save()
                    return Response({"status": "OK - WorkTime ended"}, status=status.HTTP_200_OK)
            else:
                try:
                    work_space = WorkSpace.objects.filter(start_station=weather_station).first()
                    if work_space is None:
                        return Response({"status": "ERROR - Can't start WorkTime at this station!"}, status=status.HTTP_401_UNAUTHORIZED)
                except:
                    return Response({"status": "ERROR - Invalid work_station id"}, status=status.HTTP_401_UNAUTHORIZED)
                work_time = WorkTime(employee=employee_card.employee, start_date=timezone.now(), start_station=weather_station, work_space=work_space)
                work_time.save()
                return Response({"status": "OK - WorkTime started"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "ERROR - Employee card is inactive!"}, status=status.HTTP_401_UNAUTHORIZED)


class SendWeatherDataApiView(APIView):
    """Saves weather data."""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["weather_station", "temperature", "humidity", "pressure"],
            properties={
                "weather_station": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Weather station ID"
                ),
                "temperature": openapi.Schema(type=openapi.TYPE_NUMBER),
                "humidity": openapi.Schema(type=openapi.TYPE_NUMBER),
                "pressure": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
        ),
        responses={
            200: openapi.Response(
                description="OK - weather data saved",
                examples={
                    "application/json": {
                        "status": "OK",
                    }
                },
            ),
            400: openapi.Response(
                description="Bad Request - missing parameter or parameter has wrong type",
                examples={
                    "application/json": {
                        "status": "ERROR",
                        "errors": {"weather_station": ["This field is required."]},
                    }
                },
            ),
        },
    )
    def post(self, request):
        serializer = WeatherDataAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "OK"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"status": "ERROR", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class WeatherDataApiView(ListAPIView):
    """
    Retrieves a list of weather data records.
    Supports filtering by weather station ID, start date, and end date.
    """

    serializer_class = WeatherDataSerializer
    weather_station_param = openapi.Parameter(
        "weather_station",
        openapi.IN_QUERY,
        description="ID of the weather station",
        type=openapi.TYPE_STRING,
    )
    start_date_param = openapi.Parameter(
        "start_date",
        openapi.IN_QUERY,
        description="Start date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    end_date_param = openapi.Parameter(
        "end_date",
        openapi.IN_QUERY,
        description="End date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    response_schema_dict = {
        200: openapi.Response(
            description="List of weather data records",
            schema=WeatherDataSerializer(many=True),
        )
    }

    @swagger_auto_schema(
        manual_parameters=[weather_station_param, start_date_param, end_date_param],
        responses=response_schema_dict,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = WeatherData.objects.all().order_by("-date")
        weather_station = self.request.query_params.get("weather_station", None)
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)
        if weather_station is not None:
            try:
                weather_station = uuid.UUID(weather_station)
                queryset = queryset.filter(weather_station=weather_station)
            except:
                pass
        if start_date is not None:
            try:
                start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d")
                queryset = queryset.filter(date__gte=start_date)
            except:
                pass
        if end_date is not None:
            try:
                end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(date__lte=end_date)
            except:
                pass
        return queryset


class WeatherDataDetailApiView(APIView):
    """Retrieves a single weather data record."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="OK - weather data",
                schema=WeatherDataSerializer(),
                examples={
                    "application/json": {
                        "id": "5e5b29c6-80ea-4410-b027-861c3a55134b",
                        "weather_station": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                        "temperature": 23,
                        "humidity": 43,
                        "pressure": 1000,
                        "date": "2024-01-18T11:56:58.844777Z",
                    }
                },
            ),
            404: openapi.Response(
                description="Not Found - weather data does not exist",
            ),
        },
    )
    def get(self, request, pk):
        try:
            weather_data = get_object_or_404(WeatherData, id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WeatherDataSerializer(weather_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeCardLogApiView(ListAPIView):
    """
    Retrieves a list of employee card logs.
    Supports filtering by weather station ID, employee ID, start date, and end date.
    """

    serializer_class = EmployeeCardLogSerializer
    response_schema_dict = {
        200: openapi.Response(
            description="List of employee card logs",
            schema=EmployeeCardLogSerializer(many=True),
        )
    }
    start_date_param = openapi.Parameter(
        "start_date",
        openapi.IN_QUERY,
        description="Start date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    end_date_param = openapi.Parameter(
        "end_date",
        openapi.IN_QUERY,
        description="End date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    weather_station_param = openapi.Parameter(
        "weather_station",
        openapi.IN_QUERY,
        description="ID of the weather station",
        type=openapi.TYPE_STRING,
    )
    employee_card_param = openapi.Parameter(
        "employee_card",
        openapi.IN_QUERY,
        description="Card of the employee",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        manual_parameters=[
            start_date_param,
            end_date_param,
            weather_station_param,
            employee_card_param,
        ],
        responses=response_schema_dict,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = EmployeeCardLog.objects.all().order_by("-date")
        weather_station = self.request.query_params.get("weather_station", None)
        employee_card = self.request.query_params.get("employee_card", None)
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)
        if weather_station is not None:
            try:
                weather_station = uuid.UUID(weather_station)
                queryset = queryset.filter(weather_station=weather_station)
            except:
                pass
        if employee_card is not None:
            try:
                queryset = queryset.filter(employee_card=employee_card)
            except:
                pass
        if start_date is not None:
            try:
                start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d")
                queryset = queryset.filter(date__gte=start_date)
            except:
                pass
        if end_date is not None:
            try:
                end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(date__lte=end_date)
            except:
                pass
        return queryset


class EmployeeCartLogDetailApiView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="OK - employee card log",
                schema=EmployeeCardLogSerializer(),
                examples={
                    "application/json": {
                        "id": "65d2a68f-e497-49c9-afa9-f050065541e4",
                        "employee_card": "8593e75d-78ab-469b-b311-bb8ebbfc9873",
                        "date": "2024-01-18T12:20:58.233604Z",
                        "weather_station": None,
                    }
                },
            ),
            404: openapi.Response(
                description="Not Found - employee card log does not exist",
            ),
        },
    )
    def get(self, request, pk):
        try:
            employee_card_log = get_object_or_404(EmployeeCardLog, id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeCardLogSerializer(employee_card_log)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeatherStationApiView(APIView):
    """Retrieves a list of weather stations."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="OK - weather station list",
                schema=WeatherStationSerializer(many=True),
                examples={
                    "application/json": [
                        {
                            "id": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                            "name": "Weather station 1",
                            "is_active": True,
                        },
                        {
                            "id": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                            "name": "Weather station 2",
                            "is_active": True,
                        },
                    ]
                },
            ),
        },
    )
    def get(self, request):
        weather_station = WeatherStation.objects.all()
        serializer = WeatherStationSerializer(weather_station, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeatherStationDetailApiView(APIView):
    """Retrieves a single weather station."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="OK - weather station",
                schema=WeatherStationSerializer(),
                examples={
                    "application/json": {
                        "id": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                        "name": "Weather station 1",
                        "is_active": True,
                    }
                },
            ),
            404: openapi.Response(
                description="Not Found - weather station does not exist",
            ),
        },
    )
    def get(self, request, pk):
        try:
            weather_station = get_object_or_404(WeatherStation, id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WeatherStationSerializer(weather_station)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeApiView(APIView):
    """Retrieves a list of employees."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="OK - employee list",
                schema=EmployeeSerializer(many=True),
                examples={
                    "application/json": [
                        {
                            "id": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                            "name": "Employee 1",
                            "surname": "Employee 1",
                            "phone_number": "123456789",
                            "is_active": True,
                        },
                        {
                            "id": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                            "name": "Employee 2",
                            "surname": "Employee 2",
                            "phone_number": "123456789",
                            "is_active": True,
                        },
                    ]
                },
            ),
        },
    )
    def get(self, request):
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeDetailApiView(APIView):
    """Retrieves a single employee."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="OK - employee",
                schema=EmployeeSerializer(),
                examples={
                    "application/json": {
                        "id": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                        "name": "Employee 1",
                        "surname": "Employee 1",
                        "phone_number": "123456789",
                        "is_active": True,
                    }
                },
            ),
            404: openapi.Response(
                description="Not Found - employee does not exist",
            ),
        },
    )
    def get(self, request, pk):
        try:
            employee = get_object_or_404(Employee, id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeCardApiView(APIView):
    """Retrieves a list of employee cards."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="OK - employee card list",
                schema=EmployeeCardSerializer(many=True),
                examples={
                    "application/json": [
                        {
                            "id": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                            "card_number": "123456789",
                            "employee": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                            "is_active": True,
                        },
                        {
                            "id": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                            "card_number": "123456789",
                            "employee": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                            "is_active": True,
                        },
                    ]
                },
            ),
        },
    )
    def get(self, request):
        employee_card = EmployeeCard.objects.all()
        serializer = EmployeeCardSerializer(employee_card, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeCardDetailApiView(APIView):
    """Retrieves a single employee card."""

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="OK - employee card",
                schema=EmployeeCardSerializer(),
                examples={
                    "application/json": {
                        "id": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                        "card_number": "123456789",
                        "employee": "4d438238-ff5b-4577-91c6-ffa2cb953057",
                        "is_active": True,
                    }
                },
            ),
            404: openapi.Response(
                description="Not Found - employee card does not exist",
            ),
        },
    )
    def get(self, request, pk):
        try:
            employee_card = get_object_or_404(EmployeeCard, id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeCardSerializer(employee_card)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeatherStationDataApiView(ListAPIView):
    """
    Retrieves a list of weather data records for a given weather station.
    Supports filtering by start date and end date.
    """

    serializer_class = WeatherStationDataSerializer

    start_date_param = openapi.Parameter(
        "start_date",
        openapi.IN_QUERY,
        description="Start date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    end_date_param = openapi.Parameter(
        "end_date",
        openapi.IN_QUERY,
        description="End date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    responses_schema_dict = {
        200: openapi.Response(
            description="List of weather data records",
            schema=WeatherStationDataSerializer(),
        ),
        404: openapi.Response(
            description="Not Found - weather station does not exist",
        ),
        400: openapi.Response(
            description="Bad Request - missing parameter or parameter has wrong type",
            examples={
                "application/json": {
                    "status": "ERROR",
                    "errors": {"weather_station": ["This field is required."]},
                }
            },
        ),
    }

    @swagger_auto_schema(
        manual_parameters=[start_date_param, end_date_param],
        responses=responses_schema_dict,
    )
    def get(self, request, pk):
        try:
            weather_station = get_object_or_404(WeatherStation, id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        weather_data = self.get_queryset().filter(weather_station=weather_station)
        data = {
            "station_name": str(weather_station.name),
            "station_id": str(weather_station.id),
            "weather_data": WeatherDataSerializer(weather_data, many=True).data,
        }
        serializer = WeatherStationDataSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"status": "ERROR", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_queryset(self):
        queryset = WeatherData.objects.all().order_by("-date")
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)
        if start_date is not None:
            try:
                start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d")
                queryset = queryset.filter(date__gte=start_date)
            except:
                pass
        if end_date is not None:
            try:
                end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(date__lte=end_date)
            except:
                pass
        return queryset


class EmployeeCardDataApiView(ListAPIView):
    """
    Retrieves a list of employee card logs for a given employee card.
    Supports filtering by start date and end date.
    """

    serializer_class = EmployeeCardDataSerializer

    start_date_param = openapi.Parameter(
        "start_date",
        openapi.IN_QUERY,
        description="Start date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    end_date_param = openapi.Parameter(
        "end_date",
        openapi.IN_QUERY,
        description="End date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    responses_schema_dict = {
        200: openapi.Response(
            description="List of employee card logs",
            schema=EmployeeCardDataSerializer(),
        ),
        404: openapi.Response(
            description="Not Found - employee card does not exist",
        ),
        400: openapi.Response(
            description="Bad Request - missing parameter or parameter has wrong type",
            examples={
                "application/json": {
                    "status": "ERROR",
                    "errors": {"employee_card": ["This field is required."]},
                }
            },
        ),
    }

    @swagger_auto_schema(
        manual_parameters=[start_date_param, end_date_param],
        responses=responses_schema_dict,
    )
    def get(self, request, pk):
        try:
            employee_card = get_object_or_404(EmployeeCard, id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        employee_card_log = self.get_queryset()
        employee_card_log = employee_card_log.filter(employee_card=employee_card)
        data = {
            "card_number": str(employee_card.card_number),
            "employee": EmployeeSerializer(employee_card.employee).data,
            "card_logs": EmployeeCardLogSerializer(employee_card_log, many=True).data,
        }
        serializer = EmployeeCardDataSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"status": "ERROR", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_queryset(self):
        queryset = EmployeeCardLog.objects.all().order_by("-date")
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)
        if start_date is not None:
            try:
                start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d")
                queryset = queryset.filter(date__gte=start_date)
            except:
                pass
        if end_date is not None:
            try:
                end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(date__lte=end_date)
            except:
                pass
        return queryset


class WorkTimeApiView(APIView):
    
    serializer_class = WorkTimeSerializer
    response_schema_dict = {
        200: openapi.Response(
            description="List of work times",
            schema=WorkTimeSerializer(many=True),
        )
    }
    start_date_param = openapi.Parameter(
        "start_date",
        openapi.IN_QUERY,
        description="Start date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    end_date_param = openapi.Parameter(
        "end_date",
        openapi.IN_QUERY,
        description="End date for filtering data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING,
    )
    employee_param = openapi.Parameter(
        "employee",
        openapi.IN_QUERY,
        description="ID of the employee",
        type=openapi.TYPE_STRING,
    )
    work_space_param = openapi.Parameter(
        "work_space",
        openapi.IN_QUERY,
        description="ID of the work space",
        type=openapi.TYPE_STRING,
    )
    
    @swagger_auto_schema(
        manual_parameters=[start_date_param, end_date_param, employee_param, work_space_param],
        responses=response_schema_dict,
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = WorkTimeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def get_queryset(self):
        queryset = WorkTime.objects.all().order_by("-start_date")
        if self.request.query_params.get("employee", None) is not None:
            queryset = queryset.filter(employee=self.request.query_params.get("employee", None))
        if self.request.query_params.get("work_space", None) is not None:
            queryset = queryset.filter(work_space=self.request.query_params.get("work_space", None))
        if self.request.query_params.get("start_date", None) is not None:
            queryset = queryset.filter(start_date__gte=self.request.query_params.get("start_date", None))
        if self.request.query_params.get("end_date", None) is not None:
            queryset = queryset.filter(end_date__lte=self.request.query_params.get("end_date", None))
        return queryset    
    