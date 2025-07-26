from django.contrib import admin
from .models import Product, ProductVariant, VariantImage, UserWishlist, UserCart, UserDeliveryAddress, UserOrder, UserOrderItem, CartItem, ProductReview, ReviewImage




admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(VariantImage)
admin.site.register(UserWishlist)
admin.site.register(UserCart)
admin.site.register(UserDeliveryAddress)
admin.site.register(UserOrder)
admin.site.register(UserOrderItem)
admin.site.register(CartItem)
admin.site.register(ProductReview)
admin.site.register(ReviewImage)