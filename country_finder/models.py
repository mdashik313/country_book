from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3, unique=True)

    # class Meta:
    #     db_table = "language"
    #     managed = False

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name_common = models.CharField(max_length=50)
    name_official = models.CharField(max_length=100)
    tld = models.JSONField(blank=True, null=True)
    cca2 = models.CharField(max_length=2, unique=True)
    ccn3 = models.CharField(max_length=3, blank=True, null=True)
    cca3 = models.CharField(max_length=3, unique=True)
    cioc = models.CharField(max_length=3, blank=True, null=True)
    independent = models.BooleanField(default=False)
    status = models.CharField(max_length=50)
    un_member = models.BooleanField(default=False)
    currencies = models.JSONField(blank=True, null=True)
    idd_root = models.CharField(max_length=10, blank=True, null=True)
    idd_suffixes = models.JSONField(blank=True, null=True)
    capital = models.JSONField(blank=True, null=True)
    alt_spellings = models.JSONField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='countries')
    subregion = models.CharField(max_length=50, blank=True, null=True)
    languages = models.ManyToManyField(Language)
    translations = models.JSONField(blank=True, null=True)
    latlng = models.JSONField(blank=True, null=True)
    landlocked = models.BooleanField(default=False)
    borders = models.JSONField(blank=True, null=True)
    area = models.FloatField()
    demonyms = models.JSONField(blank=True, null=True)
    flag_emoji = models.CharField(max_length=10, blank=True, null=True)
    maps_google = models.URLField(max_length=200, blank=True, null=True)
    maps_openstreet = models.URLField(max_length=200, blank=True, null=True)
    population = models.BigIntegerField()
    gini = models.JSONField(blank=True, null=True)
    fifa = models.CharField(max_length=3, blank=True, null=True)
    car_signs = models.JSONField(blank=True, null=True)
    car_side = models.CharField(max_length=10, blank=True, null=True)
    timezones = models.JSONField(blank=True, null=True)
    continents = models.JSONField(blank=True, null=True)
    flag_png = models.URLField(max_length=200, blank=True, null=True)
    flag_svg = models.URLField(max_length=200, blank=True, null=True)
    flag_alt = models.TextField(blank=True, null=True)
    coat_of_arms_png = models.URLField(max_length=200, blank=True, null=True)
    coat_of_arms_svg = models.URLField(max_length=200, blank=True, null=True)
    start_of_week = models.CharField(max_length=10, blank=True, null=True)
    capital_info_latlng = models.JSONField(blank=True, null=True)
    postal_code_format = models.CharField(max_length=50, blank=True, null=True)
    postal_code_regex = models.TextField(blank=True, null=True)
    native_names = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name_common