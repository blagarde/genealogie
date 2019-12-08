from django.test import TestCase
from arbre.models import Person
from arbre.utils import get_neighbors_dct
from ddt import ddt, data

CORE_FAMILY = "Homer Marge Bart Lisa Maggie".split(" ")
HOMERS_PARENTS = "Abraham Mona".split(" ")

TEST_CASES = [
    # List of (input, expected_output, bool_direct_siblings_only)
    ("Bart", CORE_FAMILY, True),
    ("Bart", CORE_FAMILY, False),
    ("Homer", CORE_FAMILY + HOMERS_PARENTS, True),
    ("Homer", CORE_FAMILY + HOMERS_PARENTS + ["Herb"], False),  # Herb is Homer's half brother
]


@ddt
class NeighborsTestCase(TestCase):
    fixtures = ['simpsons.json']

    @data(*TEST_CASES)
    def test_neighbors_dct(self, case):
        first_name, expected_neighbors, direct_siblings_only = case
        neighbors_dct = get_neighbors_dct(direct_siblings_only=direct_siblings_only)
        person = Person.objects.get(first_name=first_name)
        expected_neighbors = Person.objects.filter(first_name__in=expected_neighbors)
        actual_neighbors = neighbors_dct[person.id]
        self.assertEqual(actual_neighbors, {p.id for p in expected_neighbors})
