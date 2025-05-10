from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Sale, Product
from .forms import LoginForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'core/home.html')

@login_required
def sales_view(request):
    sales = Sale.objects.all()
    return render(request, 'core/sales.html', {'sales': sales})

@login_required
def product_view(request):
    products = Product.objects.all()
    return render(request, 'core/products.html', {'products': products})

def login_view(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, 'Welcome back! Login successful.')
                return redirect('home')
        else:
            form = LoginForm()
        return render(request, 'core/login.html', {'form': form})
        
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return render(request, 'core/login.html', {'form': LoginForm()})

def logout_view(request):
    logout(request)
    return redirect('login')


