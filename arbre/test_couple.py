from django.test import TestCase
from arbre.models import Person
from arbre.couple import get_couples, Couple


# Create your tests here.
class CoupleTestCase(TestCase):
    fixtures = ['simpsons.json']

    def test_get_couples(self):
        everyone = Person.objects.all()
        couple_nodes, links = get_couples(everyone)
        actual_couples = set([dct['id'] for dct in couple_nodes])
        expected_couples = {'2_3', '2_5', '1_10', '11_12', '14'}
        self.assertEqual(expected_couples, actual_couples)
        self.assertEqual(links, {
            ('11_12', 13, 'child'),
            (1, '1_10', 'couple'),
            (2, '2_3', 'couple'),
            ('11_12', 10, 'child'),
            ('11_12', 14, 'child'),
            ('1_10', 6, 'child'),
            (2, '2_5', 'couple'),
            ('2_3', 1, 'child'),
            (3, '2_3', 'couple'),
            (5, '2_5', 'couple'),
            (14, 15, 'child'),
            ('1_10', 7, 'child'),
            ('1_10', 8, 'child'),
            ('2_5', 4, 'child'),
            (10, '1_10', 'couple'),
            (11, '11_12', 'couple'),
            (12, '11_12', 'couple')
        })

    def test_couple_id_2_parents(self):
        bart = Person.objects.get(first_name='Bart')
        marge = Person.objects.get(first_name='Marge')
        homer = Person.objects.get(first_name='Homer')
        parents = Couple(bart)
        expected_couple_id = "_".join(sorted(map(str, (marge.id, homer.id))))
        self.assertEqual(parents.id, expected_couple_id)

    def test_couple_id_1_parent(self):
        ling = Person.objects.get(first_name='Ling')
        selma = Person.objects.get(first_name='Selma')
        parents = Couple(ling)
        self.assertEqual(parents.id, str(selma.id))

    def test_couple_id_zero_parent(self):
        abraham = Person.objects.get(first_name='Abraham')
        parents = Couple(abraham)
        self.assertEqual(parents.id, None)
