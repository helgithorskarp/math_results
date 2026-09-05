#!/usr/bin/env python3
"""Exhaustively compare activation CNFs and ordinary colourings on tiny graphs."""
from itertools import combinations, product
import json


def require(ok, detail):
    if not ok:
        raise RuntimeError(detail)


def main():
    cases = models = 0
    for n in (2, 3):
        pairs = list(combinations(range(n), 2))
        for edge_bits in product((False, True), repeat=len(pairs)):
            edges = [e for e, bit in zip(pairs, edge_bits) if bit]
            for optional in product((False, True), repeat=n - 2):
                selected = {0, 1} | {v + 2 for v, bit in enumerate(optional) if bit}
                for allowed_bits in product((False, True), repeat=2):
                    allowed = {c for c in range(2) if allowed_bits[c]}
                    colour = lambda v, c: 2 * v + c + 1
                    activation = lambda v: 2 * n + v + 1
                    clauses = [[-activation(v), colour(v, 0), colour(v, 1)] for v in range(n)]
                    clauses += [[-colour(u, c), -colour(v, c)] for u, v in edges for c in range(2)]
                    clauses += [[activation(v)] for v in selected] + [[colour(0, 0)]]
                    clauses += [[-colour(1, c)] for c in allowed]
                    decoded = set()
                    labels = sorted(selected)
                    for bits in product((False, True), repeat=3 * n):
                        if not all(any(bits[abs(lit) - 1] == (lit > 0) for lit in row) for row in clauses):
                            continue
                        models += 1
                        # Fix the distinguished origin to its asserted colour;
                        # check every choice from every other nonempty domain.
                        domains = [[0] if v == 0 else [c for c in range(2) if bits[colour(v, c) - 1]] for v in labels]
                        for choices in product(*domains):
                            colours = dict(zip(labels, choices))
                            require(colours[0] == 0 and colours[1] not in allowed, 'boundary decoding')
                            require(all(colours[u] != colours[v] for u, v in edges if u in selected and v in selected),
                                    'edge decoding')
                            decoded.add(choices)
                    ordinary = set()
                    for choices in product(range(2), repeat=len(labels)):
                        colours = dict(zip(labels, choices))
                        if colours[0] == 0 and colours[1] not in allowed and all(
                                colours[u] != colours[v] for u, v in edges if u in selected and v in selected):
                            ordinary.add(choices)
                    require(decoded == ordinary, ('activation equivalence', n, edges, selected, allowed))
                    cases += 1
    require(cases == 72, 'control coverage')
    print(json.dumps(dict(status='ACTIVATION AND SET-VALUED COLOUR DECODING EQUIVALENCE VERIFIED',
                          finite_graph_selection_relation_cases=cases,
                          satisfying_Boolean_models_decoded=models), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
