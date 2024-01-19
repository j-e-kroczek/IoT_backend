from django.contrib import admin

from .models import Employee, EmployeeCard, EmployeeCardLog, WeatherStation, WeatherData

admin.site.register(Employee)
admin.site.register(EmployeeCard)
admin.site.register(EmployeeCardLog)
admin.site.register(WeatherStation)
admin.site.register(WeatherData)
