from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from .forms import *
from .models import *
from . import urls
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Create new user in database
            form.save()

            # Log user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')  
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            return redirect('index')
    
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form})



def menu(request):

    # Get price infomation for Menu
    r_pizzas = OrderPizza.objects.filter(name__name="Regular") # passing the "name" - foreign key of "name" in OrderPizza
    topping_choice = ToppingChoice.objects.all().values('id','topping')
    regular_menu = []

    for option in topping_choice:
        p = {'id': option['id'], 'type': option['topping']}
        for item in r_pizzas:
            if str(item.topping_choice).strip() == option['topping']:
                if str(item.size).strip() == "Small":
                    # Modify price to display 2 decimal places
                    p['small'] = format(item.price, '.2f')
                else:
                    p['large'] = format(item.price, '.2f')
        
        regular_menu.append(p)

    s_pizzas = OrderPizza.objects.filter(name__name="Sicilian")
    sicilian_menu = []

    for option in topping_choice:
        p = {'id': option['id'], 'type': option['topping']}
        for item in s_pizzas:
            if str(item.topping_choice).strip() == option['topping']:
                if str(item.size).strip() == "Small":
                    # Modify price to display 2 decimal places
                    p['small'] = format(item.price, '.2f')
                else:
                    p['large'] = format(item.price, '.2f')
        sicilian_menu.append(p)
    

    subs = OrderSubs.objects.all()
    subs_menu = []
    subs_choice = SubsType.objects.exclude(steak_subs_extra=True).values('id', 'name')
    
    for option in subs_choice:
        p = {'id': option['id'], 'type': option['name']}
        for item in subs:
            if str(item.name).strip() == option['name']:
                if str(item.size).strip() == "Small":
                    # Modify price to display 2 decimal places
                    p['small'] = format(item.price, '.2f')
                else:
                    p['large'] = format(item.price, '.2f')
        subs_menu.append(p)
       

    pasta_menu = OrderPasta.objects.all().values('id', 'name', 'price')
    for item in pasta_menu:
        item['price'] = format(item['price'], '.2f')
   

    salads_menu = OrderSalads.objects.all().values('id', 'name','price')
    for item in salads_menu:
        item['price'] = format(item['price'], '.2f')


    dinnerplatters = OrderDP.objects.all()
    dinnerplatters_menu = []
    dinnerplatters_choice = DinnerPlattersType.objects.all().values('id', 'name')
    
    for option in dinnerplatters_choice:
        p = {'id': option['id'], 'type': option['name']}
        for item in dinnerplatters:
            if str(item.name).strip() == option['name']:
                if str(item.size).strip() == "Small":
                    # Modify price to display 2 decimal places
                    p['small'] = format(item.price, '.2f')
                else:
                    p['large'] = format(item.price, '.2f')
        dinnerplatters_menu.append(p)
    
    # Set cart num value
    if request.user.is_authenticated:
        cart_num = len(Item.objects.filter(created_by=request.user).filter(status__exact='p'))
    else:
        cart_num = 0


    context = {
        "cart_num": cart_num,  
        "r_pizzas": regular_menu, 
        "s_pizzas": sicilian_menu,
        "subs": subs_menu,
        "pastas": pasta_menu,
        "salads": salads_menu,
        "dinnerplatters": dinnerplatters_menu
    }

    return render(request, "menu.html", context)

