import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import User, UserAddress

class Command(BaseCommand):
    help = 'Fetch users from FakeStore API and save to the database'

    def handle(self, *args, **kwargs):
        try:
            # Clear existing users (non-superusers) and addresses
            User.objects.filter(is_superuser=False).delete()
            UserAddress.objects.all().delete()
            
            # Fetch users from FakeStore API
            response = requests.get('https://fakestoreapi.com/users')
            users = response.json()
            
            # Save users to database
            with transaction.atomic():
                for user_data in users:
                    # Create user address
                    address_data = user_data.get('address', {})
                    geolocation = address_data.get('geolocation', {})
                    
                    address = UserAddress.objects.create(
                        geolocation_lat=geolocation.get('lat'),
                        geolocation_long=geolocation.get('long'),
                        city=address_data.get('city', ''),
                        street=address_data.get('street', ''),
                        number=address_data.get('number', 0),
                        zipcode=address_data.get('zipcode', '')
                    )
                    
                    # Create user
                    name = user_data.get('name', {})
                    # Use create_user to hash password
                    user = User.objects.create_user(
                        username=user_data.get('username', ''),
                        email=user_data.get('email', ''),
                        password=user_data.get('password', ''),
                        first_name=name.get('firstname', ''),
                        last_name=name.get('lastname', ''),
                    )
                    user.fakestore_id = user_data.get('id')
                    user.address = address
                    user.phone = user_data.get('phone', '')
                    user.name_firstname = name.get('firstname', '')
                    user.name_lastname = name.get('lastname', '')
                    user.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(users)} users'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to import users: {str(e)}'))
