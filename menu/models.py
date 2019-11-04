from django.db import models
from django.conf import settings
from django.db.models import Q

# Create your models here.

class PizzaType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class ToppingChoice(models.Model):
    topping = models.CharField(max_length=32)
    
    def __str__(self):
        return f"{self.topping}"

class Size(models.Model):
    size = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.size}"

class Toppings(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"

class SubsType(models.Model):
    name = models.CharField(max_length=64)  
    subs_extra = models.BooleanField(default=False) # Extra toppings for subs
    steak_subs_extra = models.BooleanField(default=False) # limited to Steak subs

    def __str__(self):
        return f"{self.name}"  

class DinnerPlattersType(models.Model):
    name = models.CharField(max_length=64) 

    def __str__(self):
        return f"{self.name}" 

class OrderPizza(models.Model):
    ref = models.CharField(max_length=16, default='na')
    name = models.ForeignKey(PizzaType, on_delete=models.CASCADE)
    topping_choice = models.ForeignKey(ToppingChoice, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}, {self.topping_choice}, {self.size}" 


class OrderSubs(models.Model):
    ref = models.CharField(max_length=16, default='na')
    name = models.ForeignKey(SubsType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField()
    
    def __str__(self):
        return f"{self.name}, {self.size}" 
    
class OrderSubsX(models.Model):
    ref = models.CharField(max_length=16, default='na')
    name = models.ForeignKey(
        SubsType, 
        on_delete=models.CASCADE,
        limit_choices_to=Q(subs_extra=True) | Q(steak_subs_extra=True),
    )
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}"

class OrderPasta(models.Model):
    ref = models.CharField(max_length=16, default='na')
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}"

class OrderSalads(models.Model):
    ref = models.CharField(max_length=16, default='na')
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}"


class OrderDP(models.Model):
    ref = models.CharField(max_length=16, default='na')
    name = models.ForeignKey(DinnerPlattersType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}, {self.size}"


class Order(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL)
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.added_by = request.user
            super().save_model(request, obj, form, change)
        
    time = models.DateTimeField(auto_now=True)

    status_choices = [
        ('s', 'submitted'),
        ('p', 'processing'),
        ('c', 'completed'),
    ]
    status = models.CharField(choices=status_choices, max_length=1, blank=False, default='s')
    total_price = models.FloatField(null=True)


class Item(models.Model):
    item = models.CharField(max_length=64, null=False)
    
    size_choices = [
        ('s', 'small'),
        ('l', 'large'),
    ]
    size = models.CharField(choices=size_choices, max_length=1, blank=True)
    
    quantity_choices = [(i, i) for i in range (1, 11)]
    quantity = models.IntegerField(choices=quantity_choices, default=1)

    topping = models.ManyToManyField(Toppings, blank=True)
    def display_topping(self):
        """Create a string for the Topping. This is required to display topping in Admin."""
        return ', '.join(topping.name for topping in self.topping.all()[:3])
    
    display_topping.short_description = 'Topping'

    price = models.IntegerField()
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

   



    