"""Self-color partitions without numeric color names, for rooted hex covers.

An unordered port pair has one equality variable. Three transitivity clauses
per triple make its positive graph a disjoint union of cliques. Conditional
original-port contacts use these variables and opposite ternary states.
No topology constraint is imposed: a satisfying assignment is only a cover.
"""
from itertools import combinations

import color_state as cs
import hex_domain as hd


def partition_variables(circuit, n):
    """Exactly the equivalence relations on n ports, including singleton blocks."""
    if type(n) is not int or n < 1:
        raise ValueError('positive number of ports required')
    pairs = {(i, j): circuit.new() for i, j in combinations(range(n), 2)}
    for i, j, k in combinations(range(n), 3):
        a, b, c = pairs[i, j], pairs[i, k], pairs[j, k]
        circuit.clause([-a, -b, c])
        circuit.clause([-a, -c, b])
        circuit.clause([-b, -c, a])
    return pairs


def equality_literal(circuit, pairs, i, j):
    return circuit.true if i == j else pairs[min(i, j), max(i, j)]


def decode_partition(pairs, n, positive):
    """Reject an invalid equality graph; name each clique by its first port."""
    graph = [set([i]) for i in range(n)]
    for (i, j), literal in pairs.items():
        if literal in positive:
            graph[i].add(j); graph[j].add(i)
    labels = [1 + min(row) for row in graph]
    for i in range(n):
        for j in range(n):
            if (labels[i] == labels[j]) != (j in graph[i]):
                raise ValueError('not an equivalence relation')
    return labels


def compatibility_literals(circuit, pairs, signs):
    """Port equality and opposite states; includes self-contact forcing state0."""
    result = {}
    for i in range(len(signs)):
        pi, mi = signs[i]
        result[i, i] = circuit.and_([-pi, -mi])
        for j in range(i + 1, len(signs)):
            pj, mj = signs[j]
            result[i, j] = circuit.and_([pairs[i, j],
                -circuit.xor(pi, mj), -circuit.xor(mi, pj)])
    return result


def contact_inventory(tile, candidates, incidences):
    """ALL boundary contacts between disjoint candidate footprints and root.

    Indices are 0 for the root and 1..len(candidates). Internal shared edges
    have already been removed by the oriented boundary extractor. Overlapping
    pairs cannot both be active under the full-cell at-most-one constraints.
    """
    if len(incidences) != 1 + len(candidates):
        raise ValueError('one incidence row per copy including root required')
    cells = [set(map(tuple, tile))] + [set(c['cells']) for c in candidates]
    edges = {}
    for index, (_, ports) in enumerate(incidences):
        for port, (edge, side) in enumerate(ports):
            edges.setdefault(edge, [[], []])[side].append((index, port))
    contacts, excluded = set(), set()
    for sides in edges.values():
        for x, i in sides[0]:
            for y, j in sides[1]:
                if x == y:
                    raise ValueError('boundary edge occurs on both sides of one copy')
                if x > y:
                    a, b, p, q = y, x, j, i
                else:
                    a, b, p, q = x, y, i, j
                if cells[a] & cells[b]:
                    excluded.add((a, b)); continue
                contacts.add((a, b, min(p, q), max(p, q)))
    return sorted(contacts), len(excluded)


def build_cover(tile, radius, Circuit, states=None):
    """Complete rooted-cover synthesis over all self-colors and ternary states."""
    tile = tuple(map(tuple, tile))
    n = len(hd.boundary(tile))
    cs.validate_labels(tile, [1] * n, states if states is not None else [0] * n)
    circuit, candidates, incidences, stats = cs.cover_geometry(tile, radius, Circuit)
    pairs = partition_variables(circuit, n)
    if states is None:
        signs = [(circuit.new(), circuit.new()) for _ in range(n)]
        for p, m in signs:
            circuit.clause([-p, -m])
    else:
        signs = [(circuit.true if s == 1 else circuit.false,
                  circuit.true if s == -1 else circuit.false) for s in states]
    compatibility = compatibility_literals(circuit, pairs, signs)
    contacts, excluded = contact_inventory(tile, candidates, incidences)
    for a, b, i, j in contacts:
        circuit.clause([-incidences[a][0], -incidences[b][0], compatibility[i, j]])
    stats.update(mode='equivalence_state_cover', equality_variables=len(pairs),
                 contacts=len(contacts), overlapping_contact_pairs_omitted=excluded,
                 variables=circuit.nv, clauses=len(circuit.clauses),
                 state_mode='all ternary states' if states is None else 'fixed states')
    return circuit, candidates, pairs, signs, compatibility, stats


def exclude_motif(circuit, compatibility, port_pairs):
    """A finite marking must violate at least one checked periodic contact."""
    circuit.clause([-compatibility[min(i, j), max(i, j)] for i, j in port_pairs])


def decode_cover(tile, radius, candidates, pairs, signs, positive):
    labels = decode_partition(pairs, len(signs), positive)
    states = [1 if p in positive else -1 if m in positive else 0 for p, m in signs]
    patch = [{'level': 0, 'reflect': False, 'turns': 0, 'translation': [0, 0]}]
    patch.extend({'level': 1, 'reflect': False, 'turns': c['turns'],
                  'translation': list(c['translation'])} for c in candidates
                 if c['active'] in positive)
    witness = {'mode': 'rooted_cover', 'grid': 'hex', 'tile': tile, 'colors': labels,
               'signs': states, 'radius': radius, 'patch': patch}
    cs.check_cover(witness)
    return witness
