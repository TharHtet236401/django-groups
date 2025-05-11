from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_view, name='products'),
    path('sales/', views.sales_view, name='sales'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('add-product/', views.add_product_view, name='add_product'),
]

