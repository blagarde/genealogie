"""Utility functions that create nodes for couples."""
import datetime


def get_couples(persons):
    """Returns lists of nodes that form a couple."""
    links, couples = set([]), {}
    for person in persons:
        couple = Couple(person)

        if not couple.id:  # Parents unknown
            continue

        couples[couple.id] = couple

        links |= set(couple.links)

    couple_nodes = [c.as_dict() for c in couples.values()]
    return couple_nodes, links


class Couple(object):
    """A class to represent a set of parents."""

    def __init__(self, child):
        self._child = child
        self._parents = self._child.parent.all()

    @property
    def id(self):
        if not self._parents:
            return None
        parent_ids = {p.id for p in self._parents}
        return "_".join(map(str, sorted(parent_ids)))

    @property
    def links(self):
        """Yield edges that link parent(s), the couple node, and the child."""
        if len(self._parents) > 1:
            # Connect parents to the couple, and the couple to the child.
            for parent in self._parents:
                yield (parent.id, self.id, "couple")
                yield (self.id, self._child.id, "child")
        elif len(self._parents) == 1:
            # Connect the parent directly to their child.
            parent = self._parents[0]
            yield (parent.id, self._child.id, "child")

    def as_dict(self):
        return {
            "id": self.id,
            # HACK: get a somewhat arbitrary date, for positioning.
            "birth_date": self._get_date(),
            "type": "couple",
        }

    def _get_date(self):
        """HACK: Arbitrarily date the couple 10 years after the youngest parent.
        This is to attempt to display the couple node to the right of the parents."""
        dates = [p.birth_date for p in self._child.parent.all() if p.birth_date is not None]
        if dates:
            return max(dates) + datetime.timedelta(10 * 365)
