# core/admin.py
from django.contrib import admin
from .models import Product, Sale, Task

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Task)
