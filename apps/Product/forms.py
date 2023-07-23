
from decimal import Decimal

from django import forms
from django.forms import ModelForm
from jsonschema import ValidationError

from .models import Product, status_type


class CustomDecimalField(forms.DecimalField):
    def to_python(self, value):
        try:
            if value in self.empty_values:
                return None
            try:
                return Decimal(value.replace(',', '.').replace("R$ ", ""))
            except Decimal.InvalidOperation:
                raise ValidationError('Insira um número válido.')
        except Exception as e:
            print(f"Exceção no Custo Decimal field -  {e}")


class registerProductForm(ModelForm):
    code_bar = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Codigo de Barras",
                   "class": "form-control"}),
        max_length=18)
    active = forms.ChoiceField(
        choices=status_type.choices,
        widget=forms.Select(attrs={'class': 'form-control '}),
        label='Situação')
    price = CustomDecimalField(
        widget=forms.TextInput(
            attrs={"placeholder": "Preço",
                   "class": "form-control",
                   "oninput": "inputPriceMask(this)"}))

    class Meta:
        model = Product
        fields = ['name', 'code_bar', 'price', 'category', 'active']
        labels = {
                  'name': 'Nome',
                  'code_bar': 'Codigo De Barras',
                  'category': 'Categoria',
                  }
        widgets = {
                   'name': forms.TextInput(
                       attrs={"placeholder": "Nome do Produto",
                              "class": "form-control",
                              "maxlength": "30"}),
                   'category': forms.Select(
                       attrs={'class': 'form-control ',
                              'readonly': True}),
                   'active': forms.Select(
                       attrs={'class': 'form-control ', 'readonly': True})
                   }
