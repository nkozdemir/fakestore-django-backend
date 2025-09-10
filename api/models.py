from django.db import models
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.URLField()
    rating_rate = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    rating_count = models.IntegerField(null=True)
    fakestore_id = models.IntegerField(unique=True)
    
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        """Invalidate cache when a product is saved or updated"""
        # Invalidate product list cache
        cache.delete('product_list')
        
        # Invalidate specific product cache if it exists
        if self.fakestore_id:
            cache.delete(f'product_{self.fakestore_id}')
            
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        """Invalidate cache when a product is deleted"""
        # Invalidate product list cache
        cache.delete('product_list')
        
        # Invalidate specific product cache
        cache.delete(f'product_{self.fakestore_id}')
        
        super().delete(*args, **kwargs)

class UserAddress(models.Model):
    geolocation_lat = models.CharField(max_length=50, null=True, blank=True)
    geolocation_long = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    zipcode = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.street}, {self.city}"

class User(AbstractUser):
    """Unified User model combining Django auth user and FakeStore user fields.
    - Uses Django auth fields: username, email, password (hashed), first_name, last_name
    - Adds FakeStore fields: fakestore_id, address, phone
    - Keeps name_firstname/name_lastname for API compatibility
    """
    fakestore_id = models.IntegerField(unique=True, null=True, blank=True)
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    phone = models.CharField(max_length=20, blank=True)
    # Duplicate name fields for legacy API compatibility (optional)
    name_firstname = models.CharField(max_length=100, blank=True)
    name_lastname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

class Cart(models.Model):
    fakestore_id = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Cart {self.fakestore_id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
