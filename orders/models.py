from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User

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
        return f"{self.name} (+{self.price})"

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
        return f"{self.ref}, {self.name}, {self.size}"


class Order(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
    #     null=True, blank=True, on_delete=models.SET_NULL)
    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         # Only set added_by during the first save.
    #         obj.added_by = request.user
    #         super().save_model(request, obj, form, change)
        
    time = models.DateTimeField(auto_now=True)

    status_choices = [
        ('p', 'Pending'),
        ('s', 'Submitted'),
        ('pr', 'Processing'),
        ('c', 'Completed'),
    ]
    status = models.CharField(choices=status_choices, max_length=2, blank=False, default='p')
    total_price = models.FloatField(null=True)


    def __str__(self):
        return f"{self.id}"



class Item(models.Model):
    item = models.CharField(max_length=64, null=False)
    
    size_choices = [
        ('S', 'Small'),
        ('L', 'Large'),
    ]
    size = models.CharField(choices=size_choices, max_length=1, blank=True, default='S')
    
    quantity_choices = [(i, i) for i in range (1, 11)]
    quantity = models.IntegerField(choices=quantity_choices, default=1)

    topping = models.ManyToManyField(Toppings, blank=True)
    def display_topping(self):
        """Create a string for the Topping. This is required to display topping in Admin."""
        return ', '.join(topping.topping for topping in self.topping.all()[:3])
    display_topping.short_description = 'Topping'

    subx = models.ManyToManyField(SubsType, blank=True,
        limit_choices_to=Q(subs_extra=True) | Q(steak_subs_extra=True))
    def display_subx(self):
        """Create a string for the Sub Extra. This is required to display SubX in Admin."""
        return ', '.join(subx.name for subx in self.subx.all()[:4])
    
    display_subx.short_description = 'Sub Extra'

    # Merge Subx & Topping columns into Notes
    # def notes(obj):
    #     return f"{obj.display_topping} {obj.display_subx}"
    # notes.short_description = 'Notes'

    price = models.FloatField()

    status_choices = [
        ('p', 'Pending'),
        ('s', 'Submitted'),
        ('pr', 'Processing'),
        ('c', 'Completed'),
    ]
    status = models.CharField(choices=status_choices, max_length=2, blank=True, default='p')

    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Id: {self.id} ({self.status})"


  
 


    