from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Ingredient


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Загрузка данных из ingredient.csv"

    def handle(self, *args, **options):
        print("Загрузка ингредиентов.")

        count = 0
        for row in DictReader(
            open('./data/ingredients.csv', encoding='utf-8')
        ):
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['unit of measure']
            )
            ingredient.save()
            count += 1

        print(f'Успешно загружено {count} ингредиентов')