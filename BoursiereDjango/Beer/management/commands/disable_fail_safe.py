from django.core.management.base import BaseCommand, CommandError
from Beer.models import Beer, History, TresoFailsafe


class Command(BaseCommand):
    def handle(self, *args, **options):
        t = TresoFailsafe.objects.get(id=1)
        t.is_activbated = False
        t.save()
        print(t.is_activbated)
        print('Failsafe DISABLED - Price will now be computed using the system algorithm')
