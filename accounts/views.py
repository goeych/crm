from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import *
from .forms import OrderForm,CreateUserForm
from .filters import OrderFilter


# Create your views here.

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,"Account was created for " + user)
            #return redirect('login')

    context={'form':form}
    return render(request,'accounts/register.html',context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')

    context={'products':products}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context={'orders':orders,'customers':customers,
             'total_customers':total_customers,
             'total_orders':total_orders,
             'delivered':delivered,'pending':pending,
             }
    
    return render(request,'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    
    context={'products':products}
    return render(request,'accounts/products.html',context)

def customers(request):
    context={}
    return render(request,'accounts/customer.html',context)

def customer(request,pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    print('myFilter:',myFilter)
    orders = myFilter.qs

    context={'customer':customer,'orders':orders,
             'orders_count':orders_count,'myFilter':myFilter,
             }
    return render(request,'accounts/customer.html',context)

def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=2)
    #extra 10 is list more 10 rows in the form.
    
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #queryset=Order.objects.none() no record will show in form.
    
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')


    #form = OrderForm(initial={'customer':customer})
    #if request.method == 'POST':
        #form = OrderForm(request.POST)
        #if form.is_valid():
            #form.save()
            #return redirect('home')
    

    #context={'form':form}
    context={'formset':formset}
    return render(request,'accounts/createorder.html',context)

def updateOrder(request,pk):

    order = Order.objects.get(id=pk)

    form = OrderForm(instance = order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance = order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'accounts/createorder.html',context)


def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context={'order':order}
    return render(request,'accounts/deleteorder.html',context)

    
    

