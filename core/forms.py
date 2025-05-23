from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import Group
from .models import Product, Sale, Task
from .lists import CURRENCY_CHOICES, TASK_TYPE_CHOICES, TASK_STATUS_CHOICES

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

    
    
    
class SaleForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select a product'
        })
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter quantity',
            'min': '1'
        })
    )

    class Meta:
        model = Sale
        fields = ['product', 'quantity']

    def clean_product(self):
        product = self.cleaned_data['product']
        if product is None:
            raise forms.ValidationError('Product is required.')
        return product

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than 0.')
        return quantity


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter task title',
            'autocomplete': 'off'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter task description',
            'rows': 4
        }),
        required=False
    )
    task_type = forms.ChoiceField(
        choices=TASK_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select task type'
        })
    )
    task_status = forms.ChoiceField(
        choices=TASK_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select task status'
        })
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select assignee'
        })
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'task_type', 'task_status', 'assigned_to']

    def clean_title(self):
        try:
            title = self.cleaned_data['title']
            if len(title.strip()) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
            return title
        except Exception as e:
            raise forms.ValidationError(f'Error validating title: {str(e)}')

    def clean_assigned_to(self):
        try:
            assigned_to = self.cleaned_data['assigned_to']
            if assigned_to is None:
                raise forms.ValidationError('Please select an assignee.')
            return assigned_to
        except Exception as e:
            raise forms.ValidationError(f'Error validating assignee: {str(e)}')

    def save(self, commit=True):
        try:
            task = super().save(commit=False)
            if commit:
                task.save()
            return task
        except Exception as e:
            raise forms.ValidationError(f'Error saving task: {str(e)}')







