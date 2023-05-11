from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
 

# example
def validate_slug_field(value):
    if "@gmail.com" in value:
        return value
    else:
        raise ValidationError("This field accepts mail id of google only")
