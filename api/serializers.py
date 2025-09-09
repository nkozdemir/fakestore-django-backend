from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User as FakeStoreUser

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the Django User model (for JWT authentication)"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class FakeStoreUserSerializer(serializers.ModelSerializer):
    """Serializer for our FakeStore User model"""
    class Meta:
        model = FakeStoreUser
        fields = ('fakestore_id', 'email', 'username')
