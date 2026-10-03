"""Exact original-label footprint proposal; independent AP audit is required."""
from pathlib import Path
from itertools import combinations
from math import gcd, lcm
from hashlib import sha256
import json
import struct
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
out = args.out
out.mkdir(parents=True, exist_ok=True)
started = time.monotonic()
D = [d for d in range(1, 316) if 315 % d == 0]
A = {d: [0]*d for d in D}
for y in range(315):
    for d in D:
        A[d][y % d] |= 1 << y
R = {
    'O': sum(1 << y for y in range(315) if y % 9 != 0 and y % 5 != 1 and y % 7 != 1),
    'E2': sum(1 << y for y in range(315) if y % 9 != 0 and y % 3 != 1),
    'E4': sum(1 << y for y in range(315) if y % 9 != 0),
}
M = {t: {d: max((r & v).bit_count() for v in A[d]) for d in D} for t, r in R.items()}
S = {}
stars = []
for t, r in R.items():
    table = {}
    phase_count = 0
    digest = sha256()
    rows = []
    with (out/('star-'+t+'.bin')).open('wb') as stream:
        for u in D:
            for v, w in combinations([d for d in D if d != u], 2):
                best, witness = -1, None
                guv, guw = gcd(u, v), gcd(u, w)
                for au in range(u):
                    singleton = r & A[u][au]
                    for av in range(au % guv, v, guv):
                        first = singleton & A[v][av]
                        for aw in range(au % guw, w, guw):
                            hit = (first | (singleton & A[w][aw])).bit_count()
                            raw = struct.pack('<7H', u, v, w, au, av, aw, hit)
                            stream.write(raw)
                            digest.update(raw)
                            phase_count += 1
                            if hit > best:
                                best, witness = hit, [au, av, aw]
                table[(u, v, w)] = best
                rows.append([u, v, w, best, *witness])
    S[t] = table
    stars.append({'parent_type': t, 'triples': len(rows), 'phase_records': phase_count,
                  'all_phase_records_sha256': digest.hexdigest(), 'maxima_rows': rows})
    print(json.dumps({'parent_type': t, 'complete_phase_records': phase_count,
                      'maximum_three16_star': max(table.values())}), flush=True)
parent_types = [('O', 'O'), ('O', 'E2'), ('O', 'E4'), ('E2', 'O'),
                ('E2', 'E2'), ('E2', 'E4'), ('E4', 'O'), ('E4', 'E2')]
results = []
for kind in ('mixed', 'all16'):
    count = 0
    digest = sha256()
    maxima = [-1]*8
    witnesses = [None]*8
    with (out/(kind+'.bin')).open('wb') as stream:
        for p, q in combinations(D, 2):
            pair_lcm = lcm(p, q)
            unused = [d for d in D if d not in (p, q)]
            for u in unused:
                doubles = D if kind == 'mixed' else [d for d in unused if d != u]
                for v, w in combinations(doubles, 2):
                    triple_lcm = lcm(u, v, w)
                    capacities = [M[r][pair_lcm] +
                                  (M[t][triple_lcm] if kind == 'mixed' else S[t][(u, v, w)])
                                  for r, t in parent_types]
                    raw = struct.pack('<13H', p, q, u, v, w, *capacities)
                    stream.write(raw)
                    digest.update(raw)
                    count += 1
                    for i, value in enumerate(capacities):
                        if value > maxima[i]:
                            maxima[i], witnesses[i] = value, [p, q, u, v, w]
    results.append({'kind': kind, 'complete_original_label_records': count,
                    'all_records_sha256': digest.hexdigest(),
                    'ordered_parent_type_maxima': maxima,
                    'original_cofactor_witnesses': witnesses})
    print(json.dumps(results[-1]), flush=True)
result = {'agent': 'six-covering-3', 'role': 'researcher',
          'status': 'PRODUCER_ONLY_INDEPENDENT_AP_AUDIT_REQUIRED',
          'divisors': D, 'P_uncovered_parent_counts': {t: r.bit_count() for t, r in R.items()},
          'single_projection_maxima': M, 'stars': stars,
          'ordered_parent_types': parent_types, 'coupled_label_cases': results,
          'maximum_five_class_footprint_candidate': max(max(r['ordered_parent_type_maxima']) for r in results),
          'uniform_six_TAIL_claimed': False, 'actual_completed_BASE_H_witness_claimed': False,
          'seconds': time.monotonic()-started}
(out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k not in ('stars', 'single_projection_maxima')}, indent=2))
