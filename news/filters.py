import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post, Category


class PostFilter(FilterSet):

    header = django_filters.CharFilter(
        field_name='header',
        lookup_expr='icontains',
        label='Заголовок публикации'
    )

    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='postCategories',
        queryset=Category.objects.all(),
        label='Категории публикаций',

    )

    timeIn = django_filters.DateFilter(
        field_name='timeIn',
        lookup_expr='gt',
        label='Дата публикации',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        ),
    )
