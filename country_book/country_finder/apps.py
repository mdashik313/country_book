from django.apps import AppConfig


class CountryFinderConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'country_finder'
