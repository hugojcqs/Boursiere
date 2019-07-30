from django.core.management.base import BaseCommand
from Beer.models import TresoFailsafe
import emoji


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            t = TresoFailsafe.objects.get(id=1)
            t.is_activated = False
            t.save()
            print(emoji.emojize("The failsafe has been disabled :heavy_check_mark:"))
        except Exception as e:
            print(emoji.emojize("An error ocured while disabling the failsafe %e:x:" % e))
