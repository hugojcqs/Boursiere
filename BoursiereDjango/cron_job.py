import schedule
import datetime
import os
import time
def job():
    os.system('python.exe D:/Documents/GIT/Boursi-re/BoursiereDjango/manage.py update_prices %s' % round(datetime.datetime.timestamp(datetime.datetime.now())))
    print('python.exe D:/Documents/GIT/Boursi-re/BoursiereDjango/manage.py update_prices %s' % round(datetime.datetime.timestamp(datetime.datetime.now())))

schedule.every(15).minutes.do(job)

job()
while 1:
    schedule.run_pending()
    time.sleep(1)