#!/usr/bin/env python3
"""Replay all exact geometry and colour witnesses; regenerate proof obligations.

The two DRAT proofs certify completeness and original-module blocking.
This script alone verifies the positive certificates and the CNF hashes.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from receiver import H, D, PERMS, reconstruct, cnf, dump_cnf, require, proper

HERE = Path(__file__).resolve().parent
N = [150, 169, 287, 296]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    g = reconstruct(HERE / 'points.tsv')
    B = g['boundary']
    I = [v for v in B if v not in N]
    S = list(range(374, 509))
    rows = [line.split('\t') for line in
            (HERE / 'host_relation.tsv').read_text().splitlines()]
    require(all(len(r) == 2 for r in rows), 'relation table format')
    require(len({r[0] for r in rows}) == len(rows) == 468, '468 distinct patterns')
    require(sorted(a for a, b in g['cross_edges'] if b == 310) == N,
            'complete degree-four star neighbourhood')
    require(not any(310 in e for e in g['module_edges']), 'module star is isolated')
    small_cross = [[a, b] for a, b in g['cross_edges'] if b != 310]
    require(sorted({a for a, b in small_cross}) == I, 'complete small-side interface')
    boundary_edges = [e for e in g['host_edges'] if set(e) <= set(B)]
    require(boundary_edges == [[0, 150], [0, 169], [150, 169]], 'boundary graph')

    ext_rows = [line.split('\t') for line in
                (HERE / 'small_extensions.tsv').read_text().splitlines()]
    require(all(len(r) == 2 for r in ext_rows), 'extension table format')
    ext = dict(ext_rows)
    require(len(ext_rows) == len(ext) == 424, '424 distinct small extensions')
    for pattern, word in ext.items():
        require(len(pattern) == len(I) and set(pattern) <= set('0123'), 'I pattern')
        sc = proper(word, S, g['module_edges'])
        ic = dict(zip(I, map(int, pattern)))
        require(all(ic[a] != sc[b] for a, b in small_cross), 'small cross contacts')

    base, var = cnf(H, g['host_edges'])
    base.append([var(0, 0)])
    blocking = []
    old_projections = set()
    new_projections = set()
    palettes = Counter()
    combined_checked = 0
    parent_minus_310 = [e for e in g['edges'] if 310 not in e]
    L_edges = [e for e in g['edges'] if max(e) < 374]
    for pattern, word in rows:
        hc = proper(word, H, g['host_edges'])
        require(hc[0] == 0, 'origin normalization')
        require(''.join(str(hc[v]) for v in B) == pattern, 'witness restriction')
        require(len(set(pattern)) == 4, 'all boundary patterns use four colours')
        key = tuple(map(int, pattern))
        require(key == min(tuple(p[c] for c in key) for p in PERMS), 'canonical orbit')
        for p in PERMS:
            blocking.append([-var(v, p[hc[v]]) for v in B if v != 0])
        p = min(PERMS, key=lambda p: tuple(p[hc[v]] for v in I))
        ip = ''.join(str(p[hc[v]]) for v in I)
        k = len({hc[v] for v in N})
        palettes[k] += 1
        if k == 4:
            new_projections.add(ip)
            require(ip in ext, 'every rainbow-star projection extends through S')
            inv = {p[c]: c for c in range(4)}
            sc = {v: inv[int(c)] for v, c in zip(S, ext[ip])}
            whole = dict(hc)
            whole.update(sc)
            require(all(whole[a] != whole[b] for a, b in parent_minus_310),
                    'literal full 508-point colouring of parent minus 310')
            combined_checked += 1
        else:
            old_projections.add(ip)
            lc = dict(hc)
            lc[310] = min(set(range(4)) - {hc[v] for v in N})
            require(all(lc[a] != lc[b] for a, b in L_edges), 'L extension')
    require(palettes == {2: 14, 3: 30, 4: 424}, 'palette partition')
    require(len(old_projections) == 20 and len(new_projections) == 424,
            'projection counts')
    require(not old_projections & new_projections, 'disjoint projection sectors')
    require(new_projections == set(ext), 'complete positive small-extension sector')

    five = (HERE / 'parent_five.txt').read_text().strip()
    proper(five, list(range(509)), g['edges'], 5)
    require(set(five) == set('01234'), 'parent proper five-colour word')
    dump_cnf(out / 'completeness.cnf', base + blocking, 4 * len(H))
    parent, pv = cnf(list(range(509)), g['edges'])
    parent.append([pv(0, 0)])
    dump_cnf(out / 'parent.cnf', parent, 2036)
    (out / 'geometry.json').write_text(json.dumps(g, separators=(',', ':')) + '\n')
    result = {
        'parent_points': 509, 'parent_complete_unit_edges': len(g['edges']),
        'exact_unordered_pairs': g['unordered_pairs'],
        'host_points': len(H), 'host_complete_unit_edges': len(g['host_edges']),
        'removed_points': len(D), 'removed_internal_edges': len(g['module_edges']),
        'boundary': B, 'cross_edges': len(g['cross_edges']),
        'boundary_edges': boundary_edges,
        'canonical_host_patterns': len(rows), 'labelled_host_patterns': 24 * len(rows),
        'neighbour_palette_sizes': {str(k): palettes[k] for k in sorted(palettes)},
        'old_interface_patterns': len(old_projections),
        'new_interface_patterns': len(new_projections),
        'small_side_extension_witnesses': len(ext),
        'parent_minus_310_four_words_checked': combined_checked,
        'parent_five_word_checked': True,
        'replacement_new_point_allowance': 135, 'total_point_cap': 508,
        'complete_relation_requires_checked_completeness_proof': True,
        'original_module_blocking_requires_checked_parent_proof': True,
        'replacement_supplied': False, 'record_candidate': False,
        'completeness_cnf_sha256': digest(out / 'completeness.cnf'),
        'parent_cnf_sha256': digest(out / 'parent.cnf'),
        'host_relation_sha256': digest(HERE / 'host_relation.tsv'),
        'small_extensions_sha256': digest(HERE / 'small_extensions.tsv'),
    }
    expected = HERE / 'expected.json'
    if expected.exists():
        require(result == json.loads(expected.read_text()), 'frozen expected evidence')
    (out / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    print(json.dumps(verify(args.out), indent=2))
