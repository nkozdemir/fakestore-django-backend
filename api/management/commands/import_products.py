import requests
from django.core.management.base import BaseCommand
from django.db import connection, ProgrammingError
from api.models import Product

class Command(BaseCommand):
    help = 'Fetch products from FakeStore API and save to the database'

    def handle(self, *args, **kwargs):
        # Check if the product table exists
        try:
            # Try to get count of products as a lightweight way to check if table exists
            product_count = Product.objects.count()
            self.stdout.write(f"Found {product_count} existing products in database")
            # Clear existing products if the table exists
            Product.objects.all().delete()
        except ProgrammingError:
            self.stdout.write(self.style.WARNING("Product table doesn't exist yet. Run migrations first with:"))
            self.stdout.write("python manage.py migrate api")
            return
        
        # Fetch products from FakeStore API
        response = requests.get('https://fakestoreapi.com/products')
        products = response.json()
        
        # Save products to database
        for product_data in products:
            rating = product_data.get('rating', {})
            
            Product.objects.create(
                fakestore_id=product_data['id'],
                title=product_data['title'],
                price=product_data['price'],
                description=product_data['description'],
                category=product_data['category'],
                image=product_data['image'],
                rating_rate=rating.get('rate'),
                rating_count=rating.get('count')
            )
            
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(products)} products'))
