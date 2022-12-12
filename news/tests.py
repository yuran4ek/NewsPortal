import re

text = 'Эммануэль Пети: «Челси Мбаппе Один хочет быть одиноким номером один, как Роналду. У него может быть большое эго»'


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

    for word in bad_words:
        pattern = (r"\b" + re.escape(word) + r"\b")
        value = re.sub(pattern, (word[0] + (len(word) - 2) * '*') + word[-1], value, flags=re.I)
    return value


print(censor(text))
