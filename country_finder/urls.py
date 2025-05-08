
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from country_finder.views import CountryViewSet, RegionViewSet, LanguageViewSet, country_html_view, signup_view, api_overview
from django.contrib.auth.views import LoginView, LogoutView

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'languages', LanguageViewSet, basename='language')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', country_html_view, name='country-list'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", signup_view, name="signup"),
    path('api-overview', api_overview, name="api-overview"),
]
