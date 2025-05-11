from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Sale, Product
from .forms import LoginForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group

@login_required
def home_view(request):
    return render(request, 'core/home.html')


@permission_required('core.view_sale', raise_exception=True)
def sales_view(request):
    sales = Sale.objects.all()
    return render(request, 'core/sales.html', {'sales': sales})



@permission_required('core.view_product', raise_exception=True)
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

def register_view(request):
    try:
        form = UserRegistrationForm()
        group_names = Group.objects.values_list('name', flat=True)
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User registered successfully!')
                return redirect('login')
            else:
                messages.error(request, 'Invalid form data. Please check your input.')
        return render(request, 'core/register.html', {'form': form, 'group_names': group_names})
    except Exception as e:
        messages.error(request, f'Error during registration: {str(e)}')
        return render(request, 'core/register.html', {'error': str(e)})