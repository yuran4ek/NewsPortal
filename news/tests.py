import re
#
value = 'Эммануэль Пети: «Челси Мбаппе Один хочет быть одиноким номером один, как Роналду. У него может быть большое эго»'
BADWORDS = [
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


#
# def censor(value):
#     bad_words = [
#         'матч',
#         'Челси',
#         'осень',
#         'игроки',
#         'атаки',
#         'реализация',
#         'диск',
#         'выдерживать',
#         'корпус',
#         'производитель',
#         'один',
#         'клуб',
#         'уникальный',
#         'клавиатура',
#         'сбор',
#         'защитник',
#
#     ]
#
#     for word in bad_words:
#         pattern = (r"\b" + re.escape(word) + r"\b")
#         value = re.sub(pattern, (word[0] + (len(word) - 2) * '*') + word[-1], value, flags=re.I)
#     return value
#
#
# print(censor(text))

def censor(value: str, symbol='*'):
    badwords_in_text = set(value.lower().split()) & set(BADWORDS)  # Проверка, есть ли плохие слова в тексте
    if badwords_in_text:
        for badword in badwords_in_text:
            badword_pattern_up = r"\b" + re.escape(badword.capitalize()) + r"\b"  # Для слов с заглавной буквы
            badword_pattern_low = r"\b" + re.escape(badword) + r"\b"  # Для слов со строчной буквы
            value = re.sub(badword_pattern_up, badword.capitalize()[0] + (len(badword) - 2) * symbol + badword[-1], value)
            value = re.sub(badword_pattern_low, badword[0] + (len(badword) - 2) * symbol + badword[-1], value)
    return value


print(censor(value))
