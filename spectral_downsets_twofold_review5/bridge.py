#!/usr/bin/env python3
"""Optional byte/hash bridge and two completion-sensitive mutation controls.

An author JSON is comparison data only; it is never a mathematical input to
audit.py. Author source is not imported. No additional dense PSD elimination.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from audit import fixtures, field, matrices, data
from exact import need, matvec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--author-summary', type=Path)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    raw = (here/'expected.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() ==
         '5689f424d65958644c70cfef3d8f829c9a0a9586005078da1aa1cb8b451e16e8',
         'independent summary checksum')
    small, _ = fixtures()
    v, blocks, _ = small[0]
    V, Q, _, record = matrices(v, blocks)
    _, _, _, counts, _ = data(v, sorted(blocks))
    t = F(v-1, v-4)
    damaged = [row[:] for row in Q]
    for i, a in enumerate(V):
        for j, b in enumerate(V):
            if a.bit_count() == b.bit_count() == 1 and a != b:
                damaged[i][j] -= t*(counts[a | b]-1)
    stars = [[F(bool(A >> i & 1)) for A in V] for i in range(v)]
    need(any(matvec(damaged, x) != [F(record['s'])]*len(V) for x in stars),
         'deleting Z must break a star equation on the nonbijective design')
    blocks, _ = field(16)
    V, Q, _, record = matrices(16, blocks)
    sorted_blocks = sorted(blocks)
    _, _, H, _, _ = data(16, sorted_blocks)
    index = {A: i for i, A in enumerate(sorted_blocks)}
    damaged = [row[:] for row in Q]
    t = F(15, 12)
    for i, a in enumerate(V):
        for j, b in enumerate(V):
            if not a & b and a.bit_count() == 1 and b.bit_count() == 3:
                excess = max(H[a.bit_length()-1][index[b]]-1, 0)
                damaged[i][j] += t*excess
                damaged[j][i] += t*excess
    need(any(sum(row) != len(V) for row in damaged),
         'clamping H to a boolean must break a row equation in characteristic two')
    compared = []
    if args.author_summary:
        author = json.loads(args.author_summary.read_text())
        own = {r['v']: r for r in json.loads(raw)['finite']}
        prime = next(r for r in author['primes'] if r['v'] == 13)
        binary = author['binary16']
        pairs = [(13, prime['centered_matrix_sha256'],
                  prime['uniform_maximal']['matrix_sha256']),
                 (16, binary['matrix_sha256'],
                  binary['uniform_maximal']['matrix_sha256'])]
        for v, centered, repaired in pairs:
            need(own[v]['centered_sha256'] == centered and
                 own[v]['repaired_sha256'] == repaired, 'author/independent matrix hash bridge')
            compared.append(v)
    print(json.dumps({'agent': 'six-reviewer-5',
                      'completion_mutation_controls_rejected': 2,
                      'author_matrix_hash_comparisons': 2*len(compared),
                      'compared_orders': compared,
                      'author_data_used_as_PSD_premise': False}, sort_keys=True))


if __name__ == '__main__':
    main()
