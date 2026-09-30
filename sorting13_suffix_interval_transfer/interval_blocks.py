"""Exact suffix interval-partition recurrence; six-sorting-2, researcher.

This implements a PUBLISHED necessary condition, not a new theorem:
Codish et al.1507.01428, Theorem2 and the following consequence. Every
suffix component of a nonredundant sorting network is an interval. A
backward comparator therefore removes zero or one existing interval cuts.
Applicability to the actual K18 suffix is proved in PROOF.md by
untangling at the imported eleven-input lower bound35.
"""
import itertools


def encode(w, choices, pairs, gates, wires, terminal_empty=True):
    cuts = [[w.var() for _ in range(wires - 1)] for _ in range(gates + 1)]
    if terminal_empty:
        for cut in cuts[-1]:
            w.add(cut)
    for t in range(gates - 1, -1, -1):
        for k in range(wires - 1):
            spanning = [choices[t][j] for j, (a, b) in enumerate(pairs) if a <= k < b]
            w.add(-cuts[t][k], cuts[t + 1][k])
            for selected in spanning:
                w.add(-cuts[t][k], -selected)
            w.add(cuts[t][k], -cuts[t + 1][k], *spanning)
        for j, (a, b) in enumerate(pairs):
            for k, ell in itertools.combinations(range(a, b), 2):
                w.add(-choices[t][j], -cuts[t + 1][k], -cuts[t + 1][ell])
    return cuts
