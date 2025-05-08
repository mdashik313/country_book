from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Country, Region, Language
from .serializers import CountrySerializer, RegionSerializer, LanguageSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Handle Region
        region_data = data.pop('region', None)
        if region_data:
            region_obj, _ = Region.objects.get_or_create(name=region_data.get('name'))
            data['region'] = region_obj.id

        # Handle Languages
        languages_data = data.pop('languages', [])
        language_ids = []
        for lang in languages_data:
            obj, _ = Language.objects.get_or_create(code=lang.get('code'), defaults={'name': lang.get('name')})
            language_ids.append(obj.id)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        country = serializer.save()

        # Assign languages (M2M)
        if language_ids:
            country.languages.set(language_ids)

        return Response(self.get_serializer(country).data, status=status.HTTP_201_CREATED)

    # List same regional countries and languages of the countries
    @action(detail=True, methods=['get'], url_path='same-region')
    def same_region(self, request, pk=None):
        country = self.get_object()
        region = country.region
        if not region:
            return Response({"detail": "This country does not have a region."}, status=400)
        # countries = Country.objects.filter(region=region).exclude(id=country.id)
        # serializer = self.get_serializer(countries, many=True)
        # return Response(serializer.data)
        # Fetch other countries in the same region
        countries = Country.objects.filter(region=region).exclude(id=country.id)
        country_serializer = self.get_serializer(countries, many=True)

        # Get all languages used by those countries
        languages = Language.objects.filter(country__in=countries).distinct()
        language_serializer = LanguageSerializer(languages, many=True)

        return Response({
            "countries": country_serializer.data,
            "languages": language_serializer.data
        })

    # List countries by language name
    @action(detail=False, methods=['get'], url_path='by-language/(?P<name>[^/.]+)')
    def by_language(self, request, name=None):
        try:
            language = Language.objects.get(name__iexact=name)
        except Language.DoesNotExist:
            return Response({"detail": "Language not found."}, status=404)

        countries = Country.objects.filter(languages=language)
        serializer = self.get_serializer(countries, many=True)
        return Response(serializer.data)

    # Search by partial country name
    @action(detail=False, methods=['get'], url_path='search')
    def search_by_name(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"detail": "Search query parameter 'q' is required."}, status=400)
        countries = Country.objects.filter(Q(name_common__icontains=query) | Q(name_official__icontains=query))
        
        serializer = self.get_serializer(countries, many=True)
        return Response(serializer.data)

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


@api_view(['GET'])
def api_overview(request):
    base_url = request.build_absolute_uri('/api/countries/')

    return Response({
        "List Countries": request.build_absolute_uri('/api/countries/'),
        "Create Country": request.build_absolute_uri('/api/countries/'),
        "Retrieve/Update/Delete Country": request.build_absolute_uri('/api/countries/<id>/'),
        "Same Region Countries": request.build_absolute_uri('/api/countries/<id>/same-region/'),
        "Countries by Language": request.build_absolute_uri('/api/countries/by-language/<code>/'),
        "Search Country by Name": request.build_absolute_uri('/api/countries/search/?q=<partial-name>'),

        "List Languages": request.build_absolute_uri('/api/languages/'),
        "Create Language": request.build_absolute_uri('/api/languages/'),
        "Retrieve/Update/Delete Language": request.build_absolute_uri('/api/languages/<id>/'),

        "List Regions": request.build_absolute_uri('/api/regions/'),
        "Create Region": request.build_absolute_uri('/api/regions/'),
        "Retrieve/Update/Delete Region": request.build_absolute_uri('/api/regions/<id>/'),
    })

@login_required
def country_html_view(request):
    return render(request, "country_template.html")


# Define a view function for the registration page
def signup_view(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            # return redirect('/register/')
            return redirect("country_finder:signup")
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        # return redirect('/login/')
        return redirect("country_finder:login")
    
    # Render the registration page template (GET request)
    return render(request, "country_finder/signup.html")
