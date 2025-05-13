# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .lists import CURRENCY_CHOICES, TASK_TYPE_CHOICES, TASK_STATUS_CHOICES


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

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=200, choices=TASK_TYPE_CHOICES, default='Sales')
    task_status = models.CharField(max_length=200, choices=TASK_STATUS_CHOICES, default='Pending')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
    

