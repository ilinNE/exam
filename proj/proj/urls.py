from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", include("birthdays.urls")),
    path("admin/", admin.site.urls),
]
