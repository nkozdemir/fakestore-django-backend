import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Cart, CartItem, User, Product
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Fetch carts from FakeStore API and save to the database'

    def handle(self, *args, **kwargs):
        try:
            # Clear existing carts
            Cart.objects.all().delete()
            CartItem.objects.all().delete()
            
            # Fetch carts from FakeStore API
            response = requests.get('https://fakestoreapi.com/carts')
            carts = response.json()
            
            # Save carts to database
            with transaction.atomic():
                for cart_data in carts:
                    # Get user (skip if user doesn't exist)
                    try:
                        user = User.objects.get(fakestore_id=cart_data.get('userId'))
                    except User.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"User {cart_data.get('userId')} not found, skipping cart {cart_data.get('id')}"))
                        continue
                    
                    # Create cart
                    cart = Cart.objects.create(
                        fakestore_id=cart_data.get('id'),
                        user=user,
                        date=parse_datetime(cart_data.get('date')) if cart_data.get('date') else None
                    )
                    
                    # Add cart items
                    for item_data in cart_data.get('products', []):
                        try:
                            product = Product.objects.get(fakestore_id=item_data.get('productId'))
                            CartItem.objects.create(
                                cart=cart,
                                product=product,
                                quantity=item_data.get('quantity', 1)
                            )
                        except Product.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f"Product {item_data.get('productId')} not found, skipping"))
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(carts)} carts'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to import carts: {str(e)}'))
