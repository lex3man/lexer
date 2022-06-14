from celery import Celery

broker_url = "amqp://localhost"
redis_url = "redis://localhost"
app = Celery('tasks', broker = broker_url, backend = redis_url)

app.conf.update(
    result_expires=3600,
)