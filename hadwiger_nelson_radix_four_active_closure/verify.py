#!/usr/bin/env python3
"""Independent standard-library checker: direct pairs, norm expansion, edge masks.

Imports no producer, ancestor implementation, CAS, SAT solver or raw export.
Every finite witness is reconstructed and checked, not inferred from a count.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRIANGLE = ((0, 0), (1, 0), (0, 1))
UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
LABELS = tuple(product(range(3), repeat=5))
FM = ((0, 0, 0, 0), (0, 1, 2, 3), (0, 2, 3, 1), (0, 3, 1, 2))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def times(z, w):
    a, b = z
    c, d = w
    return a * c - b * d, (a + b) * (c + d) - a * c


def canonical(row):
    return min(tuple(times(u, d) for d in row) for u in UNITS)


def plus(a, b, scalar=1):
    out = dict(a)
    for monomial, value in b.items():
        out[monomial] = out.get(monomial, 0) + scalar * value
    return {key: value for key, value in out.items() if value}


def pmul(a, b):
    out = defaultdict(int)
    for (i, j), c in a.items():
        for (k, l), d in b.items():
            out[i + k, j + l] += c * d
    return {key: value for key, value in out.items() if value}


def primitive(poly):
    poly = {key: value for key, value in poly.items() if value}
    if not poly:
        return ()
    divisor = 0
    for value in poly.values():
        divisor = gcd(divisor, value)
    if poly[max(poly)] < 0:
        divisor = -divisor
    return tuple((i, j, c // divisor) for (i, j), c in sorted(poly.items()))


def radix_powers():
    # z = (x-y)+2*y*omega in the integral basis (1,omega).
    a, b = {(1, 0): 1, (0, 1): -1}, {(0, 1): 2}
    powers = [({(0, 0): 1}, {})]
    for _ in range(4):
        c, d = powers[-1]
        powers.append((plus(pmul(a, c), pmul(b, d), -1),
                       plus(plus(pmul(a, d), pmul(b, c)), pmul(b, d))))
    return powers


def event(row, powers):
    a, b = {}, {}
    for (c, d), (p, q) in zip(row, powers):
        a = plus(plus(a, p, c), q, -d)
        b = plus(plus(b, q, c + d), p, d)
    norm = plus(plus(pmul(a, a), pmul(a, b)), pmul(b, b))
    return primitive(plus(norm, {(0, 0): 1}, -1))


def inventory():
    groups = defaultdict(list)
    for u, v in combinations(range(243), 2):
        row = tuple((TRIANGLE[a][0] - TRIANGLE[b][0], TRIANGLE[a][1] - TRIANGLE[b][1])
                    for a, b in zip(LABELS[u], LABELS[v]))
        groups[canonical(row)].append((u, v))
    require(len(groups) == 2801, 'all difference classes')
    require(sum(map(len, groups.values())) == 29403, 'all unordered pairs')
    powers = radix_powers()
    circle = primitive({(2, 0): 1, (0, 2): 3, (0, 0): -1})
    curves, base, monomials = {}, [], []
    for row, edges in sorted(groups.items()):
        support = [i for i, d in enumerate(row) if d != (0, 0)]
        if len(support) == 1:
            monomials.append(support[0])
            if support[0] == 0:
                base += edges
            continue
        f = event(row, powers)
        require(f and f != circle and f not in curves, 'distinct nonmonomial norm event')
        curves[f] = row, edges
    require(sorted(monomials) == list(range(5)), 'five monomial classes')
    require(len(base) == 243, 'first-digit triangles')
    factors = sorted(list(curves) + [circle])
    data = {i: curves[f] for i, f in enumerate(factors) if f != circle}
    require(len(data) == 2796, 'noncircle curves')
    return factors, factors.index(circle), data, base


def colour4(weights, label):
    colour = 0
    for w, a in zip(weights, label):
        colour ^= FM[w][a]
    return colour


def signature_checked(row, edges, words4, colours4):
    values = [(a & 1) ^ ((b & 1) << 1) for a, b in row]
    pivot = next(v for v in values[1:] if v)
    inverse = next(v for v in range(1, 4) if FM[pivot][v] == 1)
    normal = tuple(FM[inverse][v] for v in values[1:])
    constant = FM[inverse][values[0]]
    actual = 0
    predicted = 0
    for i, (w, col) in enumerate(zip(words4, colours4)):
        if any(col[u] == col[v] for u, v in edges):
            actual |= 1 << i
        total = 0
        for n, a in zip(normal, w[1:]):
            total ^= FM[n][a]
        if total == constant:
            predicted |= 1 << i
    require(actual == predicted and actual.bit_count() == 64, 'direct F4 edge mask equals affine hyperplane')
    return normal, constant


def first_clique_bits(adjacency):
    all_vertices = (1 << len(adjacency)) - 1
    for a, neighbours in enumerate(adjacency):
        bs = neighbours & (all_vertices ^ ((1 << (a + 1)) - 1))
        while bs:
            b_bit = bs & -bs
            bs ^= b_bit
            b = b_bit.bit_length() - 1
            common = neighbours & adjacency[b] & (all_vertices ^ ((1 << (b + 1)) - 1))
            cs = common
            while cs:
                c_bit = cs & -cs
                cs ^= c_bit
                c = c_bit.bit_length() - 1
                ds = common & adjacency[c] & (all_vertices ^ ((1 << (c + 1)) - 1))
                if ds:
                    return a, b, c, (ds & -ds).bit_length() - 1
    raise ValueError('quartet lacks both a three-colouring and a K4 witness')


def check_clique(clique, allowed_edges):
    require(len(clique) == 4 and len(set(clique)) == 4, 'four distinct K4 labels')
    require(all(type(v) is int and 0 <= v < 243 for v in clique), 'K4 label domain')
    require(all(tuple(sorted(e)) in allowed_edges for e in combinations(clique, 2)), 'all six K4 edges')


def compute():
    factors, circle, data, base = inventory()
    words3 = [(1,) + w for w in product(range(3), repeat=4)]
    colours3 = [[sum(w * a for w, a in zip(weights, label)) % 3 for label in LABELS] for weights in words3]
    words4 = [(1,) + w for w in product(range(4), repeat=4)]
    colours4 = [[colour4(weights, label) for label in LABELS] for weights in words4]
    require(all(col[u] != col[v] for col in colours3 + colours4 for u, v in base), 'all words colour universal edges')
    masks, buckets = {}, defaultdict(list)
    for cid, (row, edges) in sorted(data.items()):
        # No displacement dot product is used for the F3 mask in this checker.
        masks[cid] = sum(1 << i for i, col in enumerate(colours3) if any(col[u] == col[v] for u, v in edges))
        buckets[signature_checked(row, edges, words4, colours4)].append(cid)
    normals = sorted({n for n, c in buckets})
    patterns = [tuple((n, c) for c in range(4)) for n in normals if all((n, c) in buckets for c in range(4))]
    require(len(normals) == 85 and len(buckets) == 336 and len(patterns) == 81, 'complete affine partition inventory')
    full = (1 << 81) - 1
    counts, supports, word_hist = Counter(), defaultdict(Counter), Counter()
    transcript = hashlib.sha256()
    obstruction_map, arities = {}, Counter()
    base_set = set(base)
    owners = {e: cid for cid, (_, edges) in data.items() for e in edges}
    for pattern in patterns:
        support = sum(bool(v) for v in pattern[0][0])
        for quartet in product(*(buckets[s] for s in pattern)):
            available = full
            for cid in quartet:
                available &= ~masks[cid]
            if available:
                wi = (available & -available).bit_length() - 1
                require(all(not (masks[cid] & (1 << wi)) for cid in quartet), 'all four edge groups coloured')
                record = [list(quartet), 'F3', wi]
                counts['linear_three_colourings'] += 1
                supports[support]['linear_three_colourings'] += 1
                word_hist[wi] += 1
            else:
                edges = base_set.union(*(set(data[cid][1]) for cid in quartet))
                adjacency = [0] * 243
                for u, v in edges:
                    adjacency[u] |= 1 << v
                    adjacency[v] |= 1 << u
                clique = first_clique_bits(adjacency)
                check_clique(clique, edges)
                obstruction = tuple(sorted({owners[e] for e in combinations(clique, 2) if e in owners}))
                require(set(obstruction) <= set(quartet), 'clique uses only claimed events')
                obstruction_map.setdefault(obstruction, clique)
                arities[len(obstruction)] += 1
                record = [list(quartet), 'K4', list(clique)]
                counts['impossible_planar_K4'] += 1
                supports[support]['impossible_planar_K4'] += 1
            transcript.update(json.dumps(record, separators=(',', ':')).encode() + b'\n')
    obstructions = [[list(q), list(w)] for q, w in sorted(obstruction_map.items())]
    for q, clique in obstructions:
        check_clique(clique, base_set.union(*(set(data[cid][1]) for cid in q)))
    interface = {
        'schema': 'hn-radix-four-active-forbidden-incidences-v1',
        'circle_id': circle, 'curve_inventory_sha256': digest(factors),
        'label_order': 'lexicographic product(range(3),repeat=5); digits=(0,1,omega)',
        'forbidden_curve_sets_with_K4_labels': obstructions,
        'scope': 'Each listed active-curve set is impossible at every complex z, even with further active curves or label coincidences. This is a sufficient list, not an exhaustive census of forbidden incidences.',
    }
    return {
        'schema': 'hn-radix-four-active-closure-v1',
        'label_vertices': 243, 'label_pairs': 29403, 'difference_classes': 2801,
        'universal_edges_off_circle': len(base), 'active_curves': len(factors),
        'circle_id': circle, 'curve_inventory_sha256': digest(factors),
        'F3_word_count': 81, 'F4_affine_word_count': 256,
        'realized_hyperplanes': len(buckets), 'eligible_patterns': len(patterns),
        'eligible_patterns_sha256': digest(patterns),
        'eligible_quartets': sum(counts.values()), **dict(counts),
        'quartet_classification_by_tail_support': {str(k): dict(v) for k, v in sorted(supports.items())},
        'F3_word_assignment_histogram': {str(k): v for k, v in sorted(word_hist.items())},
        'entrywise_witness_transcript_sha256': transcript.hexdigest(),
        'forbidden_incidence_count': len(obstructions),
        'forbidden_incidence_arity_histogram': {str(k): v for k, v in sorted(Counter(map(len, obstruction_map)).items())},
        'K4_assignment_arity_histogram': {str(k): v for k, v in sorted(arities.items())},
        'forbidden_incidence_list_sha256': digest(obstructions),
        'forbidden_incidence_interface_sha256': digest(interface),
        'unresolved_eligible_quartets': 0, 'minimum_active_curves_for_nonfour': 5,
        'proof_solver_calls': 0, 'proof_CAS_calls': 0, 'record_improvement': False,
    }, interface


def run(certificate_path, export=None):
    certificate = json.loads(Path(certificate_path).read_text())
    result, interface = compute()
    require(result == certificate, 'entrywise witness transcript and certificate fields match')
    if export is not None:
        with Path(export).open('x') as f:
            json.dump(interface, f, sort_keys=True, separators=(',', ':'))
            f.write('\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--export-interface', type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.certificate, args.export_interface), indent=2, sort_keys=True))
