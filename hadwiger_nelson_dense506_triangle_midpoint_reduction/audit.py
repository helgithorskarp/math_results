#!/usr/bin/env python3
"""Independent quotient-ring polarization and exhaustive within-fibre triples."""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / 'hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py'
if sha256(SOURCE.read_bytes()).hexdigest() != '9b7e9de99164784b1e7504800442bc1931ecdcaf5217cbae4382b026187e3b72':
    raise ValueError('independent arithmetic pin')
spec = importlib.util.spec_from_file_location('reviewer_arithmetic', SOURCE)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    source = ROOT / 'hadwiger_nelson_nonmono159_214_lowden2'
    host = R.build_host(R.read_source(source / 'points159.tsv', 159),
                        R.read_source(source / 'points214.tsv', 214), -1)
    raw = (ROOT / 'hadwiger_nelson_dense506_two_point_extension/host_colors.txt').read_bytes()
    R.require(sha256(raw).hexdigest() == '010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4', 'colour pin')
    colors = list(map(int, raw.decode().strip()))
    groups = defaultdict(list)
    vectors, norms = {}, {}
    for i in range(506):
        for j in range(i + 1, 506):
            if colors[i] == colors[j]:
                continue
            key = (R.add(host[i], host[j]), tuple(sorted((colors[i], colors[j]))))
            groups[key].append((i, j))
            vectors[i, j] = R.sub(host[j], host[i])
            norms[i, j] = R.norm(vectors[i, j])
    fibres = sorted((pal, pairs) for (_, pal), pairs in groups.items())
    actual_fibres = [[list(pal), [list(pair) for pair in pairs]] for pal, pairs in fibres]
    R.require(actual_fibres == json.loads((args.work / 'fibres.json').read_text()), 'all fibre entries')
    # This uses three squared norms to recover twice the scalar product,
    # rather than the primary real-coordinate dot product.
    four = R.scale(R.ONE, 4 * R.D ** 2)
    edges, edge_set = [], set()
    tested = triples = obstructed = 0
    for pairs in groups.values():
        for a, b in combinations(pairs, 2):
            tested += 1
            s, t = norms[a], norms[b]
            twice_dot = R.sub(R.add(s, t), R.norm(R.sub(vectors[a], vectors[b])))
            delta = R.sub(R.sub(four, s), t)
            lhs = R.multiply(R.multiply(delta, delta), R.multiply(s, t))
            rhs = R.multiply(R.multiply(R.sub(four, s), R.sub(four, t)),
                             R.multiply(twice_dot, twice_dot))
            if lhs == rhs:
                edges.append(a + b)
                edge_set.add((a, b))
        for a, b, c in combinations(pairs, 3):
            triples += 1
            obstructed += ((a, b) in edge_set and (a, c) in edge_set and (b, c) in edge_set)
    edges.sort()
    R.require([list(e) for e in edges] == json.loads((args.work / 'edges.json').read_text()), 'all compatibility edge entries')
    R.require(obstructed == 0, 'compatible host-pair triple')
    print(json.dumps({
        'root': -1, 'enumeration': 'every within-fibre host-pair triple',
        'host_pair_pairs_tested': tested, 'host_pair_triples_tested': triples,
        'compatibility_edges': len(edges), 'compatibility_triangles': obstructed,
        'fibres_sha256': R.digest(fibres), 'edges_sha256': R.digest(edges),
        'all_fibre_and_edge_entries_match': True,
        'modular_or_floating_point_filters': 0,
    }, indent=2))


if __name__ == '__main__':
    main()
