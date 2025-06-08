from django.conf import settings
from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients'
    )

    def __str__(self):
        return self.email


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created'
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings')
    clients = models.ManyToManyField(Client, related_name='mailings')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailings'
    )

    def __str__(self):
        return f"Рассылка #{self.pk} — {self.status}"


class Attempt(models.Model):
    mailing = models.ForeignKey(
        'Mailing',
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ])
    server_response = models.TextField()

    def __str__(self):
        return f"{self.time.strftime('%Y-%m-%d %H:%M')} — {self.status}"