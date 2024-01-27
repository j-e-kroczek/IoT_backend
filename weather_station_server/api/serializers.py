from rest_framework import serializers
from rest_framework.fields import empty
from .models import WeatherData, Employee, EmployeeCard, EmployeeCardLog, WeatherStation, WorkSpace, WorkTime
from django.utils import timezone


class WeatherDataAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ("weather_station", "temperature", "humidity", "pressure")

    def validate_temperature(self, value):
        if value < -100 or value > 100:
            raise serializers.ValidationError(
                "Temperature must be between -100 and 100"
            )
        return value

    def validate_humidity(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Humidity must be between 0 and 100")
        return value

    def validate_pressure(self, value):
        if value < 800 or value > 1200:
            raise serializers.ValidationError("Pressure must be between 800 and 1200")
        return value

    def create(self, validated_data):
        weather_data = WeatherData(
            weather_station=validated_data["weather_station"],
            temperature=validated_data["temperature"],
            humidity=validated_data["humidity"],
            pressure=validated_data["pressure"],
            date=timezone.now(),
        )
        weather_data.save()
        return weather_data


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "name", "surname", "phone_number", "is_active")


class EmployeeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCard
        fields = ("id", "card_number", "employee", "is_active")


class EmployeeCardLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCardLog
        fields = ("id", "employee_card", "date", "weather_station")


class WeatherStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStation
        fields = ("id", "name", "is_active")


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = (
            "id",
            "weather_station",
            "temperature",
            "humidity",
            "pressure",
            "date",
        )


class WeatherStationDataSerializer(serializers.Serializer):
    station_name = serializers.CharField()
    station_id = serializers.CharField()
    weather_data = WeatherDataSerializer(many=True)


class EmployeeCardDataSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    employee = EmployeeSerializer()
    card_logs = EmployeeCardLogSerializer(many=True)


class WorkSpaceSerializer(serializers.ModelSerializer):
    
    start_station = WeatherStationSerializer()
    end_station = WeatherStationSerializer()
    
    class Meta:
        model = WorkSpace
        fields = ("id", "name", "start_station", "end_station")
        
class WorkTimeSerializer(serializers.ModelSerializer):
    
    work_space = WorkSpaceSerializer()
    start_station = WeatherStationSerializer()
    end_station = WeatherStationSerializer()
    employee = EmployeeSerializer()
    
    class Meta:
        model = WorkTime
        fields = ("id", "work_space", "employee", "start_date", "end_date", "start_station", "end_station")
