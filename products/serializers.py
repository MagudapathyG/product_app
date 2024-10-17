
from rest_framework import serializers
    
from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category']

    def to_representation(self, instance):
        """Decrypt price when sending data."""
        ret = super().to_representation(instance)
        ret['price'] = instance.get_price()  # Decrypt the price
        return ret

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' 


