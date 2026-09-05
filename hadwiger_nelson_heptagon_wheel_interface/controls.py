"""Exhaust graph/model equivalence on sixteen small wheel interfaces."""
from itertools import product
import json
from interface import encode, lift_colouring, satisfies

cycle_edges = [(i, i+1) for i in range(1, 6)] + [(1, 6)]
star_edges = [(0, i) for i in range(1, 7)]
boundaries = [([], []), ([1], []), ([1, 2], []), ([1, 3], []),
              ([1, 4], []), ([1, 3], [2, 4]),
              ([1, 2, 3], [4, 5, 6]), ([1, 3, 5], [2, 4, 6])]
states = [row for row in product([1, 2, 3], repeat=6)
          if all(row[i] != row[(i+1) % 6] for i in range(6))]
checked = accepted = impossible_interfaces = 0
for boundary in boundaries:
    for outside_edge in [False, True]:
        edges = star_edges + cycle_edges + [(v, 7) for v in boundary[0]] + [(v, 8) for v in boundary[1]]
        if outside_edge:
            edges += [(7, 8)]
        edges.sort()
        for target in [None, [1, 3], [1, 2]]:
            instance = encode(9, edges, 0, target)
            if target == [1, 2]:
                assert instance['options'] == [[]] and [] in instance['clauses']
                impossible_interfaces += 1
            for row in states:
                for u, v in product(range(4), repeat=2):
                    colours = [0]+list(row)+[u, v]
                    good = all(colours[a] != colours[b] for a, b in edges)
                    good = good and (target is None or colours[target[0]] == colours[target[1]])
                    true = lift_colouring(instance, colours)
                    encoded = true is not None and satisfies(instance['clauses'], true)
                    assert good == encoded
                    checked += 1
                    accepted += good
print(json.dumps({'status': 'ALL SMALL INTERFACE CONTROLS PASSED',
                  'graphs': 16, 'graph_target_interfaces': 48,
                  'explicit_colouring_cases': checked, 'accepted_cases': accepted,
                  'empty_state_interfaces_checked': impossible_interfaces}, indent=2))
