from config.celery import shared_task
from django.core.mail import send_mail
from .models import Mailing, Attempt
from django.utils.timezone import now

@shared_task
def process_mailings():
    for mailing in Mailing.objects.filter(status='created', start_time__lte=now(), end_time__gte=now()):
        for client in mailing.clients.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email='noreply@yourdomain.com',
                    recipient_list=[client.email],
                    fail_silently=False
                )
                Attempt.objects.create(
                    mailing=mailing,
                    status='Успешно',
                    server_response='Письмо доставлено'
                )
            except Exception as e:
                Attempt.objects.create(
                    mailing=mailing,
                    status='Не успешно',
                    server_response=str(e)
                )
        mailing.status = 'started'
        mailing.save()
