from django import forms
from .models import User
from django.forms import ModelForm

class authForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome Usuario","class": "form-control form-control-user","title":"Nome de Usuario de Acesso ao Sistema"}),label="Nome de Usuario")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha","class": "form-control form-control-user","title":"Senha de Acesso ao Sistema"}),label="Senha")

class registerUserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome","class": "form-control","title":"Nome Propio","onchange":"generateUsername(this)"}),label="Nome")
    cpf = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "CPF","class": "form-control","title":"Cadastro de Pessoa Física","oninput":"validateCPF(this)","onchange":"validateCPF(this)"}),label="CPF")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class": "form-control","title":"Email deve ser unico"}),label="E-mail")
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome Usuario","class": "form-control","title":"Nome de Usuario"}),label="Nome de Usuario")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha","class": "form-control","title":"A Senha deve conter caracteries especiais numeros letra maiuscula e numeros"}),label="Senha",initial="@SejaBemVindo3")
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha","class": "form-control","title":"As Senhas Devem ser iguais"}),label="Confirme a Senha",initial="@SejaBemVindo3")
    is_staff = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={"title":"Esse Usuario faz parte da equipe administradora do sistemas, deixe marcado se Sim"}),initial=True,label="Faz parte da Equipe Administradora")
    class Meta:
        model = User
        fields = ['username','email','password','password_check','is_staff']
    
class updateWithoutPasswordForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome de Usuario","class": "form-control","title":"Nome de Usuario de Acesso ao Sistema"}),label="Nome de Usuario")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class": "form-control","title":"Senha de Acesso ao Sistema"}),label="E-mail")
    class Meta:
        model = User
        fields = ['username','email']

class updateUserPasswordForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha","class": "form-control","title":"A Senha deve conter caracteries especiais numeros letra maiuscula e numeros"}),label="Senha")
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha","class": "form-control","title":"As Senhas Devem ser iguais"}),label="Confirme a Senha")
    class Meta:
        model = User
        fields = ['password','password_check']
    