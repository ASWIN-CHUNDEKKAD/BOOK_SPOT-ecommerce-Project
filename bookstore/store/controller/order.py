from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from store.models import Order,Orderitem

'''function of order page ,in this page order history displayed'''
def index(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders':orders
        }
    return render(request,'store/orders/index.html',context)

'''Detailes of each order'''
def vieworder(request,t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = Orderitem.objects.filter(order=order)
    context = {
        'order':order,
        'orderitems':orderitems
        }
    return render(request,'store/orders/view.html',context)

'''invoice'''
def invoice(request,t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = Orderitem.objects.filter(order=order)
    context = {
        'order':order,
        'orderitems':orderitems
        }
    return render(request,'store/orders/invoice.html',context)
    

    