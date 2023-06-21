from django import forms
from .models import PurchaseItem
from django.forms import ModelForm

   
class PurchaseItemForm(ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['fk_purchase','fk_product','fk_collaborator', 'quantity', 'price']
        labels = {'quantity':'Quantidade','price':'Preço'}

class searchProductToPurchaseForm(forms.Form):
       code_bar = forms.CharField(label="Cod.Barras",widget=forms.TextInput(attrs={"placeholder": "Cod.Barras","class": "form-control"}),initial=0)
       quantity = forms.CharField(label="Quantidade",widget=forms.NumberInput(attrs={"placeholder": "Quantidade","class": "form-control ms-1 me-1"}),initial=1)