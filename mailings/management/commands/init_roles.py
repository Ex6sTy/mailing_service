from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from mailings.models import Client, Message, Mailing

class Command(BaseCommand):
    help = "Создать группу Менеджеры с правами"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        for model in [Client, Message, Mailing]:
            perms = Permission.objects.filter(content_type__app_label="mailings", content_type__model=model._meta.model_name, codename__startswith="can_view_all")
            group.permissions.add(*perms)

        self.stdout.write(self.style.SUCCESS("Группа 'Менеджеры' создана и права добавлены"))
