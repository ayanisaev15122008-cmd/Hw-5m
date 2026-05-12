from django.core.exceptions import ValidationError
from datetime import date

def check_birthday(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Тебе нет 18 лет, доступ запрещен!")
