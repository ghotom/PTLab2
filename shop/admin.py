from django.contrib import admin
from .models import Product, Purchase, PromoCode


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'active')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('person', 'product', 'address', 'date')
    list_filter = ('date',)
