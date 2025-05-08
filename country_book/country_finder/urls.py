
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from country_finder.views import CountryViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')


urlpatterns = [
    path('api/', include(router.urls)),
]
