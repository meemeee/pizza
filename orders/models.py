from django.db import models

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
    # subs_extra = models.BooleanField(default=False) # Extra toppings for subs
    # steak_subs_extra = models.BooleanField(default=False) # limited to Steak subs

    def __str__(self):
        return f"{self.topping}"

class SubsType(models.Model):
    name = models.CharField(max_length=64)  
    subs_extra = models.BooleanField(default=False) # Extra toppings for subs
    steak_subs_extra = models.BooleanField(default=False) # limited to Steak subs

    def __str__(self):
        return f"{self.name}"  

class OrderPizza(models.Model):
    name = models.ForeignKey(PizzaType, on_delete=models.CASCADE)
    topping_choice = models.ForeignKey(ToppingChoice, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.size} {self.name}, {self.topping_choice}, at {self.price}"
    
class OrderSubs(models.Model):
    name = models.ForeignKey(SubsType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    # steak_extra = models.ForeignKey(Toppings, on_delete=models.CASCADE, 
    # limit_choices_to= {'steak_subs_extra': True}, related_name="steak_extras")
    # extra = models.ForeignKey(Toppings, on_delete=models.CASCADE, 
    # limit_choices_to= {'subs_extra': True})
    price = models.FloatField()
    
    def __str__(self):
        return f"{self.size} {self.name} at {self.price}"

class OrderPasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} at {self.price}"

class OrderSalads(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} at {self.price}"

class OrderDinnerPlatters(models.Model):
    name = models.CharField(max_length=64)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.size} {self.name} at {self.price}"