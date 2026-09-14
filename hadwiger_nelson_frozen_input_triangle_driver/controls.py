"""Author controls: separate norm arithmetic and direct full-support search."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd
from pathlib import Path
import hashlib
import json
import verify as V

HERE = Path(__file__).resolve().parent


def independent_norm(z):
    out = {r: 0 for r in V.RAD}
    for axis in (z[:16], z[16:]):
        terms = [(rad, c) for rad, c in zip(V.RAD, axis) if c]
        for r, a in terms:
            for s, b in terms:
                g = gcd(r, s)
                out[r * s // (g * g)] += a * b * g
    return tuple(out[r] for r in V.RAD)


def source_cosets():
    """Rational quadruples in 1,sqrt33,i*sqrt3,i*sqrt11, before embedding."""
    def add(x, y):
        return tuple(a + b for a, b in zip(x, y))
    def neg(x):
        return tuple(-a for a in x)
    def conj(x):
        return x[0], x[1], -x[2], -x[3]
    def mul(x, y):
        a, b, c, d = x
        A, B, C, D = y
        return (a * A + 33 * b * B - 3 * c * C - 11 * d * D,
                a * B + b * A - c * D - d * C,
                a * C + c * A + 11 * (b * D + d * B),
                a * D + d * A + 3 * (b * C + c * B))
    one, zero = (F(1), F(0), F(0), F(0)), (F(0),) * 4
    w, eta = (F(1, 2), F(0), F(1, 2), F(0)), (F(0), F(1, 6), F(1, 6), F(0))
    powers = [one]
    for _ in range(5):
        powers.append(mul(powers[-1], w))
    seeds = [one, add(eta, neg(conj(eta))), add(eta, neg(mul(conj(eta), w))),
             eta, add(one, mul(eta, powers[2])), conj(eta), add(one, conj(mul(eta, powers[2])))]
    full = [zero] + sorted({mul(a, b) for a in seeds for b in powers})
    keep = (0, 5, 6, 9, 12, 13, 16, 17, 18, 19, 20, 22, 24, 25, 26,
            27, 28, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42)
    V.need(len(full) == 43, '43-point source pool')
    rows = [[c * 12 for c in full[i]] for i in keep]
    V.need(all(c.denominator == 1 for row in rows for c in row), 'source denominator')
    return [[int(c) for c in row] for row in rows]


def main():
    cert = json.loads((HERE / 'certificate.json').read_text())
    expected = json.loads((HERE / 'expected.json').read_text())
    V.need(V.verify(cert) == expected, 'main replay')
    src = json.loads((HERE / 'source_points.json').read_text())
    V.need(source_cosets() == src['frozen_rows'], 'F29 fixture versus coset reconstruction')
    points, edges, ge, fe, maps = V.geometry()
    for i, j in combinations(range(len(points)), 2):
        z = tuple(a - b for a, b in zip(points[i], points[j]))
        V.need(independent_norm(z) == V.norm(z), 'complete norm coefficient agreement')

    # Independently normalize all named inputs, rather than using restricted
    # growth sequences to justify the colour-name quotient.
    def normalize(w):
        seen = {}
        return ''.join(str(seen.setdefault(c, len(seen))) for c in w)
    domain = sorted({normalize(w) for w in product(range(4), repeat=8)})
    V.need(domain == list(V.patterns(8)), 'complete input quotient')
    # Here the whole 120-point graph is searched directly. The triangle
    # extension construction and the endpoint-elimination criterion are not
    # used to construct these words or prune this search.
    yes, no, nodes = 0, 0, 0
    word_hash = hashlib.sha256()
    for w in domain:
        domains = [15] * len(points)
        for v, c in zip(V.TERMINALS, w):
            domains[v] = 1 << int(c)
        answer, counts = V.search(len(points), edges, domains)
        nodes += counts['nodes']
        V.need((answer is not None) == (V.core_word(w) is not None), 'full-support relation disagreement')
        if answer is None:
            no += 1
        else:
            word = ''.join(map(str, answer))
            V.check_word(word, len(points), edges, zip(V.TERMINALS, w))
            word_hash.update((word + '\n').encode())
            yes += 1

    broken = []
    x = deepcopy(cert); x['edges'].pop(); broken.append(x)
    x = deepcopy(cert); x['edges'].append([16, 42]); broken.append(x)
    x = deepcopy(cert); x['maps'][0][0] = 6; broken.append(x)
    x = deepcopy(cert); x['maps'][1][1] = x['maps'][0][1]; broken.append(x)
    x = deepcopy(cert); x['source_four_colour_word'] = '0' * 29; broken.append(x)
    x = deepcopy(cert); x['source_four_colour_word'] = x['source_four_colour_word'][:-1]; broken.append(x)
    x = deepcopy(cert); x['schema'] = True; broken.append(x)
    for bad in broken:
        try:
            V.verify(bad)
        except ValueError:
            continue
        raise ValueError('bad certificate accepted')
    print(json.dumps({'status': 'CONTROLS_PASS', 'full_pair_norm_comparisons': 7140,
                      'source_coset_points': 43, 'source_fixture_matched': True,
                      'labelled_assignments_normalized': 65536,
                      'full_support_pattern_queries': len(domain), 'positive': yes, 'negative': no,
                      'full_search_nodes': nodes, 'direct_positive_word_stream_sha256': word_hash.hexdigest(),
                      'rejected_corruptions': len(broken)}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
