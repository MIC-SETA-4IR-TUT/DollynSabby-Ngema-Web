from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users

# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST" :
        form =  CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'store/registerPage.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'store/loginPage.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def main(request):
    context = {}
    return render(request, 'store/main.html', context)

def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store_main.html', context)

def storemain(request):
    context = {}
    return render(request, 'store/store.html', context)

@allowed_users(allowed_roles=['customer'])
def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def aboutus(request):
    context = {}
    return render(request, 'store/aboutus.html', context)
