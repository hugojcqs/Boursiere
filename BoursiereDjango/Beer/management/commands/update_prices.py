from django.core.management.base import BaseCommand
from Beer.models import Beer, TresoFailsafe, Timer, Settings
import emoji
import datetime
from django.core import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .ws_notifier import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not TresoFailsafe.objects.get(id=1).is_activated:
            Command.update_timer()
            Beer.update_prices()
            WSNotifier.notify_sound()
            print(datetime.datetime.now(), emoji.emojize('The prices has been updated :heavy_check_mark:'))
        else:
            print(emoji.emojize('Cannot compute new price, system has been overrided manually :x:'))
            print('Run "python3 or python.exe .\\manage.py disable_fail_safe"')

    @staticmethod
    def update_timer():
        timer = Timer.objects.get(id=1)
        timer.timer_is_started = True
        timer.save()

    @staticmethod
    def update_next_update():
        timer = Timer.objects.get(id=1)
        timer.timer_is_started = True
        timer.current_quarter += 1
        timer.next_update = (datetime.timestamp(datetime.now()) + Settings.objects.get(pk=1).quarter_time*60)
        timer.save()
