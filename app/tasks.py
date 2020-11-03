import app
from app import celery

@celery.task
def test_task():
    print('this works!')