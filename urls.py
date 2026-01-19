from django.urls import path
from .views import (
    RegisterView, ProductListView, ProductDetailView,
    CartView, AddToCartView, OrderCreateView
)

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    
    path('products/',ProductListView.as_view(),name='product-list'),
    path('products/<int:pk>/',ProductDetailView.as_view(),name='product-details'),

    path('cart/',CartView.as_view(),name='cart'),
    path('cart/add/',AddToCartView.as_view(),name='cart-add'),

    path('orders/create/',OrderCreateView.as_view(),name='order-create'),

]
