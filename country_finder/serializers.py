from rest_framework import serializers
from .models import Country, Region, Language


class ObjectIdField(serializers.CharField):
    def to_representation(self, value):
        return str(value)

class RegionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True) # Ensures ObjectId is handled as string
    class Meta:
        model = Region
        fields = ['id', 'name']
    
    # Override to handle incoming string data for 'region' in POST request
    def to_internal_value(self, data):
        if isinstance(data, str):
            # If a string is passed, fetch or create the region by name
            region, created = Region.objects.get_or_create(name=data)
            return {'id': str(region.id), 'name': region.name}  # Return the id and name
        return super().to_internal_value(data)

class LanguageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Language
        fields = ['id', 'name', 'code']
    
    # Override to handle incoming string data for 'languages' in POST request
    def to_internal_value(self, data):
        if isinstance(data, str):
            # If a string is passed, fetch or create the language by name
            language, created = Language.objects.get_or_create(name=data)
            return {'id': str(language.id), 'name': language.name, 'code': language.code}  # Return the id, name, and code
        return super().to_internal_value(data)

class CountrySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), required=False)
    languages = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), many=True, required=False)

    class Meta:
        model = Country
        fields = '__all__'
