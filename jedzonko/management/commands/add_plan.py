from django.core.management import BaseCommand
from random import randint
from jedzonko.models import *
from faker import Faker
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = 'Tekst pomocy'

    def handle(self, *args, **options):
        fake = Faker()
        for i in range(1, 20):
            plan = Plan()
            plan.name = f"Plan {fake.name()}"
            plan.description = fake.text()
            timezone = pytz.timezone("America/Los_Angeles")
            fakeDate = fake.past_datetime(start_date='-1000d', tzinfo=timezone)
            plan.created = fakeDate
            plan.save()
