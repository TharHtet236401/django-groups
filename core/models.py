# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

CURRENCY_CHOICES = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('GBP', 'GBP'),
    ('JPY', 'JPY'),
    ('AUD', 'AUD'),
    ('CAD', 'CAD'),
    ('CHF', 'CHF'),
    ('CNY', 'CNY'),
    ('SEK', 'SEK'),
    ('NZD', 'NZD'),
)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2 , validators=[MinValueValidator(0.01)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')


    def __str__(self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
