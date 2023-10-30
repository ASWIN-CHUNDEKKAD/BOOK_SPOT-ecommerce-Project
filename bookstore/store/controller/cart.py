from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from store.models import Product,Cart
from django.core.cache import cache

'''add to cart function'''
@login_required(login_url='loginpage')
def addtocart(request):
    # Construct a cache key based on the user's ID
    cache_key = f'cart_{request.user.id}'

    # Try to retrieve the cart content from the cache
    cart_content = cache.get(cache_key)

    if cart_content is None:
        # If the cart content is not in the cache, perform the view logic
        if request.method == 'POST':
            if request.user.is_authenticated:
                prod_id = int(request.POST.get('product_id'))
                product_check = Product.objects.select_related('category').get(id=prod_id)
                
                if product_check:
                    if Cart.objects.select_related('product').filter(user=request.user.id, product_id=prod_id):
                        return JsonResponse({'status': 'Product Already in Cart'})
                    else:
                        prod_qty = int(request.POST.get('product_qty'))
                        
                        if product_check.quantity >= prod_qty:
                            Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                            return JsonResponse({'status': 'Product Added Successfully'})
                        else:
                            return JsonResponse({'status': 'Only ' + str(product_check.quantity) + 'Quantity Available'})
                else:
                    return JsonResponse({'status': 'No Such Product Found'})
            else:
                return JsonResponse({'status': 'Login to continue'})
    else:
        # If the cart content is in the cache,
        return JsonResponse(cart_content)

    return redirect('/')

'''viewcart page function'''
@login_required(login_url='loginpage')
def viewcart(request):
    # Construct a cache key based on the user's ID
    cache_key = f'cart_{request.user.id}'

    # Try to retrieve the cart content from the cache
    cart = cache.get(cache_key)

    if cart is None:
        # If the cart content is not in the cache, execute the view logic
        cart = Cart.objects.filter(user=request.user).select_related('product')
        context = {'cart': cart}

        # Cache the cart content for future requests
        cache.set(cache_key, cart, timeout=3600)  # Cache for 1 hour 

        return render(request, 'store/cart.html', context)
    else:
        # If the cart content is in the cache,
        context = {'cart': cart}
        return render(request, 'store/cart.html', context)
      
'''PRODUCT QUANTITY INCREMENT FUNCTION'''          
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

'''DELETe CART FUNCTION'''
def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get("product_id"))
        if(Cart.objects.filter(user = request.user,product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id,user=request.user)
            cartitem.delete()
            
            # Check if a coupon code is applied and remove it
            if 'coupon_code' in request.session:
                del request.session['coupon_code']

        return JsonResponse({'status' : 'Updated Successfully'})
    return redirect('/')
            
        


    