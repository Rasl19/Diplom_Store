from django.shortcuts import render
from .models import *

def index(request):
    context = {
        'title': 'Store',
        'is_promotion': True
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': ProductModel.objects.all(),
        'categories': ProductCategoryModels.objects.all().order_by('-id'),
    }
    return render(request, 'products/products.html', context)
