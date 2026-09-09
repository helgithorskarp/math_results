"""Exact 343-point controls in an eight-radical basis, independent of the CAS."""
from itertools import combinations, product
from algebra import need

RAD = (1, 2, 3, 6, 11, 22, 33, 66)


def plus(a, b):
    return tuple(x+y for x, y in zip(a, b))


def times(a, b):
    out = [0]*8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i ^ j] += x*y*RAD[i & j]
    return tuple(out)


def normdiff(a, b):
    dx = tuple(x-y for x, y in zip(a[0], b[0]))
    dy = tuple(x-y for x, y in zip(a[1], b[1]))
    return plus(times(dx, dx), times(dy, dy))


def atoms(W, kind):
    ab = [(2*a+b, b) for a, b in W]
    X, Y = 1000, 10**9
    dx, dy = 1+3*X*X, 1+3*Y*Y
    scale = 12 if kind == 'four' else 2*dx*dy
    out = []
    for part in range(3):
        arr = []
        for a, b in ab:
            x = [0]*8; y = [0]*8
            if kind == 'four':
                # W + ((5+i sqrt11)/6)W + ((1+i sqrt2)/sqrt3)W.
                if part == 0:
                    x[0] = 6*a; y[2] = 6*b
                elif part == 1:
                    x[0] = 5*a; x[6] = -b; y[4] = a; y[2] = 5*b
                else:
                    x[2] = 2*a; x[1] = -6*b; y[3] = 2*a; y[0] = 6*b
            else:
                # W + phi(1000)W + phi(10^9)W, phi(t)=(1+i sqrt3 t)/(1-i sqrt3 t).
                if part == 0:
                    x[0] = a*dx*dy; y[2] = b*dx*dy
                elif part == 1:
                    x[0] = ((1-3*X*X)*a-6*X*b)*dy
                    y[2] = ((1-3*X*X)*b+2*X*a)*dy
                else:
                    x[0] = ((1-3*Y*Y)*a-6*Y*b)*dx
                    y[2] = ((1-3*Y*Y)*b+2*Y*a)*dx
            arr.append((tuple(x), tuple(y)))
        out.append(arr)
    return out, scale


def run(W, labels, words):
    output = []
    for kind in ('generic_three', 'four'):
        A, scale = atoms(W, kind)
        pts = [(plus(plus(A[0][a][0], A[1][b][0]), A[2][c][0]),
                plus(plus(A[0][a][1], A[1][b][1]), A[2][c][1])) for a, b, c in labels]
        need(len(pts) == len(set(pts)) == 343, 'physical injectivity')
        E = {(a, b) for a, b in combinations(range(343), 2)
             if normdiff(pts[a], pts[b]) == (scale*scale, 0, 0, 0, 0, 0, 0, 0)}
        good = [name for name, word in words if all(word[a] != word[b] for a, b in E)]
        need(bool(good), 'physical four-colouring')
        if kind == 'generic_three':
            need(len(E) == 1764 and good[0].startswith('F3'), 'generic physical product')
            t = [labels.index((i, 0, 0)) for i in (0, 1, 2)]
            need(all(tuple(sorted(e)) in E for e in combinations(t, 2)), 'physical triangle')
            lower = 3; obstruction = 'unit triangle'
        else:
            need(len(E) == 1848 and not any(name.startswith('F3') for name in good), 'physical four benchmark')
            m = [(2, 2, 0), (0, 2, 0), (1, 2, 0), (6, 2, 0), (2, 0, 0), (2, 1, 0), (2, 6, 0)]
            ids = [labels.index(q) for q in m]
            edges = [(a, b) for a, b in combinations(range(7), 2) if tuple(sorted((ids[a], ids[b]))) in E]
            need(edges == [(0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 3), (2, 3),
                           (3, 6), (4, 5), (4, 6), (5, 6)], 'physical Moser spindle')
            need(not any(all(w[a] != w[b] for a, b in edges) for w in product(range(3), repeat=7)),
                 'Moser non-three-colourability')
            lower = 4; obstruction = 'exact seven-point Moser spindle, all 2187 three-colour assignments rejected'
        output.append({'kind': kind, 'vertices': 343, 'strict_unit_edges': len(E),
                       'exact_point_pairs': 58653, 'chromatic_number': lower,
                       'proper_colour_word': good[0], 'lower_bound_witness': obstruction})
    return output
