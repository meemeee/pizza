from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from .forms import *
from .models import *
from . import urls
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    return HttpResponse("Project 3: TODO")


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
    print(s_pizzas)
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
    cart_num = len(Item.objects.filter(created_by=request.user).filter(status__exact='p'))


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
        
        # Get order ID
        # Check if user have an existing pending order: 
        if len(Order.objects.filter(created_by=request.user).filter(status__exact='p')) == 0:
            new_order = Order()
            new_order.created_by = request.user
            new_order.save()

        pendingOrder = Order.objects.filter(created_by=request.user).filter(status__exact='p')
        pendingOrder_id = pendingOrder.values_list('id', flat=True)[0]

            
        # Do not allow user to have more than 10 items per cart
        if len(Item.objects.filter(created_by=request.user).filter(status__exact='p')) > 9:
            context = {
                "cart_num": len(Item.objects.filter(created_by=request.user).filter(status__exact='p')),
            }
            return render(request, "add_item_message.html", context)
        # Create a form instance and populate it with data from the request
        form = ItemForm(request.POST)    

        # Create an object in Item model
        new_item = Item()

        # Add information to object
        if form.is_valid():
            new_item.item = dish['type'] + ": " + dish['name']
            new_item.size = form.cleaned_data['size']
            new_item.quantity = int(form.cleaned_data['quantity'])
            new_item.created_by = request.user
            new_item.order_id = Order.objects.get(pk=pendingOrder_id)

            # Calculate total price based on size & quantity + extra subs (if any)
            subX_price_per_pax = int(len(form.cleaned_data['subx'])) * 0.5
 
            if new_item.size == 'S':
                price = new_item.quantity * (float(price['small']) + subX_price_per_pax)
            elif new_item.size == 'L':
                price = new_item.quantity * (float(price['large']) + subX_price_per_pax)
            else:
                # Item is either a salad or pasta
                price = float(price['na']) * int(new_item.quantity)
            print(price)
            new_item.price = format(price, '.2f')
            print(new_item.price)
            new_item.save()


            # Add topping and subx
            new_item.topping.set(form.cleaned_data['topping'])
            new_item.subx.set(form.cleaned_data['subx'])
           
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
                "dish": new_item.item,
                "quantity": new_item.quantity,
                "size": new_item.size,
                "topping": topping,
                "subx": subx,
                "cart_num": cart_num,
            }
            return render(request, "add_item_message.html", context)
            
    
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
    paginate_by = 10

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
    # paginate_by = 10

    # Return list of orders, descending
    def get_queryset(self):
        return Order.objects.filter(created_by=self.request.user).order_by('-id')
    

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