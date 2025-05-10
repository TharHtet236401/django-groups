# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
