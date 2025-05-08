
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(("country_finder.urls", "country_finder"), "country_finder"))
]