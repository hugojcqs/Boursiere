import schedule
from datetime.datetime import timestamp, now
import os
import time
import signal
import sys

python_os = 'python3'

if os.name == 'nt':
    python_os = 'python.exe'


def handler(signum, frame):
    os.system('%s ./manage.py stop_timer' % python_os)
    sys.exit(0)


def job():
    os.system('%s ./manage.py update_prices %s' % (python_os,
                                                   round(timestamp(now()))))


signal.signal(signal.SIGINT, handler)
schedule.every(15).minutes.do(job)

job()
print('Timer has been started!')
while 1:
    schedule.run_pending()
    time.sleep(1)
