from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from store.models import Product,Cart


'''add to cart function'''
@login_required(login_url='loginpage')
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id,product_id = prod_id)):
                    return JsonResponse({'status' : 'Product Already in Cart'})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    
                    if product_check.quantity >= prod_qty :
                        Cart.objects.create(user=request.user,product_id=prod_id,product_qty=prod_qty)
                        return JsonResponse({'status' : 'Product Added Successfully'})
                       
                    else:
                        return JsonResponse({'status' : 'Only ' + str(product_check.quantity) +  'Quantity Available'})              
            else:
                return JsonResponse({'status' : 'No Such Product Found'})          
        else:
            return JsonResponse({'status':"Login to continue"}) 
    return redirect('/')    


'''viewcart page function'''
@login_required(login_url='loginpage')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart' : cart}
    return render(request,'store/cart.html',context)
            
'''product qty increment function'''          
def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get("product_id"))
        if(Cart.objects.filter(user = request.user,product_id=prod_id)):
            prod_qty = request.POST.get('product_qty')
            cart = Cart.objects.get(product_id=prod_id,user=request.user)
            cart.product_qty = prod_qty
            cart.save()
        return JsonResponse({'status' : 'Updated Successfully'})
    return redirect('/')

'''delete cart function'''
def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get("product_id"))
        if(Cart.objects.filter(user = request.user,product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id,user=request.user)
            cartitem.delete()
        return JsonResponse({'status' : 'Updated Successfully'})
    return redirect('/')
            
        


    