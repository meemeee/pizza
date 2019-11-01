from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class OrderDish(forms.Form):
    size_choices = [
        ('none', 'none'),
        ('small', 'small'),
        ('large', 'large'),
    ]
    topping = ???
    size = forms.CharField(choices=size_choices, default='none', required=False)
    quantity = forms.IntegerField(max_value=10, min_value=1, default=1)