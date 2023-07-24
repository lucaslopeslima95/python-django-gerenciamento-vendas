from django import forms


class searchProductToPurchaseForm(forms.Form):
    code_bar = forms.CharField(
              label="Código de barras",
              widget=forms.TextInput(
                     attrs={"placeholder": "Código de barras",
                            "class": "form-control"}))
