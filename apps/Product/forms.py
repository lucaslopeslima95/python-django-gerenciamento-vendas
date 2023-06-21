from django import forms
from .models import Product
from django.forms import ModelForm

class registerProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','code_bar','price','stock_quantity']
        labels = {'name':"Nome",
                  'code_bar':'Codigo De Barras',
                  'price':'Preço',
                  'stock_quantity':'Quantidade em Estoque'}
        widgets = {'name': forms.TextInput(attrs={"placeholder": "Nome do Produto","class": "form-control"}),
                   'code_bar': forms.TextInput(attrs={"placeholder": "Preço","class": "form-control"}),
                   'price': forms.TextInput(attrs={"placeholder": "Preço","class": "form-control"}),
                   'stock_quantity': forms.TextInput(attrs={"placeholder": "Quantidade em Estoque","class": "form-control"})}
        
class searchProductForm(forms.Form):
       code_bar = forms.CharField(label="Cod.Barras",widget=forms.TextInput(attrs={"placeholder": "Cod.Barras","class": "form-control"}),required=False)
        
#  name = forms.CharField(widget=
#  code_bar = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Codigo de Barras","class": "form-control"}))
#  price = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Preço","class": "form-control"}))
#  stock_quantity = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Quantidade em Estoque","class": "form-control"}))
#  widgets = {'fk_colaborattor': forms.TextInput(attrs={"placeholder": "Nome Colaborador","class": "form-control"})}        
