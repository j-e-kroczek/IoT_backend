import os
import django
from django.utils import timezone
from faker import Faker
import random
from tqdm import tqdm
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_station_server.settings")
django.setup()
fake = Faker("pl_PL")


def generate_employees(n=10):
    from api.models import Employee

    for _ in tqdm(range(n), desc="Generating employees"):
        Employee.objects.create(
            name=fake.first_name(),
            surname=fake.last_name(),
            phone_number=fake.phone_number(),
            is_active=random.choice([True, False]),
        )


def generate_employee_cards():
    from api.models import EmployeeCard, Employee

    employees = Employee.objects.all()
    for employee in tqdm(employees, desc="Generating employee cards"):
        EmployeeCard.objects.create(
            card_number=fake.credit_card_number(),
            employee=employee,
            is_active=random.choice([True, False]),
        )


def generate_weather_stations(n=3):
    from api.models import WeatherStation

    for _ in tqdm(range(n), desc="Generating weather stations"):
        WeatherStation.objects.create(
            name=fake.city(),
        )


def generate_weather_station_datas(n=3):
    from api.models import WeatherStation, WeatherData

    for weather_station in tqdm(
        WeatherStation.objects.all(),
        desc="Generating weather station datas - stations",
    ):
        last_temperature = random.uniform(-20, 20)
        last_humidity = random.uniform(0, 100)
        last_pressure = random.uniform(800, 1200)
        for day in tqdm(
            range(n),
            desc="Generating weather station datas - days",
            leave=False,
            position=1,
        ):
            for hour in tqdm(
                range(24),
                desc="Generating weather station datas - hours",
                leave=False,
                position=2,
            ):
                for minute in range(30):
                    WeatherData.objects.create(
                        weather_station=weather_station,
                        temperature=last_temperature,
                        humidity=last_humidity,
                        pressure=last_pressure,
                        date=timezone.now()
                        - timedelta(days=day, hours=hour, minutes=minute * 2),
                    )
                    last_humidity += random.uniform(-1, 1)
                    last_pressure += random.uniform(-1, 1)
                    last_temperature += random.uniform(-1, 1)
                    if last_humidity < 0:
                        last_humidity = 0
                    if last_humidity > 100:
                        last_humidity = 100
                    if last_pressure < 800:
                        last_pressure = 800
                    if last_pressure > 1200:
                        last_pressure = 1200
                    if last_temperature < -20:
                        last_temperature = -20
                    if last_temperature > 40:
                        last_temperature = 40


def generate_employee_card_logs(n=10):
    from api.models import EmployeeCard, EmployeeCardLog, WeatherStation

    for employee_card in tqdm(
        EmployeeCard.objects.all(),
        desc="Generating employee card logs",
        leave=False,
        position=0,
        ncols=100,
    ):
        for _ in range(random.randint(0, n)):
            EmployeeCardLog.objects.create(
                employee_card=employee_card,
                weather_station=random.choice(WeatherStation.objects.all()),
                date=timezone.now()
                - timedelta(
                    days=random.randint(0, 10),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                ),
            )


if __name__ == "__main__":
    generate_employees()
    generate_employee_cards()
    generate_weather_stations()
    generate_employee_card_logs()
    generate_weather_station_datas()
