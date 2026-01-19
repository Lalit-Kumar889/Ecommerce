from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField (max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    def __str__(self):
         return self.user.username
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending','Pending'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),

    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices= STATUS_CHOICES,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.product.name


