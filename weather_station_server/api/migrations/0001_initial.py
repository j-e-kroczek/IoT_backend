# Generated by Django 5.0.1 on 2024-01-25 15:36

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='WeatherStation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'WeatherStation',
                'verbose_name_plural': 'WeatherStations',
            },
        ),
        migrations.CreateModel(
            name='EmployeeCard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('card_number', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.employee')),
            ],
            options={
                'verbose_name': 'EmployeeCard',
                'verbose_name_plural': 'EmployeeCards',
            },
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('pressure', models.FloatField()),
                ('date', models.DateTimeField()),
                ('weather_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.weatherstation')),
            ],
            options={
                'verbose_name': 'WeatherData',
                'verbose_name_plural': 'WeatherDatas',
            },
        ),
        migrations.CreateModel(
            name='EmployeeCardLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('employee_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.employeecard')),
                ('weather_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.weatherstation')),
            ],
            options={
                'verbose_name': 'EmployeeCardLog',
                'verbose_name_plural': 'EmployeeCardLogs',
            },
        ),
        migrations.CreateModel(
            name='WorkTime',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.employee')),
                ('end_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='end_station', to='api.weatherstation')),
                ('start_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='start_station', to='api.weatherstation')),
            ],
        ),
    ]
