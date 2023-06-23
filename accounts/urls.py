
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),

    
    path('', views.home,name='home'),
    path('products/', views.products,name='products'),
    path('customers/', views.customers,name='customers'),
    path('customer/<str:pk>/',views.customer,name='customer'),
    path('createorder/<str:pk>/',views.createOrder,name='createOrder'),
    path('updateorder/<str:pk>/',views.updateOrder,name="updateOrder"),
    path('deleteorder/<str:pk>/',views.deleteOrder,name="deleteOrder"),
]
