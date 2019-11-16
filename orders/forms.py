from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

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
    
    def clean_renewal_date(self):
        data = self.cleaned_data['size']
        
        # Check if size has been selected. 
        if data == "":
            raise ValidationError(_('You must choose size'))

        # Remember to always return the cleaned data.
        return data

       
class OrderStatusForm(ModelForm):

    class Meta:
        model = Order
        fields = ['status']
