#!/usr/bin/env python3
"""Primary clauses for the color of the first two empty fixed signatures."""
from itertools import combinations

CASES = ((11, 'blue'), (11, 'red'), (13, 'blue'), (13, 'red'))
CORE_WORDS = {11: '100110110', 13: '110110101'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return 166+list(combinations(range(33, 43), 2)).index(tuple(sorted((a, b))))


def link(i, v):
    return 211+11*(v-33)+i


def tail(color):
    require(color in ('red', 'blue'), 'pair color')
    if color == 'red':
        return [(edge(33, 34),)]
    rows = [(-edge(33, 34),)]
    # A blue moving triangle cannot be blue to both ends of a blue edge.
    rows += [(link(i, 33), link(i, 34)) for i in range(3, 11)]
    # A common blue fixed neighbor must be red to at least two minorities.
    rows += [(edge(33, v), edge(34, v), link(i, v), link(j, v))
             for v in range(35, 43) for i, j in combinations(range(3), 2)]
    # The common blue fixed neighborhood has size at most two.
    rows += [tuple(edge(u, v) for v in fixed for u in (33, 34))
             for fixed in combinations(range(35, 43), 3)]
    # Two such common neighbors cannot both miss the same minority.
    rows += [(edge(33, v), edge(34, v), edge(33, w), edge(34, w), link(i, v), link(i, w))
             for v, w in combinations(range(35, 43), 2) for i in range(3)]
    rows = sorted(set(tuple(sorted(c)) for c in rows), key=lambda c: (len(c), c))
    require(len(rows) == 173, 'blue tail size')
    return rows


def fixture(core):
    """Thirteen vertices, blue empty pair 9,10 and two common blue neighbors."""
    words = CORE_WORDS[core]
    signatures = (0, 0, 3, 5)
    red = []
    for a, b in combinations(range(13), 2):
        if b < 9:
            i, s = divmod(a, 3)
            j, t = divmod(b, 3)
            bit = i == j or words[3*[(0, 1), (0, 2), (1, 2)].index((i, j))+(t-s) % 3] == '1'
        elif a < 9:
            bit = bool(signatures[b-9] & (1 << (a//3)))
        else:
            bit = False
        if bit:
            red.append((a, b))
    return '13 '+str(len(red))+'\n'+''.join(f'{a} {b}\n' for a, b in red)


def name(core, color):
    require((core, color) in CASES, 'case')
    return f'c{core}_{color}'
