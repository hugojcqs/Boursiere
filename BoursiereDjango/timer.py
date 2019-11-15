import schedule
from datetime import datetime
import os
import time
import signal
import sys

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
schedule.every(1).minutes.do(job)

job()
print('Timer has been started!')
while 1:
    schedule.run_pending()
    time.sleep(1)
