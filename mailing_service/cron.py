from mailing_service.services import mailing_worker


def my_scheduled_job():
    mailing_worker()
