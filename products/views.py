from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required


def index(request):
    context = {
        'title': 'Store',
        'is_promotion': True
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    if category_id:
        product = ProductModel.objects.filter(category_id=category_id)
    else:
        product = ProductModel.objects.all()
    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategoryModels.objects.all().order_by('-id'),
        'products': product,
    }
    return render(request, 'products/products.html', context)


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
