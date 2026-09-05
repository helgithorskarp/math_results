#!/usr/bin/env python3
"""Definition-level checks of the local reduction, relabelings and fixture."""
from itertools import combinations, product
from pathlib import Path
import ast
import random
from check_certificate import require, unit_conflict


def local_profiles():
    valid = []
    for weights in product(range(4), repeat=7):
        full = weights.count(3)
        deficit = sum(2-w+3*(w == 3) for w in weights)
        allowed = [a for a in range(20)
                   if a+3*full <= 4 and 18 <= 2+a+sum(weights) <= 24]
        require(bool(allowed) == (deficit <= 2), 'deficit equivalence')
        valid.extend((a, weights) for a in allowed)
    require(len(valid) == 52, 'local profile count')
    print('LOCAL_AUDIT cross_profiles=16384 fixed_count_profiles=327680 feasible=52 PASS')


def elementary_logic():
    clauses = []
    for states in product((-1, 0, 1), repeat=2):
        clauses.append(tuple((i+1)*s for i, s in enumerate(states) if s))
    tested = 0
    for mask in range(1 << len(clauses)):
        formula = [c for i, c in enumerate(clauses) if (mask >> i) & 1]
        for assumptions in [(), (1,), (-1,), (2,), (-2,)]:
            satisfiable = any(
                all(values[abs(x)-1] == (x > 0) for x in assumptions) and
                all(any(values[abs(x)-1] == (x > 0) for x in c) for c in formula)
                for values in product((False, True), repeat=2))
            require(not unit_conflict(formula, assumptions) or not satisfiable,
                    'unit propagation claimed a false conflict')
            tested += 1
    # Exhaust the exact lexicographic CNF schema at four coordinates.
    lex_clauses = []
    for position in range(4):
        for prefix in product((False, True), repeat=position):
            clause = []
            for i, value in enumerate(prefix):
                clause.extend((-(i+1), -(i+5)) if value else (i+1, i+5))
            lex_clauses.append(tuple(clause+[-position-1, position+5]))
    for values in product((False, True), repeat=8):
        truth = all(any(values[abs(x)-1] == (x > 0) for x in c) for c in lex_clauses)
        require(truth == (values[:4] <= values[4:]), 'lex formula')
    print(f'LOGIC_AUDIT unit_propagation_cases={tested} lex_assignments=256 PASS')


def actual_counters():
    # Extract only the production counter function, without running its CLI.
    source = ast.parse((Path(__file__).parent/'generate.py').read_text())
    function = next(node for node in source.body if isinstance(node, ast.FunctionDef)
                    and node.name == 'atmost')
    code = compile(ast.Module(body=[function], type_ignores=[]), 'counter', 'exec')
    tested = 0
    for n in range(1, 7):
        patterns = [list(range(1, n+1)), [i if i % 2 else -i for i in range(1, n+1)],
                    [1 if i < 3 else i-1 for i in range(n)]]
        for inputs in patterns:
            largest = max(map(abs, inputs))
            for bound in range(n+1):
                clauses = []
                namespace = dict(nv=largest, add=lambda c: clauses.append(tuple(c)))
                exec(code, namespace)
                namespace['atmost'](inputs, bound)
                for bits in product((False, True), repeat=largest):
                    valuation = {i+1: x for i, x in enumerate(bits)}
                    count = 0
                    variable = largest
                    for position, lit in enumerate(inputs, 1):
                        count += valuation[abs(lit)] == (lit > 0)
                        for threshold in range(1, min(position, bound+1)+1):
                            variable += 1
                            valuation[variable] = count >= threshold
                    if count <= bound:
                        require(all(any(valuation[abs(x)] == (x > 0) for x in c)
                                    for c in clauses), 'counter lost a valid assignment')
                    else:
                        assumptions = [i+1 if x else -i-1 for i, x in enumerate(bits)]
                        require(unit_conflict(clauses, assumptions), 'counter permits overflow')
                    tested += 1
    print(f'COUNTER_AUDIT assignments={tested} signed_and_repeated_inputs=YES PASS')


