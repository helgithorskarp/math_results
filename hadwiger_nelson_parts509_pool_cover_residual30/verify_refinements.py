#!/usr/bin/env python3
"""Check the additional positive cover refinements without a SAT solver."""
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, expected in manifest['input_sha256'].items():
        require(sha256((REPO / name).read_bytes()).hexdigest() == expected,
                ('baseline input hash', name))
    expected = json.loads((HERE / 'refinements_expected.json').read_text())
    raw = (HERE / 'refinements.json').read_bytes()
    require(sha256(raw).hexdigest() == expected['certificate_sha256'], 'refinement input hash')
    rows = json.loads(raw)
    spec = importlib.util.spec_from_file_location('baseline_verifier', HERE / 'verify.py')
    baseline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(baseline)
    den, points, vertices, U, edges = baseline.load_geometry()
    L, S, Q = set(range(374)), set(range(374, 509)), set(U[135:])
    us = set(U)
    family = []
    initial = json.loads((REPO / 'hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json').read_text())
    require(initial['U'] == list(U), 'initial universe')
    family.extend(set(row['D']) for row in initial['sets'])
    sonly = json.loads((REPO / 'hadwiger_nelson_parts509_s_replacement_budget/certificate.json').read_text())
    require(sonly['pool'] == list(U), 'S-only universe')
    family.extend(set(row['D']) for row in sonly['killing_sets'])
    for a in (6, 7):
        family.extend(set(row) for row in baseline.read_cnf(REPO /
            f'hadwiger_nelson_parts509_pool_shape{a}_verified/killing_clauses.cnf', U))
    family = [set(row) for row in sorted({tuple(sorted(row)) for row in family})]
    require(len(family) == 17250, 'baseline public cover size')
    original = json.loads((HERE / 'certificate.json').read_text())
    left_rows = json.loads((REPO / 'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())['classes']
    original['l'] = left_rows[original['p']]['witness_colouring_L']
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)

    def check_coloring(row):
        D = row['D']
        require(D and all(type(v) is int for v in D) and D == sorted(set(D)) and
                set(D) <= us, 'killing-set labels')
        require(len(row['l']) == 374 and set(row['l']) <= set('0123'), 'L colours')
        require(len(row['c']) == 303 and set(row['c']) <= set('.0123'), 'pool colours')
        require({v for v, c in zip(U, row['c']) if c == '.'} == set(D), 'omitted pool labels')
        cmap = dict(enumerate(row['l']))
        cmap.update({v: c for v, c in zip(U, row['c']) if c != '.'})
        ee = [(a, b) for a, b in edges if a in cmap and b in cmap]
        require(all(cmap[a] != cmap[b] for a, b in ee), 'improper complement colouring')
        return set(D), cmap, ee

    seed_D, _, _ = check_coloring(original)
    require(seed_D not in family, 'seed already in public family')
    family.append(seed_D)
    facts, selections = [], []
    for i, row in enumerate(rows):
        D, cmap, ee = check_coloring(row)
        for key, allowed in [('R', S), ('A', Q)]:
            require(all(type(v) is int for v in row[key]) and
                    row[key] == sorted(set(row[key])) and set(row[key]) <= allowed, key)
        R, A = set(row['R']), set(row['A'])
        X = (S - R) | A
        selections.append(X)
        H = L | X
        require(len(X) <= 134 and len(A) >= 8, 'selection counts')
        require(all(X & old for old in family), ('candidate fails earlier cover', i))
        require(not X & D, ('new row does not exclude candidate', i))
        he = [(a, b) for a, b in edges if a in H and b in H]
        degree = Counter(v for edge in he for v in edge)
        require(min(degree[v] for v in X) >= 4, 'selected pool degree')
        require(all(cmap[a] != cmap[b] for a, b in he), 'candidate colouring')
        require(all({cmap[w] for w in adjacency[v] if w in cmap} == set('0123') for v in D),
                'extension not maximal with colours fixed')
        require(not any(old <= D for old in family), 'old clause subsumes new row')
        facts.append(dict(index=i, additions=len(A), removed_S=len(R),
                          vertices=len(H), unit_edges=len(he), minimum_pool_degree=min(degree[v] for v in X),
                          killing_size=len(D), killing_S=len(D & S), killing_Q5=len(D & Q),
                          extension_vertices=len(cmap), extension_edges=len(ee),
                          edge_sha256=sha256(''.join(f'{a},{b}\n' for a, b in he).encode()).hexdigest()))
        family.append(D)
    covering = [[j for j, row in enumerate(rows) if not X.intersection(row['D'])]
                for X in selections]
    result = dict(status='ADDITIONAL COVER REFINEMENTS VERIFIED',
                  new_rows=len(rows), baseline_distinct_sets=17250, seed_rows=1,
                  final_distinct_sets=len(family), points=len(vertices), edges=len(edges),
                  denominator=den, facts=facts, covering_new_row_indices=covering,
                  added_rows_irredundant=all(indices == [i] for i, indices in enumerate(covering)))
    require(result == expected['result'], 'computed facts differ from recorded facts')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
