# from celery.decorators import task
from celery.task import task
from celery.utils.log import get_task_logger

from doggroomer.emails import send_reminder_email

logger = get_task_logger(__name__)


@task(name="send_reminder_email_task")
def send_reminder_email_task(booking_time, dog_name, email):
    """sends an email in async mode """
    logger.info("Sent feedback email")
    return send_reminder_email(booking_time, dog_name, email)


@task(name="test_task")
def add(x,y):
    return x+y