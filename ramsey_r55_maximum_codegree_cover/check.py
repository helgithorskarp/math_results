"""Check the complete cover data and failed-method controls, using integers.

This is NOT a proof checker for a good43 nonexistence certificate. No case is
closed by this package. Catalogue completeness is an explicit external premise.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from graphs import (SEEDS, clique_masks, complement, cyclic_core, decode,
                    frame, good, maximum_codegree, require)

HERE = Path(__file__).resolve().parent
RAMSEY = {(1, t): 1 for t in range(1, 6)}
RAMSEY.update({(2, t): t for t in range(2, 6)})
RAMSEY.update({(3, 3): 6, (3, 4): 9, (3, 5): 14,
               (4, 4): 18, (4, 5): 25})
RAMSEY.update({(b, a): v for (a, b), v in list(RAMSEY.items())})


def check_catalogues():
    manifest = json.loads((HERE / 'catalogue_manifest.json').read_text())
    counts = {}
    for c in (10, 11, 12, 13):
        data = (HERE / 'catalog' / f'r35_{c}.g6').read_bytes()
        meta = manifest[str(c)]
        require(sha256(data).hexdigest() == meta['sha256'], 'catalogue hash')
        rows = data.decode('ascii').splitlines()
        require(len(rows) == meta['count'], 'catalogue count')
        require(len(rows) == len(set(rows)), 'literal duplicate catalogue row')
        for s in rows:
            a = decode(s)
            require(len(a) == c and good(a, 3, 5), 'invalid catalogue graph')
        counts[str(c)] = len(rows)
    # Integer check of the Goodman lower bound used in the written proof.
    require(43 * 441 == 18963, 'degree product bound')
    require(12341 - 18962 // 2 == 2860, 'triangle lower bound')
    require(3 * 2860 > 903 * 9, 'maximum codegree lower bound')
    return counts


def check_orbits():
    h = cyclic_core()
    require(good(h, 3, 5), 'cyclic core is not (3,5)')
    independent4 = list(clique_masks(complement(h), 4))
    transversals = [s for s in range(1 << 13)
                    if all(s & q for q in independent4)]
    hist = Counter(s.bit_count() for s in transversals)
    require(hist == {5: 65, 6: 416, 7: 910, 8: 1014, 9: 676,
                     10: 286, 11: 78, 12: 13, 13: 1}, 'transversal census')
    orbits = []
    for seed in SEEDS.values():
        orbit = set()
        for m in (1, 5, 8, 12):
            for b in range(13):
                perm = [(m * x + b) % 13 for x in range(13)]
                require(all(((h[u] >> v) & 1) ==
                            ((h[perm[u]] >> perm[v]) & 1)
                            for u, v in combinations(range(13), 2)),
                        'not a core automorphism')
                orbit.add(sum(1 << perm[x] for x in seed))
        orbits.append(orbit)
    require([len(o) for o in orbits] == [52, 13], 'orbit sizes')
    require(not (orbits[0] & orbits[1]), 'orbit overlap')
    require(orbits[0] | orbits[1] ==
            {s for s in transversals if s.bit_count() == 5}, 'orbit cover')
    # Full automorphism-group enumeration is unnecessary: these explicit
    # automorphisms already cover all 65 five-point transversals.
    return {'independent4': len(independent4), 'size5_orbits': [52, 13]}


def check_capacity_certificate(path):
    cert = json.loads(path.read_text())
    a = frame(cert['seed'], cert['kind'])
    require(good(a), 'bad fixed frame')
    blue = complement(a)
    allv = (1 << 16) - 1
    denominator = cert['denominator']
    require(type(denominator) is int and denominator > 0, 'denominator')
    entries = cert['weights']
    require(len(entries) == len({m for m, _ in entries}), 'duplicate star')
    cliques = {}
    for color, graph in ((1, a), (0, blue)):
        cliques[color] = [(0, 0)] + [(q, k) for k in range(1, 5)
                                                for q in clique_masks(graph, k)]
    for mask, weight in entries:
        require(type(mask) is int and 0 <= mask <= allv and
                type(weight) is int and weight > 0, 'invalid weight or mask')
        require(mask & 3 != 3, 'root common-neighborhood extension')
        require(all(mask & q != q for q, k in cliques[1] if k == 4),
                'new red K5')
        require(all(mask & q != 0 for q, k in cliques[0] if k == 4),
                'new blue K5')
        for v in range(16):
            common = (a[v] & mask) if mask >> v & 1 else (blue[v] & (allv ^ mask))
            require(common.bit_count() <= 13, 'new edge codegree')
    total = sum(w for _, w in entries)
    require(total >= 27 * denominator, 'insufficient relaxation mass')
    # Also compatible with the external R(5,5)<=46 mass bound 29.
    require(total <= 29 * denominator, 'exceeds optional global size bound')
    checked = 0
    for r, kr in cliques[1]:
        for b, kb in cliques[0]:
            if r & b or kr + kb == 0:
                continue
            inside = sum((a[v] & r) == r and (blue[v] & b) == b
                         for v in range(16) if not ((r | b) >> v & 1))
            cap = RAMSEY[5 - kr, 5 - kb] - 1 - inside
            lhs = sum(w for mask, w in entries if mask & r == r and mask & b == 0)
            require(cap >= 0 and lhs <= cap * denominator,
                    f'mixed capacity row {(r, b)}')
            checked += 1
    return {'seed': cert['seed'], 'kind': cert['kind'], 'support': len(entries),
            'mass_numerator': total, 'mass_denominator': denominator,
            'rows_checked_without_deduplication': checked,
            'status': 'EXACT_FEASIBLE_NECESSARY_SYSTEM_NOT_A_GRAPH'}


def check_physical_controls():
    controls = json.loads((HERE / 'physical42_controls.json').read_text())
    require({(x['seed'], x['kind']) for x in controls} ==
            {(s, k) for s in ('5', '6') for k in ('A', 'T')}, 'control coverage')
    for x in controls:
        a = decode(x['graph6'])
        require(len(a) == 42 and good(a), 'not a good42 control')
        require(maximum_codegree(a) == 13, 'control maximum codegree')
        if x['color'] == 0:
            a = complement(a)
        else:
            require(x['color'] == 1, 'invalid color')
        perm = x['permutation']
        require(sorted(perm) == list(range(42)), 'control permutation')
        f = frame(x['seed'], x['kind'])
        require(all(((a[perm[u]] >> perm[v]) & 1) == ((f[u] >> v) & 1)
                    for u, v in combinations(range(16), 2)), 'frame mismatch')
    return {'four_frames_extend_to_order_42': True,
            'new_good43_witnesses': 0, 'status': 'REPRODUCED_PUBLISHED_CONTROLS'}


def check_residual(counts):
    rows = json.loads((HERE / 'residual.json').read_text())['cases']
    expected = [(c, i) for c in (10, 11, 12, 13) for i in range(counts[str(c)])]
    require([(x['c'], x['catalogue_row']) for x in rows] == expected,
            'incomplete cover ledger')
    for x in rows:
        c = x['c']
        k = 41 - c
        require(x['status'] == 'UNRESOLVED' and x['physical_decision'] is None,
                'this package carries no physical exclusion certificate')
        require(x['raw_marked_assignments'] == str(3**k * 2**(c*k + k*(k-1)//2)),
                'raw domain count')
        catalogue = (HERE / 'catalog' / f'r35_{c}.g6').read_text().splitlines()
        spec = {'n': 43, 'maximum_monochromatic_edge_codegree': c,
                'red_root_edge': [0, 1],
                'common_red_core_vertices': list(range(2, c + 2)),
                'core_graph6': catalogue[x['catalogue_row']],
                'exterior_root_states': ['RB', 'BR', 'BB'],
                'exterior_vertices': list(range(c + 2, 43)),
                'all_physical_K5_constraints': True,
                'all_physical_monochromatic_edge_codegrees_at_most_c': True}
        encoded = json.dumps(spec, sort_keys=True, separators=(',', ':')).encode()
        require(x['case_spec_sha256'] == sha256(encoded).hexdigest(),
                'semantic case specification hash')
    return {'cases': len(rows), 'closed': 0, 'unresolved': len(rows)}


def main():
    counts = check_catalogues()
    out = {'catalogue_counts': counts, 'transversal_cover': check_orbits(),
           'capacity_controls': [check_capacity_certificate(p) for p in
                                 sorted((HERE / 'certificates').glob('*.json'))],
           'physical42_controls': check_physical_controls(),
           'physical_residual': check_residual(counts),
           'first_result_gate': 'MISSED_NO_TERMINAL_PHYSICAL_DECISION'}
    require(len(out['capacity_controls']) == 4, 'four capacity certificates required')
    require({(x['seed'], x['kind']) for x in out['capacity_controls']} ==
            {(s, k) for s in ('5', '6') for k in ('A', 'T')}, 'certificate coverage')
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
