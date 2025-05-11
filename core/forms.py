from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import Group
from .models import Product
from .currency import CURRENCY_CHOICES

ROLE_CHOICES = (
    ('Salesperson', 'Salesperson'),
    ('ProductManager', 'Product Manager'),
    ('Marketing', 'Marketing'),
)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
    )

    def clean(self):
        try:
            cleaned_data = super().clean()
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            
            if username and password:
                self.user = authenticate(username=username, password=password)
                if self.user is None:
                    raise forms.ValidationError('Invalid username or password')
            return cleaned_data
        except Exception as e:
            raise forms.ValidationError(f'An error occurred during validation: {str(e)}')

    def get_user(self):
        return self.user

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already in use.')
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            selected_role = self.cleaned_data['role']
            group = Group.objects.get(name=selected_role)
            user.groups.add(group)
        return user
        
    


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter product name',
            'autocomplete': 'off'
        })
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter product price',
            'min': '0.01',
            'step': '0.01'
        }),
        decimal_places=2,
        max_digits=10
    )
    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select currency'
        })
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'currency']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Price must be greater than 0.')
        return price

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Product.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Product already exists.')
        return name

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
        return product

    
    
    
