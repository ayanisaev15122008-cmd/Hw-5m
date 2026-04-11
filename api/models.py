from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    def __str__(self): return self.title

class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    def __str__(self): return f'Review for {self.product.title}'