def normalizations():
    rng = random.Random(550308)
    pairs = list(combinations(range(43), 2))
    sigma = [3*(v//3)+(v+1) % 3 if v < 24 else v for v in range(43)]
    for profile in range(256):
        graph = {}
        for a, b in pairs:
            if (a, b) in graph:
                continue
            internal = b < 24 and a//3 == b//3
            value = bool((profile >> (a//3)) & 1) if internal else bool(rng.randrange(2))
            for _ in range(3):
                graph[tuple(sorted((a, b)))] = value
                a, b = sigma[a], sigma[b]
        reverse = profile.bit_count() > 4
        colors = [bool((profile >> i) & 1) ^ reverse for i in range(8)]
        order = sorted(range(8), key=lambda i: not colors[i])
        mapping = [3*i+s for i in order for s in range(3)]+list(range(24, 43))

        def color(a, b):
            return graph[tuple(sorted((mapping[a], mapping[b])))] ^ reverse

        for i in range(1, 8):
            old = mapping[3*i:3*i+3]
            for shift in range(3):
                mapping[3*i:3*i+3] = old[shift:]+old[:shift]
                word = tuple(color(0, 3*i+s) for s in range(3))
                if word == tuple(sorted(word, reverse=True)):
                    break
            else:
                raise ValueError('anchor phase normalization')
        fixed = sorted(range(24, 43), key=lambda f: tuple(color(3*i, f) for i in range(8)))
        mapping[24:] = [mapping[f] for f in fixed]
        require(sorted(mapping) == list(range(43)), 'relabeling is not a permutation')
        require(all(mapping[sigma[v]] == sigma[mapping[v]] for v in range(43)),
                'relabeling fails to commute with rotation')
        rows = [tuple(color(3*i, f) for i in range(8)) for f in range(24, 43)]
        require(rows == sorted(rows), 'fixed-signature normalization')
        r = min(profile.bit_count(), 8-profile.bit_count())
        require(all(color(3*i, 3*i+1) == (i < r) for i in range(8)), 'internal colors')
        for i in range(1, 8):
            word = tuple(color(0, 3*i+s) for s in range(3))
            require(word == tuple(sorted(word, reverse=True)), 'anchor word')
        normalized = {(a, b): color(a, b) for a, b in pairs}
        require(all(normalized[a, b] == normalized[tuple(sorted((sigma[a], sigma[b])))]
                    for a, b in pairs), 'normalized graph is not invariant')
    print('NORMALIZATION_AUDIT internal_profiles=256 pairs_per_graph=903 PASS')


def fixture():
    lines = (Path(__file__).parent/'moving24.edges').read_text().splitlines()
    require(lines[0] == '24 138', 'fixture header')
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    require(len(edges) == len(set(edges)) == 138, 'fixture edges')
    require(all(0 <= a < b < 24 for a, b in edges), 'fixture endpoint')
    red = set(edges)
    def color(a, b):
        return tuple(sorted((a, b))) in red
    for vertices in combinations(range(24), 5):
        require(len({color(a, b) for a, b in combinations(vertices, 2)}) == 2,
                'fixture has a monochromatic five-set')
    sigma = [3*(v//3)+(v+1) % 3 for v in range(24)]
    require({tuple(sorted((sigma[a], sigma[b]))) for a, b in red} == red, 'fixture rotation')
    for i in range(8):
        internal = i < 4
        require(all(color(a, b) == internal for a, b in combinations(range(3*i, 3*i+3), 2)),
                'fixture internal color')
        weights = [sum(color(3*i, v) == internal for v in range(3*j, 3*j+3))
                   for j in range(8) if j != i]
        require(sum(2-w+3*(w == 3) for w in weights) <= 2, 'fixture deficit')
    print('FIXTURE_AUDIT vertices=24 red_edges=138 five_sets=42504 deficit_bound=2 PASS')


if __name__ == '__main__':
    local_profiles()
    elementary_logic()
    actual_counters()
    normalizations()
    fixture()
