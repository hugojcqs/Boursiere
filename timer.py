from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
token = 'CABB74F774DD3ACB'


@sched.scheduled_job('interval', seconds=15)        # timer function , can replace seconds with minutes, hours, etc...
def timed_job():
    print('send http request to url , (token: %s)' % token)

sched.start()       # launch timer


# --- make a task at a precise time ---

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')
