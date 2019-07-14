from django.core.management.base import BaseCommand, CommandError
from Beer.models import Beer, History


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('time', type=int, help='Next utime for update in second')

    def handle(self, *args, **options):
        Beer._update_prices()