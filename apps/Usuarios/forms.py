from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

class authForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome Usuario","class": "form-control form-control-user"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha","class": "form-control form-control-user"}))

class registerUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome Usuario","class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password","class": "form-control"}))
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password check","class": "form-control"}))
    is_staff = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={}),initial=True)
    class Meta:
        model = User
        fields = ['username','email','password','password_check','is_staff']
    
class updateWithoutPasswordForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username","class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class": "form-control"}))
    class Meta:
        model = User
        fields = ['username','email']

class updateUserPasswordForm(ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password","class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Repeat Password","class": "form-control"}))
    class Meta:
        model = User
        fields = ['password1','password2']