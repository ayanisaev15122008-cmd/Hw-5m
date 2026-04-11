from rest_framework import serializers
from api.models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    def validate_name(self, value):
        if len(value) < 2: raise serializers.ValidationError('Слишком короткое название!')
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    def validate_price(self, value):
        if value <= 0: raise serializers.ValidationError('Цена должна быть больше нуля!')
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    def validate_stars(self, value):
        if not (1 <= value <= 5): raise serializers.ValidationError('Оценка должна быть от 1 до 5!')
        return value
