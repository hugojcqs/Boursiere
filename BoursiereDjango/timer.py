import schedule
import datetime
import os
import time
import signal
import sys


def handler(signum, frame):
    os.system('python ./manage.py stop_timer')
    print('Timer has been stopped!')
    sys.exit(0)


signal.signal(signal.SIGINT, handler)


def job():
    os.system('python ./manage.py update_prices %s' % round(datetime.datetime.timestamp(datetime.datetime.now())))
    print('python ./manage.py update_prices %s' % round(datetime.datetime.timestamp(datetime.datetime.now())))

schedule.every(15).minutes.do(job)

job()
print('Timer has been started!')
while 1:
    schedule.run_pending()
    time.sleep(1)
