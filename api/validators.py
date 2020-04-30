import datetime as dt
from django.core.exceptions import ValidationError


def validate_year(val):
    nowYear = int(dt.datetime.today().year)
    if val < 0 or val > nowYear:
        raise ValidationError(
            'Год должен быть больше нуля и  меньше или равен текущему')


def validate_score(val):
    if val < 1 or val > 10:
        raise ValidationError(
            'Оценка произведения должна быть в диапазоне от 1 до 10')
