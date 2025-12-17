from django.test import TestCase
from shop.forms import PromoCodeForm


class PromoCodeFormTest(TestCase):
    def test_valid_form_with_code(self):
        form = PromoCodeForm(data={'code': 'TOY10'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['code'], 'TOY10')

    def test_valid_form_empty_code(self):
        form = PromoCodeForm(data={'code': ''})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['code'], '')

    def test_form_without_data(self):
        form = PromoCodeForm(data={})
        self.assertTrue(form.is_valid())  # required=False
        self.assertEqual(form.cleaned_data['code'], '')
