from django.db import models

# Create your models here.

class PizzaType(models.Model):
    types = models.CharField(max_length=32)

class ToppingChoice(models.Model):
    topping = models.CharField(max_length=32)

class Size(models.Model):
    size = models.CharField(max_length=32)

class Toppings(models.Model):
    topping = models.CharField(max_length=64)

class SubType(models.Model):
    name = models.CharField(max_length=64)

class SubExtra(models.Model):
    extra = models.CharField(max_length=64) 
    steak_limited = models.BooleanField() # limited to Steak sub

class OrderPizza(models.Model):
    name = models.ForeignKey(PizzaType, on_delete=models.CASCADE)
    topping_choice = models.ForeignKey(ToppingChoice, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.IntegerField()
    
class OrderSub(models.Model):
    name = models.ForeignKey(SubType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    steak_extra = models.ForeignKey(SubExtra, on_delete=models.CASCADE, 
    limit_choices_to= {'steak_limted': True}, related_name="steak_extras")
    extra = models.ForeignKey(SubExtra, on_delete=models.CASCADE, 
    limit_choices_to= {'steak_limted': False})
    price = models.IntegerField()

class OrderPasta(models.Model):
    name = models.ForeignKey(SubType, on_delete=models.CASCADE)
    price = models.IntegerField()

class OrderSalads(models.Model):
    name = models.ForeignKey(SubType, on_delete=models.CASCADE)
    price = models.IntegerField()

class OrderDinnerPlatters(models.Model):
    name = models.ForeignKey(SubType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.IntegerField()