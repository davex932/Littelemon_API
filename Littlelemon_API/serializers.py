from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['id', 'username', 'email', 'groups']

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class MenuItemSerializer(serializers.ModelSerializer):
    category= categorySerializer(read_only=True)
    category_id=serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    class Meta:
        model= MenuItem
        fields= ['id', 'category_id', 'title', 'price', 'featured', 'category']

class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField()  
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['price', 'user']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields= ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= OrderItem
        fields= '__all__'
    


    