from django.shortcuts import render,redirect
from django.contrib import messages
from . models import Category,Product,Banner,Category_slider,Author,Testimonial
from django.http.response import JsonResponse
from django.core.cache import cache

# Create your views here.

'''FUNCTION OF HOMEPAGE OF THE WEBSITE'''
def home(request):
    # Construct a cache key for the home page
    cache_key = 'home_page_data'

    # Try to retrieve the cached data
    cached_data = cache.get(cache_key)

    if cached_data is None:
        # If the data is not in the cache, 
        trending_products = Product.objects.filter(trending=1).select_related('category')
        cate_slider = Category_slider.objects.all()
        authors = Author.objects.all()
        testimonial = Testimonial.objects.filter(status=1)
        banner = Banner.objects.filter(status=1)

        context = {
            'trending_products': trending_products,
            'cate_slider': cate_slider,
            'authors': authors,
            'testimonial': testimonial,
            'banner': banner,
        }

        # Cache the data for future requests
        cache.set(cache_key, context, timeout=10)  # Cache for 3600 sec

        return render(request, 'store/index.html', context)
    else:
        # If the data is in the cache,
        return render(request, 'store/index.html', cached_data)

'''AUTHORS'''
def authors(request):
    # Check if data is already cached
    authors = cache.get('authors')
    
    if authors is None:
        # If data is not cached, retrieve it from the database
        authors = Author.objects.all()
        
        # Cache the data for future requests
        cache.set('authors', authors, timeout=10)  # Cache for 10 sec
    context = {
        'authors': authors
    }
    
    return render(request, 'store/authors/authors.html', context)

'''AUTHORSVIEW PAGE'''
def authorsview(request, auth_name):
    # Check if the author data is already cached
    author = cache.get(f'author_{auth_name}')
    
    if author is None:
        # If data is not cached, retrieve it from the database
        author = Author.objects.filter(name=auth_name).first()
        
        if author:
            # Cache the author data for future requests
            cache.set(f'author_{auth_name}', author, timeout=10)  # Cache for 10 sec

    if author:
        context = {
            'author': author
        }
        return render(request, 'store/authors/authors_view.html', context)
    else:
        return redirect('authors')
    
'''ABOUT US'''
def about_us(request):
    # Check if the view is already cached
    cached_response = cache.get('about_us_view')
    
    if cached_response is None:
        # If the view is not cached, render the template
        cached_response = render(request, 'store/footer/about_us.html')

        # Cache the entire view response for future requests
        cache.set('about_us_view', cached_response, timeout=10)  # Cache for 10 sec 

    return cached_response


'''CATEGORY OF BOOKS(FICTION, NON-FICTION,...)'''
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

'''SEARCH PRODUCTS'''
def searchproduct(request):
    if request.method == "POST":
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            # Construct a cache key based on the search term
            cache_key = f'search_{searchedterm}'

            # Try to retrieve the search result from the cache
            product = cache.get(cache_key)

            if product is not None:
                # If the product is found in the cache, use it and display it
                return redirect('category' + '/' + product.category.name + '/' + product.name)
            
            # If the product is not in the cache, perform the search
            product = Product.objects.filter(name__contains=searchedterm).first()

            if product:
                # Cache the search result for future requests
                cache.set(cache_key, product, timeout=10)  # Cache for 10 sec
                print(f"Search result for '{searchedterm}' not found in cache, generated and cached.")
                return redirect('category' + '/' + product.category.name + '/' + product.name)
            else:
                messages.info(request, "No product matched your search")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))