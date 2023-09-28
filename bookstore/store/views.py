from django.shortcuts import render,redirect
from django.contrib import messages
from . models import Category,Product,Banner
from django.http.response import JsonResponse

# Create your views here.

'''Function of website homepage'''
def home(request):
    # banner = Banner.objects.all()
    # context = {'banner':banner}
    trending_products = Product.objects.filter(trending=1)
    context = {
        'trending_products':trending_products
    }
    
    return render(request,'store/index.html',context)

# def banner(request):
#     banner = Banner.objects.all()
#     context = {'banner':banner}
#     return render(request,'store/index.html',context)

'''Category of books(fiction,non-fiction,...)'''
def category(request):
    category = Category.objects.filter(status=0)
    context = {'category':category}
    return render(request,'store/category.html',context)

'''Each category there are several books,This function represents the filteration of products by category'''
def categoryview(request,name):
    if(Category.objects.filter(name=name,status=0)):                
        products = Product.objects.filter(category__name=name,status=0)
        category = Category.objects.filter(name=name).first()
        context = {'products':products,'category':category}
        return render(request,'store/products/index.html',context)
    else:
        messages.warning(request,"no such category found")
        return redirect('category')
    
    
'''Detail view of each product'''
def productview(request,cate_name,prod_name):
    if(Category.objects.filter(name=cate_name,status=0)):
        if(Product.objects.filter(name=prod_name,status=0)):
            products = Product.objects.filter(name=prod_name,status=0).first()
            context = {'products':products}
        else:
            messages.error(request,"No such product found")
            return redirect('category')
    else:
        messages.error(request,"No such category found")
        return redirect('category')
    return render(request,'store/products/view.html',context)

def productlistAjax(request):
    products = Product.objects.filter(status=0).values_list('name',flat=True)
    productsList = list(products)
    
    
    return JsonResponse(productsList,safe=False)

def searchproduct(request):
    if request.method == "POST":
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searchedterm).first()
            
            if product:
                return redirect('category'+'/'+product.category.name+'/'+product.name)
            else:
                messages.info(request,"No product matched your search")
                return redirect(request.META.get('HTTP_REFERER'))
                
            
    return redirect(request.META.get('HTTP_REFERER'))