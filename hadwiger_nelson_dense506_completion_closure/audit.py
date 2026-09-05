#!/usr/bin/env python3
"""Audit every geometric pair with reviewer-1's independent quotient-ring arithmetic."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from math import comb
from pathlib import Path
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REVIEW = ROOT / 'hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py'
REVIEW_PIN = '9b7e9de99164784b1e7504800442bc1931ecdcaf5217cbae4382b026187e3b72'
POINT_PIN = '3bcfcab7e411f6adff3426ceb1cfff97718d634fe41a0e7a71982a57995c4c45'


def audit(work):
    if sha256(REVIEW.read_bytes()).hexdigest() != REVIEW_PIN:
        raise ValueError('review checker pin')
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('review_geometry', REVIEW)
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    table = json.loads((work / 'candidates.json').read_text())
    R.require(R.digest(table['points']) == POINT_PIN, 'complete candidate set pin')
    added = [R.decode_candidate(row) for row in table['points']]
    raw = (HERE / 'colors.txt').read_bytes()
    R.require(len(raw) == 1927 and raw[-1:] == b'\n' and set(raw[:-1]) <= set(b'0123'), 'colour encoding')
    colors = [int(chr(x)) for x in raw[:-1]]
    source = ROOT / 'hadwiger_nelson_nonmono159_214_lowden2'
    a = R.read_source(source / 'points159.tsv', 159)
    v = R.read_source(source / 'points214.tsv', 214)
    R.require(R.ROOT_Z ** 2 % R.PRIME == 33 and
              R.ROOT_R ** 2 % R.PRIME == (-408 + 72 * R.ROOT_Z) % R.PRIME,
              'invalid modular homomorphism')
    basis = [tuple(int(i == j) for j in range(8)) for i in range(8)]
    for x, y in ((x, y) for x in basis for y in basis):
        R.require(R.sigma(R.multiply(x, y)) == R.multiply(R.sigma(x), R.sigma(y)), 'sigma multiplication')
    for x in basis:
        R.require(R.conjugate(R.sigma(x)) == R.sigma(R.conjugate(x)), 'sigma conjugation')
    results = []
    previous = None
    for epsilon in (1, -1):
        host = R.build_host(a, v, epsilon)
        extra = added if epsilon == 1 else [(R.sigma(x), d) for x, d in added]
        points = [(x, R.D) for x in host] + extra
        canonical = [R.normalize(x, d) for x, d in points]
        R.require(len(set(canonical)) == len(points) == 1926, 'distinct points')
        edges, tested = R.graph_edges(points)
        R.require(all(colors[i] != colors[j] for i, j in edges), 'monochromatic geometric edge')
        if previous is not None:
            R.require(previous == edges, 'root graphs differ')
        previous = edges
        # Rebuild all three edge classes; never trust the supplied neighbour/edge lists.
        hedges = [(i, j) for i, j in edges if j < 506]
        neighbors = [[] for _ in extra]
        cedges = []
        for i, j in edges:
            if i < 506 <= j:
                neighbors[j - 506].append(i)
            elif i >= 506:
                cedges.append((i - 506, j - 506))
        R.require(neighbors == table['neighbors'] and [list(e) for e in cedges] == table['candidate_edges'],
                  'entry-level adjacency mismatch')
        # Independent sufficient check of the propagation mechanism via synchronous rounds.
        lists = [{c for c in range(4) if all(colors[h] != c for h in nn)} for nn in neighbors]
        adjacency = [set() for _ in lists]
        for i, j in cedges:
            adjacency[i].add(j)
            adjacency[j].add(i)
        rounds = []
        while True:
            before = [set(s) for s in lists]
            for i, s in enumerate(before):
                if len(s) == 1:
                    for j in adjacency[i]:
                        lists[j] -= s
            R.require(all(lists), 'propagation contradiction')
            changed = sum(s != t for s, t in zip(before, lists))
            if not changed:
                break
            rounds.append({'changed_lists': changed, 'singletons': sum(len(s) == 1 for s in lists)})
        residual = {i for i, s in enumerate(lists) if len(s) > 1}
        remadj = {i: adjacency[i] & residual for i in residual}
        # Forest iff repeated deletion of degree-at-most-one vertices exhausts it.
        peeled = []
        while remadj:
            leaves = sorted(i for i, nn in remadj.items() if len(nn) <= 1)
            R.require(leaves, 'residual contains a cycle')
            peeled.append(len(leaves))
            for i in leaves:
                for j in remadj.pop(i):
                    if j in remadj:
                        remadj[j].discard(i)
        results.append({'root': epsilon, 'pairs_checked': comb(len(points), 2),
                        'exact_tests_after_screen': tested, 'unit_edges': len(edges),
                        'edge_sha256': R.digest(edges), 'host_edges': len(hedges),
                        'host_candidate_edges': sum(map(len, neighbors)), 'candidate_edges': len(cedges),
                        'synchronous_propagation_rounds': rounds,
                        'final_list_size_histogram': dict(sorted(Counter(map(len, lists)).items())),
                        'forest_leaf_peeling_rounds': peeled, 'monochromatic_edges': 0})
    return {'arithmetic_source': 'reviewer-1 generic quotient-ring monomial reduction',
            'screen': {'prime': R.PRIME, 'z': R.ROOT_Z, 'r': R.ROOT_R},
            'both_root_edge_lists_identical': True, 'roots': results,
            'colour_sha256': sha256(raw).hexdigest()}


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(audit(args.work), indent=2))


if __name__ == '__main__':
    main()
