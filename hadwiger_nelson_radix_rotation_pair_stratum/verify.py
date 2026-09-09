#!/usr/bin/env python3
"""Complete determinant/fibre coverage and Cartesian exact physical verification."""
import argparse
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path
from flint import fmpz_poly as Z, fmpq_poly as Q, fmpq
from common import (HERE, V, X, G, PAIRS, INPUT_SHA, inventory,
                    coefficients, coordinate_digest)


def evaluate(poly,x):
    value = F(0)
    for c in reversed(poly):value = value*x+F(c)
    return value


def isolate(q,intervals):
    X.need(Q(q).gcd(Q(q).derivative()) == 1, 'squarefree real-root parameter')
    parsed = [list(map(F,I)) for I in intervals]
    X.need(all(len(I) == 2 and I[0]<I[1] for I in parsed), 'proper isolating intervals')
    X.need(all(parsed[k][1]<parsed[k+1][0] for k in range(len(parsed)-1)),
           'disjoint ordered isolating intervals')
    for a,b in parsed:
        X.need(evaluate(q,a)*evaluate(q,b)<0 and X.root_count(q,a,b) == 1,
               'exactly one real root per interval, with nonzero endpoints')
    X.need(X.root_count(q) == len(parsed), 'every real root covered')
    return len(parsed)


def finite(poly,p):
    result = []
    for c in poly:
        c = F(str(c))
        X.need(c.denominator%p != 0, 'all rational denominators survive modulo prime')
        result.append(c.numerator%p*pow(c.denominator%p,-1,p)%p)
    return X.trim(result)


