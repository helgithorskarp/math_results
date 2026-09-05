"""Independent tensor arithmetic in zeta7, omega6, w=(1+sqrt(-11))/2."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import time

Z = (0,)*24
O = (1,)+Z[1:]


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def scale(a, n): return tuple(n*x for x in a)


def monomial(a, b, c):
    # z^6=-(1+...+z^5), omega^2=omega-1, w^2=w-3.
    z = [(a % 7, 1)] if a % 7 < 6 else [(i, -1) for i in range(6)]
    omega = [(b, 1)] if b < 2 else [(0, -1), (1, 1)]
    ww = [(c, 1)] if c < 2 else [(0, -3), (1, 1)]
    terms = {}
    for (i, x), (j, y), (k, v) in product(z, omega, ww):
        terms[i+6*j+12*k] = x*y*v
    return terms


TABLE = [[monomial(i % 6+j % 6, i//6 % 2+j//6 % 2, i//12+j//12)
          for j in range(24)] for i in range(24)]


def mul(a, b):
    result = [0]*24
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    for k, v in TABLE[i][j].items():
                        result[k] += x*y*v
    return tuple(result)


def zp(a):
    a %= 7
    return tuple(int(i == a) for i in range(24)) if a < 6 else (-1,)*6+(0,)*18


OMEGA = (0,)*6+(1,)+(0,)*17
W = (0,)*12+(1,)+(0,)*11
S = sub(scale(W, 2), O)
T = mul(zp(6), OMEGA)
TP = [O]
for _ in range(11): TP.append(mul(TP[-1], T))
CB = []
for i in range(24):
    value = zp(-(i % 6))
    if i//6 % 2: value = mul(value, sub(O, OMEGA))
    if i//12: value = mul(value, sub(O, W))
    CB.append(value)


def conjugate(a):
    result = Z
    for i, v in enumerate(a): result = add(result, scale(CB[i], v))
    return result


def norm(a): return mul(a, conjugate(a))


def inverse_sine_numerator(k):
    result = Z
    for j in range(7): result = add(result, scale(zp(k+2*k*j), j))
    assert mul(sub(zp(k), zp(-k)), result) == scale(O, 7)
    return result


def decode(row):
    result = Z
    for i in range(12):
        result = add(result, scale(TP[i], row[i]))
        result = add(result, scale(mul(TP[i], S), row[i+12]))
    return result


def proper(c, edges, n):
    return len(c) == n and all(v in range(4) for v in c) and all(c[a] != c[b] for a, b in edges)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    here = Path(__file__).parent
    expected = json.loads((here/'expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (args.work/'graph.json').read_bytes()
    assert sha256(raw).hexdigest() == expected['graph_sha256']
    g = json.loads(raw)
    p = inverse_sine_numerator(4)
    q = scale(mul(sub(O, OMEGA), inverse_sine_numerator(1)), -1)
    r = scale(mul(OMEGA, inverse_sine_numerator(2)), -1)
    hn = [mul(a, zp(j)) for a in [p, q, r] for j in range(7)]
    H = [scale(a, 6) for a in hn]
    u, v = sub(hn[7], hn[0]), sub(hn[14], hn[0])
    dirs = [u, v, add(u, v)]
    M = [Z]+[scale(a, 6) for a in dirs]+[add(scale(a, 4), scale(mul(W, a), 2)) for a in dirs]
    assert H == list(map(decode, g['H'])) and M == list(map(decode, g['M']))
    G = list(map(decode, g['points']))
    assert len(G) == len(set(G)) == 143 and set(G) == {add(a, b) for a in H for b in M}
    index = {p: i for i, p in enumerate(G)}
    representations = [[] for _ in G]
    for a in range(21):
        for b in range(7): representations[index[add(H[a], M[b])]].append([a, b])
    assert representations == g['representations']
    all_edges = []
    for points, supplied in [(H, g['H_edges']), (M, g['M_edges']), (G, g['edges'])]:
        edges = [[i, j] for i, j in combinations(range(len(points)), 2)
                 if norm(sub(points[i], points[j])) == scale(O, 42**2)]
        assert edges == supplied
        all_edges.append(edges)
    he, me, ge = all_edges
    factor = {tuple(sorted([index[add(H[a], m)], index[add(H[b], m)]])) for a, b in he for m in M}
    factor |= {tuple(sorted([index[add(h, M[a])], index[add(h, M[b])]])) for a, b in me for h in H}
    assert factor == set(map(tuple, ge)) == set(map(tuple, g['factor_edges']))
    assert not g['extra_edges']
    # Enumerate spindle rows by recursive edge propagation, independently of product filtering.
    c = [0, 1, 2, 3, -1, -1, -1]
    spindle_rows = []
    def recurse(i):
        if i == 7:
            spindle_rows.append(c.copy()); return
        for colour in range(4):
            c[i] = colour
            if all(c[a] < 0 or c[b] < 0 or c[a] != c[b] for a, b in me): recurse(i+1)
        c[i] = -1
    recurse(4)
    assert len(spindle_rows) == 10
    potentials = json.loads((here.parent/'hadwiger_nelson_heptagon_difference_lifts/potentials.json').read_text())
    colours = []
    for p in potentials:
        assert proper(p, he, 21)
        for q in spindle_rows:
            row = []
            for fiber in representations:
                values = {p[a]^q[b] for a, b in fiber}
                assert len(values) == 1
                row.append(values.pop())
            assert proper(row, ge, 143)
            colours.append(bytes(row))
    assert len(colours) == len(set(colours)) == 420
    assert sha256(b''.join(sorted(colours))).hexdigest() == expected['colouring_stream_sha256']
    certificate = json.loads((here/'certificate.json').read_text())
    assert certificate == json.loads((args.work/'certificate.json').read_text())
    assert bytes(certificate['colouring']) == colours[0]
    # Lower bound: the spindle admits no three-colouring, normalized on its first triangle.
    three_colourings = [row for tail in product(range(3), repeat=4)
                        if all((row := [0, 1, 2]+list(tail))[a] != row[b] for a, b in me)]
    assert not three_colourings
    embedding = [index[add(H[0], point)] for point in M]
    assert len(set(embedding)) == 7 and all(tuple(sorted((embedding[a], embedding[b]))) in factor for a, b in me)
    assert mul(S, S) == scale(O, -11) and conjugate(S) == scale(S, -1)
    assert mul(OMEGA, OMEGA) == sub(OMEGA, O)
    bad = certificate['colouring'].copy(); bad[ge[0][0]] = bad[ge[0][1]]
    assert not proper(bad, ge, 143) and not proper(certificate['colouring'][:-1], ge, 143)
    hd = {sub(a, b) for a in H for b in H if a != b}
    md = {sub(a, b) for a in M for b in M if a != b}
    assert (len(hd), len(md)) == (420, 34)
    out = {'status': 'EXACT143-POINT SUM IS FOUR-CHROMATIC; NO EXTRA UNIT EDGES',
           'H_pair_checks': 210, 'M_pair_checks': 21, 'sum_pair_checks': 10153,
           'vertices': len(G), 'unit_edges': len(ge), 'product_edge_images': len(factor),
           'collision_fibers': [r for r in representations if len(r) > 1],
           'XOR_colourings': len(colours), 'colour_edge_checks': 420*len(ge),
           'normalized_M_three_colour_cases': 81, 'proper_M_three_colourings': 0,
           'spindle_embedding': embedding, 'invalid_colourings_rejected': 2,
           'H_directed_differences': len(hd), 'M_directed_differences': len(md),
           'generic_rotation_exception_bound': 3*len(hd)*len(md),
           'seconds': time.perf_counter()-started}
    (args.work/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
