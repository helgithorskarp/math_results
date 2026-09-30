"""Exact six-word minimum DFA and additional witnessed union capacities.

Author: six-sorting-2, researcher. No unary events are front-loaded.
"""
from sequential_sat import neg

POSITIONS = ((0, 1, 5), (0, 1, 2), (0, 1, 3), (0, 1, 4),
             (0, 1, 5), (0, 1, 0), (0, 0, 0))
FIRST = {(2, 5): 1, (3, 5): 2, (4, 5): 3,
         (5, 6): 4, (5, 7): 4, (5, 8): 4}
ADVANCE = {1: (0, 2), 2: (0, 3), 3: (0, 4), 4: (0, 5), 5: (0, 1)}


def destination(state, pair):
    if not any(p in pair for p in POSITIONS[state]):
        return state
    if state == 0:
        return FIRST.get(pair)
    if state in ADVANCE and pair == ADVANCE[state]:
        return 6 if state == 5 else 5
    return None


def minimum_dfa(w, choices, pairs, gates):
    phase = [[w.var() for _ in POSITIONS] for _ in range(gates + 1)]
    for row in phase:
        w.exactly_one(row)
    w.add(phase[0][0])
    w.add(phase[-1][6])
    for t in range(gates):
        for state in range(len(POSITIONS)):
            for j, pair in enumerate(pairs):
                dest = destination(state, pair)
                if dest is None:
                    w.add(-phase[t][state], -choices[t][j])
                else:
                    w.add(-phase[t][state], -choices[t][j], phase[t + 1][dest])
    return phase


def extra_bounds(w, choices, pairs, bits, records, gates):
    for r in records:
        x, y = r['x'], r['y']
        hits = [w.var() for _ in range(gates)]
        for t in range(gates):
            for j, (a, b) in enumerate(pairs):
                c = choices[t][j]
                outside = (bits[x][t][a], bits[x][t][b],
                           neg(bits[y][t][a]), neg(bits[y][t][b]))
                for literal in outside:
                    w.add(-c, neg(literal), hits[t])
                w.add(-c, -hits[t], *outside)
        w.at_most(hits, r['cap'] + gates - 18)
