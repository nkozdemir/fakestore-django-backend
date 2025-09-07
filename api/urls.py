
from django.urls import path
from . import views

urlpatterns = [

    # Products
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Carts
    path('carts/', views.CartListView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', views.CartDetailView.as_view(), name='cart-detail'),
    path('carts/user/<int:user_id>/', views.UserCartListView.as_view(), name='user-cart-list'),


    # Users
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),


    # Auth
    path('auth/login/', views.AuthLoginView.as_view(), name='auth-login'),
]
