from django.core.management.base import BaseCommand
from Beer.models import Timer
import emoji


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            timer = Timer.objects.get(id=1)
            timer.timer_is_started = False
            timer.save()
            print(emoji.emojize('The timer has been stopped :heavy_check_mark:'))
        except Exception as e:
            print(emoji.emojize('Error - %s - Please run "python.exe .\\manage.py init_db" before stoping the timer :x:' % e))
