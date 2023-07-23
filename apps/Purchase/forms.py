from django import forms


class searchProductToPurchaseForm(forms.Form):
    code_bar = forms.CharField(
              label="Cod.Barras",
              widget=forms.TextInput(
                     attrs={"placeholder": "Cod.Barras",
                            "class": "form-control"}))
