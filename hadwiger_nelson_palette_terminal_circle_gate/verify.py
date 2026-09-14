"""Exact finite circle-arrangement gate; Python 3.11 standard library only.

Contacts use field identities or the defining circle-intersection identity.
Noncontacts use rational outward enclosures, never floating-point tolerances.
Every physical pair is classified or verification fails.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import gcd, isqrt
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
RAD = (1, 3, 5, 7, 15, 21, 35, 105)
T = (5, 6, 7, 8, 12, 13, 14, 15)
CELL = ((0, 1), (0, 4), (1, 2), (2, 3), (3, 4), (2, 5),
        (3, 5), (2, 6), (3, 6), (0, 7), (4, 7), (0, 8), (4, 8))
SECOND = (1, 0, 9, 10, 11, 12, 13, 14, 15)


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def r(rad=1, coefficient=0):
    return tuple(F(coefficient) if x == rad else F(0) for x in RAD)


ZERO = r()
ONE = r(1, 1)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(a, k):
    return tuple(k * x for x in a)


def mul(a, b):
    out = [F(0)] * 8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    g = gcd(RAD[i], RAD[j])
                    out[RAD.index(RAD[i] * RAD[j] // (g * g))] += x * y * g
    return tuple(out)


def padd(a, b):
    return add(a[0], b[0]), add(a[1], b[1])


def pscale(a, k):
    return scale(a[0], k), scale(a[1], k)


def sub(a, b):
    return padd(a, pscale(b, -1))


def norm(a):
    return add(mul(a[0], a[0]), mul(a[1], a[1]))


def jmul(a, factor):
    return scale(mul(a[1], factor), -1), mul(a[0], factor)


def original_points():
    p = [(r(1, F(-1, 2)), ZERO), (r(1, F(1, 2)), ZERO),
         (r(1, F(3, 4)), r(15, F(1, 4))),
         (ZERO, add(r(15, F(1, 4)), r(7, F(1, 4)))),
         (r(1, F(-3, 4)), r(15, F(1, 4)))]
    for a, b in ((2, 3), (4, 0)):
        for sign in (1, -1):
            p.append(pscale(padd(padd(p[a], p[b]),
                       pscale(jmul(sub(p[b], p[a]), r(3, 1)), sign)), F(1, 2)))
    return p + [pscale(x, -1) for x in p[2:]]


# Intervals have exact rational endpoints. Only sqrt needs rounding, and its
# dyadic floor/ceiling are proved by integer square comparisons.
def ia(a, b):
    return a[0] + b[0], a[1] + b[1]


def ine(a):
    return -a[1], -a[0]


def im(a, b):
    products = [x * y for x in a for y in b]
    return min(products), max(products)


def isc(a, value):
    return im(a, (F(value), F(value)))


def inv(a):
    need(a[0] > 0, 'interval reciprocal requires positive denominator')
    return 1 / a[1], 1 / a[0]


def sq(a):
    if a[0] <= 0 <= a[1]:
        return F(0), max(a[0] * a[0], a[1] * a[1])
    return min(x * x for x in a), max(x * x for x in a)


def sqrt_bounds(a, bits):
    need(a[0] >= 0 and a[0] <= a[1], 'square-root interval domain')
    denominator = 1 << bits
    endpoints = []
    for x in a:
        n = isqrt((x.numerator * denominator * denominator) // x.denominator)
        lo = F(n, denominator)
        hi = lo if lo * lo == x else F(n + 1, denominator)
        need(lo * lo <= x <= hi * hi, 'integer sqrt enclosure')
        endpoints.append((lo, hi))
    return endpoints[0][0], endpoints[1][1]


def enclosure(a, bits):
    out = (F(0), F(0))
    for coefficient, rad in zip(a, RAD):
        out = ia(out, isc(sqrt_bounds((F(rad), F(rad)), bits), coefficient))
    return out


def box(point, bits):
    return tuple(enclosure(axis, bits) for axis in point)


def norm_box(a, b):
    return ia(sq(ia(a[0], ine(b[0]))), sq(ia(a[1], ine(b[1]))))


def disjoint(a, b):
    return any(x[1] < y[0] or y[1] < x[0] for x, y in zip(a, b))


def physical_graph(bits=80):
    base = original_points()
    points = [{'exact': p, 'box': box(p, bits), 'centres': ()} for p in base]
    need(len(set(base)) == 16, 'original coordinate collision')
    rows, excluded = [], []
    # All 28 terminal pairs, in lexicographic vertex-label order; + root first.
    for i, j in combinations(T, 2):
        d = sub(base[j], base[i])
        n = norm(d)
        ni = enclosure(n, bits)
        need(ni[0] > 0, 'distinct terminal pair')
        if ni[0] > 4:
            excluded.append([i, j])
            continue
        need(ni[1] < 4, 'unresolved circle intersection / tangency')
        m = pscale(padd(base[i], base[j]), F(1, 2))
        k = mul(n, add(r(1, 4), scale(n, -1)))
        ri = sqrt_bounds(enclosure(k, bits), bits)
        factor = isc(im(ri, inv(ni)), F(1, 2))
        for sign in (1, -1):
            exact = None
            # These are all roots in the old core and all additional degree-3
            # points. Their radicals simplify directly in the base field.
            if n == r(1, 3) or n == r(1, F(5, 2)):
                root = r(3, 1) if n == r(1, 3) else r(15, F(1, 2))
                need(mul(root, root) == k, 'simplified radicand identity')
                exact = padd(m, pscale(jmul(d, root), F(sign, 1) / (2 * n[0])))
                bx = box(exact, bits)
                for centre in (i, j):
                    need(norm(sub(exact, base[centre])) == ONE, 'exact root contact')
            else:
                mb, db = box(m, bits), box(d, bits)
                bx = (ia(mb[0], isc(im(db[1], factor), -sign)),
                      ia(mb[1], isc(im(db[0], factor), sign)))
            match = next((v for v, q in enumerate(points)
                          if exact is not None and q['exact'] == exact), None)
            if match is None:
                need(all(disjoint(bx, q['box']) for q in points),
                     'unresolved physical collision')
                match = len(points)
                points.append({'exact': exact, 'box': bx, 'centres': (i, j)})
            rows.append([i, j, sign, match])
    need(sorted(row[3] for row in rows if row[3] < 16) == sorted(set(range(16)) - set(T)),
         'the roots must include each original nonterminal exactly once')
    edges = []
    classifications = {'field_unit': 0, 'circle_identity_unit': 0, 'interval_nonunit': 0}
    # The dyadic margins are intentionally coarse, explicit lower bounds.
    # A successful run proves every distinct squared distance >= 2^-20 and
    # every nonunit squared distance separated from 1 by at least 2^-20.
    margin = F(1, 1 << 20)
    for i, j in combinations(range(len(points)), 2):
        a, b = points[i], points[j]
        enclosure_ij = norm_box(a['box'], b['box'])
        need(enclosure_ij[0] > margin, 'collision-separation margin')
        if a['exact'] is not None and b['exact'] is not None:
            unit = norm(sub(a['exact'], b['exact'])) == ONE
            reason = 'field_unit'
        else:
            unit = i in b['centres'] or j in a['centres']
            reason = 'circle_identity_unit'
        if unit:
            need(enclosure_ij[0] <= 1 <= enclosure_ij[1], 'contact enclosure inconsistency')
            edges.append([i, j])
            classifications[reason] += 1
        else:
            need(enclosure_ij[1] < 1 - margin or enclosure_ij[0] > 1 + margin,
                 'unresolved unit contact')
            classifications['interval_nonunit'] += 1
    old_edges = sorted(set(CELL) | {tuple(sorted((SECOND[a], SECOND[b]))) for a, b in CELL})
    need([tuple(e) for e in edges if e[1] < 16] == old_edges, 'original graph alignment')
    return points, rows, excluded, edges, classifications


def canonical_patterns(n):
    def grow(word):
        if len(word) == n:
            yield ''.join(map(str, word))
        else:
            for colour in range(min(3, max(word, default=-1) + 1) + 1):
                yield from grow(word + (colour,))
    return list(grow(()))


@lru_cache(None)
def endpoint_relation(w):
    p, q = set(w[:2]), set(w[2:])
    out = set()
    for a, b in product('0123', repeat=2):
        if a == b or a in q:
            continue
        for d, c, e in product('0123', repeat=3):
            if d not in p and c not in p and e not in q and d != c and c != e and e != a and d != b:
                out.add((a, b))
                break
    return out


def relation_counts():
    domain = canonical_patterns(8)
    negative = [w for w in domain if not endpoint_relation(w[:4]).intersection(
        (b, a) for a, b in endpoint_relation(w[4:]))]
    return {'domain': len(domain), 'allowed': len(domain) - len(negative),
            'forbidden': len(negative), 'negative_sha256': digest(negative)}


def verify(certificate, bits=80):
    need(set(certificate) == {'schema', 'root_map', 'edges', 'three_colour_word'}, 'certificate fields')
    need(type(certificate['schema']) is int and certificate['schema'] == 1, 'certificate schema')
    points, roots, excluded, edges, kinds = physical_graph(bits)
    need(certificate['root_map'] == roots, 'root-map mismatch')
    need(certificate['edges'] == edges, 'complete edge mismatch')
    word = certificate['three_colour_word']
    need(isinstance(word, str) and len(word) == len(points), 'colour word length')
    need(set(word) <= set('012'), 'three-colour alphabet')
    need(all(word[a] != word[b] for a, b in edges), 'improper colour word')
    need(all(list(e) in edges for e in ((2, 3), (2, 5), (3, 5))), 'unit triangle')
    neighbours = [[u if v == i else v for u, v in edges if i in (u, v)]
                  for i in range(16, len(points))]
    need(all(all(v < 16 for v in nb) and len(nb) <= 3 for nb in neighbours),
         'universal extension premise failed')
    need(len(roots) + 2 * len(excluded) == 56, 'complete pair-root coverage')
    return {'status': 'VERIFIED_NEUTRAL_TERMINAL_CIRCLE_DRIVER',
            'points': len(points), 'unit_edges': len(edges), 'chromatic_number': 3,
            'terminal_pairs': 28, 'intersecting_pairs': len(roots) // 2,
            'disjoint_circle_pairs': len(excluded), 'root_occurrences': len(roots),
            'old_core_root_occurrences': sum(row[3] < 16 for row in roots),
            'new_points': len(neighbours), 'new_point_degree_histogram': {
                str(d): sum(len(nb) == d for nb in neighbours) for d in sorted({len(nb) for nb in neighbours})},
            'new_new_edges': sum(a >= 16 for a, b in edges),
            'new_neighbour_sets': neighbours, 'unit_edge_sha256': digest(edges),
            'root_map_sha256': digest(roots), 'full_pair_checks': len(points) * (len(points) - 1) // 2,
            'classification': kinds, 'dyadic_distance_margin': '1/1048576',
            'restriction_to_all_original_16_vertices_is_surjective': True,
            'terminal_relation_unchanged': relation_counts(), 'record_improved': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--bits', type=int, default=80)
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    need(32 <= args.bits <= 256, 'supported enclosure precision: 32 through 256 bits')
    result = verify(json.loads(args.certificate.read_text()), args.bits)
    if args.check_expected:
        need(result == json.loads((HERE / 'expected.json').read_text()), 'expected result mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))
