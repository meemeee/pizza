from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .forms import RegisterForm
from .models import *

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

    print(regular_menu)

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


    dinnerplatters = OrderDinnerPlatters.objects.all()
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
        

    context = {   
        "r_pizzas": regular_menu, 
        "s_pizzas": sicilian_menu,
        "subs": subs_menu,
        "pastas": pasta_menu,
        "salads": salads_menu,
        "dinnerplatters": dinnerplatters_menu
    }

    return render(request, "menu.html", context)

def order(request, item_id):
    item = item_id.split("_")
    dish = {}
    
    short = ['regular', 'sicilian', 'sub', 'pasta', 'salad', 'dp']
    full = ['Regular Pizza', 'Sicilian Pizza', 'Sub', 'Pasta', 'Salad', 'Dinner Platter']
    database = [ToppingChoice, ToppingChoice, SubsType, OrderPasta, OrderSalads, DinnerPlattersType]
    
    for i in range(len(short)):
        if item[0] == short[i]:
            dish['name'] = full[i]
            try:
                if item[0] in ['pasta', 'salad']:
                    # Convert to string to avoid <databse:result> format
                    dish['type'] = str(database[i].objects.get(pk=item[1]).name)
                else:
                    dish['type'] = str(database[i].objects.get(pk=item[1]))
            except database[i].DoesNotExist:
                raise Http404("Dish does not exist")
            
            break
    context = {
        "dish": dish
    } 
    return render(request, "single_item.html", context)
