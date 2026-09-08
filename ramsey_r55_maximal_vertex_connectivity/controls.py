#!/usr/bin/env python3
"""Small exact controls for the algebra, physical fixture and clause scope."""
import copy
import json
from itertools import combinations
from pathlib import Path

from guarded_cut import clause
from verify_core import verify


def need(ok, message):
    if not ok:
        raise ValueError(message)


def controls():
    identities = 0
    # All red graphs through order 5, with literal degree/common counts.
    for n in range(3, 6):
        edges = list(combinations(range(n), 2))
        for word in range(1 << len(edges)):
            red = [set() for _ in range(n)]
            for i, (u, v) in enumerate(edges):
                if word >> i & 1:
                    red[u].add(v)
                    red[v].add(u)
            for t in combinations(range(n), 3):
                if not all(v in red[u] for u, v in combinations(t, 2)):
                    continue
                common = set.intersection(*(red[u] for u in t))
                direct = 1 + sum(len(red[u]) for u in t) - len(common)
                contacts = [sum(v in red[u] for u in t) for v in range(n) if v not in t]
                need(direct == 2*n + 1 - 2*contacts.count(0) - contacts.count(1),
                     'triangle contact identity')
                identities += 1

    inequalities = 0
    for delta in range(18, 25):
        for k in range(delta):
            for a, cap in ((2, 13), (3, 4), (4, 0)):
                literal = a*(delta-a+1) - (a-1)*k
                bound = delta - (a-1)**2
                need(literal >= bound > cap, 'clique common-neighbor bound')
                if k == delta-1:
                    need(literal == bound, 'sharp algebra at k=delta-1')
                inequalities += 1
    # Reject an exploratory transcription error: delta-a+1 is not the
    # lower bound obtained by substituting k=delta-1 when a is 3 or 4.
    need(3*(18-3+1) - 2*17 == 14 < 18-3+1, 'wrong-formula negative control')

    # The n=10 independent-triple argument uses a real order boundary.
    # u=0,w=1 share v=2, have four neighbors each, with union of size 7.
    blue = [set() for _ in range(10)]
    for u, v in [(0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 6), (1, 7), (1, 8)]:
        blue[u].add(v)
        blue[v].add(u)
    available = set(range(10)) - blue[0] - blue[1] - {0, 1}
    need(available == {9}, 'ten-vertex boundary fixture')
    need(not (set(range(9)) - blue[0] - blue[1] - {0, 1}), 'nine-vertex boundary fixture')
    need(2 in blue[0] & blue[1] and not blue[9], 'shared blue neighbor fixture')

    here = Path(__file__).resolve().parent
    fixture = json.loads((here/'UNEXTENDABLE_CORE.json').read_text())
    mutations = []
    x = copy.deepcopy(fixture); x['n'] = 24; mutations.append(x)
    x = copy.deepcopy(fixture); x['red_hex'] = '0'*64; mutations.append(x)
    x = copy.deepcopy(fixture); x['red_hex'] = 'f'*64; mutations.append(x)
    rejected = 0
    for x in mutations:
        try:
            verify(x)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('invalid physical core accepted')

    a, b = list(range(11)), list(range(11, 24))
    for color in ('red', 'blue'):
        c = clause(a, b, color)
        need(c['separator_size'] == 19 and len(c['negated_degree_guards']) == 43,
             'global guard count')
        need(all(g['degree_at_least'] == 20 and g['color'] == color
                 for g in c['negated_degree_guards']), 'guard threshold and color')
        need({tuple(x['pair']) for x in c['physical_edge_literals']} ==
             {(u, v) for u in a for v in b}, 'physical cut coverage')
        need(all(x['red_value'] == (color == 'red') for x in c['physical_edge_literals']),
             'physical literal polarity')
    bad_cuts = [([0], [0], 'red'), ([1, 0], b, 'red'), ([], b, 'red'),
                (a, [43], 'blue'), ([0], [1], 'red'), (a, b, 'green')]
    for args in bad_cuts:
        try:
            clause(*args)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('invalid cut scope accepted')
    return {'status': 'VERIFIED_ALGEBRA_AND_SCOPE_CONTROLS',
            'literal_triangle_identities': identities,
            'clique_degree_inequalities': inequalities,
            'exploratory_wrong_formula_rejected': True,
            'order10_boundary_fixture': True,
            'invalid_core_or_cut_inputs_rejected': rejected,
            'physical_cut_polarities_checked': 2}


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2, sort_keys=True))
