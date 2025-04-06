# from django.shortcuts import render
from django.views.generic.edit import CreateView
from orders.forms import OrderForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from common.views import TitleMixin
from django.views.generic.base import TemplateView
from orders.models import Order
from products.models import Basket


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = '-created'

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_success')
    title = 'Store - Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        # return super(OrderCreateView, self).form_valid(form)
        response = super().form_valid(form)

        # Получаем корзину пользователя
        baskets = Basket.objects.filter(user=self.request.user)

        # Сохраняем историю корзины
        self.object.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        self.object.status = Order.PAID
        self.object.save()

        # Очищаем корзину
        baskets.delete()

        return response
