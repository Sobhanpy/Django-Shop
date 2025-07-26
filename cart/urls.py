from django.urls import path
from cart.views import *

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('update-cart/', UpdateCartView.as_view(), name='update-cart'),
    path(
        'delete-from-cart/<str:uid>/',
        DeleteCartItemView.as_view(),
        name='delete-product',
    ),
    path('clean-cart/', CleanCartItemView.as_view(), name='clean-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
