from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import MinLengthValidator

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




