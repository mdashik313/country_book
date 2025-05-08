import requests
from django.core.management.base import BaseCommand
from country_finder.models import Country, Language, Region
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch a single country from REST Countries API by CCA3 code'

    def add_arguments(self, parser):
        parser.add_argument('cca3', type=str, help='CCA3 code of the country (e.g., USA)')

    def handle(self, *args, **kwargs):
        cca3 = kwargs['cca3'].upper()
        print('fetching single')
        # Modified URL to fetch a single country by CCA3 code
        url = f"https://restcountries.com/v3.1/alpha/{cca3}"
        print('fetching completed single')
        try:
            response = requests.get(url)
            response.raise_for_status()
            # Changed to handle single country data directly
            country_data = response.json()[0] if isinstance(response.json(), list) else response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch data for CCA3 {cca3}: {e}")
            self.stdout.write(self.style.ERROR(f"Failed to fetch data for CCA3 {cca3}: {e}"))
            return
        except (KeyError, IndexError):
            logger.error(f"No country found with CCA3: {cca3}")
            self.stdout.write(self.style.ERROR(f"No country found with CCA3: {cca3}"))
            return

        try:
            # Handle languages
            language_objects = []
            if 'languages' in country_data:
                for code, name in country_data['languages'].items():
                    lang, _ = Language.objects.get_or_create(
                        code=code,
                        defaults={'name': name}
                    )
                    language_objects.append(lang)

            # Handle regions
            region_objects = []
            if 'region' in country_data and country_data['region']:
                region, _ = Region.objects.get_or_create(
                    name=country_data['region']
                )
                region_objects.append(region)

            # Create or update country
            country, created = Country.objects.update_or_create(
                cca3=country_data.get('cca3'),
                defaults={
                    'name_common': country_data.get('name', {}).get('common', ''),
                    'name_official': country_data.get('name', {}).get('official', ''),
                    'tld': country_data.get('tld', []),
                    'cca2': country_data.get('cca2', ''),
                    'ccn3': country_data.get('ccn3', ''),
                    'cioc': country_data.get('cioc', ''),
                    'independent': country_data.get('independent', False),
                    'status': country_data.get('status', ''),
                    'un_member': country_data.get('unMember', False),
                    'currencies': country_data.get('currencies', {}),
                    'idd_root': country_data.get('idd', {}).get('root', ''),
                    'idd_suffixes': country_data.get('idd', {}).get('suffixes', []),
                    'capital': country_data.get('capital', []),
                    'alt_spellings': country_data.get('altSpellings', []),
                    'subregion': country_data.get('subregion', ''),
                    'translations': country_data.get('translations', {}),
                    'latlng': country_data.get('latlng', []),
                    'landlocked': country_data.get('landlocked', False),
                    'borders': country_data.get('borders', []),
                    'area': country_data.get('area', 0.0),
                    'demonyms': country_data.get('demonyms', {}),
                    'flag_emoji': country_data.get('flag', ''),
                    'maps_google': country_data.get('maps', {}).get('googleMaps', ''),
                    'maps_openstreet': country_data.get('maps', {}).get('openStreetMaps', ''),
                    'population': country_data.get('population', 0),
                    'gini': country_data.get('gini', {}),
                    'fifa': country_data.get('fifa', ''),
                    'car_signs': country_data.get('car', {}).get('signs', []),
                    'car_side': country_data.get('car', {}).get('side', ''),
                    'timezones': country_data.get('timezones', []),
                    'continents': country_data.get('continents', []),
                    'flag_png': country_data.get('flags', {}).get('png', ''),
                    'flag_svg': country_data.get('flags', {}).get('svg', ''),
                    'flag_alt': country_data.get('flags', {}).get('alt', ''),
                    'coat_of_arms_png': country_data.get('coatOfArms', {}).get('png', ''),
                    'coat_of_arms_svg': country_data.get('coatOfArms', {}).get('svg', ''),
                    'start_of_week': country_data.get('startOfWeek', ''),
                    'capital_info_latlng': country_data.get('capitalInfo', {}).get('latlng', []),
                    'postal_code_format': country_data.get('postalCode', {}).get('format', ''),
                    'postal_code_regex': country_data.get('postalCode', {}).get('regex', ''),
                    'native_names': country_data.get('name', {}).get('nativeName', {}),
                }
            )

            # Set many-to-many relationships
            country.languages.set(language_objects)
            # Changed to set region as ForeignKey
            if region_objects:
                country.region = region_objects[0]
                country.save()

            self.stdout.write(self.style.SUCCESS(f"Processed {country.name_common}"))

        except Exception as e:
            logger.error(f"Error processing {country_data.get('name', {}).get('common', 'Unknown')}: {e}")
            self.stdout.write(self.style.WARNING(f"Error processing {country_data.get('name', {}).get('common', 'Unknown')}"))