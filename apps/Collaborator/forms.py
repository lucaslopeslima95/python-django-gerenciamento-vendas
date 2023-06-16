from django import forms
from .models import Collaborator
from django.forms import ModelForm

class registerCollaboratorForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome Usuario","class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha","class": "form-control"}))
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirme a Senha","class": "form-control"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome","class": "form-control"}))
    cpf = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Cpf","class": "form-control"}))
    class Meta:
        model = Collaborator
        fields = ['username','email','password','password_check','name','cpf']
    
class updateWithoutPasswordForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username","class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class": "form-control"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome","class": "form-control"}))
    cpf = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Cpf","class": "form-control"}))
    class Meta:
        model = Collaborator
        fields = ['username','email']

class updateUserPasswordForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password","class": "form-control"}))
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password check","class": "form-control"}))
    class Meta:
        model = Collaborator
        fields = ['password','password_check']