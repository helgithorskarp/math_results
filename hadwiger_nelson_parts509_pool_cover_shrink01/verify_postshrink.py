#!/usr/bin/env python3
"""Check one residual selection and positive cut after all subset replacements."""
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def compute():
    manifest = json.loads((HERE / 'postshrink_manifest.json').read_text())
    for name, expected in manifest['input_sha256'].items():
        require(sha256((REPO / name).read_bytes()).hexdigest() == expected,
                ('input hash', name))
    prior = REPO / 'hadwiger_nelson_parts509_pool_cover_residual30'
    spec = importlib.util.spec_from_file_location('prior_reader', prior / 'verify.py')
    baseline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(baseline)
    den, _, vertices, U, edges = baseline.load_geometry()
    L, S, Q = set(range(374)), set(range(374, 509)), set(U[135:])
    row = json.loads((HERE / 'postshrink_residual.json').read_text())
    for key, allowed in [('R', S), ('A', Q), ('D', set(U))]:
        require(all(type(v) is int for v in row[key]) and
                row[key] == sorted(set(row[key])) and set(row[key]) <= allowed, key)
    R, A, D = (set(row[key]) for key in ('R', 'A', 'D'))
    X = (S - R) | A
    H = L | X
    require(len(H) == 508 and len(R) == 28 and len(A) == 27, 'selection size')
    require(len(D) == 31 and not X & D, 'new cut excludes selection')
    require(len(row['l']) == 374 and set(row['l']) <= set('0123'), 'L colours')
    require(len(row['c']) == 303 and set(row['c']) <= set('.0123'), 'pool colours')
    require({v for v, c in zip(U, row['c']) if c == '.'} == D, 'omitted vertices')
    colors = dict(enumerate(row['l']))
    colors.update({v: c for v, c in zip(U, row['c']) if c != '.'})
    require(set(colors) == L | (set(U) - D), 'colouring domain')
    extension_edges = [(a, b) for a, b in edges if a in colors and b in colors]
    require(all(colors[a] != colors[b] for a, b in extension_edges), 'colouring')
    candidate_edges = [(a, b) for a, b in edges if a in H and b in H]
    require(H <= set(colors), 'candidate is coloured')
    degree = Counter(v for e in candidate_edges for v in e)
    require(min(degree[v] for v in X) >= 4, 'selected pool degrees')
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    require(all({colors[w] for w in adjacency[v] if w in colors} == set('0123')
                for v in D), 'fixed-colour extension maximality')

    initial = json.loads((REPO /
        'hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json').read_text())
    sonly = json.loads((REPO /
        'hadwiger_nelson_parts509_s_replacement_budget/certificate.json').read_text())
    require(initial['U'] == list(U) == sonly['pool'], 'family universe')
    families = {'a0_to_a5': [r['D'] for r in initial['sets']],
                'S_only': [r['D'] for r in sonly['killing_sets']]}
    for a in (6, 7):
        families[f'a{a}'] = baseline.read_cnf(REPO /
            f'hadwiger_nelson_parts509_pool_shape{a}_verified/killing_clauses.cnf', U)
    families['first_residual'] = [json.loads((prior / 'certificate.json').read_text())['D']]
    families['refinements'] = [r['D'] for r in
                              json.loads((prior / 'refinements.json').read_text())]
    families['subset_replacements'] = [r['D'] for r in
                                       json.loads((HERE / 'colourings.json').read_text())]
    union = set()
    for name, rows in families.items():
        for values in rows:
            require(values and all(type(v) is int for v in values) and
                    list(values) == sorted(set(values)) and set(values) <= set(U),
                    ('family labels', name))
            require(bool(X.intersection(values)), ('missed earlier clause', name))
            union.add(tuple(values))
    require(not any(set(old) <= D for old in union), 'old clause subsumes new cut')
    return dict(status='POST-SHRINK RESIDUAL AND NEW KILLING SET VERIFIED',
                points=len(vertices), unit_edges=len(edges), denominator=den,
                candidate_vertices=len(H), candidate_edges=len(candidate_edges),
                removed_S=len(R), added_Q5=len(A),
                minimum_selected_pool_degree=min(degree[v] for v in X),
                killing_size=len(D), killing_S=len(D & S), killing_Q5=len(D & Q),
                extension_vertices=len(colors), extension_edges=len(extension_edges),
                public_family_rows={name: len(rows) for name, rows in families.items()},
                public_family_total_rows=sum(map(len, families.values())),
                public_family_distinct_sets=len(union), missed_public_sets=0,
                candidate_edges_sha256=sha256(''.join(f'{a},{b}\n' for a, b in
                                                     candidate_edges).encode()).hexdigest(),
                public_family_sha256=sha256(json.dumps(sorted(union),
                    separators=(',', ':')).encode()).hexdigest())


def main():
    result = compute()
    require(result == json.loads((HERE / 'postshrink_expected.json').read_text()),
            'recorded facts differ')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
