from django.core.management.base import BaseCommand
from Beer.models import Timer
import emoji


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            t = Timer.objects.get(id=1)
            t.next_update = 0
            t.timer_is_started = False
            t.current_quarter=1
            t.save()



        except Exception as e:
            print(emoji.emojize('Timer initialisation - %s but it does now :heavy_check_mark:' % e))
            Timer.objects.create(id=1, next_update=0, timer_is_started=False, current_quarter=1)
