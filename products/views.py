from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    context = {
        'title': 'Store',
        'is_promotion': True
    }
    return render(request, 'products/index.html', context)


# def products(request, category_id=None, page_number=1):
#     if category_id:
#         product = ProductModel.objects.filter(category_id=category_id)
#     else:
#         product = ProductModel.objects.all()
#
#     per_page = 3
#     paginator = Paginator(product, per_page)
#     product_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Store - Каталог',
#         'categories': ProductCategoryModels.objects.all().order_by('-id'),
#         'products': product_paginator,
#         'category_id': category_id,
#     }
#     return render(request, 'products/products.html', context)

def products(request, category_id=None):
    PER_PAGE = 3
    if category_id:
        category = ProductCategoryModels.objects.get(id=category_id)
        products = ProductModel.objects.filter(category=category)
    else:
        products = ProductModel.objects.all()
    page = request.GET.get('page', 1)
    if not isinstance(page, int):
        if page.isdigit():
            page = int(page)
        else:
            page = 1
    paginator = Paginator(products, per_page=PER_PAGE)
    page_products = paginator.page(page)
    return render(request, 'products/products.html', context={
        'title': 'Store - продукты',
        'products': page_products,
        'categories': ProductCategoryModels.objects.all(),
        'category_id': category_id
    })


@login_required
def basket_add(request, product_id):
    product = ProductModel.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id, user=request.user)
    if basket is not None:
        basket.delete()
    return redirect(request.META['HTTP_REFERER'])
