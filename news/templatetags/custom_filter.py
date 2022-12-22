from django import template
import re

register = template.Library()


@register.filter()
def censor(value: str, symbol='*'):
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
    # Проверка, есть ли плохие слова в тексте
    badwords_in_text = set(value.lower().split()) & set(bad_words)
    if badwords_in_text:
        for badword in badwords_in_text:
            # Для слов с заглавной буквы
            badword_pattern_up = r"\b" + re.escape(badword.capitalize()) + r"\b"
            # Для слов со строчной буквы
            badword_pattern_low = r"\b" + re.escape(badword) + r"\b"
            value = re.sub(badword_pattern_up, badword.capitalize()[0] + (len(badword) - 2) * symbol + badword[-1],
                           value)
            value = re.sub(badword_pattern_low, badword[0] + (len(badword) - 2) * symbol + badword[-1], value)
    return value
