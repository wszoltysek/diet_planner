from django.core.management import BaseCommand
from random import randint
from jedzonko.models import *
from faker import Faker
from datetime import datetime


class Command(BaseCommand):
    help = 'Tekst pomocy'

    def handle(self, *args, **options):
        fake = Faker()
        for i in range(1, 100):
            recipe = Recipe()
            recipe.name = f"Przepis {fake.name()}"
            recipe.ingredients = fake.sentences(nb=1)[0]
            recipe.description = fake.text()
            recipe.created = fake.date_time()
            recipe.updated = datetime.now()
            recipe.preparation_time = randint(5, 60)
            recipe.votes = randint(0, 200)
            recipe.save()
