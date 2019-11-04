from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PizzaType)
admin.site.register(ToppingChoice)
admin.site.register(Size)
admin.site.register(Toppings)
admin.site.register(SubsType)
admin.site.register(DinnerPlattersType)


# admin.site.register(OrderPizza)
# Defind the admin class
class OrderPizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'topping_choice', 'size', 'price', 'ref')
    list_filter = ('ref', 'topping_choice', 'size')
# Register the admin class with associated model
admin.site.register(OrderPizza, OrderPizzaAdmin)


# admin.site.register(OrderSubs)
class OrderSubsAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'price', 'ref')
    list_filter = ('ref', 'size')
admin.site.register(OrderSubs, OrderSubsAdmin)


# admin.site.register(OrderSubsX)
class OrderSubsXAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'ref')
admin.site.register(OrderSubsX, OrderSubsXAdmin)


#admin.site.register(OrderPasta)
class OrderPastaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'ref')
  
admin.site.register(OrderPasta, OrderPastaAdmin)


#admin.site.register(OrderSalads)
class OrderSaladsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'ref')
   
admin.site.register(OrderSalads, OrderSaladsAdmin)


#admin.site.register(OrderDP)
class OrderDPAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'price', 'ref')
    list_filter = ('ref', 'size')
admin.site.register(OrderDP, OrderDPAdmin)


# admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_price', 'created_by', 'time', 'status')
admin.site.register(Order, OrderAdmin)


# admin.site.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'display_topping', 'size', 'quantity', 'price', 'order_id')
admin.site.register(Item, ItemAdmin)

