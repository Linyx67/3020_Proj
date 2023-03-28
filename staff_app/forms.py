import datetime
from django import forms
from django.contrib.auth.forms import UserChangeForm
from hris_app.models import CustomUser
from .functions import year_choices, academic_year_choices, year_choice
from .models import (
    Employee,
    Requests,
    Leave,
    Awards,
    Publications,
    Conferences,
    Consultancies,
    Manuscripts,
    Development,
    Presentations,
    Grants,
    Specialisation,
    Supervision,
    Research,
    Roles,
    Honours,
    Contributions,
    Activities,
    Contacts
)

# Employee


class EmployeeCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Employee
        exclude = ['is_blocked', 'is_deleted', 'created', 'updated', 'user']
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 100, 'rows': 5, 'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'othername': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'nisnumber': forms.TextInput(attrs={'class': 'form-control'}),
            'employeeid': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.SelectDateWidget(years=year_choice(), attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'vitae': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'employeetype': forms.Select(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg. +18682224444'})
        }

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if not email.endswith("sta.uwi.edu"):
            raise forms.ValidationError("This is not a valid email address")
        else:
            return email

    def clean_nisnumber(self, *args, **kwargs):
        nisnumber = self.cleaned_data.get("nisnumber")
        if len(str(nisnumber)) > 9:
            raise forms.ValidationError("This is not a valid NIS Number")
        else:
            return nisnumber

    def clean_employeeid(self, *args, **kwargs):
        employeeid = self.cleaned_data.get("employeeid")
        if len(str(employeeid)) > 9:
            raise forms.ValidationError("This is not a valid ID")
        else:
            return employeeid


class RequestsCreateForm(forms.ModelForm):
    class Meta:
        model = Requests
        exclude = ['user', 'updated', 'created']
        widgets = {
            'information': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'form-control'})
        }


class PublicationsCreateForm(forms.ModelForm):

    class Meta:
        model = Publications
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(choices=academic_year_choices(), attrs={'class': 'form-control'}),
            'publicationtype': forms.Select(attrs={'class': 'form-control'}),
        }


class AwardsCreateForm(forms.ModelForm):

    class Meta:
        model = Awards
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(choices=academic_year_choices(), attrs={'class': 'form-control'}),
        }


class ConferencesCreateForm(forms.ModelForm):

    class Meta:
        model = Conferences
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(choices=academic_year_choices(), attrs={'class': 'form-control'}),

        }


class PresentationsCreateForm(forms.ModelForm):

    class Meta:
        model = Presentations
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(choices=academic_year_choices(), attrs={'class': 'form-control'}),
        }


class DevelopmentCreateForm(forms.ModelForm):

    class Meta:
        model = Development
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year_start': forms.Select(choices=year_choices(), attrs={'class': 'form-control'}),
            'year_end': forms.Select(choices=year_choices(), attrs={'class': 'form-control'}),
        }

    def clean_endyear(self):
        year_end = self.cleaned_data['year_end']
        year_start = self.cleaned_data['year_start']
        year_today = datetime.date.today().year()

        if (year_start or year_end) < year_today:  # both dates must not be in the past
            raise forms.ValidationError(
                "Selected Years are incorrect,please select again")
        elif year_start >= year_end:  # TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
            raise forms.ValidationError("Selected Years are wrong")
        return year_end


class ConsultanciesCreateForm(forms.ModelForm):
    class Meta:
        model = Consultancies
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'period': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ManuscriptsCreateForm(forms.ModelForm):
    class Meta:
        model = Manuscripts
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class GrantsCreateForm(forms.ModelForm):
    class Meta:
        model = Grants
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RolesCreateForm(forms.ModelForm):
    class Meta:
        model = Roles
        exclude = ['created', 'updated', 'user']
        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'association': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.SelectDateWidget(years=year_choice(), attrs={'class': 'form-control'}),
        }


class ResearchCreateForm(forms.ModelForm):
    class Meta:
        model = Research
        exclude = ['created', 'updated', 'user']
        widgets = {
            'research': forms.TextInput(attrs={'class': 'form-control'}),
            'interest': forms.Textarea(attrs={'class': 'form-control'}),

        }


class SupervisionCreateForm(forms.ModelForm):
    class Meta:
        model = Supervision
        exclude = ['created', 'updated', 'user']
        widgets = {

            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(choices=academic_year_choices(), attrs={'class': 'form-control'}),
        }


class SpecialisationCreateForm(forms.ModelForm):
    class Meta:
        model = Specialisation
        exclude = ['created', 'updated', 'user']
        widgets = {
            'area': forms.TextInput(attrs={'class': 'form-control'}),
        }


class HonoursCreateForm(forms.ModelForm):
    class Meta:
        model = Honours
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'competition': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(choices=academic_year_choices(), attrs={'class': 'form-control'}),
        }


class ActivitiesCreateForm(forms.ModelForm):
    class Meta:
        model = Activities
        exclude = ['created', 'updated', 'user']
        widgets = {
            'activity': forms.TextInput(attrs={'class': 'form-control'}),

        }


class ContributionsCreateForm(forms.ModelForm):
    class Meta:
        model = Contributions
        exclude = ['created', 'updated', 'user']
        widgets = {
            'contribution': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(choices=academic_year_choices(), attrs={'class': 'form-control'}),
        }


class LeaveCreateForm(forms.ModelForm):

    class Meta:
        model = Leave
        exclude = ['user', 'defaultdays', 'status',
                   'is_approved', 'updated', 'created']
        widgets = {
            'startdate': forms.SelectDateWidget(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'form-control'}),
            'enddate': forms.SelectDateWidget(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'form-control'}),
            'leavetype':  forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 12, 'cols': 40, 'class': 'form-control'})
        }

    def clean_enddate(self):
        enddate = self.cleaned_data['enddate']
        startdate = self.cleaned_data['startdate']
        today_date = datetime.date.today()

        if (startdate or enddate) < today_date:  # both dates must not be in the past
            raise forms.ValidationError(
                "Selected dates are incorrect,please select again")
        elif startdate >= enddate:  # TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
            raise forms.ValidationError("Selected dates are wrong")
        return enddate
