import schedule
from datetime import datetime
import os
import time
import signal
import sys
from BoursiereDjango import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BoursiereDjango.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from Beer.models import Settings



python_os = 'python3'

if os.name == 'nt':
    python_os = 'python.exe'


def handler(signum, frame):
    os.system('%s ./manage.py stop_timer' % python_os)
    #os.system('py ./manage.py stop_timer')
    sys.exit(0)


def job():
    os.system('%s ./manage.py update_prices' % python_os)
    #os.system('py ./manage.py update_prices')

signal.signal(signal.SIGINT, handler)
schedule.every(Settings.objects.all()[0].quarter_time).minutes.do(job)

job()
print('Timer has been started!')
while 1:
    schedule.run_pending()
    time.sleep(1)
