from django import forms
from .models import Collaborator, status_collaborator
from django.forms import ModelForm


class registerCollaboratorForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome","class": "form-control","onchange":"generateUsername(this)"}),label="Nome")
    cpf = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "CPF","class": "form-control","onchange":"validateCPF(this)"}),label="CPF")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class": "form-control"}),label="Email")
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome Usuario","class": "form-control"}),label="Nome de Usuario")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha","class": "form-control"}),label="Senha")
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirme a Senha","class": "form-control","onchange":"validatePassword()"}),label="Confirme a senha")
    class Meta:
        model = Collaborator
        fields = ['name','cpf','username','email','password','password_check']
        
    
class updateWithoutPasswordForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome","class": "form-control"}),label="Nome")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class": "form-control"}),label="E-mail")
    cpf = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "CPF","class": "form-control","onchange":"validateCPF(this)"}),label="CPF")
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome de Usuario","class": "form-control"}),label="Nome de Usuario")
    active = forms.ChoiceField(choices=status_collaborator.choices,widget=forms.Select(attrs={'class': 'form-control '}),label= 'Situação')
    class Meta:
        model = Collaborator
        fields = ['name','email','cpf','username','active']
    

class updateUserPasswordForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha","class": "form-control"}),label="Senha")
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha","class": "form-control","onchange":"validatePassword()"}),label="Confirme a Senha")
    class Meta:
        model = Collaborator
        fields = ['password','password_check']
        
class findByNameForm(forms.Form):
   name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome","class": "form-control"}),label="Nome")
   