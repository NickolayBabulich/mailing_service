from config import settings
from django.utils import timezone
from mailing_service.models import Client, Mailing, Logs
from django.core.mail import get_connection, EmailMultiAlternatives
import datetime


def send_mail(obj: Mailing):
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        use_ssl=settings.EMAIL_USE_SSL,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
    )
    connection.open()
    for obj_email in obj.clients.all():
        email = EmailMultiAlternatives(
            subject=obj.message.subject,
            body=obj.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[obj_email.email],
            connection=connection
        )
        status = email.send()
        now = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
        Logs.objects.create(
            time=now,
            mailing=obj,
            mail=obj_email.email,
            response=bool(status),
            owner=obj.owner
        )

    connection.close()


def mailing_worker():
    mailing_list = Mailing.objects.all()
    for obj_mail in mailing_list:
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        if obj_mail.status == 1:
            if obj_mail.time_to_start <= now:
                obj_mail.time_to_start = now
                obj_mail.status = 2
                obj_mail.save()
                # send_mail(obj_mail)
        if obj_mail.status == 2:
            if obj_mail.time_to_finish <= now:
                obj_mail.status = 0
                obj_mail.save()
            elif obj_mail.next_try <= now:
                send_mail(obj_mail)
                if obj_mail.periodicity == '1':
                    obj_mail.next_try = now + datetime.timedelta(days=1)
                elif obj_mail.periodicity == '2':
                    obj_mail.next_try = now + datetime.timedelta(days=7)
                elif obj_mail.periodicity == '3':
                    obj_mail.next_try = now + datetime.timedelta(days=30)
                obj_mail.save()
