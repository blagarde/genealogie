from arbre import couple
import itertools
import networkx as nx

from arbre.models import Person


def get_data(persons):
    person_nodes = [p.as_dict() for p in persons]
    couple_nodes, links = couple.get_couples(persons)
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
