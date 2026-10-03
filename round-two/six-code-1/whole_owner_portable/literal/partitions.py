"""Literal right-interface invariant and separate point-bijection checker."""
import argparse
import hashlib
from itertools import permutations
import json
from pathlib import Path
import sys
import time
from model import Budget, Guard, digest, encode, literal37, load, need, validate


def key(M, F, budget):
    H = set(range(5))
    columns = [set(f) for f in F] + [set(range(15)) - set().union(*(set(f) for f in F))]
    color = lambda s: sum(1 << a for a in s & H)
    candidates = []
    for p in permutations(range(3)):
        budget.tick()
        columns2 = [columns[j] for j in p] + [columns[3]]
        rows = [[color(set(m)), [[color(set(m) & c), len((set(m) & c) - H)] for c in columns2]] for m in M]
        candidates.append([2, [color(c) for c in columns2], sorted(rows)])
    # Sorting colors is forced by lexicographic minimization; all row/cell
    # data are retained, with the hole column always last.
    return min(candidates)


def point_bijections(M, F, targetM, targetF, budget):
    # Independent MRV on relations of actual point triples, not descriptors.
    def labels(M1, F1):
        rows = {a: i for i, row in enumerate(M1) for a in row}
        cols = {a: j for j, col in enumerate(F1) for a in col}
        for a in range(15):
            cols.setdefault(a, 3)
        return rows, cols
    r, c = labels(M, F)
    rr, cc = labels(targetM, targetF)
    image = dict(zip(range(5), range(5)))
    solutions = []
    if any((c[a] == 3) != (cc[a] == 3) for a in range(5)) or any(
            (r[a] == r[b]) != (rr[a] == rr[b]) or
            (c[a] == c[b]) != (cc[a] == cc[b]) for a in range(5) for b in range(5)):
        budget.tick()
        return []

    def compatible(a, b):
        budget.tick()
        return (c[a] == 3) == (cc[b] == 3) and all(
            (r[a] == r[u]) == (rr[b] == rr[v]) and
            (c[a] == c[u]) == (cc[b] == cc[v]) for u, v in image.items())

    def visit():
        budget.tick()
        if len(image) == 15:
            need(sorted(image.values()) == list(range(15)) and all(
                 sorted(sorted(image[a] for a in cell) for cell in source) == sorted(sorted(cell) for cell in target)
                 for source, target in [(M, targetM), (F, targetF)]), 'literal entire point-partition images')
            solutions.append(tuple(image[a] for a in range(15)))
            return
        candidates = []
        unused = set(range(5, 15)) - set(image.values())
        for a in range(5, 15):
            if a in image:
                continue
            targets = [b for b in sorted(unused) if compatible(a, b)]
            if not targets:
                return
            candidates.append((len(targets), a, targets))
        _, a, targets = min(candidates)
        for b in targets:
            image[a] = b
            visit()
            del image[a]

    visit()
    return sorted(solutions)


