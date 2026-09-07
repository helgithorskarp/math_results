#!/usr/bin/env python3
"""Regenerate the complete fresh-triangle geometry and verify the target-order gate."""
import argparse
import base64
from itertools import product
import json
from pathlib import Path
import gate_geometry
from reproduce import HERE, SEED, require, seed_check, sha


def matching(a, b, c):
    # Explicit system of distinct representatives, independent of Hall's formula.
    for x in range(4):
        if not (a >> x) & 1:
            continue
        for y in range(4):
            if x != y and (b >> y) & 1 and c & ~(1 << x | 1 << y):
                return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    summary = gate_geometry.generate(args.output)
    geometry = json.loads((args.output / 'gate_geometry.json').read_text())
    certificate = json.loads((HERE / 'gate_certificate.json').read_text())
    seed_cert = json.loads((SEED / 'certificate.json').read_text())
    inputs = seed_check.load_inputs(seed_cert)
    labels, rows, swaps = seed_check.construct(seed_cert, inputs)
    edges = seed_check.strict_edges(rows)
    base, _, _ = seed_check.check_colourings(seed_cert, inputs, labels, swaps, edges)
    extra = base64.b64decode(certificate['additional_rows_base64'], validate=True)
    sizes = certificate['additional_family_sizes']
    require(len(sizes) == 509 and all(type(n) is int and n >= 0 for n in sizes),
            'invalid family sizes')
    require(sum(sizes) == certificate['additional_rows'] and len(extra) == 127 * sum(sizes)
            and sha(extra) == certificate['additional_rows_sha256'], 'additional rows mismatch')
    kn = [p['neighbours'] for p in geometry['K_points']]
    nn = [p[:2] for p in geometry['nonK_points']]
    constraints = [tuple(tuple(kn[q]) for q in t) for t in geometry['K_triangles']]
    constraints += [tuple(tuple(nn[q]) for q in t) for t in geometry['nonK_triangles']]
    unique = sorted({tuple(sorted(c)) for c in constraints})
    require(len(unique) == certificate['canonical_neighbour_triples'], 'boundary pattern count')
    position = {c: i for i, c in enumerate(unique)}
    ids = [position[tuple(sorted(c))] for c in constraints]
    table = {(a, b, c): matching(a, b, c) for a, b, c in product(range(16), repeat=3)}
    missed = [[] for _ in unique]
    offset = 0
    for d, count in enumerate(sizes):
        family = [seed_check.unpack(base[127*d:127*(d+1)], d)]
        for _ in range(count):
            word = seed_check.unpack(extra[offset:offset+127], d)
            offset += 127
            require(all(word[a] != word[b] for a, b in edges if d not in (a, b)),
                    'invalid additional seed-deletion word')
            family.append(word)
        covered = set()
        for word in family:
            for i, pattern in enumerate(unique):
                if i in covered:
                    continue
                masks = tuple(15 ^ sum(1 << colour for colour in
                              {word[v] for v in neighbours if v != d}) for neighbours in pattern)
                if table[masks]:
                    covered.add(i)
        for i in range(len(unique)):
            if i not in covered:
                missed[i].append(d)
    declarations = [missed[i] for i in ids]
    nk = len(geometry['K_triangles'])
    kh = {str(n): sum(len(u) == n for u in declarations[:nk])
          for n in sorted({len(u) for u in declarations[:nk]})}
    nh = {str(n): sum(len(u) == n for u in declarations[nk:])
          for n in sorted({len(u) for u in declarations[nk:]})}
    require(kh == certificate['K_U_histogram'] and nh == certificate['nonK_U_histogram'],
            'coverage histogram mismatch')
    require(max(map(len, declarations), default=0) <= 3, 'unresolved four-deletion candidate')
    result = {'all_checks': True, 'geometry': summary, 'seed_deletion_words_checked': 509,
              'additional_words_checked': sum(sizes), 'K_U_histogram': kh,
              'nonK_U_histogram': nh, 'maximum_declared_deletions': max(map(len, declarations)),
              'target_order': 508, 'gate_four_colourable': True}
    (args.output / 'gate_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
