#!/usr/bin/env python3
"""Exact local arithmetic, small formula/counter and literal relabeling checks."""
from itertools import combinations, product
from math import factorial
from pathlib import Path
import argparse
import json
import random
import generate as gen

need = gen.require


def local_profiles():
    rows, histogram, bad_budget, missing_upper = 0, {}, 0, 0
    for weights in product(range(4), repeat=10):
        m = weights.count(3)
        d = sum((2, 1, 0, 2)[w] for w in weights)
        allowed = [a for a in range(11) if a+3*m <= 4 and 18 <= 2+a+sum(weights) <= 24]
        lo, hi = max(0, d-4-3*m), min(10, 4-3*m, d+2-3*m)
        need(allowed == list(range(lo, hi+1)), 'local interval mismatch')
        need(bool(allowed) == (d <= 8 and m <= 1), 'existence criterion')
        bad_budget += d <= 8 and not allowed
        missing_upper += sum(a+3*m <= 4 and 2+a+sum(weights) > 24 for a in range(11))
        rows += len(allowed)
        if allowed:
            key = f'{m},{d}'
            histogram[key] = histogram.get(key, 0)+len(allowed)
    # Independently count the same objects by occupancy numbers and multinomials.
    second = {}
    for n0 in range(11):
        for n1 in range(11-n0):
            for n2 in range(11-n0-n1):
                n3 = 10-n0-n1-n2
                multiplicity = factorial(10)//(factorial(n0)*factorial(n1)*factorial(n2)*factorial(n3))
                weight_sum = n1+2*n2+3*n3
                count = sum(a+3*n3 <= 4 and 18 <= 2+a+weight_sum <= 24 for a in range(11))
                if count:
                    key = f'{n3},{2*n0+n1+2*n3}'
                    second[key] = second.get(key, 0)+count*multiplicity
    need(histogram == second, 'multinomial reconstruction differs')
    return dict(weight_vectors=4**10, fixed_count_trials=11*4**10, feasible_profiles=rows,
                budget_only_false_weight_vectors=bad_budget,
                profiles_admitted_without_upper_degree=missing_upper, by_complete_and_deficit=histogram)


def conflict(formula, assumptions):
    values = {}
    for lit in assumptions:
        if abs(lit) in values and values[abs(lit)] != (lit > 0):
            return True
        values[abs(lit)] = lit > 0
    while True:
        changed = False
        for clause in formula:
            remaining = []
            for lit in clause:
                if abs(lit) not in values:
                    remaining.append(lit)
                elif values[abs(lit)] == (lit > 0):
                    break
            else:
                if not remaining:
                    return True
                if len(remaining) == 1:
                    values[abs(remaining[0])] = remaining[0] > 0
                    changed = True
        if not changed:
            return False


def counters():
    trials = 0
    for n in range(1, 7):
        for inputs in (list(range(1, n+1)), [(-1)**i*i for i in range(1, n+1)],
                       [1 if i < 3 else i-1 for i in range(n)]):
            primary = max(map(abs, inputs))
            for bound in range(n+1):
                f = gen.Formula(primary)
                f.atmost(inputs, bound)
                for bits in product((False, True), repeat=primary):
                    values = {i+1: b for i, b in enumerate(bits)}
                    count, variable = 0, primary
                    for i, lit in enumerate(inputs, 1):
                        count += values[abs(lit)] == (lit > 0)
                        for j in range(1, min(i, bound+1)+1):
                            variable += 1
                            values[variable] = count >= j
                    if count <= bound:
                        need(all(any(values[abs(lit)] == (lit > 0) for lit in clause)
                                 for clause in f.clauses), 'counter lost a valid primary assignment')
                    else:
                        assumptions = [i+1 if b else -i-1 for i, b in enumerate(bits)]
                        need(conflict(f.clauses, assumptions), 'counter did not force overflow')
                    trials += 1
    return dict(signed_and_repeated_assignments=trials)


def small_ramsey():
    counts = []
    for r in range(3):
        nv, _, _, _, _, edge = gen.model(r, k=2, n=7)
        f = gen.Formula(nv)
        gen.ramsey(f, edge, 7)
        good = 0
        for bits in product((False, True), repeat=nv):
            def color(a, b):
                lit = edge(a, b)
                return lit == gen.T if abs(lit) == gen.T else bits[lit-1]
            literal = all(len({color(a, b) for a, b in combinations(five, 2)}) == 2
                          for five in combinations(range(7), 5))
            encoded = all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause) for clause in f.clauses)
            need(literal == encoded, 'small literal Ramsey mismatch')
            good += literal
        counts.append(dict(red_cycles=r, assignments=1 << nv, ramsey=good))
    return counts


def normalizations():
    rng = random.Random(550311)
    sigma = [3*(v//3)+(v+1) % 3 if v < 33 else v for v in range(43)]
    pairs = list(combinations(range(43), 2))
    for mask in range(1 << 11):
        graph = {}
        for a, b in pairs:
            if (a, b) in graph:
                continue
            value = bool((mask >> (a//3)) & 1) if b < 33 and a//3 == b//3 else bool(rng.randrange(2))
            for _ in range(3):
                graph[tuple(sorted((a, b)))] = value
                a, b = sigma[a], sigma[b]
        reverse = mask.bit_count() > 5
        colors = [bool((mask >> i) & 1) ^ reverse for i in range(11)]
        order = sorted(range(11), key=lambda i: not colors[i])
        p = [3*i+t for i in order for t in range(3)]+list(range(33, 43))

        def color(a, b):
            return graph[tuple(sorted((p[a], p[b])))] ^ reverse

        for j in range(1, 11):
            old = p[3*j:3*j+3]
            for shift in range(3):
                p[3*j:3*j+3] = old[shift:]+old[:shift]
                word = tuple(color(0, 3*j+t) for t in range(3))
                if word == tuple(sorted(word, reverse=True)):
                    break
            else:
                raise ValueError('no normalized phase')
        order = sorted(range(1, 11), key=lambda j:
                       (not color(3*j, 3*j+1), sum(color(0, 3*j+t) for t in range(3))))
        blocks = [p[3*j:3*j+3] for j in order]
        p[3:33] = [v for block in blocks for v in block]
        order = sorted(range(33, 43), key=lambda v: tuple(color(3*i, v) for i in range(11)))
        p[33:] = [p[v] for v in order]
        need(sorted(p) == list(range(43)), 'invalid permutation')
        need(all(p[sigma[v]] == sigma[p[v]] for v in range(43)), 'not a centralizer relabeling')
        need(all(color(a, b) == color(sigma[a], sigma[b]) for a, b in pairs), 'lost invariance')
        r = min(mask.bit_count(), 11-mask.bit_count())
        need(all(color(3*i, 3*i+1) == (i < r) for i in range(11)), 'internal colors')
        for j in range(1, 11):
            word = tuple(color(0, 3*j+t) for t in range(3))
            need(word == tuple(sorted(word, reverse=True)), 'phase failure')
        for j in range(1, 10):
            if (j < r) == (j+1 < r):
                need(all(color(0, 3*j+t) <= color(0, 3*(j+1)+t) for t in range(3)), 'anchor order')
        signatures = [tuple(color(3*i, v) for i in range(11)) for v in range(33, 43)]
        need(signatures == sorted(signatures), 'fixed signature order')
    return dict(internal_color_profiles=2048, literal_pairs_per_graph=903,
                complement_counts=list(range(6)), all_relabelings_centralize=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    report = dict(local_arithmetic=local_profiles(), counters=counters(),
                  small_ramsey=small_ramsey(), normalizations=normalizations())
    a.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, sort_keys=True))
