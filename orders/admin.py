from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PizzaType)
admin.site.register(ToppingChoice)
admin.site.register(Size)
admin.site.register(Toppings)
admin.site.register(SubsType)
admin.site.register(DinnerPlattersType)
admin.site.register(OrderPizza)
admin.site.register(OrderSubs)
admin.site.register(OrderPasta)
admin.site.register(OrderSalads)
admin.site.register(OrderDinnerPlatters)
admin.site.register(Order)

