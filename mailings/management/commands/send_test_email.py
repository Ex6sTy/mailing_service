
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Отправляет тестовое письмо через SMTP'

    def handle(self, *args, **options):
        try:
            send_mail(
                subject='Тестовое письмо',
                message='Это тест для проверки SMTP-настройки.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Письмо успешно отправлено!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при отправке: {e}'))
