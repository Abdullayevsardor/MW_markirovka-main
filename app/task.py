from app.celery import celery

@celery.task
def heavy_task(x, y):
    return x + y
