from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product, Purchase, PromoCode
from .forms import PromoCodeForm


def index(request):
    products = Product.objects.all()

    form = PromoCodeForm(request.GET or None)
    discount = 0
    error_message = None

    if form.is_valid():
        code = form.cleaned_data.get('code')
        if code:
            try:
                promo = PromoCode.objects.get(code__iexact=code, active=True)
                discount = promo.discount_percent
            except PromoCode.DoesNotExist:
                error_message = "Неверный или неактивный промокод"

    if discount > 0:
        for product in products:
            product.discounted_price = product.price * (100 - discount) // 100
    else:
        for product in products:
            product.discounted_price = product.price

    context = {
        'products': products,
        'form': form,
        'discount': discount,
        'error_message': error_message,
    }
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')
