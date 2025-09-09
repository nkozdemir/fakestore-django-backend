
from django.urls import path
from . import db_views
from . import user_views
from . import cart_views
from . import fakestore_auth_views

urlpatterns = [
    # Database-backed product endpoints
    path('products/', db_views.DBProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', db_views.DBProductDetailView.as_view(), name='product-detail'),
    
    # Database-backed user endpoints
    path('users/', user_views.DBUserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', user_views.DBUserDetailView.as_view(), name='user-detail'),
    
    # Database-backed cart endpoints
    path('carts/', cart_views.DBCartListView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', cart_views.DBCartDetailView.as_view(), name='cart-detail'),
    path('carts/user/<int:user_id>/', cart_views.DBUserCartListView.as_view(), name='user-cart-list'),
    
    # FakeStore API direct proxy for authentication
    path('auth/login/', fakestore_auth_views.AuthLoginView.as_view(), name='auth-login'),
]
