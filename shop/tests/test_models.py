from django.test import TestCase
from shop.models import Product, PromoCode, Purchase
from datetime import datetime


class ProductModelTest(TestCase):
    def setUp(self):
        Product.objects.create(name="Конструктор LEGO", price=2990)
        Product.objects.create(name="Плюшевый мишка", price=890)

    def test_product_fields_types(self):
        lego = Product.objects.get(name="Конструктор LEGO")
        bear = Product.objects.get(name="Плюшевый мишка")

        self.assertIsInstance(lego.name, str)
        self.assertIsInstance(lego.price, int)
        self.assertIsInstance(bear.name, str)
        self.assertIsInstance(bear.price, int)

    def test_product_data_correctness(self):
        self.assertEqual(Product.objects.get(name="Конструктор LEGO").price, 2990)
        self.assertEqual(Product.objects.get(name="Плюшевый мишка").price, 890)


class PromoCodeModelTest(TestCase):
    def setUp(self):
        PromoCode.objects.create(code="TOY5", discount_percent=5, active=True)
        PromoCode.objects.create(code="TOY15", discount_percent=15, active=False)

    def test_promo_code_str(self):
        promo = PromoCode.objects.get(code="TOY5")
        self.assertEqual(str(promo), "TOY5 (5%)")

    def test_promo_code_fields(self):
        promo = PromoCode.objects.get(code="TOY15")
        self.assertEqual(promo.discount_percent, 15)
        self.assertFalse(promo.active)


class PurchaseModelTest(TestCase):
    def setUp(self):
        product = Product.objects.create(name="Кукла Barbie", price=1500)
        Purchase.objects.create(
            product=product,
            person="Иванов Иван",
            address="ул. Светлая, д. 10"
        )

    def test_purchase_fields_types(self):
        purchase = Purchase.objects.first()
        self.assertIsInstance(purchase.person, str)
        self.assertIsInstance(purchase.address, str)
        self.assertIsInstance(purchase.date, datetime)

    def test_purchase_data(self):
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.person, "Иванов Иван")
        self.assertEqual(purchase.address, "ул. Светлая, д. 10")
        self.assertIsNotNone(purchase.date)
