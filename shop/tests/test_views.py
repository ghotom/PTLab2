from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, PromoCode, Purchase


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(name="Машинка Hot Wheels", price=500)
        self.product2 = Product.objects.create(name="Набор кубиков", price=1200)
        PromoCode.objects.create(code="TOY10", discount_percent=10, active=True)
        PromoCode.objects.create(code="OLD", discount_percent=15, active=False)

    def test_index_page_accessible(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_index_without_promo(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, "500")
        self.assertContains(response, "1200")
        self.assertNotContains(response, "450")
        self.assertEqual(response.context['discount'], 0)
        self.assertIsNone(response.context.get('error_message'))

    def test_index_with_valid_promo(self):
        response = self.client.get(reverse('index'), {'code': 'TOY10'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Применена скидка 10%")
        
        products = response.context['products']
        prices = [p.discounted_price for p in products]
        self.assertIn(450, prices)
        self.assertIn(1080, prices)
        
        self.assertEqual(response.context['discount'], 10)

    def test_index_with_invalid_promo(self):
        response = self.client.get(reverse('index'), {'code': 'BADCODE'})
        self.assertContains(response, "Неверный или неактивный промокод")
        self.assertEqual(response.context['discount'], 0)
        self.assertNotContains(response, "Применена скидка")

    def test_index_with_inactive_promo(self):
        response = self.client.get(reverse('index'), {'code': 'OLD'})
        self.assertContains(response, "Неверный или неактивный промокод")
        self.assertEqual(response.context['discount'], 0)


class PurchaseCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Пазл 1000 деталей", price=900)
        self.url = reverse('buy', args=[self.product.id])

    def test_purchase_page_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_purchase(self):
        data = {
            'product': self.product.id,
            'person': 'Петров Пётр',
            'address': 'ул. Центральная, д. 5'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Спасибо за покупку, Петров Пётр!")
        
        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.person, "Петров Пётр")
        self.assertEqual(purchase.product, self.product)
