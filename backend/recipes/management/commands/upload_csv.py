import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('./data/ingredients.csv', encoding='utf-8') as csvfile:
            names = ['name', 'measurement_unit']
            reader = csv.DictReader(csvfile, fieldnames=names)
            ingredients = [
                Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
                for row in reader
            ]
            Ingredient.objects.bulk_create(ingredients)
