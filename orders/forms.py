from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Order

from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=32, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['subx', 'topping', 'size', 'quantity']
        widgets = {
        'subx': forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            'topping': _('Hold ⇧ or ⌘ to select more toppings. '),
        }

        def clean_size(self):
            
            size = self.cleaned_data['size']

            # Check if size is valid
            if 

       
class OrderStatusForm(ModelForm):
    # status_choices = [
    #     ('pr', 'Processing'),
    #     ('c', 'Completed'),
    # ]
    # new_status = forms.ChoiceField(choices=status_choices, required=True)

    class Meta:
        model = Order
        fields = ['status']