def run(path):
    data = json.loads(Path(path).read_text())
    X.need(data['schema'] == 'hn-radix-rotation-pairs-v1', 'certificate schema')
    X.need(data['pair_rows'] == PAIRS and data['source_frontier_sha256'] == INPUT_SHA,
           'exact four source rows and frontier provenance')
    fs,circle,monos,rowids,images = inventory()
    X.need(data['expanded_pair_exclusions'] == [list(p) for p in images],
           'complete eight physical pair exclusions')
    prime = data['modular_prime']
    X.need(type(prime) is int and X.is_prime(prime), 'prime proof modulus')
    cases = data['charts']
    X.need(all(c['pair'] in [p[:2] for p in PAIRS] for c in cases), 'only selected pairs')
    outputs = []; circle_slots = 0; physical_slots = 0; norm_checks = 0
    for a,b,mask,bound,allowance in PAIRS:
        def as_x(poly):
            # Coefficients in Z[y], with x as the eliminated variable.
            out = [Z([]) for _ in range(max(i for i,j,c in poly)+1)]
            for i,j,c in poly:out[i] += Z([0]*j+[c])
            return G.trim(out)
        f,g = as_x(fs[a]),as_x(fs[b])
        determinant = G.resultant(f,g)
        X.need(determinant, 'nonzero complete Sylvester eliminant')
        selected = [c for c in cases if c['pair'] == [a,b]]
        X.need(selected, 'pair has a complete factor cover')
        product = Z([1])
        for c in selected:
            q = c['q']
            X.need(all(type(v) is int for v in q) and tuple(q) == G.primitive(Z(q)),
                   'primitive positive-leading integral parameter polynomial')
            product *= Z(q)
        X.need(G.primitive(product) == G.primitive(determinant),
               'complete exact eliminant factor product, including multiplicities')
        for c in selected:
            q = c['q'];mod = Q(q)
            X.need(q[-1]%prime != 0, 'parameter degree preserved modulo prime')
            xx = Q([fmpq(s) for s in c['x']]);yy = Q([0,1])
            X.need(xx.degree()<mod.degree(), 'reduced x coordinate')
            gcd = G.monic_gcd(f,g,mod)
            X.need(len(gcd) == 2 and gcd[1] == 1 and gcd[0] == -xx,
                   'complete linear fibre with every divided coefficient a checked unit')
            for equation in (f,g):
                value = Q([])
                for coefficient in reversed(equation):value = (value*xx+Q(coefficient))%mod
                X.need(not value, 'constructed coordinates satisfy both original norm equations')
            roots = isolate(q,c['isolating_intervals'])
            radius = (xx*xx+3*yy*yy)%mod
            if c['closed_unit_circle']:
                X.need(radius == 1, 'entire chart belongs to accepted h4139 unit circle')
                circle_slots += roots
                outputs.append({'pair':[a,b], 'degree':len(q)-1,
                                'real_parameter_slots':roots, 'disposition':'closed_unit_circle_h4139'})
                continue
            X.need(X.gcd_is_one(q,finite(radius-1,prime),prime),
                   'entire physical chart is off the closed unit circle')
            physical_slots += roots
            # Independent Cartesian multiplication: z = x+i*sqrt(3)*y.
            def add(a,b,scale=1):return tuple((v+scale*w)%mod for v,w in zip(a,b))
            def mul(a,b):return ((a[0]*b[0]-3*a[1]*b[1])%mod,
                                 (a[0]*b[1]+a[1]*b[0])%mod)
            zero = Q([]);one = Q([1]);half = Q([fmpq(1,2)])
            digits = ((zero,zero),(one,zero),(half,half))
            powers = [(one,zero)]
            for _ in range(4):powers.append(mul(powers[-1],(xx,yy)))
            points = []
            for label in V.LABELS:
                point = (zero,zero)
                for k,d in enumerate(label):point = add(point,mul(powers[k],digits[d]))
                points.append(point)
            X.need(coordinate_digest(points) == c['coordinate_sha256'],
                   'all 243 Cartesian coordinates agree with Eisenstein producer')
            word = c['colour_word']
            X.need(len(word) == 5 and all(type(v) is int and 0<=v<3 for v in word),
                   'three-colour word')
            colours = [sum(a*b for a,b in zip(word,label))%3 for label in V.LABELS]
            X.need(all(a*a+a*b+b*b == 1 for a,b in V.UNITS),
                   'row normalization units preserve the physical norm')
            cache = {};edges = [];active = set()
            for i,j in itertools.combinations(range(243),2):
                raw = tuple((V.DIGITS[a][0]-V.DIGITS[b][0],V.DIGITS[a][1]-V.DIGITS[b][1])
                            for a,b in zip(V.LABELS[i],V.LABELS[j]))
                row = V.canonical_row(raw)
                if row not in cache:
                    dx,dy = add(points[i],points[j],-1)
                    norm = (dx*dx+3*dy*dy)%mod
                    X.need(X.gcd_is_one(q,finite(norm,prime),prime),
                           'every physical displacement is nonzero at every root')
                    h = norm-1
                    if h:
                        X.need(X.gcd_is_one(q,finite(h,prime),prime),
                               'every absent unit edge excluded at every root')
                    cache[row] = not h
                if cache[row]:
                    X.need(colours[i] != colours[j], 'proper colour on every actual unit edge')
                    edges.append([i,j]);owner = V.edge_owner(i,j,monos,rowids,circle)
                    if owner != 'base':active.add(owner)
            X.need(len(cache) == 2801, 'all canonical displacement classes covered')
            norm_checks += len(cache)
            X.need(len(points) == c['vertices'] == 243 and len(edges) == c['unit_edges'],
                   'complete physical graph order and size')
            X.need(X.digest(edges) == c['edge_sha256'], 'complete strict edge set')
            X.need(sorted(active) == c['active_curves'] == [a,b],
                   'exactly the two defining curves are active')
            X.need(all(e in edges for e in ([0,81],[0,162],[81,162])), 'unit triangle lower bound')
            outputs.append({'pair':[a,b], 'degree':len(q)-1, 'real_parameter_slots':roots,
                            'vertices':243, 'unit_edges':len(edges), 'active_curves':sorted(active),
                            'chromatic_number':3, 'edge_sha256':X.digest(edges),
                            'coordinate_sha256':coordinate_digest(points)})
    X.need(len(cases) == len(outputs), 'every chart checked exactly once')
    return {'verified':True, 'pair_systems':4, 'expanded_pair_exclusions':8,
            'charts':len(cases), 'off_circle_parameter_values_in_canonical_pairs':physical_slots,
            'previously_closed_circle_parameter_slots':circle_slots,
            'new_physical_edge_patterns':len({c['edge_sha256'] for c in outputs if 'edge_sha256' in c}),
            'canonical_displacement_checks':norm_checks,
            'label_pair_checks':4*math.comb(243,2), 'outcomes':outputs,
            'every_physical_member_chromatic_number':3, 'record_improvement':False}


if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    p.add_argument('--check-expected',action='store_true');a = p.parse_args()
    result = run(a.certificate)
    if a.check_expected:X.need(result == json.loads((HERE/'EXPECTED.json').read_text()),'expected outcome')
    print(json.dumps(result,indent=2,sort_keys=True))
