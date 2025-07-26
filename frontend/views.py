from django.shortcuts import render
from .models import Product, ProductVariant, CartItem, UserWishlist, UserCart, UserOrder, UserOrderItem
from authentication.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


def HomePageView(request):

    products = Product.objects.all()[:8]
    products_to_show = {}

    for product in products:

        products_to_show[product] = ProductVariant.objects.filter(product=product)


    return render(request, 'index.html', {"slider_products" : products_to_show})



def ShopPageView(request):


    return render(request, 'shop.html')




def ShopCategoryPageView(request, category_name):

    modified_cat_name = str(category_name)[0].upper()


    if request.user.is_authenticated:

        cart, _ = UserCart.objects.get_or_create(user=request.user)
    
        cart_products = [i.product for i in cart.cart_items.all()] 
    
    else : 

        cart_products = "No Authenticated"


    if request.user.is_authenticated:

        wishlist, _ = UserWishlist.objects.get_or_create(user=request.user)
    
        wishlist_products = [i for i in wishlist.products.all()]
    
    else:

        wishlist_products = "No Authenticated"


    match modified_cat_name:

        case 'M' | 'W':

            products_to_show = {}
            products = Product.objects.filter(product_category=modified_cat_name)
            
            for product in products:

                products_to_show[product] = ProductVariant.objects.filter(product=product)
        
        case 'C':

            products_to_show = {}
            products = Product.objects.filter(product_category=modified_cat_name)

            for product in products:

                products_to_show[product] = ProductVariant.objects.filter(product=product)
        
        case _:

            products = 'No Product'

    return render(request, 'shop-category.html', {'name':category_name, 'products':products_to_show, 'cart_prods' : cart_products, 'wishlist_prods' : wishlist_products})





def ProductDetailsView(request, product_id):

    if request.user.is_authenticated:

        cart, _ = UserCart.objects.get_or_create(user=request.user)
    
        cart_products = [i.product for i in cart.cart_items.all()]
    
    else : 

        cart_products = "No Authenticated"


    if request.user.is_authenticated:

        wishlist, _ = UserWishlist.objects.get_or_create(user=request.user)
    
        wishlist_products = [i for i in wishlist.products.all()]
    
    else:

        wishlist_products = "No Authenticated"


    product = Product.objects.get(id=product_id)

    product_variants = ProductVariant.objects.filter(product=product)


    return render(request, 'product-details.html', {'product' : product, 'variants' : product_variants, 'cart_prods' : cart_products, 'wishlist_prods' : wishlist_products})




@login_required(login_url='/authentication/user-login')
def BuyNowView(request, product_id):

    product = Product.objects.get(id=product_id)

    return render(request, 'buy-now.html', {'product' : product})



def SearchPageView(request, search_query):

    return render(request, 'search.html')



@login_required(login_url='/authentication/user-login')
def UserProfileView(request):

    return render(request, 'user-profile.html')



@login_required(login_url='/authentication/user-login')
def UserCartView(request):

    return render(request, 'user-cart.html')




@login_required(login_url='/authentication/user-login')
def UserWishlistView(request):

    return render(request, 'user-wishlist.html')





def ContactView(request):

    return render(request, 'contact.html')




def BlogsView(request):

    return render(request, 'blogs.html')




class ManageCartProduct(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        prod_id = request.data.get("prod_id",None)

        product = Product.objects.get(id=prod_id)

        user_cart = request.user.user_cart

        if product in [i.product for i in user_cart.cart_items.all()]:

            CartItem.objects.delete(cart=user_cart,product=product)

            return Response("R", status=status.HTTP_200_OK)

        else:

            CartItem.objects.create(cart=user_cart,product=product)

            return Response("C", status=status.HTTP_200_OK)



class ManageWishlistProduct(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        prod_id = request.data.get("prod_id",None)

        product = Product.objects.get(id=prod_id)

        user_wishlist = request.user.user_wishlist

        if product in [i for i in request.user.user_wishlist.products.all()]:

            user_wishlist.products.remove(product)

            return Response("R", status=status.HTTP_200_OK)

        else:

            user_wishlist.products.add(product)

            return Response("C", status=status.HTTP_200_OK)
