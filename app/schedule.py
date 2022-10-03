import logging

import email_sender

from apscheduler.schedulers.background import BackgroundScheduler

import requests_saver

tz = ''
scheduler = BackgroundScheduler()
scheduler.configure(timezone=tz)