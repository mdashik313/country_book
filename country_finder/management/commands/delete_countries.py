from django.core.management.base import BaseCommand
from country_finder.models import Country

class Command(BaseCommand):
    help = 'Delete countries from the database with an optional limit.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Number of countries to delete (default: all)'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        countries = Country.objects.all().order_by('id')

        if limit:
            countries = list(countries[:limit])
        else:
            countries = list(countries)

        total = len(countries)

        if countries:
            Country.objects.filter(pk__in=[c.pk for c in countries]).delete()

        self.stdout.write(self.style.SUCCESS(f"✅ Deleted {total} country(ies) from the database."))
