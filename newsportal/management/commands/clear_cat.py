from django.core.management.base import BaseCommand, CommandError
from newsportal.models import Category, Post


class Command(BaseCommand):
    help = 'Команда удаляет указанную категорию'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        category = Category.objects.get(name=options['category'])
        try:

            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Successfully deleted all news from category {category.name}'))  # в случае неправильного подтверждения, говорим что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {category.name}'))