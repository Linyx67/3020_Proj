from django import forms
from staff_app.functions import academic_year_choices
from staff_app.models import Contacts
# creating a form to submit for generating academic year reports


class ReportForm(forms.Form):
    firstname = forms.CharField(max_length=20, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    lastname = forms.CharField(max_length=20, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    year = forms.CharField(max_length=9, required=True, widget=forms.Select(
        choices=academic_year_choices(), attrs={'class': 'form-control'}))


class ContactsCreateForm(forms.ModelForm):
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Contacts
        exclude = ['created', 'updated']
        widgets = {

            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'information': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if not email.endswith("sta.uwi.edu"):
            raise forms.ValidationError("This is not a valid email address")
        else:
            return email
