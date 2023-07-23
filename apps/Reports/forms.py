from Collaborator.models import Collaborator
from django import forms


class reportsForm(forms.Form):
    collaborator = forms.ModelChoiceField(
        queryset=Collaborator.objects.filter(
         active=True),
        widget=forms.Select(
         attrs={'class': 'form-control'}),
        label="Escolha o colaborador")
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control',
                   'type': 'date',
                   'placeholder': 'Selecione uma data',
                   'autocomplete': 'off', 'value': ''}),
        label="Começa em")
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control',
                   'type': 'date',
                   'placeholder': 'Selecione uma data',
                   'autocomplete': 'off',
                   'value': ''}),
        label="Até")
