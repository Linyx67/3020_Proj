from django import forms
from django.contrib.auth.forms import UserChangeForm
from hris_app.models import CustomUser
from .functions import year_choices, academic_year_choices, year_choice
from .models import (
    Emergency,
    Employee,
    Religion,
    Leave,
    Awards,
    Publications,
    Conferences,
    Consultancies,
    Manuscripts,
    Development,
    Presentations,
    Grants
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
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.SelectDateWidget(years=year_choice(), attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'onchange': 'previewImage(this);'}),
            'vitae': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'employeetype': forms.Select(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg. +18682224444'})
        }

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if not email.endswith("edu"):
            raise forms.ValidationError("This is not a valid email address")
        else:
            return email

    def clean_nisnumber(self, *args, **kwargs):
        nisnumber = self.cleaned_data.get("nisnumber")
        if len(str(nisnumber)) > 9:
            raise forms.ValidationError("This is not a valis NIS Number")
        else:
            return nisnumber
        # def clean_user(self):
        # 	user = self.cleaned_data['user'] #returns <User object>,not id as in [views <-> templates]

        # 	qry = Employee.objects.filter(user = user)#check, whether any employee exist with username - avoid duplicate users - > many employees
        # 	if qry:
        # 		raise forms.ValidationError('Employee exists with username already')
        #   return user


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


class EmergencyCreateForm(forms.ModelForm):

    class Meta:
        model = Emergency
        fields = ['employee', 'fullname', 'tel', 'location', 'relationship']


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
            'in_preparation': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'in_review': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class GrantsCreateForm(forms.ModelForm):
    class Meta:
        model = Grants
        exclude = ['created', 'updated', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
