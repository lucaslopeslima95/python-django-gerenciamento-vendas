from django import forms
from .models import Category
from django.forms import ModelForm

class registerCategoryForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome Categoria","class": "form-control","onchange":"generateUsername(this)"}),label="Nome")
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Descrição da categoria","class": "form-control"}),label="Descrição da categoria")
    class Meta:
        model = Category
        fields = ['name','description']

   