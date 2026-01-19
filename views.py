from rest_framework import generics,permissions
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Category,Product,Cart,CartItem,Order,OrderItem
from.serializers import (

    UserSerializer,CategorySerializer,ProductSerializer,
    CartSerializer,CartItemSerializer,OrderSerializer
)


# Create your views here.

#user registration

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

#product view

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


#CartView

class CartView(APIView):
    def get(self,request):
        cart,created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if quantity <= 0:
            return Response(
                {"error": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        cart_item.quantity += quantity if not created else quantity
        cart_item.save()

        return Response({"message": "Product added to cart"})

# order view

class OrderCreateView(APIView):
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_price = sum(
            item.product.price * item.quantity
            for item in cart.items.all()
        )

        order = Order.objects.create(
            user=request.user,
            total_price=total_price
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()
        return Response(OrderSerializer(order).data)


