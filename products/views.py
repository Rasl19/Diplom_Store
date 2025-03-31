from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from .forms import *
from django.db.models import Q


class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Store'
        context['is_promotion'] = True
        return context


def products(request, category_id=None):
    search_form = SearchForm(request.GET)
    price_filter_form = PriceFilterForm(request.GET)
    in_stock = PriceFilterForm(request.GET)
    if 'query' in request.GET:
        query = request.GET['query']
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        in_stock = request.GET.get('in_stock')
        products = ProductModel.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if in_stock:
            products = products.filter(quantity__gt=0)
    elif category_id:
        category = ProductCategoryModels.objects.get(id=category_id)
        products = ProductModel.objects.filter(category=category)
    else:
        products = ProductModel.objects.all()
    PER_PAGE = 3
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
        'category_id': category_id,
        'search_form': search_form,
        'price_filter_form': price_filter_form,
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
