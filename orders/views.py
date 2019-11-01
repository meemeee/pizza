from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
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
    topping_choice = ToppingChoice.objects.all().values_list('topping', flat=True)
    regular_menu = []
    for option in topping_choice:
        p = {'choice': option}
        for item in r_pizzas:
            if str(item.topping_choice).strip() == option:
                if str(item.size).strip() == "Small":
                    # Modify price to display 2 decimal places
                    p['small'] = format(item.price, '.2f')
                else:
                    p['large'] = format(item.price, '.2f')
        
        regular_menu.append(p)
    
    s_pizzas = OrderPizza.objects.filter(name__name="Sicilian")
    sicilian_menu = []
    for option in topping_choice:
        p = {'choice': option}
        for item in s_pizzas:
            if str(item.topping_choice).strip() == option:
                if str(item.size).strip() == "Small":
                    # Modify price to display 2 decimal places
                    p['small'] = format(item.price, '.2f')
                else:
                    p['large'] = format(item.price, '.2f')
        sicilian_menu.append(p)
    
    subs = OrderSubs.objects.all()
    subs_menu = []
    subs_choice = SubsType.objects.all().values_list('name', flat=True)

    for option in subs_choice:
        p = {'choice': option}
        for item in subs:
            if str(item.name).strip() == option:
                if str(item.size).strip() == "Small":
                    # Modify price to display 2 decimal places
                    p['small'] = format(item.price, '.2f')
                else:
                    p['large'] = format(item.price, '.2f')
        subs_menu.append(p)
   
    pastas_menu = OrderPasta.objects.all().values('name','price')

    salads_menu = OrderSalads.objects.all().values('name','price')


    dinnerplatters = OrderDinnerPlatters.objects.all()
    dinnerplatters_menu = []
    dinnerplatters_choice = DinnerPlattersType.objects.all().values_list('name', flat=True)

    for option in dinnerplatters_choice:
        p = {'choice': option}
        for item in dinnerplatters:
            if str(item.name).strip() == option:
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
        "pastas": pastas_menu,
        "salads": salads_menu,
        "dinnerplatters": dinnerplatters_menu
    }

    return render(request, "menu.html", context)
