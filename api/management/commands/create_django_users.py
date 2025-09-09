from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import User as FakeStoreUser

class Command(BaseCommand):
    help = 'Creates Django auth users for existing FakeStore users'

    def handle(self, *args, **kwargs):
        fakestore_users = FakeStoreUser.objects.all()
        created_count = 0
        skipped_count = 0
        
        self.stdout.write(self.style.SUCCESS(f'Found {fakestore_users.count()} FakeStore users'))
        
        for fs_user in fakestore_users:
            # Check if Django user with same username already exists
            if User.objects.filter(username=fs_user.username).exists():
                self.stdout.write(self.style.WARNING(f'User {fs_user.username} already exists, skipping'))
                skipped_count += 1
                continue
                
            # Create Django user with same username
            # Note: FakeStore passwords are not secure, using a default password for all users
            user = User.objects.create_user(
                username=fs_user.username,
                email=fs_user.email,
                # password='Fakestore123!'  # Using a default password
                password=fs_user.password  # Using a default password
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created Django user for {fs_user.username}'))
            created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} Django users, skipped {skipped_count}'))
        
        if created_count > 0:
            self.stdout.write(self.style.SUCCESS('All users have their FakeStore password as default password'))
