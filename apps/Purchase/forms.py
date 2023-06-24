from django import forms

class searchProductToPurchaseForm(forms.Form):
       code_bar = forms.CharField(label="Cod.Barras",widget=forms.TextInput(attrs={"placeholder": "Cod.Barras","class": "form-control"}))
       #quantity = forms.IntegerField(label="Quantidade",widget=forms.NumberInput(attrs={"placeholder": "Quantidade","class": "form-control ms-1 me-1"}),initial=1)