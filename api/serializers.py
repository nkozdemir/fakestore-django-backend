from rest_framework import serializers
from django.conf import settings
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the unified User model"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'fakestore_id', 'phone')

class FakeStoreUserSerializer(serializers.ModelSerializer):
    """Serializer for FakeStore shaped data from unified User model"""
    class Meta:
        model = User
        fields = ('fakestore_id', 'email', 'username')
