from django import forms
from django.contrib.auth.forms import UserChangeForm
import datetime
from hris_app.models import CustomUser
from .models import (
    Emergency,
    Employee,
    Religion,
    Leave,
    Awards,
    Publications
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
            'tinnumber': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'onchange': 'previewImage(this);',
                                            'class': 'form-control-file'}),
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
            'startdate': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'form-control'}),
            'enddate': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'form-control'}),
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
    year = forms.IntegerField(
        min_value=1900, max_value=datetime.date.today().year)

    class Meta:
        model = Publications
        exclude = ['created', 'updated', 'user']


class AwardsCreateForm(forms.ModelForm):
    year = forms.IntegerField(
        min_value=1900, max_value=datetime.date.today().year)

    class Meta:
        model = Awards
        exclude = ['created', 'updated', 'user']
