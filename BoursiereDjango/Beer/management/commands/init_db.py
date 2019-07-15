from django.core.management.base import BaseCommand, CommandError
from Beer.models import Timer, TresoFailsafe


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Timer.objects.get(id=1)
        except Exception as e:
            print('Timer initialisation - %s but it does now!' % e)
            Timer.objects.create(id=1, next_update=0, timer_is_started=False)

        try:
            TresoFailsafe.objects.get(id=1)
        except Exception as e:
            print('Timer initialisation - %s but it does now!' % e)
            TresoFailsafe.objects.create(id=1, is_activated=False)
