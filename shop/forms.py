from django import forms


class PromoCodeForm(forms.Form):
    code = forms.CharField(
        max_length=20,
        required=False,
        label="Промокод",
        widget=forms.TextInput(attrs={'placeholder': 'Введите промокод'})
    )
