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
    context = {
        "r_pizzas": OrderPizza.objects.filter(name=Regular)
        "s_pizzas" : OrderPizza.objects.filter(name=Sicilian)
        "subs": OrderSubs.objects.all()
        "pastas": OrderPasta.objects.all()
        "salads": OrderSalads.objects.all()
        "dinnerplatters": OrderDinnerPlatters.objects.all()
    }

    return render(request, "orders/menu.html", context)