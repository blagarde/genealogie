import collections
from datetime import datetime

from django.core.management.base import BaseCommand
from tree.models import Person


class Command(BaseCommand):
    help = 'Dump data in GEDCOM format to stdout.'

    def handle(self, *args, **options):
        persons = Person.objects.all()
        gedcom = GedCom(persons)
        gedcom.print()


def _unique_families(persons):
    '''Yield unique Family() instances.'''
    seen = set()
    i = 0
    for p in persons:
        parents, siblings = p.parents, p.siblings
        family = list(parents) + list(siblings)
        family_id = frozenset([p.id for p in family])
        # Yield a family entry only if at least one parent is known.
        if parents and family_id not in seen:
            yield Family(i, parents, siblings)
            i += 1
        seen |= {family_id}


class GedCom(object):
    def __init__(self, persons):
        self._persons = persons
        self.families = list(_unique_families(persons))

        # `famc_dct` and `fams_dct` are dictionaries like `{person_id: set(family_id)}`
        # "famc" is a family in which a person is a child.
        # "fams" is a family in which a person is a spouse.
        self.famc_dct = collections.defaultdict(set)
        self.fams_dct = collections.defaultdict(set)

        for family in self.families:
            for child in family.children:
                self.famc_dct[child.id] |= {family.id}
            for spouse in family.parents:
                self.fams_dct[spouse.id] |= {family.id}

    @property
    def lines(self):
        yield from self.header
        yield from self.body
        yield from self.footer

    @property
    def body(self):
        for p in self._persons:
            yield from self._person_details(p)
        for f in self.families:
            yield from f.get_gedcom_lines

    def _person_details(self, person):
        p = GedComPerson(person)
        yield from p.gedcom_str
        yield from self._family_rows(p)

    def _family_rows(self, person):
        for f in self.famc_dct[person.id]:
            yield f"1 FAMC @F{f}@"
        for f in self.fams_dct[person.id]:
            yield f"1 FAMS @F{f}@"

    @property
    def header(self):
        yield "0 HEAD"
        yield "1 GEDC"
        yield "2 VERS 5.5.5"
        yield "2 FORM LINEAGE-LINKED"
        yield "3 VERS 5.5.5"
        yield "1 CHAR UTF-8"
        # Source
        yield "1 SOUR baptiste_lagarde"
        # Submitter (`@I1@` is Baptiste Lagarde)
        yield "0 @I1@ SUBM"
        yield "1 NAME Baptiste Lagarde"
    
    @property
    def footer(self):
        yield "0 TRLR"

    def print(self):
        for line in self.lines:
            print(line)


class GedComPerson(object):
    def __init__(self, person):
        self._person = person
        self.id = person.id
        
    @property
    def full_name(self):
        '''Full name, formatted like: `First Middle /Last/`.

        This is apparently how GedCOM is formatted, don't ask questions.
        '''
        p = self._person
        return f"{p.given_names} /{p.last_name}/"
    
    @property    
    def gedcom_str(self):
        p = self._person
        yield f"0 @I{p.id}@ INDI"
        yield f"1 NAME {self.full_name}"
        yield f"2 SURN {p.last_name}"
        yield f"2 GIVN {p.given_names}"
        yield f"1 SEX {p.gender}"
        if p.birth_date:
            dob_str = str.upper(datetime.strftime(p.birth_date, "%d %b %Y"))
            yield "1 BIRT"
            yield f"2 DATE {dob_str}"


class Family(object):
    def __init__(self, family_id, parents, children):
        '''`family_id` is just an int; `parents` and `children` are Django querysets.'''
        self.id = family_id
        self.parents, self.children = parents, children

    @property
    def get_gedcom_lines(self):
        yield f"0 @F{self.id}@ FAM"
        for husb in self.parents.filter(gender='M'):
            yield f"1 HUSB @I{husb.id}@"
        for wife in self.parents.filter(gender='F'):
            yield f"1 WIFE @I{wife.id}@"
        for c in self.children:
            yield f"1 CHIL @I{c.id}@"
