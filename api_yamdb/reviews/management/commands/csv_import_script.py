import csv

from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    TitleGenre,
    User,
)


class Command(BaseCommand):
    help = 'Transserfing from csv to database'

    def handle(self, *args, **options):
        csv_path = './static/data/'
        csv_files = [
            'category.csv',
            'genre.csv',
            'titles.csv',
            'genre_title.csv',
            'users.csv',
            'review.csv',
            'comments.csv',
        ]
        model_list = [
            Category,
            Genre,
            Title,
            TitleGenre,
            User,
            Review,
            Comment,
        ]

        for csv_file, model in zip(csv_files, model_list):
            print(csv_file)
            with open(csv_path + csv_file, encoding='utf-8') as file:
                if csv_file != 'users.csv':
                    reader = csv.reader(file)
                    next(reader)

                    model.objects.all().delete()

                    for row in reader:
                        print(row)
                        obg = model(*row)
                        obg.save()

                else:
                    reader = csv.DictReader(file)

                    model.objects.all().delete()

                    for row in reader:
                        print(row)
                        obg = model(
                            id=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=['last_name'],
                        )
                        obg.save()
