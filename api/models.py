from django.db import models
from django.utils import timezone

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

class UserAddress(models.Model):
    geolocation_lat = models.CharField(max_length=50, null=True, blank=True)
    geolocation_long = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    zipcode = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.street}, {self.city}"

class User(models.Model):
    fakestore_id = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # Note: In real apps, never store plain passwords
    name_firstname = models.CharField(max_length=100)
    name_lastname = models.CharField(max_length=100)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='users')
    phone = models.CharField(max_length=20)
    
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
