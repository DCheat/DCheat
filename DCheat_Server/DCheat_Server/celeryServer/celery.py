from celery import Celery

app = Celery('celeryServer',
             broker='amqp://guest:guest@localhost:5672',
             include=['.task'])

if __name__ == '__main__':
    app.start()