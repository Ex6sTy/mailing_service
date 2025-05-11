from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Mailing, MailingAttempt
from django.conf import settings

def check_and_send_mailings():
    active_mailings = Mailing.objects.filter(
        status='created',
        start_time__lte=now(),
        end_time__gte=now()
    )

    for mailing in active_mailings:
        message = mailing.message
        for client in mailing.clients.all():
            already_sent = MailingAttempt.objects.filter(mailing=mailing, mailing__clients=client).exists()
            if already_sent:
                continue

            try:
                send_mail(
                    subject=message.subject,
                    message=message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="success",
                    server_response="OK"
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="failure",
                    server_response=str(e)
                )

        mailing.status = "started"
        mailing.save()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(check_and_send_mailings, "interval", seconds=30, id="mailing_check", replace_existing=True)
    scheduler.start()
