from apscheduler.schedulers.blocking import BlockingScheduler
import requests

import datetime
from time import strftime

sched = BlockingScheduler()
TOKEN = 'CABB74F774DD3ACB'


@sched.scheduled_job('interval', minutes=15)        # timer function , can replace seconds with minutes, hours, etc...
def timed_job():
    data = {'token':'CABB74F774DD3ACB'}
    r = requests.post(url='http://127.0.0.1:8000/update_price/', data=data)
    #print(r.text)
    print('%s | POST(update request) | (token=%s)' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),TOKEN))

sched.start()       # launch timer


# --- make a task at a precise time ---

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')
