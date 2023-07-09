from django import forms
from .models import Product
from django.forms import ModelForm

class registerProductForm(ModelForm):
    code_bar = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Codigo de Barras","class": "form-control","onchange":"validateCodeBar(this)"}),max_length=18)
    class Meta:
        model = Product
        fields = ['name','code_bar','price','stock_quantity','category']
        labels = {
                  'name':"Nome",
                  'code_bar':'Codigo De Barras',
                  'price':'Preço',
                  'stock_quantity':'Quantidade em Estoque',
                  'category':'Categoria'
                  }
        widgets = {'name': forms.TextInput(attrs={"placeholder": "Nome do Produto","class": "form-control","maxlength": "30"}),
                   'price': forms.TextInput(attrs={"placeholder": "Preço","class": "form-control"}),
                   'stock_quantity': forms.TextInput(attrs={"placeholder": "Quantidade em Estoque","class": "form-control"}),
                   'category':forms.Select(attrs={'class': 'form-control ','readonly':True})
                   }
        
class searchProductForm(forms.Form):
       name = forms.CharField(label="Nome Produto",widget=forms.TextInput(attrs={"placeholder": "Nome","class": "form-control"}),required=False)