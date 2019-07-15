from django.core.management.base import BaseCommand, CommandError
from Beer.models import Beer, History, TresoFailsafe


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('time', type=int, help='Next utime for update in second')

    def handle(self, *args, **options):
        if not TresoFailsafe.objects.get(id=1).is_activated:
            Beer._update_prices()
        else:
            print('Cannot compute new price, system has been overrided manually\nRun "py .\\manage.py disbale_fail_safe"')