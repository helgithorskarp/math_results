#!/usr/bin/env python3
"""Check exact geometry, fixtures and optionally every generated relation row.

Full relation verification regenerates two CNFs. Their UNSAT proof checks are
separate: positive witnesses alone do not prove completeness or blocking.
"""
import argparse
from collections import Counter
import hashlib
import json
from math import factorial
from pathlib import Path
from geometry import H, D, PERMS, reconstruct, cnf, dump_cnf, require, proper

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_row(pattern, word, g):
    col = proper(word, H, g['host_edges'])
    require(col[0] == 0, 'origin colour')
    require(''.join(str(col[v]) for v in g['boundary']) == pattern, 'exact boundary restriction')
    key = tuple(map(int, pattern))
    require(key == min(tuple(p[c] for c in key) for p in PERMS), 'canonical S4 representative')


def basic(out):
    g = reconstruct(HERE / 'points.tsv')
    fx = json.loads((HERE / 'fixtures.json').read_text())
    proper(fx['parent_five'], list(range(509)), g['edges'], 5)
    require(set(fx['parent_five']) == set('01234'), 'proper parent five-word')
    for row in fx['host_rows']:
        check_row(row['pattern'], row['witness'], g)
    require(len(fx['host_rows']) == 9, 'nine fixtures')
    result = dict(parent_points=509, parent_complete_edges=2442, all_exact_pairs=129286,
                  host_points=136, host_edges=564, removed_points=373, removed_edges=1836,
                  cross_edges=42, boundary=g['boundary'], boundary_edges=0,
                  replacement_new_point_cap=372, total_point_cap=508,
                  parent_five_checked=True, fixture_rows_checked=9,
                  complete_relation_checked=False, replacement_supplied=False,
                  record_candidate=False)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'geometry.json').write_text(json.dumps(g, separators=(',', ':')) + '\n')
    return g, result


def verify(out, relation=None):
    out = Path(out)
    g, result = basic(out)
    if relation is None:
        return result
    rows = [line.split('\t') for line in Path(relation).read_text().splitlines()]
    require(all(len(r) == 2 for r in rows), 'tab-separated pattern and full host word')
    rows.sort()
    patterns = [r[0] for r in rows]
    require(len(patterns) == len(set(patterns)) == 41025, '41025 distinct patterns')
    for pattern, word in rows:
        check_row(pattern, word, g)
    stream = ''.join(p + '\n' for p in patterns).encode()
    phash = hashlib.sha256(stream).hexdigest()
    require(phash == 'f67f18e35fcd20c46c405c2b7458712091afd12f5fdeaee6443555735fb56649',
            'complete frozen canonical pattern set')
    (out / 'canonical_patterns.txt').write_bytes(stream)
    palette = Counter(len(set(p)) for p in patterns)
    require(palette == {2: 7, 3: 1500, 4: 39518}, 'boundary palette histogram')
    require('0' * len(g['boundary']) not in patterns, 'monochromatic boundary absent')
    base, var = cnf(H, g['host_edges'])
    base.append([var(0, 0)])
    for pattern in patterns:
        col = dict(zip(g['boundary'], map(int, pattern)))
        for p in PERMS:
            base.append([-var(v, p[col[v]]) for v in g['boundary'] if v != 0])
    dump_cnf(out / 'completeness.cnf', base, 4 * len(H))
    parent, pv = cnf(list(range(509)), g['edges'])
    parent.append([pv(0, 0)])
    dump_cnf(out / 'parent.cnf', parent, 2036)
    result.update(complete_relation_checked=True, host_words_checked=len(rows),
                  canonical_patterns=41025,
                  labelled_patterns=sum(24 // factorial(4-len(set(p))) for p in patterns),
                  boundary_palette_histogram={str(k): palette[k] for k in sorted(palette)},
                  canonical_patterns_sha256=phash, completeness_variables=544,
                  completeness_clauses=len(base),
                  completeness_cnf_sha256=digest(out / 'completeness.cnf'),
                  parent_cnf_sha256=digest(out / 'parent.cnf'),
                  negative_proof_checks_still_required=True)
    expected = HERE / 'expected.json'
    if expected.exists():
        require(result == json.loads(expected.read_text()), 'frozen exact output')
    (out / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--relation', type=Path)
    a = ap.parse_args()
    print(json.dumps(verify(a.out, a.relation), indent=2))
