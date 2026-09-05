#!/usr/bin/env python3
"""Solver-free verification of smaller positive killing sets."""
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
                ('input hash mismatch', name))
    source = REPO / 'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py'
    spec = importlib.util.spec_from_file_location('reviewed_integer_geometry', source)
    geometry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geometry)
    den, points, vertices, U, edges = geometry.read_geometry()
    originals = json.loads((REPO / 'hadwiger_nelson_parts509_pool_cover_residual30/refinements.json').read_text())
    rows = json.loads((HERE / 'colourings.json').read_text())
    require(len(originals) == len(rows) == 16, 'row count')
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)

    def coloring(row):
        D = row['D']
        require(D and all(type(v) is int for v in D) and D == sorted(set(D)) and
                set(D) <= set(U), 'deleted vertex labels')
        require(len(row['l']) == 374 and set(row['l']) <= set('0123'), 'L colours')
        require(len(row['c']) == 303 and set(row['c']) <= set('.0123'), 'pool colours')
        require({v for v, c in zip(U, row['c']) if c == '.'} == set(D), 'colour domain')
        c = dict(enumerate(row['l']))
        c.update({v: col for v, col in zip(U, row['c']) if col != '.'})
        es = [(a, b) for a, b in edges if a in c and b in c]
        require(all(c[a] != c[b] for a, b in es), 'improper four-colouring')
        require(all({c[w] for w in adjacency[v] if w in c} == set('0123') for v in D),
                'colouring not maximal with colours fixed')
        return set(D), len(c), len(es)

    facts = []
    for i, (old, row) in enumerate(zip(originals, rows)):
        old_D, _, _ = coloring(old)
        D, order, size = coloring(row)
        require(type(row['parent_index']) is int and row['parent_index'] == i, 'parent index')
        require(D <= old_D, 'subset relation')
        if D == old_D:
            require(row['l'] == old['l'] and row['c'] == old['c'], 'unchanged witness')
        facts.append(dict(parent_index=i, original_size=len(old_D), final_size=len(D),
                          original_S=sum(v < 509 for v in old_D), final_S=sum(v < 509 for v in D),
                          restored_vertices=sorted(old_D-D), extension_vertices=order,
                          extension_edges=size))
    sets = [set(row['D']) for row in rows]
    distinct = {tuple(row['D']) for row in rows}
    nonredundant = [i for i, D in enumerate(sets) if not any(
        other < D or (other == D and j < i) for j, other in enumerate(sets))]
    result = dict(status='SUBSET KILLING CERTIFICATES VERIFIED', rows=16,
                  points=len(vertices), unit_edges=len(edges), denominator=den,
                  improved_rows=sum(f['final_size'] < f['original_size'] for f in facts),
                  original_total=sum(f['original_size'] for f in facts),
                  final_total=sum(f['final_size'] for f in facts),
                  restored_occurrences=sum(len(f['restored_vertices']) for f in facts),
                  distinct_sets=len(distinct), rows_surviving_family_subset_pruning=nonredundant,
                  S_only_row_indices=[i for i, D in enumerate(sets) if all(v < 509 for v in D)],
                  facts=facts)
    require(result == json.loads((HERE / 'expected.json').read_text()), 'recorded facts differ')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
