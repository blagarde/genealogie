from django.core.management.base import BaseCommand, CommandError
from tree.models import Person, Relationship
from tree.django_utils import get_or_none
from csv import DictReader
import datetime
import dateutil.parser
import re
import collections
from django.db import transaction
import logging


FIELDS = 'first_name middle_name last_name birth_date birth_place death_date death_place gender comments'.split(' ')

class Command(BaseCommand):
    help = 'Loads data from CSV.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('--truncate', default=False, type=bool)

    @transaction.atomic
    def handle(self, *args, **options):
        if options['truncate']:
            Person.objects.all().delete()
            Relationship.objects.all().delete()
        with open(options['path']) as fh:
            rows = list(DictReader(open(options['path'])))
            persons_dct = dict(self.load_persons(rows))
            self.load_edges(persons_dct, rows)
        print("Person table entry count:", Person.objects.count())
        self.add_relationships()
        print("Relationship table entry count:", Relationship.objects.count())

    def load_persons(self, rows):
        for row_dct in rows:
            for field in ('birth_date', 'death_date'):
                row_dct[field + '_is_approximative'], row_dct[field] = self.parse_date(row_dct[field])
            person = self.load_one(row_dct)
            yield row_dct['id'], person

    def load_one(self, row_dct):
        """Load one person if it doesn't already exist, else create it. Return it either way."""
        first_name, last_name, birth_date = row_dct['first_name'], row_dct['last_name'], row_dct['birth_date']
        person = get_or_none(Person, first_name=first_name, last_name=last_name, birth_date=birth_date)
        if person:
            for f in FIELDS:
                old, new = getattr(person, f), row_dct[f]
                if old != new:
                    fmt = "Field '{f}' differs for: {p}. Old: {o}\t New: {n}"
                    logging.warning(fmt.format(f=f, p=person, o=old, n=new))
                    setattr(person, f, old or new)  # TODO: write fancier logic for merging entries.
            person.save()
        else:
            dct = {f: row_dct[f] for f in FIELDS}
            person = Person.objects.create(**dct)
        return person

    def load_edges(self, persons_dct, rows):
        for row_dct in rows:
            child_id, father_id, mother_id = row_dct['id'], row_dct['father_id'], row_dct['mother_id']
            child = persons_dct[child_id]
            if father_id:
                father = persons_dct[father_id]
                child.parent.add(father.id)
            if mother_id:
                mother = persons_dct[mother_id]
                child.parent.add(mother.id)
            child.save()

    def add_relationships(self):
        for p in Person.objects.all():
            parents = p.parent.all()
            if parents.count() >= 2:
                queryset = Relationship.objects.filter()
                for p in parents:
                    # Narrow down the queryset to a Relationship entry that references all parents.
                    queryset = queryset.filter(person=p.id)
                if queryset.count() == 0:
                # Create a Relationship entry for this set of parents if it doesn't exist.
                    relationship = Relationship.objects.create()
                    relationship.person.add(*[p.id for p in parents])
                    relationship.save()

    @staticmethod
    def parse_date(date_str):
        if date_str == '':
            return False, None
        if re.match(r'^\d{4}$', date_str):
            # If only the year is available, arbitrarily set the Month/Day to January 1st and indicate uncertainty.
            return True, datetime.date(int(date_str), 1, 1)
        return False, dateutil.parser.parse(date_str, yearfirst=True, dayfirst=False).date()
