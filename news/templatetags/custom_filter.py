from django import template
import re

register = template.Library()


@register.filter()
def censor(value):
    bad_words = [
        'матч',
        'Челси',
        'осень',
        'игроки',
        'атаки',
        'реализация',
        'диск',
        'выдерживать',
        'корпус',
        'производитель',
        'один',
        'клуб',
        'уникальный',
        'клавиатура',
        'сбор',
        'защитник',

    ]

    if not isinstance(value, str):
        raise TypeError('Переменная должна быть строкового типа!')
    for word in bad_words:
        pattern = (r"\b" + re.escape(word) + r"\b")
        value = re.sub(pattern, (word[0] + (len(word) - 2) * '*') + word[-1], value, flags=re.I)
    return value
