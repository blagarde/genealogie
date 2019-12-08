from django.test import TestCase
from arbre.models import Person
from arbre.utils import get_neighbors_dct, get_partial
from ddt import ddt, data

CORE_FAMILY = "Homer Marge Bart Lisa Maggie".split(" ")
HOMERS_PARENTS = "Abraham Mona".split(" ")
MARGES_RELATIVES = "Clancy Jacqueline Patty Selma".split(" ")

TEST_CASES_1 = [
    # List of (input, expected_output, bool_direct_siblings_only)
    ("Bart", CORE_FAMILY, True),
    ("Bart", CORE_FAMILY, False),
    ("Homer", CORE_FAMILY + HOMERS_PARENTS, True),
    ("Homer", CORE_FAMILY + HOMERS_PARENTS + ["Herb"], False),  # Herb is Homer's half brother
]


TEST_CASES_2 = [
    ("Bart", 0, ["Bart"]),
    ("Bart", 1, CORE_FAMILY),
    ("Bart", 2, CORE_FAMILY + HOMERS_PARENTS + MARGES_RELATIVES),
    ("Selma", 0, ["Selma"]),
    ("Selma", 1, "Selma Ling Patty Marge Clancy Jacqueline".split(" ")),

    # Half siblings count as 2 degrees apart.
    ("Herb", 1, ["Herb", "Abraham", "Gaby"]),  # Gaby is Herb's mom, Abraham's ex-wife.
    ("Herb", 2, ["Herb", "Abraham", "Homer", "Mona", "Gaby"]),
]


@ddt
class NeighborsTestCase(TestCase):
    fixtures = ['simpsons.json']

    @data(*TEST_CASES_1)
    def test_neighbors_dct(self, case):
        first_name, expected_neighbors, direct_siblings_only = case
        neighbors_dct = get_neighbors_dct(direct_siblings_only=direct_siblings_only)
        person = Person.objects.get(first_name=first_name)
        expected_neighbors = Person.objects.filter(first_name__in=expected_neighbors)
        actual_neighbors = neighbors_dct[person.id]
        self.assertEqual(actual_neighbors, {p.id for p in expected_neighbors})

    @data(*TEST_CASES_2)
    def test_partial(self, case):
        first_name, distance, expected_neighbors = case
        person = Person.objects.get(first_name=first_name)
        expected_neighbors = Person.objects.filter(first_name__in=expected_neighbors)
        actual_neighbors = get_partial(person.id, distance)
        self.assertEqual({p.id for p in actual_neighbors}, {p.id for p in expected_neighbors})
