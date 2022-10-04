import json as reproduce_to_json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from api.models import Ingredient


class Command(BaseCommand):
    help = 'loading ingredients from data in json'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join('data', options['filename']), 'r',
                      encoding='utf-8') as f:
                data = reproduce_to_json.load(f)
                for ingredient in data:
                    Ingredient.objects.get_or_create(name=ingredient["name"],
                                                     measurement_unit=ingredient[
                        "measurement_unit"])
        except FileNotFoundError:
            raise CommandError('Файл отсутствует в директории data')
