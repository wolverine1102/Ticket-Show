from celery import Celery

celery = Celery('daily_reminder',
                 broker='redis://localhost:6379/',
                 backend='redis://localhost:6379/',
                 enable_utc=False,
                 timezone='Asia/Kolkata'
                 )
