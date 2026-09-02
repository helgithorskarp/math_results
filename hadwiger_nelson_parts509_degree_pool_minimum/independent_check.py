#!/usr/bin/env python3
"""Independent check of a tie-union certificate with SymPy arithmetic (no shared code with
tie_union_certificate.py): rebuilds every coordinate as an exact SymPy expression in Q(√3,√5,√11),
recomputes the unit-distance edge list of A* (float screen, then exact expansion of every candidate
squared distance; non-candidates are provably not at distance 1 because |x|,|y| < 8 keeps the
double-precision error of the squared distance below 1e-9, far under the 1e-6 screen), and replays
every forced-vertex and killing-set witness colouring against that edge list.  Prints the edge count
(to compare with the main verifier) and the replay results.
usage: independent_check.py certificate_P25.json"""
import json, sys, time, math
from fractions import Fraction
import sympy as sp
K = 4
R3, R5, R11 = sp.sqrt(3), sp.sqrt(5), sp.sqrt(11)
BASIS = [sp.Integer(1), R3, R5, R3 * R5, R11, R3 * R11, R5 * R11, R3 * R5 * R11]
FB = [1.0, math.sqrt(3), math.sqrt(5), math.sqrt(15), math.sqrt(11), math.sqrt(33), math.sqrt(55), math.sqrt(165)]

def exact(strs):
    return sum(sp.Rational(Fraction(s).numerator, Fraction(s).denominator) * b for s, b in zip(strs, BASIS))

def approx(strs):
    return sum(float(Fraction(s)) * b for s, b in zip(strs, FB))

def main():
    t0 = time.time()
    cert = json.loads(open(sys.argv[1]).read())
    star = cert['vertices']
    ex = {v: (exact(cert['coordinates'][str(v)][0]), exact(cert['coordinates'][str(v)][1])) for v in star}
    fl = {v: (approx(cert['coordinates'][str(v)][0]), approx(cert['coordinates'][str(v)][1])) for v in star}
    assert all(abs(fl[v][0]) < 8 and abs(fl[v][1]) < 8 for v in star)
    n = len(star); edges = set(); cand = 0
    for i in range(n):
        a = star[i]; xa, ya = fl[a]
        for j in range(i + 1, n):
            b = star[j]; dx = xa - fl[b][0]; dy = ya - fl[b][1]
            if abs(dx * dx + dy * dy - 1.0) < 1e-6:
                cand += 1
                d2 = sp.expand((ex[a][0] - ex[b][0]) ** 2 + (ex[a][1] - ex[b][1]) ** 2)
                if d2 == 1:
                    edges.add((a, b))
    print(f'(1) SymPy exact edge list: {n} vertices, {len(edges)} unit-distance pairs ({cand} candidates) ({time.time()-t0:.0f}s)')
    adj = {v: set() for v in star}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    def proper(colstr, verts):
        assert len(colstr) == len(verts)
        col = dict(zip(verts, colstr))
        return all(col[w] != col[v] for v in verts for w in adj[v] if w in col) and set(colstr) <= set('0123')
    F = cert['forced']; R = cert['free']; S = set(star)
    assert sorted(F + R) == sorted(star)
    okF = all(proper(cert['forced_witness'][str(u)], [v for v in star if v != u]) for u in F)
    print(f'(2) forced witnesses proper: {okF} ({len(F)} colourings)')
    Rset = set(R); okD = True
    for row in cert['family']:
        D = set(row['D']); assert D <= Rset
        okD &= proper(row['witness'], [v for v in star if v not in D])
    print(f'(3) killing-set witnesses proper: {okD} ({len(cert["family"])} colourings)')
    # sanity: the free pool points are exactly the free elements outside V
    assert set(cert['pool_free']) == {v for v in R if v >= 509}
    print(f'independent_check {"PASSED" if okF and okD else "FAILED"} ({time.time()-t0:.0f}s)')

if __name__ == '__main__':
    main()
