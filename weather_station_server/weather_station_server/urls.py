from django.contrib import admin

from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import include


schema_view = get_swagger_view(title="Pastebin API")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
]
