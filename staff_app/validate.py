import datetime
from django.core.validators import MaxValueValidator

# function that returns the current year as an integer value.


def current_year():
    return datetime.date.today().year


""" 
function takes a value as an argument and returns the result of calling MaxValueValidator() on that value, 
where the maximum value is set to the current year obtained from current_year()
this will be used as a validator.
"""


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)
