from django.test import TestCase
from arbre.models import Person
from arbre.utils import get_neighbors_dct, get_partial, get_descendants, get_ancestors
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


TEST_DESCENDANTS = [
    ("Homer", 0, ["Homer"]),
    ("Homer", 1, ["Homer", "Bart", "Lisa", "Maggie"]),
    ("Homer", 2, ["Homer", "Bart", "Lisa", "Maggie"]),
    ("Mona", 0, ["Mona"]),
    ("Mona", 1, ["Mona", "Homer"]),
    ("Mona", 2, ["Mona", "Homer", "Bart", "Lisa", "Maggie"]),
    ("Abraham", 0, ["Abraham"]),
    ("Abraham", 1, ["Abraham", "Homer", "Herb"]),
    ("Abraham", 2, ["Abraham", "Homer", "Herb", "Bart", "Lisa", "Maggie"]),
]


TEST_ANCESTORS = [
    ("Maggie", 0, ["Maggie"]),
    ("Maggie", 1, ["Maggie", "Homer", "Marge"]),
    ("Maggie", 2, ["Maggie", "Homer", "Marge", "Abraham", "Mona", "Clancy", "Jacqueline"]),
    ("Homer", 0, ["Homer"]),
    ("Homer", 1, ["Homer", "Abraham", "Mona"]),
    ("Homer", 2, ["Homer", "Abraham", "Mona"]),  # Homer's grandparents are unknown.
    ("Herb", 1, ["Herb", "Abraham", "Gaby"]),
    ("Ling", 0, ["Ling"]),
    ("Ling", 1, ["Ling", "Selma"]),
    ("Ling", 2, ["Ling", "Selma", "Clancy", "Jacqueline"]),
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


@ddt
class DescendantsTestCase(TestCase):
    fixtures = ['simpsons.json']

    @data(*TEST_DESCENDANTS)
    def test_descendants(self, case):
        ancestor_name, distance, descendant_names = case
        ancestor = Person.objects.get(first_name=ancestor_name)
        expected_descendants = Person.objects.filter(first_name__in=descendant_names)
        actual_descendants = get_descendants(ancestor.id, distance)
        self.assertEqual({p["id"] for p in actual_descendants["nodes"]}, {p.id for p in expected_descendants})


@ddt
class AncestorsTestCase(TestCase):
    fixtures = ['simpsons.json']

    @data(*TEST_ANCESTORS)
    def test_ancestors(self, case):
        descendant_name, distance, ancestor_names = case
        descendant = Person.objects.get(first_name=descendant_name)
        expected_ancestors = Person.objects.filter(first_name__in=ancestor_names)
        actual_ancestors = get_ancestors(descendant.id, distance)
        self.assertEqual({p["id"] for p in actual_ancestors["nodes"]}, {p.id for p in expected_ancestors})
