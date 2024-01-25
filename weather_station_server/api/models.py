from django.db import models
import uuid


class Employee(models.Model):
    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " " + self.surname


class EmployeeCard(models.Model):
    class Meta:
        verbose_name = "EmployeeCard"
        verbose_name_plural = "EmployeeCards"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_number = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.card_number + " " + self.employee.name + " " + self.employee.surname


class EmployeeCardLog(models.Model):
    class Meta:
        verbose_name = "EmployeeCardLog"
        verbose_name_plural = "EmployeeCardLogs"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_card = models.ForeignKey(EmployeeCard, on_delete=models.CASCADE)
    weather_station = models.ForeignKey(
        "WeatherStation", on_delete=models.SET_NULL, null=True
    )
    date = models.DateTimeField()

    def __str__(self):
        return (
            self.employee_card.card_number
            + " "
            + self.employee_card.employee.name
            + " "
            + self.employee_card.employee.surname
            + " "
            + str(self.date)
        )
        
class WorkSpace(models.Model):
    class Meta:
        verbose_name = "WorkSpace"
        verbose_name_plural = "WorkSpaces"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    start_station = models.ForeignKey(
        "WeatherStation", on_delete=models.CASCADE, related_name="work_space_start_station"
    )
    end_station = models.ForeignKey(
        "WeatherStation", on_delete=models.CASCADE,  related_name="work_space_end_station"
    )
    def __str__(self):
        return self.name
        
class WorkTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    start_station = models.ForeignKey(
        "WeatherStation", on_delete=models.SET_NULL, null=True, related_name="start_station"
    )
    end_station = models.ForeignKey(
        "WeatherStation", on_delete=models.SET_NULL, null=True, blank=True, related_name="end_station"
    )
    
    def __str__(self):
        return (
            self.employee.name
            + " "
            + self.employee.surname
            + " "
            + str(self.start_date)
            + " "
            + str(self.end_date)
        )

class WeatherStation(models.Model):
    class Meta:
        verbose_name = "WeatherStation"
        verbose_name_plural = "WeatherStations"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.id}"


class WeatherData(models.Model):
    class Meta:
        verbose_name = "WeatherData"
        verbose_name_plural = "WeatherDatas"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    weather_station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return (
            str(self.temperature)
            + " "
            + str(self.humidity)
            + " "
            + str(self.pressure)
            + " "
            + str(self.date)
        )
