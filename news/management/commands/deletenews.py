from django.core.management.base import BaseCommand, CommandError

from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все новости из выбранной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        admins_answer = input(f'После ввода "yes", все публикации в категории "{options["category"]}" будут удалены.'
                              f' Вы уверены, что хотите удалить все публикации в категории "{options["category"]}"?\n'
                              f'yes/no:\n')
        if admins_answer == 'yes':
            try:
                category = Category.objects.get(categories=options['category'])
                Post.objects.filter(postCategories=category).delete()

                self.stdout.write(self.style.SUCCESS(
                    f'Все публикации в категории "{options["category"]}" успешно удалены'))

            except category.DoesNotExist():
                self.stdout.write(self.style.ERROR(f'Не удалось найти категорю. Попробуйте ещё раз'))

        else:
            self.stdout.write(self.style.ERROR('Удаление публикаций отменено'))

