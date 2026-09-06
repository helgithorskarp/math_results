#!/usr/bin/env python3
"""Independent finite oracle and exact geometric bridge; Python standard library.

Does not import the relation producer, compiler, SAT solver, or old geometry code.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RAD = (1,3,5,15,11,33,55,165)
NEIGHBOURS = [[361,417,495,503,509], [418,498,506,508],
              [359,362,502], [358,416,507]]
BOUNDARY = {0} | {v for row in NEIGHBOURS for v in row}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(p):
    return json.loads(p.read_text())


def scale(raw):
    q = [[96*Fraction(x) for x in axis] for axis in raw]
    need(len(q)==2 and all(len(a)==8 for a in q), 'coordinate dimensions')
    need(all(x.denominator==1 for a in q for x in a), 'integral scale 96')
    return tuple(tuple(int(x) for x in a) for a in q)


def distance(p, q):
    result = [0]*8
    for axis in range(2):
        d = [(i,p[axis][i]-q[axis][i]) for i in range(8) if p[axis][i]!=q[axis][i]]
        for i,x in d:
            result[0] += x*x*RAD[i]
        for (i,x),(j,y) in combinations(d,2):
            result[i ^ j] += 2*x*y*gcd(RAD[i],RAD[j])
    return tuple(result)


def geometry():
    for filename, digest in load(HERE/'manifest.json').items():
        need(sha256((REPO/filename).read_bytes()).hexdigest()==digest, ('input digest',filename))
    old = load(REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json')
    labels = [v for v in range(553) if '510' in old['provenance'][v]]
    points = [scale(old['coordinates'][str(v)]) for v in labels]
    pool = load(REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json')
    points += [scale(next(r for r in pool if r['centre_index']==j)['coordinates']) for j in (170,436,1239,1527)]
    need(len(points)==len(set(points))==514, 'distinct support')
    need(points[0]==((0,)*8,(0,)*8), 'forced origin')
    unit = (96*96,)+(0,)*7
    edges = [(u,v) for u,v in combinations(range(514),2) if distance(points[u],points[v])==unit]
    need(len(edges)==2526, 'complete unit-edge graph')
    need([(u,v) for u,v in edges if u>=510]==[(510,511),(511,512),(512,513)], 'induced P4')
    actual = [[u for u,v in edges if v==510+i and u<510] for i in range(4)]
    need(actual==[[0]+n for n in NEIGHBOURS], 'complete attachment neighbourhoods')
    witnesses = load(HERE/'boundary_witnesses.json')
    need([r['omitted_vertex'] for r in witnesses]==sorted(BOUNDARY), 'all boundary witnesses exactly once')
    checks = 0
    for row in witnesses:
        c = row['colouring']; v = row['omitted_vertex']
        need(len(c)==514 and set(c)<=set('.0123'), 'colour domain')
        need([i for i,x in enumerate(c) if x=='.']==[v], 'singleton omission')
        for a,b in edges:
            if v not in (a,b):
                need(c[a]!=c[b], 'positive singleton-deletion witness')
                checks += 1
    parent = load(REPO/'hadwiger_nelson_heule514_interface/verification.json')
    need(not set(parent['free_vertices']) & BOUNDARY, 'all parent residuals retain boundary')
    return edges, checks, sorted(BOUNDARY)


def colourings(mask):
    selected = [i for i in range(4) if mask & (1 << i)]
    result = []
    for colours in product(range(3), repeat=len(selected)):
        row = [-1]*4
        for i,c in zip(selected,colours):
            row[i] = c
        if all(row[i]<0 or row[i+1]<0 or row[i]!=row[i+1] for i in range(3)):
            result.append(tuple(row))
    return result


def oracle(assignments, lists):
    return next((c for c in assignments if all(x<0 or lists[i] & (1 << x) for i,x in enumerate(c))), None)


def val_bits(mask, lists):
    return mask | sum(lists[i] << (4+3*i) for i in range(4))


def clause_true(clause, bits):
    return any((bool(bits & (1 << (abs(v)-1))) if v>0 else not bits & (1 << (-v-1))) for v in clause)


def check_local(cert):
    clauses = [r['clause'] for r in cert['obstructions']]
    need(len(clauses)==len({tuple(c) for c in clauses})==37, 'distinct clause count')
    for clause in clauses:
        need(len(clause)==len(set(clause)) and all((-4<=v<=-1) or (5<=v<=16) for v in clause), 'unate literal domain')
    assignments = [colourings(m) for m in range(16)]
    hist = Counter(); digest = sha256(); active_clause_checks = 0
    for mask in range(16):
        # Independently specialize path selectors in the projected formula.
        active = [[v-5 for v in c if v>0] for c in clauses
                  if all(mask & (1 << (-v-1)) for v in c if v<0)]
        for lists in product(range(8), repeat=4):
            good = oracle(assignments[mask], lists) is not None
            bits = val_bits(mask,lists)
            need(all(clause_true(c,bits) for c in clauses)==good, 'exhaustive clause/oracle equality')
            availability = bits >> 4
            need(all(any(availability & (1 << v) for v in c) for c in active)==good, 'specialized projected kernel')
            hist[mask,good] += 1; digest.update(bytes([good])); active_clause_checks += len(active)
    need(digest.hexdigest()==cert['truth_sha256'], 'producer/oracle complete truth stream')
    need(cert['states']==65536 and cert['accepted']==sum(hist[m,True] for m in range(16)), 'state counts')
    need(cert['by_mask']==[dict(mask=m,accepted=hist[m,True],rejected=hist[m,False]) for m in range(16)], 'mask census')
    # Maximal false states prove clause irredundancy. Every favourable one-bit
    # flip has a direct colouring, proving no literal can be removed.
    prime_controls = 0
    for row in cert['obstructions']:
        mask,lists,clause = row['mask'],row['lists'],row['clause']
        need(0<=mask<16 and len(lists)==4 and all(0<=x<8 for x in lists), 'obstruction state domain')
        bits = val_bits(mask,lists)
        need(oracle(assignments[mask],lists) is None, 'maximal bad state')
        need([c for c in clauses if not clause_true(c,bits)]==[clause], 'irredundant clause')
        # Variables not appearing in the clause take their favourable value.
        for i in range(4):
            need(bool(mask & (1 << i)) == (-i-1 in clause), 'minimal selected interval')
        for i in range(4):
            for c in range(3):
                need(bool(lists[i] & (1 << c)) == (5+3*i+c not in clause), 'maximal allowed lists')
        for literal in clause:
            m = mask; ls = list(lists)
            if literal<0:
                m &= ~(1 << (-literal-1))
            else:
                i,c = divmod(literal-5,3); ls[i] |= 1 << c
            witness = oracle(assignments[m],ls)
            need(witness is not None, 'literal deletion would reject a colourable state')
            prime_controls += 1
    need(prime_controls==cert['literals']==286, 'literal count')
    # Each a <-> conjunction of negated boundary-colour indicators is checked
    # for all Boolean assignments, including indicators from non-one-hot models.
    reification_controls = 0
    for neighbours in NEIGHBOURS:
        for colour in range(3):
            for xs in product((False,True), repeat=len(neighbours)):
                for a in (False,True):
                    clauses_hold = all(not a or not x for x in xs) and (a or any(xs))
                    need(clauses_hold == (a == (not any(xs))), 'exact availability definition')
                    reification_controls += 1
    return dict(states=65536, accepted=cert['accepted'], rejected=65536-cert['accepted'],
                clauses=37,literals=286,irredundancy_states=37,prime_literal_controls=prime_controls,
                availability_definition_controls=reification_controls,
                specialized_clause_evaluations=active_clause_checks,
                truth_sha256=digest.hexdigest(), by_mask=cert['by_mask'])


def verify():
    start = time.monotonic()
    edges,checks,boundary = geometry()
    result = check_local(load(HERE/'certificate.json'))
    return dict(status='COMPLETE EXACT OPTIONAL-P4 PROJECTION VERIFIED',
                record_improvement=False, family_decision='OPEN; no new graph query',
                vertices=514,unit_edges=len(edges),exact_pairs=514*513//2,
                boundary=boundary,singleton_witnesses=16,witness_edge_checks=checks,
                local=result,solver_used=False,seconds=time.monotonic()-start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--report',type=Path)
    args = parser.parse_args(); result = verify()
    if args.report:
        args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
