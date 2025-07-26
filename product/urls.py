from django.urls import path
from product.views import *

app_name = 'product'

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('list/', ProductsList.as_view(), name='products-list'),
    path(
        'list/category/',
        ProductsList.as_view(),
        name='products-list-by-category',
    ),
    path(
        'list/detail-category/',
        ProductsList.as_view(),
        name='products-list-detail',
    ),
    path(
        'list/price-range/',
        ProductsList.as_view(),
        name='products-list-by-price-range',
    ),
    path(
        'list/with-guarantee/',
        ProductsList.as_view(),
        name='products-list-by-guarantee',
    ),
    path(
        'detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'
    ),
    path(
        'add-comment/<int:pk>/',
        ProductCommentView.as_view(),
        name='product-comment',
    ),
    path(
        'add-replay/<int:pk>/', ProductReplayView.as_view(), name='add-replay'
    ),
    path('list/search/', ProductsList.as_view(), name='product-by-search'),
]
