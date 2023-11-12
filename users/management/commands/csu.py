from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mailing.com',
            first_name='Arya',
            last_name='Stark',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('1')
        user.save()
