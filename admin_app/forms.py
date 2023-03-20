from django import forms
from staff_app.functions import academic_year_choices

# creating a form to submit for generating academic year reports


class ReportForm(forms.Form):
    firstname = forms.CharField(max_length=20, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    lastname = forms.CharField(max_length=20, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    year = forms.CharField(max_length=9, required=True, widget=forms.Select(
        choices=academic_year_choices(), attrs={'class': 'form-control'}))
