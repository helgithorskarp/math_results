"""Exact metric docking obstruction and positive two-pin certificates; stdlib."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
RAD = (1, 3, 5, 7, 15, 21, 35, 105)
T = (5, 6, 7, 8, 12, 13, 14, 15)


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(x, c):
    return tuple(c * a for a in x)


def mul(x, y):
    from math import gcd
    out = [0] * 8
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            if a and b:
                g = gcd(RAD[i], RAD[j])
                out[RAD.index(RAD[i] * RAD[j] // (g * g))] += a * b * g
    return tuple(out)


def basis(r):
    return tuple(int(x == r) for x in RAD)


def construct_g():
    """Closed complex formulas, independent of the coordinate fixture."""
    z = (0,) * 8
    def pt(x, y=z):
        return tuple(x) + tuple(y)
    A, B = pt(scale(basis(1), -4)), pt(scale(basis(1), 4))
    D = pt(scale(basis(1), 6), scale(basis(15), 2))
    C = pt(z, scale(add(basis(15), basis(7)), 2))
    E = pt(scale(basis(1), -6), scale(basis(15), 2))
    def apices(a, b):
        d = add(b, scale(a, -1))
        rot = pt(scale(mul(basis(3), d[8:]), -1), mul(basis(3), d[:8]))
        return [scale(add(add(a, b), scale(rot, s)), Fraction(1, 2)) for s in (1, -1)]
    xp, xm = apices(D, C)
    yp, ym = apices(E, A)
    first = [A, B, D, C, E, xp, xm, yp, ym]
    return first + [scale(v, -1) for v in first[2:]]


def gnorm(a, b):
    d = add(a, scale(b, -1))
    return add(mul(d[:8], d[:8]), mul(d[8:], d[8:]))


def fnorm(a, b):
    a, b, c, d = (x - y for x, y in zip(a, b))
    return (a*a + 33*b*b + 3*c*c + 11*d*d, 2*a*b + 2*c*d)


def geometry():
    raw = (HERE / 'source_points.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == '9d80a8e7997d5d2780c3ec783dbdc02e6e4678b7454b72787b34a6268188ea99', 'source fixture hash')
    src = json.loads(raw)
    g = [tuple(v) for v in src['coupler_rows']]
    f = [tuple(v) for v in src['frozen_rows']]
    need(src['coupler_denominator'] == 8 and src['frozen_denominator'] == 12, 'denominators')
    need(tuple(src['coupler_radicals']) == RAD, 'radical basis')
    need(g == construct_g(), 'closed coupler formulas')
    need(len(set(g)) == 16 and len(set(f)) == 29, 'distinct source points')
    gd = {(a, b): gnorm(g[a], g[b]) for a, b in combinations(T, 2)}
    fd = {(a, b): fnorm(f[a], f[b]) for a, b in combinations(range(29), 2)}
    # G distances lie in Q(sqrt5,sqrt21); F distances in Q(sqrt33).
    need(all(all(n[i] == 0 for i in (1, 3, 4, 6)) for n in gd.values()), 'G distance field')
    rational_g = {ab: Fraction(n[0], 64) for ab, n in gd.items() if not any(n[1:])}
    rational_f = {ab: Fraction(n[0], 144) for ab, n in fd.items() if n[1] == 0}
    # The distinct squarefree radicals 1,sqrt5,sqrt21,sqrt105,sqrt33
    # are Q-linearly independent. Thus equal cross-source distances must
    # be rational. Compare all rational candidates exactly.
    compatible = sorted(ab for ab, q in rational_g.items() if q in rational_f.values())
    need(compatible == [(5, 6), (7, 8), (12, 13), (14, 15)], 'compatible pair graph')
    need(all(Fraction(gd[ab][0], 64) == 3 for ab in compatible), 'shared squared distance')
    need(all(sum(t in ab for ab in compatible) == 1 for t in T), 'compatible graph is a matching')
    fpairs = sorted(ab for ab, q in rational_f.items() if q == 3)
    need(len(fpairs) == 17, 'all compatible F29 pairs')
    edges = sorted(ab for ab, n in fd.items() if n == (144, 0))
    need(len(edges) == 75, 'complete F29 unit graph')
    return g, f, gd, fd, rational_g, rational_f, compatible, fpairs, edges


def verify(cert):
    g, f, gd, fd, rg, rf, compatible, fpairs, edges = geometry()
    need(set(cert) == {'schema', 'pair_words'} and cert['schema'] == 1, 'certificate schema')
    expected = [(a, b, c) for a, b in fpairs for c in (0, 1)]
    need(len(cert['pair_words']) == len(expected), 'certificate coverage')
    for row, (a, b, c) in zip(cert['pair_words'], expected):
        need(set(row) == {'pair', 'second_colour', 'word'}, 'row fields')
        need(row['pair'] == [a, b] and row['second_colour'] == c, 'ordered pin request')
        w = row['word']
        need(isinstance(w, str) and len(w) == 29 and set(w) <= set('0123'), 'proper word alphabet')
        need(w[a] == '0' and w[b] == str(c), 'pinned colours')
        need(all(w[u] != w[v] for u, v in edges), 'monochromatic unit edge')
    hist = {}
    for q in rf.values():
        hist[str(q)] = hist.get(str(q), 0) + 1
    return {'status': 'VERIFIED_DIRECT_DOCKING_FAILURE',
            'source_orders': [16, 29], 'coupler_terminal_pair_checks': len(gd),
            'F29_complete_pair_checks': len(fd), 'F29_unit_edges': len(edges),
            'rational_coupler_terminal_pairs': [[*ab, str(q)] for ab, q in rg.items()],
            'F29_rational_distance_histogram': dict(sorted(hist.items())),
            'compatible_terminal_pairs': [list(ab) for ab in compatible],
            'maximum_terminal_overlap_under_any_real_isometry': 2,
            'F29_compatible_pairs': len(fpairs), 'positive_pair_words': len(expected),
            'word_edge_checks': len(expected)*len(edges),
            'eight_pin_docking_realizable': False, 'record_signal': False}


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--check-expected', action='store_true')
    args = ap.parse_args()
    out = verify(json.loads((HERE / 'certificate.json').read_text()))
    if args.check_expected:
        need(out == json.loads((HERE / 'expected.json').read_text()), 'expected output')
    print(json.dumps(out, indent=2))
