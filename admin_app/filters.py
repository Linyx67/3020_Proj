# used for the django_filters 3rd party installed ap
import django_filters
from django_filters import CharFilter
from staff_app.models import (
    Employee,
    Leave,
    Awards,
    Publications,
    Conferences,
    Development,
    Manuscripts,
    Presentations,
    Consultancies,
    Grants
)


class AwardsFilter(django_filters.FilterSet):

    class Meta:
        model = Awards
        fields = ['title', 'year']


class EmployeeFilter(django_filters.FilterSet):
    firstname = CharFilter(field_name="firstname",
                           lookup_expr='icontains', label='First Name')
    lastname = CharFilter(field_name='lastname',
                          lookup_expr='icontains', label='Surname')

    class Meta:
        model = Employee
        fields = ['firstname', 'lastname']
