from django.core.exceptions import ValidationError
import re


def validate_at_least_one_digit(val):
    if re.search('\d', val) is None:
        raise ValidationError('Password must contain at least 1 digit (0-9)')

def validate_at_least_one_lower_case(val):
    if re.search('[a-z]', val) is None:
        raise ValidationError('Password must contain at least 1 lower case letter (a-z)')

def validate_at_least_one_upper_case(val):
    if re.search('[A-Z]', val) is None:
        raise ValidationError('Password must contain at least 1 upper case letter (a-z)')

def validate_at_least_one_special_character(val):
    if re.search(r'[*!@$%^&(){}\[\]:;<>,\.\?\/~_\+\-=|]', val) is None:
        raise ValidationError(
            'Password must contain at least 1 special character ' + 
            '(*.!@$%^&(){}[]:;<>,?/~_+-=|)'
            )

def validate_password_length(val):
    if re.fullmatch(r"[\da-zA-Z*!@$%^&(){}\[\]:;<>,\.\?\/~_\+\-=|]{8,30}", val) is None:
        raise ValidationError('Password\'s length must be between 8 and 30 characters')



def validate_username(val):
    if re.fullmatch(r'[a-zA-Z0-9_.]{3,}', val) is None:
        raise ValidationError(
            'Username must have between 1 and 30 characters,' + 
            ' and are only allowed to contain alphanumerics and the symbols . and _'
            )
