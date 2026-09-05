"""Exact spectra and the complete collision set of the fixed sum H+rM."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from hashlib import sha256
import argparse, json, math, time
import field as F


def canonical(a, d):
    assert d > 0 and len(a) == 24
    common = math.gcd(d, *a)
    return tuple(x//common for x in a), d//common


def spectrum(points, d):
    pairs = [(i, j, canonical(F.norm(F.sub(points[i], points[j])), d*d))
             for i, j in combinations(range(len(points)), 2)]
    norms = sorted({n for i, j, n in pairs})
    index = {n: i for i, n in enumerate(norms)}
    return {'norms': norms, 'pairs': [[i, j, index[n]] for i, j, n in pairs],
            'multiplicities': [sum(n == v for i, j, v in pairs) for n in norms]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    H, M, d = F.construction()
    hs, ms = spectrum(H, d), spectrum(M, d)
    common = set(hs['norms']) & set(ms['norms'])
    assert common == {(F.ONE, 1)}
    hd = {F.sub(a, b) for a in H for b in H if a != b}
    md = {F.sub(a, b) for a in M for b in M if a != b}
    hn = {a: F.norm(a) for a in hd}
    mn = {b: F.norm(b) for b in md}
    rotations = Counter()
    comparisons = 0
    for a in sorted(hd):
        for b in sorted(md):
            comparisons += 1
            if hn[a] == mn[b]:
                assert hn[a] == F.scale(F.ONE, d*d)
                # |b/d|=1, so a/b=(a/d)*conjugate(b/d).
                rotations[canonical(F.mul(a, F.conjugate(b)), d*d)] += 1
    cert = {'coordinate_denominator': d, 'H': hs, 'M': ms}
    certificate_raw = (json.dumps(cert, separators=(',', ':'))+'\n').encode()
    (args.out/'certificate.json').write_bytes(certificate_raw)
    rows = [{'r': r, 'multiplicity': rotations[r]} for r in sorted(rotations)]
    rotation_raw = (json.dumps(rows, separators=(',', ':'))+'\n').encode()
    (args.out/'rotations.json').write_bytes(rotation_raw)
    result = {'status': 'ALL COLLISION ROTATIONS ARE THE252 PREVIOUSLY CLOSED ROTATIONS',
              'H_squared_distances': len(hs['norms']), 'M_squared_distances': len(ms['norms']),
              'H_pair_checks': len(hs['pairs']), 'M_pair_checks': len(ms['pairs']),
              'H_rational_squared_distances': [[list(n), den] for n, den in hs['norms'] if not any(n[1:])],
              'M_rational_squared_distances': [[list(n), den] for n, den in ms['norms'] if not any(n[1:])],
              'common_squared_distances': [[list(n), den] for n, den in sorted(common)],
              'H_directed_differences': len(hd), 'M_directed_differences': len(md),
              'difference_pair_comparisons': comparisons,
              'equal_length_difference_pairs': sum(rotations.values()),
              'collision_rotations': len(rotations),
              'collision_multiplicity_histogram': dict(sorted(Counter(rotations.values()).items())),
              'certificate_sha256': sha256(certificate_raw).hexdigest(),
              'rotation_stream_sha256': sha256(rotation_raw).hexdigest(),
              'new_graphs_constructed': 0, 'native_solver_calls': 0}
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-start})+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
