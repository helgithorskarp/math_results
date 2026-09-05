#!/usr/bin/env python3
"""Definition-level checks of the local reduction, relabelings and fixture."""
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import ast
import json
import random


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unit_conflict(formula, assumptions):
    values = {}
    for lit in assumptions:
        variable, value = abs(lit), lit > 0
        if variable in values and values[variable] != value:
            return True
        values[variable] = value
    while True:
        changed = False
        for clause in formula:
            pending = []
            for lit in clause:
                if abs(lit) not in values:
                    pending.append(lit)
                elif values[abs(lit)] == (lit > 0):
                    break
            else:
                if not pending:
                    return True
                if len(pending) == 1:
                    lit = pending[0]
                    values[abs(lit)] = lit > 0
                    changed = True
        if not changed:
            return False


def local_profiles():
    valid = []
    budget_only_false = 0
    for weights in product(range(4), repeat=9):
        full = weights.count(3)
        deficit = sum(2-w+3*(w == 3) for w in weights)
        allowed = [a for a in range(14)
                   if a+3*full <= 4 and 18 <= 2+a+sum(weights) <= 24]
        require(bool(allowed) == (deficit <= 6 and full <= 1), 'deficit equivalence')
        budget_only_false += deficit <= 6 and not allowed
        valid.extend((a, weights) for a in allowed)
    require(len(valid) == 10679 and budget_only_false == 1380, 'local profile count')
    print('LOCAL_AUDIT cross_profiles=262144 fixed_count_profiles=3670016 feasible=10679 budget_only_false=1380 PASS')


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
    rng = random.Random(550310)
    pairs = list(combinations(range(43), 2))
    sigma = [3*(v//3)+(v+1) % 3 if v < 30 else v for v in range(43)]
    for profile in range(1024):
        graph = {}
        for a, b in pairs:
            if (a, b) in graph:
                continue
            internal = b < 30 and a//3 == b//3
            value = bool((profile >> (a//3)) & 1) if internal else bool(rng.randrange(2))
            for _ in range(3):
                graph[tuple(sorted((a, b)))] = value
                a, b = sigma[a], sigma[b]
        reverse = profile.bit_count() > 5
        colors = [bool((profile >> i) & 1) ^ reverse for i in range(10)]
        order = sorted(range(10), key=lambda i: not colors[i])
        mapping = [3*i+s for i in order for s in range(3)]+list(range(30, 43))

        def color(a, b):
            return graph[tuple(sorted((mapping[a], mapping[b])))] ^ reverse

        for i in range(1, 10):
            old = mapping[3*i:3*i+3]
            for shift in range(3):
                mapping[3*i:3*i+3] = old[shift:]+old[:shift]
                word = tuple(color(0, 3*i+s) for s in range(3))
                if word == tuple(sorted(word, reverse=True)):
                    break
            else:
                raise ValueError('anchor phase normalization')
        # Freeze the relabeled blocks before mutating the mapping.
        nonanchor = sorted(range(1,10), key=lambda i:
                           (not color(3*i,3*i+1), sum(color(0,3*i+t) for t in range(3))))
        blocks = [mapping[3*i:3*i+3] for i in nonanchor]
        mapping[3:30] = [v for block in blocks for v in block]
        for i in range(1,9):
            if color(3*i,3*i+1) == color(3*i+3,3*i+4):
                require(all(color(0,3*i+t) <= color(0,3*(i+1)+t) for t in range(3)),
                        'anchor weight ordering')
        fixed = sorted(range(30, 43), key=lambda f: tuple(color(3*i, f) for i in range(10)))
        mapping[30:] = [mapping[f] for f in fixed]
        require(sorted(mapping) == list(range(43)), 'relabeling is not a permutation')
        require(all(mapping[sigma[v]] == sigma[mapping[v]] for v in range(43)),
                'relabeling fails to commute with rotation')
        rows = [tuple(color(3*i, f) for i in range(10)) for f in range(30, 43)]
        require(rows == sorted(rows), 'fixed-signature normalization')
        r = min(profile.bit_count(), 10-profile.bit_count())
        require(all(color(3*i, 3*i+1) == (i < r) for i in range(10)), 'internal colors')
        for i in range(1, 10):
            word = tuple(color(0, 3*i+s) for s in range(3))
            require(word == tuple(sorted(word, reverse=True)), 'anchor word')
        normalized = {(a, b): color(a, b) for a, b in pairs}
        require(all(normalized[a, b] == normalized[tuple(sorted((sigma[a], sigma[b])))]
                    for a, b in pairs), 'normalized graph is not invariant')
    print('NORMALIZATION_AUDIT internal_profiles=1024 pairs_per_graph=903 PASS')


def fixture():
    lines = (Path(__file__).parent/'moving30.edges').read_text().splitlines()
    require(lines[0] == '30 219', 'fixture header')
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    require(len(edges) == len(set(edges)) == 219, 'fixture edges')
    require(all(0 <= a < b < 30 for a, b in edges), 'fixture endpoint')
    red = set(edges)
    def color(a, b):
        return tuple(sorted((a, b))) in red
    for vertices in combinations(range(30), 5):
        require(len({color(a, b) for a, b in combinations(vertices, 2)}) == 2,
                'fixture has a monochromatic five-set')
    sigma = [3*(v//3)+(v+1) % 3 for v in range(30)]
    require({tuple(sorted((sigma[a], sigma[b]))) for a, b in red} == red, 'fixture rotation')
    for i in range(10):
        internal = i < 5
        require(all(color(a, b) == internal for a, b in combinations(range(3*i, 3*i+3), 2)),
                'fixture internal color')
        weights = [sum(color(3*i, v) == internal for v in range(3*j, 3*j+3))
                   for j in range(10) if j != i]
        require(sum(2-w+3*(w == 3) for w in weights) <= 6, 'fixture deficit')
        require(weights.count(3) <= 1, 'fixture complete-block cap')
    print('FIXTURE_AUDIT vertices=30 red_edges=219 five_sets=142506 deficit_bound=6 PASS')


def anchor_profiles():
    # Two distinct enumerations: sorted multisets, and unrestricted labeled
    # weights followed by canonicalization. No graph realization is asserted.
    direct = {r:set() for r in range(1,6)}
    for weights in product(range(4),repeat=9):
        if weights.count(3)>1 or sum(2-w+3*(w==3) for w in weights)>6:
            continue
        for r in range(1,6):
            if 3 not in weights[:r-1]:
                direct[r].add(tuple(sorted(weights[:r-1]))+tuple(sorted(weights[r-1:])))
    for r,expected in enumerate((25,56,82,98,105),1):
        canonical = set()
        for left in combinations_with_replacement(range(3),r-1):
            for right in combinations_with_replacement(range(4),10-r):
                weights=left+right
                if weights.count(3)<=1 and sum(2-w+3*(w==3) for w in weights)<=6:
                    canonical.add(weights)
        require(canonical == direct[r], 'anchor profile completeness')
        require(len(canonical)==expected, 'anchor profile count')
        if r==4:
            stored=json.loads((Path(__file__).parent/'anchor_r4.json').read_text())
            require(stored['red_cycles']==4 and stored['blue_cycles']==6, 'stored anchor split')
            require(len(stored['weights'])==98 and
                    {tuple(w) for w in stored['weights']}==canonical, 'stored anchor coverage')
    print('ANCHOR_AUDIT red_counts=1,2,3,4,5 canonical_profiles=25,56,82,98,105 PASS')


if __name__ == "__main__":
    local_profiles()
    elementary_logic()
    actual_counters()
    normalizations()
    fixture()
    anchor_profiles()
