from django.shortcuts import render
from django.http import HttpResponse

from .models import *

# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='pending').count()

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

def customer(request):
    context={}
    return render(request,'accounts/customer.html',context)

def customer(request,pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()

    context={'customer':customer,
             'orders':orders}
    return render(request,'accounts/customer.html',context)
    
