#!/usr/bin/env python3
"""Solver-free verification of a residual selection and a new killing set.

Rebuild every unit edge with the independently reviewed integer geometry,
check the explicit colouring, and test the selected set against four
specified committed positive families. No SAT status is an assumption.
"""
import argparse
from collections import Counter
import importlib.util
import json
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load_geometry():
    source = REPO / 'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py'
    spec = importlib.util.spec_from_file_location('reviewed_integer_geometry', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.read_geometry()


def read_cnf(path, universe):
    lines = path.read_text(encoding='ascii').splitlines()
    header = lines[0].split()
    require(header[:3] == ['p', 'cnf', '303'], ('DIMACS header', str(path)))
    result = []
    for line in lines[1:]:
        row = tuple(map(int, line.split()))
        require(row and row[-1] == 0, 'unterminated positive clause')
        row = row[:-1]
        require(row and row == tuple(sorted(set(row))) and
                all(1 <= x <= 303 for x in row), 'invalid positive clause')
        result.append(tuple(universe[x - 1] for x in row))
    require(len(result) == int(header[3]), 'DIMACS row count')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, expected in manifest['input_sha256'].items():
        require(digest(REPO / name) == expected, ('input hash', name))
    denominator, points, all_vertices, universe, edges = load_geometry()
    U, L = set(universe), set(range(374))
    S, Q = set(range(374, 509)), set(universe[135:])
    certificate = json.loads((HERE / 'certificate.json').read_text())

    def labelled_set(key, allowed):
        row = certificate[key]
        require(all(type(x) is int for x in row) and
                row == sorted(set(row)) and set(row) <= allowed, key)
        return set(row)

    R = labelled_set('R', S)
    A = labelled_set('A', Q)
    D = labelled_set('D', U)
    X = (S - R) | A
    require(len(R) == 31 and len(A) == 30 and len(X) == 134,
            'candidate counts')
    require(len(D) == 39 and len(D & S) == 10 and len(D & Q) == 29,
            'new killing-set counts')
    require(not (X & D), 'new clause must exclude the candidate')
    interface = json.loads((REPO / 'hadwiger_nelson_parts509_interface_lemma/'
                            'interface_L.json').read_text())
    p = certificate['p']
    require(type(p) is int and 0 <= p < len(interface['classes']), 'L witness index')
    left = interface['classes'][p]['witness_colouring_L']
    colors = certificate['c']
    require(len(left) == 374 and set(left) <= set('0123'), 'L colouring format')
    require(len(colors) == 303 and set(colors) <= set('.0123'), 'pool colouring format')
    require({v for v, c in zip(universe, colors) if c == '.'} == D,
            'colouring must omit exactly D')
    coloring = dict(enumerate(left))
    coloring.update({v: c for v, c in zip(universe, colors) if c != '.'})
    require(set(coloring) == L | (U - D), 'coloured vertex set')
    extension_edges = [(a, b) for a, b in edges if a in coloring and b in coloring]
    require(all(coloring[a] != coloring[b] for a, b in extension_edges),
            'improper extension colouring')
    H = L | X
    candidate_edges = [(a, b) for a, b in edges if a in H and b in H]
    require(all(coloring[a] != coloring[b] for a, b in candidate_edges),
            'improper candidate colouring')
    degree = Counter(v for edge in candidate_edges for v in edge)
    require(min(degree[v] for v in X) >= 4, 'selected-pool degree condition')
    adjacency = {v: set() for v in all_vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    require(all({coloring[w] for w in adjacency[v] if w in coloring} == set('0123')
                for v in D), 'extension is not maximal with colours fixed')

    families = {}
    initial = json.loads((REPO / 'hadwiger_nelson_parts509_pool_shape_closure/'
                          'killing_sets.json').read_text())
    require(initial['U'] == list(universe), 'initial family universe')
    families['a0_to_a5'] = [tuple(row['D']) for row in initial['sets']]
    sonly = json.loads((REPO / 'hadwiger_nelson_parts509_s_replacement_budget/'
                        'certificate.json').read_text())
    require(sonly['pool'] == list(universe), 'S-only family universe')
    families['S_only'] = [tuple(row['D']) for row in sonly['killing_sets']]
    for a in (6, 7):
        families[f'a{a}'] = read_cnf(
            REPO / f'hadwiger_nelson_parts509_pool_shape{a}_verified/killing_clauses.cnf',
            universe)
    for name, rows in families.items():
        for row in rows:
            require(row and all(type(v) is int for v in row) and
                    tuple(sorted(set(row))) == row and set(row) <= U,
                    ('old killing set format', name))
            require(bool(X.intersection(row)), ('missed old killing set', name, row))
    union = set(row for rows in families.values() for row in rows)
    require(not any(set(row) <= D for row in union), 'an old clause subsumes the new row')
    facts = dict(
        status='RESIDUAL SELECTION AND NEW KILLING SET VERIFIED',
        denominator=denominator, pool_union_points=len(all_vertices),
        pool_union_edges=len(edges), candidate_vertices=len(H),
        candidate_edges=len(candidate_edges), removed_S=len(R), added_Q5=len(A),
        minimum_selected_pool_degree=min(degree[v] for v in X),
        extension_vertices=len(coloring), extension_edges=len(extension_edges),
        killing_size=len(D), killing_S=len(D & S), killing_Q5=len(D & Q),
        interface_index=p, fixed_colouring_maximal=True,
        public_family_rows={name: len(rows) for name, rows in families.items()},
        public_family_total_rows=sum(map(len, families.values())),
        public_family_distinct_sets=len(union), missed_public_sets=0,
        candidate_edges_sha256=sha256(''.join(f'{a},{b}\n' for a, b in candidate_edges)
                                      .encode('ascii')).hexdigest(),
        public_family_sha256=sha256(json.dumps(sorted(union), separators=(',', ':'))
                                    .encode('ascii')).hexdigest(),
    )
    require(facts == json.loads((HERE / 'expected.json').read_text()),
            'computed facts differ from the recorded certificate')
    text = json.dumps(facts, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
