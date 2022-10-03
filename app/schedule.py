import logging

import email_sender

from apscheduler.schedulers.background import BackgroundScheduler

import requests_saver

tz = ''
scheduler = BackgroundScheduler()
scheduler.configure(timezone=tz)

scheduler.add_job(func=email_sender.main, trigger='cron', year='*', month='*', hour='23', minute=0)
scheduler.add_job(func=requests_saver.clear_file_requests, trigger='cron', year='*', month='*', hour='23', minute=30)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
scheduler.start()
