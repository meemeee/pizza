from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from .models import *
from . import urls

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
    dinnerplatters_choice = OrderDP.objects.all().values('id', 'name')
    
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
        

    context = {   
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
                    
                    # Retrive price for each size
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
        # Create a form instance and populate it with data from the request
        form = ItemForm(request.POST)    

        # Create an object in Item model
        new_item = Item()

        # Add information to object
        if form.is_valid():
            new_item.item = dish['type'] + ": " + dish['name']
            new_item.size = form.cleaned_data['size']
            new_item.quantity = form.cleaned_data['quantity']
            
            

            # Calculate total price based on size & quantity
            if new_item.size == 's':
                new_item.price = float(price['small']) * int(new_item.quantity)
            elif new_item.size == 'l':
                new_item.price = float(price['large']) * int(new_item.quantity)
            else:
                new_item.price = float(price['na']) * int(new_item.quantity)
            
            # form.order_id = 1
            
            new_item.save()

            new_item.topping.set(form.cleaned_data['topping'])
            new_item.subx.set(form.cleaned_data['subx'])
            # Add values to ManyToManyField
            # print(form.cleaned_data['topping'])
            # for topping in form.cleaned_data['topping']:
            #     new_item.topping.add(topping)
            # for subx in form.cleaned_data['subx']:
            #     new_item.subx.add(subx)
            
            # new_item.topping = form.cleaned_data['topping']
            # new_item.subx = form.cleaned_data['subx']
            # print(form.topping, form.subx)
            return HttpResponseRedirect(reverse("menu"))
    
    else:
        # Create form from Order Model
        form = ItemForm()
        # form.item = dish['type'] +" "+ dish['name']
        # form.save(commit=False)
      
        context = {
            "price": price,
            "dish": dish,
            "form": form
        } 
        return render(request, "single_item.html", context)
        
    # return render(request, "menu/<str:item_id>", {'form': form})

