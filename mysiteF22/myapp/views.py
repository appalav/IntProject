# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import random
import string

from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404, render, redirect
from .forms import OrderForm, InterestForm, RegisterForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from mysiteF22.settings import EMAIL_HOST_USER
from .forms import *
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404, HttpResponseRedirect
from .models import Category, Product, Client, Order
from django.shortcuts import render, redirect, reverse
from datetime import date
from datetime import datetime
from .forms import OrderForm, InterestForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'cat_list': cat_list})
    # product_list = Product.objects.all().order_by('-price')[:5]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of categories: ' + '</p>'
    # response.write(heading1)
    # for category in cat_list:
    #    para = '<p>'+ str(category.id) + ': ' + str(category) + '</p>'
    #    response.write(para)
    # heading2 = '<p>' + 'List of products: ' + '</p>'
    # response.write(heading2)
    # for product in product_list:
    #    para = '<p>' + str(product.id)+':' + str(product) + '</p>'
    #    response.write(para)
    # return response


def about(request):
    # return HttpResponse("This is an Online Store APP")
    if request.COOKIES.get('about_visits'):
        visits = int(request.COOKIES.get('about_visits'))
        visits += 1
    else:
        visits = 1
    response = render(request, 'myapp/about.html', {'visits': visits})
    response.set_cookie('about_visits', visits, max_age=300)
    return response


def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    products = Product.objects.filter(category=category)
    return render(request, 'myapp/detail.html', {'category': category, 'products': products})
    # detail_response = HttpResponse()
    # heading = '<p>' + 'Warehouse location - ' + category.warehouse + '</p>'
    # heading += '<p>' + 'List of products for the category:' + '</p>'
    # detail_response.write(heading)
    #
    # for product in products:
    #     para = '<p>' + str(product.id) + ': ' + str(product) + '</p>'
    #     detail_response.write(para)
    # return detail_response


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prod_list': prodlist})


@login_required
def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                msg = 'Your order has been placed successfully.'
                order.product.stock -= order.num_units
                order.product.save()
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_responce.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/place_older.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    product = Product.objects.get(pk=prod_id)
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid() and int(form.cleaned_data['interested']) == 1:
            product.Interested += 1
            product.save()
            msg = 'Order was successful'
            return render(request, 'myapp/order_responce.html', {'msg': msg})
        else:
            msg = 'Some error occured in passing the form'
            return render(request, 'myapp/order_responce.html', {'msg': msg})
    else:
        form = InterestForm()
    return render(request, 'myapp/productdetail.html', {'form': form, 'product': product})


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details")
    else:
        form = LoginForm()
        return render(request, 'myapp/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def myorders(request):
    try:
        user = request.user
        print(user)
        client = Client.objects.get(username=user.username)
        orders = Order.objects.filter(client=client)
        msg = f'Orders placed by {client} :-'
        if orders.count() == 0:
            msg = 'Client has not placed any orders'
        return render(request, 'myapp/myorders.html', {'orders': orders, 'msg': msg})
    except Client.DoesNotExist:
        msg = 'You are not a registered client'
        return render(request, 'myapp/myorders.html', {'msg': msg})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            random_password = ''.join(random.choice(string.ascii_letters) for i in range(10))
            password = make_password(random_password)
            Client.objects.filter(email=form.cleaned_data['Email']).update(password=password)

            subject = 'New Password'
            message = 'Your new password is ' + random_password
            recipient = form.cleaned_data['Email']
            send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
            return HttpResponse('A password has been sent to your inbox')
        else:
            return HttpResponse('Incorrect details')
    else:
        form = ForgotPasswordForm()
        return render(request, 'myapp/forgot_password.html', {'form': form})


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("myapp:user_login")
        else:
            print('form invalid')
    else:
        form = RegisterForm()
    return render(request=request, template_name="myapp/register.html", context={"register_form": form})
