from django.urls import path, include
from products.views import *

urlpatterns = [
    path('', index, name='index'),
    path('products/', products, name='products'),
]
