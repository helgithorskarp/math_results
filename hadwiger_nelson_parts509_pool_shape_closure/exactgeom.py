#!/usr/bin/env python3
"""Independent exact reconstruction of the L-union-pool geometry of the Parts 509 graph.

Field K = Q(sqrt3, sqrt5, sqrt11) with basis e_m = prod_{bit in m} sqrt(p_bit),
p = (3, 5, 11), bit0 -> sqrt3, bit1 -> sqrt5, bit2 -> sqrt11 (same convention as the
committed data files, so indices can be compared).  All arithmetic is exact:
coordinates are 8-tuples of Fraction, unit tests are done on integer 8-tuples after
scaling to a common denominator.

This file re-derives the vertex coordinates from the published Mathematica source
`parts509.vtx` with sympy and the completion points from `completion_points.json`,
then recomputes every unit pair inside L u U from scratch.  It does not import any
module of the committed contributions.
"""
from __future__ import annotations
import json, sys
from fractions import Fraction
from math import lcm
from pathlib import Path

PRIMES = (3, 5, 11)
NB = 8


def basis_prod(mask):
    v = 1
    for b in range(3):
        if mask >> b & 1:
            v *= PRIMES[b]
    return v


# multiplication table:  e_i * e_j = MULC[i][j] * e_{i^j}
MULC = [[basis_prod(i & j) for j in range(NB)] for i in range(NB)]


def imul(x, y):
    out = [0] * NB
    for i, a in enumerate(x):
        if a:
            for j, b in enumerate(y):
                if b:
                    out[i ^ j] += MULC[i][j] * a * b
    return out


def parse_vtx(path):
    """Parse the Mathematica point list into exact 8-tuples of Fraction."""
    import sympy as sp
    s3, s5, s11 = sp.sqrt(3), sp.sqrt(5), sp.sqrt(11)
    keymap = {}
    for m in range(NB):
        e = sp.Integer(1)
        for b in range(3):
            if m >> b & 1:
                e *= sp.sqrt(PRIMES[b])
        keymap[sp.expand(e)] = m
    pts = []
    for line in Path(path).read_text().split('\n'):
        line = line.strip()
        if not line:
            continue
        assert line.startswith('{') and line.endswith('}'), line
        body = line[1:-1]
        depth = 0
        for i, ch in enumerate(body):
            if ch in '([{':
                depth += 1
            elif ch in ')]}':
                depth -= 1
            elif ch == ',' and depth == 0:
                cut = i
                break
        else:
            raise ValueError(line)
        parts = [body[:cut], body[cut + 1:]]
        coords = []
        for t in parts:
            t = t.replace('Sqrt[', 'sqrt(').replace(']', ')')
            raw = sp.sympify(t, locals={'sqrt': sp.sqrt})
            e = raw
            for _ in range(4):
                e2 = sp.expand(sp.sqrtdenest(sp.radsimp(e)))
                if e2 == e:
                    break
                e = e2
            vec = [Fraction(0)] * NB
            for term in sp.Add.make_args(e):
                c, rest = term.as_coeff_Mul()
                rest = sp.expand(rest)
                assert rest in keymap, (line, term, rest)
                c = sp.Rational(c)
                vec[keymap[rest]] += Fraction(int(sp.numer(c)), int(sp.denom(c)))
            # numeric guard against a mis-parse
            chk = sum(float(v) * float(sp.sqrt(basis_prod(m))) for m, v in enumerate(vec))
            assert abs(chk - float(raw.evalf(30))) < 1e-18 + 1e-12 * abs(chk), (line, chk)
            coords.append(tuple(vec))
        pts.append((coords[0], coords[1]))
    return pts


def points_from_json(pts):
    out = []
    for p in pts:
        x = tuple(Fraction(s) for s in p['x'])
        y = tuple(Fraction(s) for s in p['y'])
        out.append((x, y))
    return out


def scale_points(points):
    """Common denominator D and integer coordinate tuples."""
    D = 1
    for x, y in points:
        for c in x + y:
            D = lcm(D, c.denominator)
    ipts = []
    for x, y in points:
        ipts.append(([int(c * D) for c in x], [int(c * D) for c in y]))
    return D, ipts


def unit_pairs(ipts, D, idxs):
    """All pairs (i, j) from idxs at squared distance exactly 1."""
    target = D * D
    edges = []
    n = len(idxs)
    for a in range(n):
        i = idxs[a]
        xi, yi = ipts[i]
        for b in range(a + 1, n):
            j = idxs[b]
            xj, yj = ipts[j]
            dx = [p - q for p, q in zip(xi, xj)]
            dy = [p - q for p, q in zip(yi, yj)]
            s = imul(dx, dx)
            t = imul(dy, dy)
            if s[0] + t[0] != target:
                continue
            if any(s[k] + t[k] for k in range(1, NB)):
                continue
            edges.append((i, j))
    return edges


def build(repo=None):
    repo = Path(repo) if repo is not None else Path(__file__).resolve().parent.parent
    V = parse_vtx(repo / 'hadwiger_nelson_parts509_criticality' / 'parts509.vtx')
    assert len(V) == 509
    cp = json.loads((repo / 'hadwiger_nelson_parts509_swap_closure' / 'completion_points.json').read_text())
    Q = points_from_json(cp['points'])
    assert len(Q) == 1158
    return V + Q, cp


if __name__ == '__main__':
    pts, cp = build()
    D, ipts = scale_points(pts)
    print('points', len(pts), 'common denominator', D, flush=True)
    REPO = Path(__file__).resolve().parent.parent
    pool = json.loads((REPO / 'hadwiger_nelson_parts509_s_replacement_budget' / 'pool_S.json').read_text())
    U = sorted(pool['W_S'])
    L = list(range(374))
    idxs = L + U
    print('L', len(L), 'U', len(U), 'total', len(idxs), flush=True)
    E = unit_pairs(ipts, D, idxs)
    print('exact unit pairs inside L u U:', len(E), flush=True)
    amb = json.loads((REPO / 'hadwiger_nelson_parts509_pair_closure' / 'ambient_w3_edges.json').read_text())
    keep = set(idxs)
    Eamb = {(a, b) for a, b in amb['edges'] if a in keep and b in keep}
    Emine = {(min(a, b), max(a, b)) for a, b in E}
    print('committed edges restricted to L u U:', len(Eamb))
    print('identical:', Emine == Eamb)
    print('missing from committed:', sorted(Emine - Eamb)[:10])
    print('extra in committed:', sorted(Eamb - Emine)[:10])
    json.dump({'D': D, 'L': L, 'U': U, 'edges': sorted(Emine)},
              open(Path(__file__).resolve().parent / 'pool_geometry.json', 'w'))
