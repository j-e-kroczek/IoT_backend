from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Weather Station API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("check_employee_card/", views.CheckEmployeeCardView.as_view()),
    path("handle_work_time/", views.HandleWorkTimeView.as_view()),
    path("send_weather_data/", views.SendWeatherDataApiView.as_view()),
    path("weather_data/", views.WeatherDataApiView.as_view()),
    path("weather_data/<slug:pk>/", views.WeatherDataDetailApiView.as_view()),
    path("employee_card_log/", views.EmployeeCardLogApiView.as_view()),
    path("employee_card_log/<slug:pk>/", views.EmployeeCartLogDetailApiView.as_view()),
    path("weather_station/", views.WeatherStationApiView.as_view()),
    path("weather_station/<slug:pk>/", views.WeatherStationDetailApiView.as_view()),
    path("weather_station/<slug:pk>/data/", views.WeatherStationDataApiView.as_view()),
    path("employee/", views.EmployeeApiView.as_view()),
    path("employee/<slug:pk>/", views.EmployeeDetailApiView.as_view()),
    path("employee_card/", views.EmployeeCardApiView.as_view()),
    path("employee_card/<slug:pk>/", views.EmployeeCardDetailApiView.as_view()),
    path("employee_card/<slug:pk>/data", views.EmployeeCardDataApiView.as_view()),
    path("work_space/", views.WorkTimeApiView.as_view()),
]
