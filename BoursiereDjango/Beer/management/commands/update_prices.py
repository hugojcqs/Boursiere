from django.core.management.base import BaseCommand, CommandError
from Beer.models import Beer, History


class Command(BaseCommand):
    help = 'Update the prices'
    args = 'Next update time in ms'

    def handle(self, *args, **options):
        Beer._update_prices()
        self.stdout.write(self.style.SUCCESS('Successfully'))