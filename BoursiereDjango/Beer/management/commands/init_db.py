from django.core.management.base import BaseCommand
from Beer.models import Timer, TresoFailsafe, Settings
import emoji


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Timer.objects.get(id=1)
        except Exception as e:
            print(emoji.emojize('Timer initialisation - %s but it does now :heavy_check_mark:' % e))
            Timer.objects.create(id=1, next_update=0, timer_is_started=False, current_quarter=1)

        try:
            TresoFailsafe.objects.get(id=1)
        except Exception as e:
            print(emoji.emojize('Timer initialisation - %s but it does now! :heavy_check_mark:' % e))
            TresoFailsafe.objects.create(id=1, is_activated=False)

        try:
            Settings.objects.get(id=1)
        except Exception as e:
            print(emoji.emojize('Settings initialisation - %s but it does now :heavy_check_mark:' % e))
            Settings.objects.create().save()
