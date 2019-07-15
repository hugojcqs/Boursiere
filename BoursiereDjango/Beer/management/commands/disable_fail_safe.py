from django.core.management.base import BaseCommand, CommandError
from Beer.models import Beer, History, TresoFailsafe


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            t = TresoFailsafe.objects.get(id=1)
            t.is_activated = False
            t.save()
            print(t.is_activated)
            print('Failsafe DISABLED - Price will now be computed using the system algorithm')
        except Exception as e:
            print(e)