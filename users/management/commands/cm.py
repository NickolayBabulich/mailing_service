from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='moder@mailing.com',
            first_name='James',
            last_name='Hatfild',
            is_staff=True,
        )
        user.set_password('1')
        user.save()
