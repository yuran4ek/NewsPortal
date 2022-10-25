from django import template
from flashtext import KeywordProcessor


register = template.Library()


keyword_processor = KeywordProcessor()

keyword_dict = {
    'м**ч': ['матч'],
    'Ч***и': ['Челси'],
    'о***ь': ['осень'],
    'и****и': ['игроки'],
    'а***и': ['атаки'],
    'р********я': ['реализация'],
    'д**к': ['диск'],
    'в*********ь': ['выдерживать'],
    'к****с': ['корпус'],
    'п***********ь': ['производитель']
}

keyword_processor.add_keywords_from_dict(keyword_dict)

@register.filter()
def censor(value):
    """
    value: значение, к которому будем применять фильтр
    """
    new_value = keyword_processor.replace_keywords(value)
    return f'{new_value}'
