from rest_framework import serializers
from api.models import Category, Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars product'.split()
    
    def validate_stars(self, value):
        if not (1 <= value <= 5): raise serializers.ValidationError('Оценка должна быть от 1 до 5!')
        return value

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title description price category reviews rating'.split()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return sum([r.stars for r in reviews]) / reviews.count()
        return 0

    def validate_price(self, value):
        if value <= 0: raise serializers.ValidationError('Цена должна быть больше нуля!')
        return value

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, obj):
        return obj.products.count()
