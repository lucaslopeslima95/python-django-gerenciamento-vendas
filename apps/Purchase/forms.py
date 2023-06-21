from django import forms
from .models import Purchase
from .models import PurchaseItems
from django.forms import ModelForm



class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['fk_colaborattor']
        labels = {'fk_colaborattor': 'Colaborador'}
        widgets = {'fk_colaborattor': forms.TextInput(attrs={"placeholder": "Nome Colaborador","class": "form-control"})}
        
class PurchaseItemsForm(ModelForm):
    class Meta:
        model = PurchaseItems
        fields = ['fk_purchase','fk_product','fk_collaborator', 'quantity', 'price']
        labels = {'quantity':'Quantidade','price':'Preço'}

class PurchaseRegisterForm(forms.Form):
    total_cost = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}),label="Valor Total")
    
