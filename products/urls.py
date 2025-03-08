from django.urls import path, include
from products.views import *

urlpatterns = [
    path('', products, name='products'),
    path('category/<int:category_id>/', products, name='category'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
