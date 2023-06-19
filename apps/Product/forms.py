from django import forms
from .models import Product
from django.forms import ModelForm

class registerProductForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome do Produto","class": "form-control"}))
    code_bar = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Codigo de Barras","class": "form-control"}))
    price = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Preço","class": "form-control"}))
    stock_quantity = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Quantidade em Estoque","class": "form-control"}))
    class Meta:
        model = Product
        fields = ['name','code_bar','price','stock_quantity']

        
