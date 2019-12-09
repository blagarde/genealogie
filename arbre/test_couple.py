from django.test import TestCase
from arbre.models import Person
from arbre.couple import get_couples, Family, Link
from ddt import ddt, data
from arbre.utils import get_partial


PARENTS = frozenset(["Homer", "Marge"])
CHILDREN = {"Bart", "Lisa", "Maggie"}
CORE_FAMILY = PARENTS.union(CHILDREN)
CORE_LINKS = {
   Link(1, "1_10", "couple"),  # Homer -> (Homer|Marge)
   Link(10, "1_10", "couple"),  # Homer -> (Homer|Marge)
   Link("1_10", 6, "child"),  # (Homer|Marge) -> Bart
   Link("1_10", 7, "child"),  # (Homer|Marge) -> Lisa
   Link("1_10", 8, "child"),  # (Homer|Marge) -> Maggie
}
HOMER_LINKS = {
    Link(2, "2_3", "couple"),  # Abraham -> (Abraham|Mona)
    Link(3, "2_3", "couple"),  # Mona -> (Abraham|Mona)
    Link("2_3", 1, "child"),  # (Abraham|Mona) -> Homer
}
MARGE_LINKS = {
    Link(11, "11_12", "couple"),  # Clancy -> (Clancy|Jacqueline)
    Link(12, "11_12", "couple"),  # Jacqueline -> (Clancy|Jacqueline)
    Link("11_12", 10, "child"),  # (Clancy|Jacqueline) -> Marge
    Link("11_12", 13, "child"),  # (Clancy|Jacqueline) -> Patty
    Link("11_12", 14, "child"),  # (Clancy|Jacqueline) -> Selma
}
TEST_CASES = [
    ("Bart", 0, set(), set()),
    ("Bart", 1, {PARENTS}, CORE_LINKS),
    ("Bart", 2, {
        frozenset(("Homer", "Marge")),
        frozenset(("Abraham", "Mona")),
        frozenset(("Clancy", "Jacqueline")),
    }, CORE_LINKS | HOMER_LINKS | MARGE_LINKS),
]


def couple_id_to_name_set(couple_id):
    """Helper function that returns a set consisting of the first names of the couple members."""
    ids = [i for i in couple_id.split("_")]
    return frozenset([p.first_name for p in Person.objects.filter(id__in=ids)])


@ddt
class GetCouplesTestCase(TestCase):
    fixtures = ['simpsons.json']

    @data(*TEST_CASES)
    def test_get_couples(self, case):
        first_name, distance, expected_couples, expected_links = case

        # Get the actual couple nodes and links
        person = Person.objects.get(first_name=first_name)
        persons = get_partial(person.id, distance)
        couple_nodes, actual_links = get_couples(persons)

        actual_couples = {couple_id_to_name_set(dct['id']) for dct in couple_nodes}

        self.assertEqual(actual_couples, expected_couples)
        self.assertEqual(actual_links, expected_links)

    def test_get_couples_single_parent(self):
        # If the filter set supplied contains only Bart and Homer, return only this link:
        # Homer -> Bart
        # * not *
        # Homer -> (couple) -> Bart
        homer = Person.objects.get(first_name="Homer")
        bart = Person.objects.get(first_name="Bart")
        homer_and_bart = Person.objects.filter(first_name__in=["Homer", "Bart"])
        expected_links = {(homer.id, bart.id, "child")}

        couple_nodes, actual_links = get_couples(homer_and_bart)
        self.assertEqual(actual_links, expected_links)


class CoupleIdTestCase(TestCase):

    fixtures = ['simpsons.json']

    def test_couple_id_2_parents(self):
        bart = Person.objects.get(first_name='Bart')
        parent_ids = {1, 10}
        family = Family(parent_ids, {bart})
        self.assertEqual(family.couple_id, "1_10")

    def test_couple_id_1_parent(self):
        ling = Person.objects.get(first_name='Ling')
        parent_ids = {14}  # Selma
        family = Family(parent_ids, {ling})
        self.assertEqual(family.couple_id, 14)

    def test_couple_id_zero_parent(self):
        abraham = Person.objects.get(first_name='Abraham')
        family = Family({}, {abraham})
        self.assertEqual(family.couple_id, None)
