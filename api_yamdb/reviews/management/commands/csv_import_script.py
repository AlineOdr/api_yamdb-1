import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, TitleGenre


class Command(BaseCommand):
    help = 'Transserfing from csv to database'

    def handle(self, *args, **options):
        csv_path = './static/data/'
        csv_files = [
            'category.csv',
            'genre.csv',
            'titles.csv',
            'genre_title.csv',
        ]
        model_list = [Category, Genre, Title, TitleGenre]

        for csv_file, model in zip(csv_files, model_list):
            print(csv_file)
            with open(csv_path + csv_file, encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)

                model.objects.all().delete()

                for row in reader:
                    obg = model(*row)
                    obg.save()
