from django.core.management.base import BaseCommand
from datetime import datetime
import keyboard
import time
import sys
import os

class Command(BaseCommand):
    def handle(self, *args, **options):

        '''
        Final Command for launch the Boursiere.

        TODO: add color
        TODO: each second print the time
        TODO: type launch to launch
        TODO: when launch is type, set all cmd
        TODO: add keyboard to pip requirements
        '''

        launched = False

        while not launched:
            launched = str(input('type launch to start: ')).upper() == 'LAUNCH'
            time.sleep(1)
        self.launch()
        

    def launch(self):

        #run not syncroned command

        os.system("python3 ./manage.py init_db")
        os.system("python3 ./manage.py stop_timer")
        os.system("python3 ./manage.py disable_fail_safe")
        os.system("python3 ./manage.py reset_timer")

        os.system("python3 ./manage.py parse")

        now = datetime.now()
        seconds = int (now.strftime("%S"))
        minutes = int (now.strftime("%M"))

        while not ((minutes % 15) == 0 and seconds == 0) :

            time.sleep(1)

            remin = 15-(minutes%15)
            resec = 60 - seconds

            print('wait .. %d:%d'%(remin, resec))

            now = datetime.now()
            seconds = int (now.strftime("%S"))
            minutes = int (now.strftime("%M"))

        #run all timer needs script
        #TODO: run it in a screen
        os.system("python3 ./timer.py")

        print('--- boursiere launched ---')