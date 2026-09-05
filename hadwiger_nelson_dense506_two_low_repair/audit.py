#!/usr/bin/env python3
"""Independent grouping-by-neighbour audit with direct quotient-ring norms."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import argparse
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py'
if sha256(SOURCE.read_bytes()).hexdigest() != '9b7e9de99164784b1e7504800442bc1931ecdcaf5217cbae4382b026187e3b72':
    raise ValueError('independent arithmetic source pin')
spec = importlib.util.spec_from_file_location('review_arithmetic', SOURCE)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)


def audit(candidate_work, centre_work, pair_work):
    table = json.loads((centre_work / 'centres.json').read_text())
    pins = {'points': '28b46f5eae9a537d8a189d03284e32d9012fbccde35f05bd72e19ee1f1699f43',
            'host_pairs': 'df22d5b218106b24ee0651fd6b7c8e79038765a75a90a923de507efa8299c8f0',
            'eligible_candidate_neighbors': '3e622b2e34c439bce776300c06890141458f568927e5e476c6dd19d865a13d39'}
    for field, pin in pins.items():
        R.require(R.digest(table[field]) == pin, 'centre identity: ' + field)
    raw = (ROOT / 'hadwiger_nelson_dense506_two_point_extension/host_colors.txt').read_bytes()
    R.require(sha256(raw).hexdigest() == '010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4', 'host colour identity')
    colors = list(map(int, raw.decode().strip()))
    candidate_data = json.loads((candidate_work / 'candidates.json').read_text())
    R.require(R.digest(candidate_data['neighbors']) == '7c71b32a5807e4e9baab0c17953c9e2ba688e7e0d290caa9be6e23b752f564af', 'candidate incidence identity')
    candidate_lists = [set(range(4)) - {colors[v] for v in nn} for nn in candidate_data['neighbors']]
    points = [R.decode_candidate(row) for row in table['points']]
    groups = defaultdict(list)
    palettes = []
    for i, (hp, cn) in enumerate(zip(table['host_pairs'], table['eligible_candidate_neighbors'])):
        palette = tuple(sorted(set(range(4)) - {colors[v] for v in hp}))
        R.require(len(palette) == 2, 'outside list cardinality')
        palettes.append(palette)
        for c in cn:
            R.require(candidate_lists[c] and candidate_lists[c] <= set(palette), 'candidate list eligibility')
            groups[(c, palette)].append(i)
    triples = []
    rows = defaultdict(list)
    for (c, palette), indices in sorted(groups.items()):
        for i, j in combinations(indices, 2):
            triples.append((i, j, c))
            rows[(i, j)].append(c)
    listed = [(i, j, sorted(cs)) for (i, j), cs in sorted(rows.items())]
    primary_pairs = json.loads((pair_work / 'pairs.json').read_text())
    R.require([[i, j, cs] for i, j, cs in listed] == primary_pairs, 'pair grouping entry mismatch')
    certificate = []
    for line in (HERE / 'squared_distances.tsv').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        d, a, b, c, e, multiplicity = map(int, line.split())
        R.require(d > 0 and multiplicity > 0 and gcd(d, a, b, c, e) == 1, 'noncanonical norm row')
        certificate.append(((d, a, b, c, e), multiplicity))
    R.require(len(certificate) == len({row for row, _ in certificate}), 'duplicate norm row')
    summaries = []
    for epsilon in (1, -1):
        pts = points if epsilon == 1 else [(R.sigma(a), d) for a, d in points]
        squared = Counter()
        norm_rows = []
        for i, j, _ in listed:
            a, d = pts[i]
            b, e = pts[j]
            delta = R.sub(R.scale(a, e), R.scale(b, d))
            norm = R.norm(delta)
            R.require(norm != R.scale(R.ONE, (d * e) ** 2), 'unit-distance obstruction')
            R.require(not any(norm[k] for k in (2, 3, 6, 7)), 'imaginary norm')
            values = tuple(Q(norm[k], (d * e) ** 2) for k in (0, 1, 4, 5))
            denominator = lcm(*(x.denominator for x in values))
            key = (denominator,) + tuple(int(x * denominator) for x in values)
            squared[key] += 1
            norm_rows.append((i, j, key))
        expected = certificate if epsilon == 1 else [((d, a, b, -c, -e), n) for (d, a, b, c, e), n in certificate]
        R.require(sorted(squared.items()) == sorted(expected), 'norm spectrum mismatch')
        if epsilon == 1:
            stored = json.loads((pair_work / 'norms.json').read_text())
            R.require([[i, j, list(k)] for i, j, k in norm_rows] == stored, 'every primary norm must match')
        summaries.append({'root': epsilon, 'direct_norm_checks': len(norm_rows),
                          'distinct_squared_distances': len(squared),
                          'norm_stream_sha256': R.digest(norm_rows), 'unit_pairs': 0})
    colour_stream = sha256()
    for i, j, c in sorted(triples):
        cp = min(candidate_lists[c])
        cx = next(x for x in palettes[i] if x != cp)
        R.require(cx in palettes[j], 'outside colour disagreement')
        colour_stream.update(json.dumps([i, j, c, cx, cx, cp], separators=(',', ':')).encode() + b'\n')
    return {'enumeration': 'groups by candidate neighbour and available colour pair',
            'groups': len(groups), 'group_order_histogram': dict(sorted(Counter(map(len, groups.values())).items())),
            'pairs': len(listed), 'common_neighbor_triples': len(triples),
            'pair_sha256': R.digest(listed), 'pair_neighbor_triple_sha256': R.digest(sorted(triples)),
            'all_pair_rows_and_primary_norms_match': True, 'roots': summaries,
            'colouring_stream_sha256': colour_stream.hexdigest(), 'unit_pairs': 0}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate-work', type=Path, required=True)
    p.add_argument('--centre-work', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(audit(args.candidate_work, args.centre_work, args.work), indent=2))


if __name__ == '__main__':
    main()
