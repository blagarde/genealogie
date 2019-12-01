import time
import statistics
import datetime


def get_data(persons):
    person_nodes = [p.as_dict() for p in persons]
    couple_nodes, links = get_couples(persons)
    return {
        "nodes": person_nodes + couple_nodes,
        "links": [{'source': x, 'target': y, 'type': z} for x, y, z in links]
    }


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
        if len(self) > 1:
            keys = self.keys()
            return "_".join(map(str, sorted(keys)))
        elif len(self) == 1:
            return self.keys()[0]

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
