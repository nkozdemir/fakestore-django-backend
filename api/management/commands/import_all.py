from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Import all data from FakeStore API'

    def handle(self, *args, **kwargs):
        # First import products
        self.stdout.write(self.style.NOTICE('Importing products...'))
        call_command('import_products')
        
        # Then import users
        self.stdout.write(self.style.NOTICE('Importing users...'))
        call_command('import_users')
        
        # Finally import carts (depends on users and products)
        self.stdout.write(self.style.NOTICE('Importing carts...'))
        call_command('import_carts')
        
        self.stdout.write(self.style.SUCCESS('All data imported successfully'))
