from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category,Product,Cart,CartItem,Order,OrderItem

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['id','username','email','password']


    def create(self,validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    
class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ['id','name']

    
class ProductSerializer(serializers.ModelSerializer):
        category = CategorySerializer(read_only=True)
        category_id = serializers.PrimaryKeyRelatedField(
            queryset = Category.objects.all(),source='category',write_only = True

        )

        class Meta:
         model = Product
         fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'category', 'category_id']

class CartItemSerializer(serializers.ModelSerializer):
     product = ProductSerializer(read_only=True)
     product_id = serializers.PrimaryKeyRelatedField(
          queryset = Product.objects.all(),source='product',write_only = True
     )


     class Meta:
          model = CartItem
          fields = ['id','product','product_id','quantity']

class CartSerializer(serializers.ModelSerializer):
     items = CartItemSerializer(many=True,read_only=True)

     class Meta:
          model = Cart
          fields = ['id','user','items']


class OrderItemSerializer(serializers.ModelSerializer):
     product = ProductSerializer(read_only=True)


     class Meta:
          model = OrderItem
          fields = ['id','product','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'items']
