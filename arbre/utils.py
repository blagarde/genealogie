import time
import statistics
import datetime
from arbre.models import Person
from django.db import connection


def get_data(persons):
    person_nodes = [p.as_dict() for p in persons]
    couple_nodes, links = get_couples(persons)
    return {
        "nodes": person_nodes + couple_nodes,
        "links": [{'source': x, 'target': y, 'type': z} for x, y, z in links]
    }


def get_neighbors(person_ids):
    """Get the IDs of parents, children, other parents of children, and siblings.

    From this stackoverflow entry (Not using collections):
    https://stackoverflow.com/questions/19807987/sql-compare-two-sets"""
    all_parents = Person.objects.filter(children__in=person_ids)
    all_children = Person.objects.filter(parent__in=person_ids)
    all_spouses = Person.objects.filter(children__parent__in=person_ids)
    result = all_parents.union(all_children).union(all_spouses)
    result = {person.id for person in result}
    with connection.cursor() as cursor:
        for person_id in person_ids:
            # This complicated query retrieves the persons who share
            # the same set of parents as `persons_id`.)
            query = """
            WITH edges AS (
                SELECT DISTINCT
                     from_person_id,
                     to_person_id
                FROM   arbre_person_parent
                WHERE  from_person_id = {person_id}
            )
            SELECT edges1.from_person_id
            FROM   arbre_person_parent edges1
                INNER JOIN
                edges
                ON (edges1.to_person_id = edges.to_person_id)
            GROUP BY edges1.from_person_id
            HAVING COUNT( DISTINCT edges1.to_person_id ) = ( SELECT COUNT(1) FROM edges );
            """.format(person_id=person_id)

            cursor.execute(query)
            result |= {row[0] for row in cursor.fetchall()}
    return result


def get_couples(persons):
    """Returns lists of nodes that form a couple."""
    links, couples = set([]), {}
    for person in persons:
        couple = Couple(person, persons)

        couples[couple.id] = couple

        if couple.id is None:
            continue

        if len(couple) > 1:
            # Connect parents to the couple, and the couple to the child.
            for parent in couple.values():
                links |= set([(parent.id, couple.id, "couple"), (couple.id, person.id, "child")])
        elif len(couple) == 1:   
            # Connect the parent directly to their child.
            links |= set([(couple.id, person.id, "child")])

    couple_nodes = [c.as_dict() for c in couples.values()]
    return couple_nodes, links


class Couple(dict):

    def __init__(self, child, persons):
        self._child = child
        for parent in child.parent.filter(id__in=persons):
            self[parent.id] = parent

    @property
    def id(self):
        keys = self.keys()
        return "_".join(map(str, sorted(keys)))

    def as_dict(self):
        return {
            "id": self.id,
            # HACK: position the couple node between the members of the couple
            "birth_date": self._get_date(),
            "type": "couple",
        }

    def _get_date(self):
        persons = self.values()
        ref_date = datetime.date(1900, 1, 1)
        time_deltas = [(p.birth_date - ref_date).total_seconds() for p in persons if p.birth_date is not None]
        if len(time_deltas) > 0:
            avg_delta = statistics.mean(time_deltas)
            return ref_date + datetime.timedelta(0, avg_delta)

