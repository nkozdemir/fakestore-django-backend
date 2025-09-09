from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Drops all Django auth users except superusers'

    def handle(self, *args, **kwargs):
        # Count users before deletion
        total_users = User.objects.filter(is_superuser=False).count()
        
        # Delete all non-superuser users
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {total_users} users')
        )
