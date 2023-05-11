import logging
from csv import DictReader

from django.core.management import BaseCommand
from recipes.models import Tag

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Command(BaseCommand):
    help = "Загрузка данных из tags.csv"

    def handle(self, *args, **options):
        logger.info("Загрузка тэгов.")

        tag_list = []
        count = 0
        for row in DictReader(open('./data/tags.csv', encoding='utf-8')):
            tag = Tag(
                name=row['name'],
                color=row['color'],
                slug=row['slug'],
            )
            tag_list.append(tag)
            count += 1

        Tag.objects.bulk_create(tag_list)

        logger.info(f'Успешно загружено {count} тэгов')
