#!/usr/bin/env python3
"""SymPy lexicographic elimination and Eisenstein-coordinate certificate producer."""
import argparse
import itertools
import json
from pathlib import Path
import sympy as s
from flint import fmpq_poly as Q, fmpq
from common import V, X, PAIRS, INPUT_SHA, inventory, coefficients, coordinate_digest


def run():
    fs,circle,monos,rowids,images = inventory()
    x,y = s.symbols('x y')
    def convert(expr):
        poly = s.Poly(expr,y)
        return Q([fmpq(str(poly.nth(i))) for i in range(poly.degree()+1)])
    charts = []
    for a,b,mask,bound,allowance in PAIRS:
        f = sum(c*x**i*y**j for i,j,c in fs[a])
        g = sum(c*x**i*y**j for i,j,c in fs[b])
        basis = s.groebner([f,g],x,y,order='lex')
        uni = next(p.as_expr() for p in basis.polys if not p.as_expr().has(x))
        for factor,multiplicity in s.factor_list(uni)[1]:
            X.need(multiplicity == 1, 'squarefree projection factor')
            factor = s.Poly(factor,y)
            q = [int(factor.nth(i)) for i in range(factor.degree()+1)]
            mod = Q(q)
            refined = s.groebner([f,g,factor.as_expr()],x,y,order='lex')
            X.need(len(refined.polys) == 2, 'single finite-coordinate chart')
            xx = convert(s.solve(refined.polys[0].as_expr(),x)[0])
            yy = Q([0,1]); radius = (xx*xx+3*yy*yy)%mod
            intervals = [[str(a),str(b)] for (a,b),m in
                         s.polys.polytools.intervals(factor.as_expr(),eps=s.Rational(1,100000))]
            chart = {'pair':[a,b], 'q':q, 'x':coefficients(xx),
                     'isolating_intervals':intervals, 'closed_unit_circle':radius == 1}
            if radius == 1:
                charts.append(chart)
                continue
            def add(a,b,scale=1):return tuple((v+scale*w)%mod for v,w in zip(a,b))
            def mul(a,b):
                return ((a[0]*b[0]-a[1]*b[1])%mod,
                        (a[0]*b[1]+a[1]*b[0]+a[1]*b[1])%mod)
            z = (xx-yy,2*yy)
            powers = [(Q([1]),Q([]))]
            for _ in range(4):powers.append(mul(powers[-1],z))
            points = []
            for label in V.LABELS:
                v = (Q([]),Q([]))
                for i,d in enumerate(label):
                    v = add(v,mul(powers[i],(Q([int(d==1)]),Q([int(d==2)]))))
                points.append(v)
            edges = []; active = set(); cache = {}
            for i,j in itertools.combinations(range(243),2):
                raw = tuple((V.DIGITS[a][0]-V.DIGITS[b][0], V.DIGITS[a][1]-V.DIGITS[b][1])
                            for a,b in zip(V.LABELS[i],V.LABELS[j]))
                row = V.canonical_row(raw)
                if row not in cache:
                    u,v = add(points[i],points[j],-1)
                    norm = (u*u+u*v+v*v)%mod
                    X.need(norm and norm.gcd(mod) == 1, 'no physical label collision')
                    h = norm-1
                    X.need(not h or h.gcd(mod) == 1, 'constant edge set across chart')
                    cache[row] = not h
                if cache[row]:
                    edges.append([i,j]); owner = V.edge_owner(i,j,monos,rowids,circle)
                    if owner != 'base':active.add(owner)
            words = [(1,)+w for w in itertools.product(range(3),repeat=4)]
            word = next(w for w in words if all(
                sum(w[k]*(V.LABELS[i][k]-V.LABELS[j][k]) for k in range(5))%3
                for i,j in edges))
            chart.update({'vertices':243, 'unit_edges':len(edges),
                          'edge_sha256':X.digest(edges), 'active_curves':sorted(active),
                          'colour_word':list(word),
                          'coordinate_sha256':coordinate_digest([(a+b/2,b/2) for a,b in points])})
            charts.append(chart)
    return {'schema':'hn-radix-rotation-pairs-v1', 'source_frontier_sha256':INPUT_SHA,
            'pair_rows':PAIRS, 'modular_prime':1000003,
            'expanded_pair_exclusions':images, 'charts':charts}


if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a = p.parse_args()
    result = run()
    with a.out.open('x') as f:json.dump(result,f,sort_keys=True,separators=(',',':'));f.write('\n')
    print(json.dumps({'charts':len(result['charts']), 'certificate_sha256':X.digest(result)},indent=2))
