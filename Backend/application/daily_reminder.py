from celery.schedules import crontab
from json import dumps
from httplib2 import Http
from datetime import datetime
import time
from .models import *
from .tasks import celery

WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAUSNB9Lg/messages?key=" \
              "AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=tq3YiYiiAX6Vw8LvKMoBpo7LTFnFurhDOfAbTkcdNgQ"


@celery.task
def daily_reminder():
    users = Users.query.all()
    if users:
        for user in users:
            time_difference = datetime.now() - user.login_time 
            hours = (time_difference.total_seconds()) / 3600
            if hours > 24:
                url = WEBHOOK_URL
                app_message = {
                    'text': 'Hi there. Visit Ticket Show today to book your favourite shows'}
                message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
                http_obj = Http()
                response = http_obj.request(
                    uri=url,
                    method='POST',
                    headers=message_headers,
                    body=dumps(app_message),
                )
                print(response)
                return "Daily Reminder will be sent shortly..."


@celery.on_after_configure.connect
def setup_daily_reminder(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=14, minute=12),
        daily_reminder.s(),
    )