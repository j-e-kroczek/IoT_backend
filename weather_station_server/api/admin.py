from django.contrib import admin

from .models import Employee, EmployeeCard, EmployeeCardLog, WeatherStation, WeatherData, WorkTime, WorkSpace

admin.site.register(EmployeeCardLog)
admin.site.register(WeatherStation)
admin.site.register(WeatherData)
admin.site.register(WorkSpace)

@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date')
    
class WorkTimeInline(admin.TabularInline):
    model = WorkTime
    extra = 0
    
class EmployeeCardInline(admin.TabularInline):
    model = EmployeeCard
    extra = 0
    
class EmployeeCardLogInline(admin.TabularInline):
    model = EmployeeCardLog
    extra = 0
    
@admin.register(EmployeeCard)
class CardAdmin(admin.ModelAdmin):
    inlines = [EmployeeCardLogInline]
    list_display = ('card_number', 'employee')
    search_fields = ['card_number', 'employee__name', 'employee__surname']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [WorkTimeInline, EmployeeCardInline]
    list_display = ('name', 'surname','phone_number')
    search_fields = ['name', 'surname', 'phone_number']
    
    
