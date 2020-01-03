from django.core.management.base import BaseCommand, CommandError
from tree.models import Person
from csv import DictReader
import datetime
import dateutil.parser
import re


class Command(BaseCommand):
    help = 'Loads data from CSV.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('--truncate', default=False, type=bool)

    def handle(self, *args, **options):
        if options['truncate']:
            Person.objects.all().delete()
        with open(options['path']) as fh:
            reader = DictReader(fh)
            for row_dct in reader:
                for field in ('birth_date', 'death_date'):
                    date_str = row_dct[field]
                    if row_dct[field] == '':
                        del row_dct[field]
                    elif re.match(r'^\d{4}$', date_str):
                        # If only the year is available, arbitrarily set the Month/Day to January 1st and indicate uncertainty.
                        row_dct[field] = datetime.date(int(date_str), 1, 1)
                        row_dct[field + '_is_approximative'] = True
                    else:
                        row_dct[field] = dateutil.parser.parse(date_str, yearfirst=True, dayfirst=False)
                Person.objects.create(**row_dct)
        print("Person table entry count:", Person.objects.count())
