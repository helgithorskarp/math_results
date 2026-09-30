"""Exact actual-image gate activity; six-sorting-2, researcher.

Necessity for K18 follows by deleting an inactive actual gate from its
35-comparator generalized eleven-input sorter and untangling the result.
This is not inferred merely from activity in a fixed normalized frame.
"""


def neg(literal):
    return not literal if isinstance(literal, bool) else -literal


def encode(w, choices, pairs, bits, states, gates, require_every=True):
    swaps = []
    for t in range(gates):
        row = []
        for state in states:
            flag = w.var()
            row.append(flag)
            for j, (a, b) in enumerate(pairs):
                selected = choices[t][j]
                xa, xb = bits[state][t][a], bits[state][t][b]
                w.add(-selected, -flag, xa)
                w.add(-selected, -flag, neg(xb))
                w.add(-selected, flag, neg(xa), xb)
        if require_every:
            w.add(*row)
        swaps.append(row)
    return swaps
