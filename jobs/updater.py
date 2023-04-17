from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import rfi_api


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(rfi_api, 'interval', days=6)
    scheduler.start()
