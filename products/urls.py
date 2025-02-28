from django.urls import path, include
from products.views import *

urlpatterns = [
    path('', products, name='products'),
]
