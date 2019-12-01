import time
import statistics
import datetime
from arbre.models import Person
import collections
import itertools
import networkx as nx


def get_data(persons):
    person_nodes = [p.as_dict() for p in persons]
    couple_nodes, links = get_couples(persons)
    return {
        "nodes": person_nodes + couple_nodes,
        "links": [{'source': x, 'target': y, 'type': z} for x, y, z in links]
    }


def get_neighbors(neighbors_dct, person_ids):
    """Get the IDs of parents, children, other parents of children, and siblings."""
    return set(itertools.chain(*[v_set for k, v_set in neighbors_dct.items() if k in person_ids]))


def get_neighbors_dct(direct_siblings_only=True):
    """Build a dictionary like: `{person_id: set([neighbor_id])}`.

    A neighbor is a parent, child, sibling, or the other parent of a child.
    Direct siblings are those who share the same set of parents."""
    G = nx.DiGraph()
    for person in Person.objects.all():
        edges = [(person.id, parent_id) for parent_id in person.parent.values_list('id', flat=True)]
        G.add_edges_from(edges)
    neighbors_dct = {p: set(G.neighbors(p)) for p in G.nodes()}

    for person in G.nodes():
        parents = frozenset(G.successors(person))

        # Loop over parents to add a couple of connections.
        for p, q in itertools.product(parents, parents):
            neighbors_dct[p] |= set([person])  # Children are neighbors of their parents.
            if p != q:
                # Consider parents direct neighbors, despite being separated by 2 edges.
                neighbors_dct[p] |= set([q])

        # Add siblings.
        if len(parents) == 0:
            continue  # Parents unknown => doesn't have siblings.
        all_siblings = set(itertools.chain(*[list(G.predecessors(parent)) for parent in parents]))
        direct_siblings = set([s for s in all_siblings if frozenset(G.successors(s)) == parents])
        neighbors_dct[person] |= direct_siblings if direct_siblings_only else all_siblings

    return neighbors_dct


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

