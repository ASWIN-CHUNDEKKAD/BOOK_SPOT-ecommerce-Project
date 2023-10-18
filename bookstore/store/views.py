from django.shortcuts import render,redirect
from django.contrib import messages
from . models import Category,Product,Banner,Category_slider,Author,Testimonial
from django.http.response import JsonResponse

# Create your views here.

'''FUNCTION OF HOMEPAGE OF THE WEBSITE'''
def home(request):
    
    # TODO: CACHE GENERAL DATAS AND REUSED, USE SIGNALS TO INVALIDATE CACHE DATA FOR CRUD OPERATIONS
    trending_products = Product.objects.filter(trending=1)
    cate_slider = Category_slider.objects.all()
    authors = Author.objects.all()
    testimonial = Testimonial.objects.filter(status=1)
    banner = Banner.objects.filter(status=1)
    
    context = {
        'trending_products':trending_products,
        'cate_slider':cate_slider,
        'authors' : authors,
        'testimonial' : testimonial,
        'banner' : banner,
        
        
    }
    return render(request,'store/index.html',context)

'''AUTHORS'''
def authors(request):
    authors = Author.objects.all()
    context = {
        'authors' : authors
    }
    return render(request, 'store/authors/authors.html',context)

'''AUTHORSVIEW PAGE'''
def authorsview(request, auth_name):
    author = Author.objects.filter(name=auth_name).first()
    if author:
        context = {
            'author': author
        }
        return render(request, 'store/authors/authors_view.html', context)
    else:
        return redirect('authors')


def about_us(request):
    return render(request,'store/footer/about_us.html')


'''CATEGORY OF BOOKS(FICTION, NON-FICTION,...)'''
def category(request):
    category = Category.objects.filter(status=0)
    context = {
        'category':category
        }
    return render(request,'store/category.html',context)

'''EACH CATEGORY THERE ARE SEVERAL BOOKS,THIS FUNCTION REPRESENTS THE FILTERATION BY CATEGORY'''
def categoryview(request,name):
    if(Category.objects.filter(name=name,status=0)):                
        products = Product.objects.filter(category__name=name,status=0)
        category = Category.objects.filter(name=name).first()
        context = {
            'products':products,
            'category':category
            }
        return render(request,'store/products/index.html',context)
    else:
        messages.warning(request,"no such category found")
        return redirect('category')
    
    
'''DETAIL VIEW OF EACH PRODUCT'''
def productview(request,cate_name,prod_name):
    if(Category.objects.filter(name=cate_name,status=0)):
        if(Product.objects.filter(name=prod_name,status=0)):
            products = Product.objects.filter(name=prod_name,status=0).first()
            context = {
                'products':products
                }
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

'''SEARCH PRODUCTS'''
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