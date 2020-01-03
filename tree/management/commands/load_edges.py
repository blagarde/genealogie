from django.core.management.base import BaseCommand, CommandError
from tree.models import Person
from django.db import connection
from csv import DictReader


class Command(BaseCommand):
    help = 'Loads data from CSV.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('--truncate', default=False, type=bool)

    def handle(self, *args, **options):
        if options['truncate']:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM `tree_person_parent`")
        with open(options['path']) as fh:
            reader = DictReader(fh)
            for row_dct in reader:
                child_id, parent_id = row_dct["child_id"], row_dct["parent_id"]
                child = Person.objects.get(id=child_id)
                parent = Person.objects.get(id=parent_id)
                child.parent.add(parent)
                child.save()
