from __future__ import absolute_import
from celery import Celery

app = Celery('tasks',
             broker='amqp://guest:guest@localhost:5672',
             include=['tasks'])

if __name__ == '__main__':
    app.start()