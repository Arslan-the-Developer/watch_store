from django.urls import path
from . import views


urlpatterns = [

    path('', views.HomePageView),

    path('shop', views.ShopPageView),

    path('shop/<str:category_name>', views.ShopCategoryPageView),
    
    path('search/<str:search_query>', views.SearchPageView),
    
    path('product-details/<str:product_id>', views.ProductDetailsView),
    
    path('buy-now/<str:product_id>', views.BuyNowView),

    path('user-profile', views.UserProfileView),
    
    path('user-cart', views.UserCartView),
    
    path('user-wishlist', views.UserWishlistView),
    
    path('contact', views.ContactView),
    
    path('blogs', views.BlogsView),
    
    path('manage-cart-product', views.ManageCartProduct.as_view()),
    
    path('manage-wishlist-product', views.ManageWishlistProduct.as_view()),

]
