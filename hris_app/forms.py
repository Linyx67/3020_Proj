from django import forms
from . models import CustomUser


class AddAccountForm(forms.Form):
    firstname = forms.CharField(label='First Name', max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='Last Name', max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    type = forms.ChoiceField(label='Account Type', choices=[('administrator', 'Admin'), (
        'staff', 'Staff')], widget=forms.Select(attrs={'class': 'form-control'}))
