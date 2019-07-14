from django.core.management.base import BaseCommand, CommandError
from Beer.models import Timer

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            timer = Timer.objects.get(id=1)
            timer.timer_is_started = False
            timer.save()
        except Exception as e:
            print('Error - %s - Please run "python.exe .\\manage.py init_db" before stoping the timer' % e)