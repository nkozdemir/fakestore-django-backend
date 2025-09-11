
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import db_views
from . import user_views
from . import cart_views
from . import auth_views

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
    
    # JWT Authentication endpoints
    path('auth/register/', auth_views.RegisterView.as_view(), name='auth-register'),
    path('auth/login/', auth_views.LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', auth_views.UserInfoView.as_view(), name='user-info'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/logout-all/', auth_views.LogoutAllView.as_view(), name='logout_all'),
]
