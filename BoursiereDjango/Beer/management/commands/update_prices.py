from django.core.management.base import BaseCommand
from Beer.models import Beer, TresoFailsafe, Timer
import emoji
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not TresoFailsafe.objects.get(id=1).is_activated:
            Command._update_timer()
            Beer._update_prices()
            print(datetime.datetime.now(), emoji.emojize('The prices has been updated :heavy_check_mark:'))
        else:
            print(emoji.emojize('Cannot compute new price, system has been overrided manually :x:'))
            print('Run "python3 or python.exe .\\manage.py disable_fail_safe"')

    def _update_timer():
        timer = Timer.objects.get(id=1)
        timer.timer_is_started = True
        timer.save()
