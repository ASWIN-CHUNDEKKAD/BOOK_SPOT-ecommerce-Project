from django.urls import path
from . import views

from store.controller import authview, cart, wishlist,checkout,order

urlpatterns = [
    # homepage,category
    path('',views.home,name='home'),
    path('category',views.category,name='category'),
    path('category/<str:name>',views.categoryview,name='categoryview'),
    path('category/<str:cate_name>/<str:prod_name>',views.productview,name='productview'),
    path('authors',views.authors,name='authors'),
    path('authors/<str:auth_name>',views.authorsview,name='authorsview'),
    
    path('product-list',views.productlistAjax),
    path('searchproduct',views.searchproduct,name='searchproduct'),
    
    # user reg.login...
    path('register',authview.register,name='register'),
    path('login',authview.loginpage,name='loginpage'),
    path('logout',authview.logoutpage,name='logout'),
    path('edit_profile',authview.edit_profile,name='edit_profile'),
    
    # cart
    path('add-to-cart',cart.addtocart,name='addtocart'),
    path('cart',cart.viewcart,name='cart'),
    path('update-cart',cart.updatecart,name='updatecart'),
    path('delete-cart-item',cart.deletecartitem,name='deletecartitem'),
    
    # wishlist
    path('wishlist',wishlist.index,name='wishlist'),
    path('add-to-wishlist',wishlist.addtowishlist,name='addtowishlist'),
    path('delete-wishlist-item',wishlist.deletewishlistitem,name='deletewishlistitem'),
    
    # checkout
    path('checkout',checkout.index,name='checkout'),
    path('place-order',checkout.placeorder,name='placeorder'),
    
    # order history
    path('my-orders',order.index,name='myorders'),
    path('view-order/<str:t_no>',order.vieworder,name='orderview'),
    path('invoice/<str:t_no>',order.invoice,name='invoice'),
    
    # Generation of pdf
    path('generate_pdf/<str:t_no>', order.generate_pdf, name='generate_pdf'),
    
    # Razorpay payment
    path('proceed-to-pay',checkout.razorpaycheck),
    
]
