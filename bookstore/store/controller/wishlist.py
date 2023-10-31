from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from store.models import Wishlist,Product
from django.core.cache import cache

@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
    context = {'wishlist':wishlist}
    return render(request,'store/wishlist.html',context)


def addtowishlist(request):
    '''ADD TO WISHLIST'''

    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user,product_id=prod_id)):
                    return JsonResponse({'status':'product allready in wishlist'})
                else:
                    Wishlist.objects.create(user=request.user,product_id=prod_id)
                    return JsonResponse({'status':'product added to wishlist'})
            else:
                return JsonResponse({'status':'no such product found'})
        else:
            return JsonResponse({'status':'Login to continue'})
                                      
    return redirect('/')

'''DELETe FUNCTIONALITY'''
def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            
            # Use filter to get a queryset of matching Wishlist items
            wishlist_items = Wishlist.objects.filter(user=request.user, product_id=prod_id)
            
            if wishlist_items.exists():
                # Delete all matching items in the queryset
                wishlist_items.delete()
                return JsonResponse({'status': 'Product removed from wishlist'})
            else:                
                return JsonResponse({'status': 'Product not found in wishlist'})
        else:
            return JsonResponse({'status': 'Login to continue'})
    
    return redirect('/')
