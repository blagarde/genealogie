"""Utility functions that create nodes for couples."""
import datetime
from collections import namedtuple, defaultdict
from itertools import chain
from arbre.models import Person


Link = namedtuple("Link", field_names="source target type")


def get_couples(persons):
    """Returns lists of nodes that form a couple and internal family links."""
    families = defaultdict(set)
    for child in persons:
        parents = frozenset([p.id for p in child.parent.all()])

        if not parents:  # Parents unknown
            continue

        families[parents] |= set([child])

    families = {Family(parent_ids, children) for parent_ids, children in families.items()}
    for f in families:
        f.filter(persons)
    families = {f for f in families if f.couple_id is not None}

    links = chain(*[list(f.links) for f in families])
    couple_nodes = [f.couple_dict() for f in families]
    return couple_nodes, set(links)


class Family(object):
    """A class that contains a set of parents and their children."""

    def __init__(self, parent_ids, children):
        self.children = children
        self.parents = set(Person.objects.filter(id__in=parent_ids))

    @property
    def couple_id(self):
        return make_couple_id(self.parents)

    @property
    def links(self):
        """Yield edges that link parent(s), the couple node, and the child."""
        if len(self.parents) > 1:
            # Connect parents to the couple, and the couple to the child.
            for parent in self.parents:
                yield Link(parent.id, self.couple_id, "couple")
        # If there's a single parent, connect them directly to their children.
        source = self.parents[0].id if len(self.parents) == 1 else self.couple_id
        for child in self.children:
            yield Link(source, child.id, "child")

    def filter(self, persons):
        person_ids = [p.id for p in persons]
        self.parents = [p for p in self.parents if p.id in person_ids]
        self.children = [c for c in self.children if c.id in person_ids]

    def couple_dict(self):
        return {
            "id": self.couple_id,
            # HACK: get a somewhat arbitrary date, for positioning.
            "birth_date": self._get_date(),
            "type": "couple",
        }

    def _get_date(self):
        """HACK: Arbitrarily date the couple 10 years after the youngest parent.
        This is to attempt to display the couple node to the right of the parents."""
        dates = [p.birth_date for p in self.parents if p.birth_date is not None]
        if dates:
            return max(dates) + datetime.timedelta(10 * 365)

    def __repr__(self):
        parents = "|".join([p.first_name for p in self.parents])
        children = "|".join([c.first_name for c in self.children])
        return "({parents}):({children})".format(parents=parents, children=children)


def make_couple_id(persons):
    if len(persons) > 1:
        ids = {p.id for p in persons}
        return "_".join(map(str, sorted(ids)))
    elif len(persons) == 1:
        return list(persons)[0].id