@login_required
def item(request, item_id):
    # Get item's info from item_id
    item = item_id.split("_")   

    # Retrieve item's name                    
    dish = {}
    price = {}
    
    short = ['regular', 'sicilian', 'sub', 'pasta', 'salad', 'dp']
    full = ['Pizza', 'Pizza', 'Sub', 'Pasta', 'Salad', 'Dinner Platter']
    database = [OrderPizza, OrderPizza, OrderSubs, OrderPasta, OrderSalads, OrderDP]
    if not item[0] in short:
        raise Http404("Wrong URL") 
    
    for i in range(len(short)):
        if item[0] == short[i]:
            dish['type'] = full[i]
            try:                  
                if item[0] in ['salad', 'pasta']:
                    # These items get only 1 result per id.
                    dish_data = database[i].objects.get(ref=item_id)
                    dish['name'] = str(dish_data.name)

                    # Retrive price, format to show 2 decimal places
                    price['na'] = format(float(dish_data.price),'.2f')
                else:
                    # These items get 2 results per id.
                    dish_data = database[i].objects.filter(ref=item_id)
                    dish['name'] = dish_data.values_list('name__name', flat=True)[0]

                    # Plus 'Topping Choice' for pizza
                    if item[0] in ['regular', 'sicilian']:
                        dish['name'] = dish['name'] + " " + dish_data.values_list('topping_choice__topping', flat=True)[0]
                    
                    # Retrieve price for each size
                    for value in dish_data.values():
                        # id 1 corresponding to size 'small'
                        if value['size_id'] == 1:
                            price['small'] = format(float(value['price']), '.2f')
                        else:
                            price['large'] = format(float(value['price']), '.2f')

            except database[i].DoesNotExist:
                raise Http404("Dish does not exist")           
            break

    if request.method == "POST":
        # Create form from Order Model
        form2 = ItemForm()

        # Get order ID
        # Check if user have an existing pending order: 
        if len(Order.objects.filter(created_by=request.user).filter(status__exact='p')) == 0:
            new_order = Order()
            new_order.created_by = request.user
            new_order.save()

        pendingOrder = Order.objects.filter(created_by=request.user).filter(status__exact='p')
        pendingOrder_id = pendingOrder.values_list('id', flat=True)[0]

            
        # Do not allow user to have more than 10 items per cart
        pendingItems = Item.objects.filter(created_by=request.user).filter(status__exact='p')
    
        if len(pendingItems) > 9:
            context = {
                "cart_num": len(Item.objects.filter(created_by=request.user).filter(status__exact='p')),
                "error": "Cannot add more than 10 dishes per cart.",
                "form": form2,
                "price": price,
                "dish": dish,
            }
            # return render(request, "add_item_message.html", context)
            return render(request, "single_item.html", context)
        # Create a form instance and populate it with data from the request
        form = ItemForm(request.POST)    

        def add_details(obj, prev_quantity, form):
            # Calculate total price based on size & quantity + extra subs (if any)
            subX_price_per_pax = int(len(form.cleaned_data['subx'])) * 0.5

            # add up any previous quantity (if any)
            obj.quantity = prev_quantity + int(form.cleaned_data['quantity'])
            
            # Do not allow user to have more than 10 items per dish
            if obj.quantity > 10:
                context = {
                    "cart_num": len(Item.objects.filter(created_by=request.user).filter(status__exact='p')),
                    "error": "Cannot add more than 10 items per dish.",
                    "form": form2,
                    "price": price,
                    "dish": dish,
                }
                
            else:
                if obj.size == 'S':
                    obj.price = obj.quantity * (float(price['small']) + subX_price_per_pax)
                elif obj.size == 'L':
                    obj.price = obj.quantity * (float(price['large']) + subX_price_per_pax)
                else:
                    # Item is either a salad or pasta
                    obj.price = float(price['na']) * int(obj.quantity)
                
                obj.save()
                
                # Add topping and subx results into list
                topping = list()
                for item in form.cleaned_data['topping'].values_list('topping', flat=True):
                    topping.append(item)
            
                subx = list()
                for item in form.cleaned_data['subx'].values_list('name', flat=True):
                    subx.append(item)
                # Set new cart num value
                cart_num = len(Item.objects.filter(created_by=request.user).filter(status__exact='p'))
                success = True
    
                context = {
                    "success": success,
                    "dish": dish,
                    "price": price,
                    "quantity": int(form.cleaned_data['quantity']),
                    "size": obj.size,
                    "topping": topping,
                    "subx": subx,
                    "cart_num": cart_num,
                    "form": form2,
                }
            return context
            
        if form.is_valid():
        # Iterate through existing pending items, only create a new object if the same item does not exist
            dish_name = dish['name'] + " " + dish['type']
            for item in pendingItems:
                if (item.item == dish_name and 
                    item.size == form.cleaned_data['size'].strip() and
                    list(item.topping.all()) == list(form.cleaned_data['topping']) and
                    list(item.subx.all()) == list(form.cleaned_data['subx'])):
                   
                    context = add_details(item, item.quantity, form)

                    # return render(request, "add_item_message.html", context)
                    return render(request, "single_item.html", context)
                    break
         
            #Else, create a new object in Item model
            new_item = Item()
            
            # Add initial information to object
            
            new_item.item = dish['name'] + " " + dish['type']
            new_item.size = form.cleaned_data['size']
            new_item.created_by = request.user
            new_item.order_id = Order.objects.get(pk=pendingOrder_id)

            # Add further details, then return context
            context = add_details(new_item, 0, form)

            new_item.save()
            # Add topping and subx
            new_item.topping.set(form.cleaned_data['topping'])
            new_item.subx.set(form.cleaned_data['subx'])
            
            # return render(request, "add_item_message.html", context)
            return render(request, "single_item.html", context)
                      
    else:
        # Create form from Order Model
        form = ItemForm()
        
    # Set cart num value
    cart_num = len(Item.objects.filter(created_by=request.user).filter(status__exact='p'))

    context = {
        "price": price,
        "dish": dish,
        "form": form,
        'cart_num': cart_num,
    } 
    return render(request, "single_item.html", context) 
        

class ItemListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view showing by current user."""
    model = Item
    template_name ='cart.html'

    # Return list of items
    def get_queryset(self):
        return Item.objects.filter(created_by=self.request.user).filter(status__exact='p').order_by('id')

    # Add additional data
    def get_context_data(self, **kwargs):
        # Set cart num value
        cart_num = len(Item.objects.filter(created_by=self.request.user).filter(status__exact='p'))

        # Call the base implementation first to get the context
        context = super(ItemListView, self).get_context_data(**kwargs)
        
        # Add cart_num data & order id to the context
        context['cart_num'] = cart_num
        items = Item.objects.filter(created_by=self.request.user).filter(status__exact='p').order_by('id')
        if len(items) > 0:    
            context['order_id'] = items.values_list('order_id', flat=True)[0]

        return context

@login_required
def submit_order(request):
    if request.method == "POST":
        order_id = int(request.POST["order_id"])
        # Change order status to 'submitted'
        order = get_object_or_404(Order, pk=order_id)
        order.status = 's'
        order.save()
        
        # Change items status AND calculate total price
        total_price = 0
        items = get_list_or_404(Item, order_id=order_id)
        for item in items:
            item.status = 's'
            item.save()
            total_price += float(item.price)
        
        order.total_price = format(total_price, '.2f')
        order.save()
      
        # Redirect to success page
        # Set new cart num value
        cart_num = len(Item.objects.filter(created_by=request.user).filter(status__exact='p'))
        context = {
            "items": items,
            "order_id": order_id,
            "cart_num": cart_num,
        }
        return render(request, "place_order_message.html", context)


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name ='orders.html'

    # Return list of orders, descending
    def get_queryset(self):
        return Order.objects.filter(created_by=self.request.user).exclude(status='p').order_by('-id')
    

    # Add additional data
    def get_context_data(self, **kwargs):
        # Set cart num value
        cart_num = len(Item.objects.filter(created_by=self.request.user).filter(status__exact='p'))

        # Call the base implementation first to get the context
        context = super(OrderListView, self).get_context_data(**kwargs)
        
        # Add cart_num data & order id to the context
        context['cart_num'] = cart_num
        
        return context

class OrderDetailView(generic.DetailView):
    model = Order
    
    # Add additional data
    def get_context_data(self, **kwargs):
        # Set cart num value
        cart_num = len(Item.objects.filter(created_by=self.request.user).filter(status__exact='p'))

        # Call the base implementation first to get the context
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        
        # Add cart_num data & order id to the context
        context['cart_num'] = cart_num

        return context

@permission_required('orders.can_change_status')
def change_status_admin(request, pk):
    order_instance = get_object_or_404(Order, pk=pk)

    if request.method =='POST':
        #Create a form instance and populate form data
        form = OrderStatusForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Change order status
            order_instance.status = form.cleaned_data['status']
            order_instance.save()

            # Change items status accordingly
            items = get_list_or_404(Item, order_id=order_instance.id)
            for item in items:
                item.status = form.cleaned_data['status']
                item.save()
            return HttpResponseRedirect(reverse('all-orders'))
       

    else:
        form = OrderStatusForm()
    # Set cart num value
    cart_num = len(Item.objects.filter(created_by=request.user).filter(status__exact='p'))

    context = {
        'form': form,
        'order_instance': order_instance,
        'cart_num': cart_num,
    }

    return render(request, 'orders/change_order_status.html', context)


class AllOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name ='all_orders.html'

    # Return list of 'submitted' orders
    def get_queryset(self):
        return Order.objects.filter(status='s').order_by('id')
    

    # Add additional data
    def get_context_data(self, **kwargs):
        # Set cart num value
        cart_num = len(Item.objects.filter(created_by=self.request.user).filter(status__exact='p'))

        # Call the base implementation first to get the context
        context = super(AllOrdersListView, self).get_context_data(**kwargs)
        
        # Add cart_num data to the context
        context['cart_num'] = cart_num

        # Add another query (a list of 'processing' orders) to the context
        context['processing_orders'] = Order.objects.filter(status='pr').order_by('id')
        
        return context


def remove_item(request):
    if request.method == 'POST':
        item_id = request.POST.get("item_id")
        item = Item.objects.get(pk=item_id)
        if item: 
            item.delete()
            return HttpResponseRedirect(reverse('cart'))
    return HttpResponse("Something went wrong.")


