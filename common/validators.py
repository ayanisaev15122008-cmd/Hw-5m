from django.core.exceptions import ValidationError
from datetime import date
def validate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 18:
        raise ValidationError('Возраст должен быть не менее 18 лет.')
