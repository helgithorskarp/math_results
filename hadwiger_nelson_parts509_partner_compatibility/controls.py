#!/usr/bin/env python3
"""Exhaustive small controls for actual composition and available-list semantics."""
from itertools import combinations, product
import json
from data import composition, require


def clauses(raw):
    lines = raw.decode().splitlines()
    variables, count = map(int, lines[0].split()[2:])
    rows = [list(map(int, line.split()[:-1])) for line in lines[1:]]
    require(len(rows) == count and all(line.endswith(' 0') for line in lines[1:]), 'DIMACS controls')
    return variables, rows


def main():
    cases = models = 0
    pairs = list(combinations(range(3), 2))
    for bits in product((False, True), repeat=3):
        edges = [e for e, bit in zip(pairs, bits) if bit]
        data = dict(vertices=[0, 1], S=[2], interface=[0], all_edges=edges)
        variables, rows = clauses(composition(data))
        require(variables == 14, 'tiny production encoding size')
        for active in (False, True):
            selected = [0, 1, 2] if active else [0, 2]
            formula = rows + ([[14]] if active else [])
            decoded = set()
            for assignment in product((False, True), repeat=variables):
                if not all(any(assignment[abs(v) - 1] == (v > 0) for v in row) for row in formula):
                    continue
                colours = {v: next(c for c in range(4) if assignment[4 * v + c]) for v in selected}
                require(colours[0] == 0, 'normalized origin')
                require(all(colours[u] != colours[v] for u, v in edges if u in selected and v in selected), 'composition decoding')
                decoded.add(tuple(colours[v] for v in selected))
                models += 1
            ordinary = set()
            for colours in product(range(4), repeat=len(selected)):
                mapping = dict(zip(selected, colours))
                if mapping[0] == 0 and all(mapping[u] != mapping[v] for u, v in edges if u in selected and v in selected):
                    ordinary.add(colours)
            require(decoded == ordinary, 'guarded full composition equivalence')
            cases += 1
    list_cases = 0
    pairs = list(combinations(range(4), 2))
    for bits in product((False, True), repeat=6):
        edges = [e for e, bit in zip(pairs, bits) if bit]
        for c0, c1 in product(range(2), repeat=2):
            if (0, 1) in edges and c0 == c1:
                continue
            fixed = {0: c0, 1: c1}
            masks = {v: {0, 1} - {fixed[u] for u in fixed if (u, v) in edges} for v in (2, 3)}
            for c2, c3 in product(range(2), repeat=2):
                all_colours = fixed | {2: c2, 3: c3}
                actual = all(all_colours[u] != all_colours[v] for u, v in edges)
                listed = c2 in masks[2] and c3 in masks[3] and ((2, 3) not in edges or c2 != c3)
                require(actual == listed, 'available lists equal full-colouring extension')
            list_cases += 1
    require(cases == 16 and list_cases == 192, 'control coverage')
    print(json.dumps(dict(status='COMPOSITION AND LIST EQUIVALENCE CONTROLS PASSED',
                          production_composition_cases=cases, satisfying_Boolean_models_decoded=models,
                          fixed_colouring_list_cases=list_cases), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
