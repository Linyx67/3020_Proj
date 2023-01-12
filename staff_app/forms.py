from django import forms
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
    image = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'onchange': 'previewImage(this);'}))

    class Meta:
        model = Employee
        exclude = ['is_blocked', 'is_deleted', 'created', 'updated', 'user']
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 100, 'rows': 5})
        }

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if not email.endswith("edu"):
            raise forms.ValidationError("This is not a valid email address")
        else:
            return email

        # def clean_user(self):
        # 	user = self.cleaned_data['user'] #returns <User object>,not id as in [views <-> templates]

        # 	qry = Employee.objects.filter(user = user)#check, whether any employee exist with username - avoid duplicate users - > many employees
        # 	if qry:
        # 		raise forms.ValidationError('Employee exists with username already')
        #   return user


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
