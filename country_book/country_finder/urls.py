
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from country_finder.views import CountryViewSet, RegionViewSet, LanguageViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'languages', LanguageViewSet, basename='language')

urlpatterns = [
    path('api/', include(router.urls)),
]
