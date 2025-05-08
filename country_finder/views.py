from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Country, Region, Language
from .serializers import CountrySerializer, RegionSerializer, LanguageSerializer
from django.db.models import Q


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

    # List same regional countries
    @action(detail=True, methods=['get'], url_path='same-region')
    def same_region(self, request, pk=None):
        country = self.get_object()
        region = country.region
        if not region:
            return Response({"detail": "This country does not have a region."}, status=400)
        countries = Country.objects.filter(region=region).exclude(id=country.id)
        serializer = self.get_serializer(countries, many=True)
        return Response(serializer.data)

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
