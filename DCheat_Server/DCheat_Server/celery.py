from __future__ import absolute_import
from celery import Celery

app = Celery('task',
             broker='amqp://guest:guest@localhost:5672',
             include=['task'])

if __name__ == '__main__':
    app.start()