from app import celery

@celery.task()
def send_async_email():
    return 'this works!'