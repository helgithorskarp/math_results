#!/usr/bin/env python3
"""Exact capped H certificates for two explicitly defined nine-point downsets.

Standard library only. The finite claim and product consequences are proved
in NINE_POINT_PROOF.md. Floating discovery is not imported by this checker.
"""
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from pathlib import Path
import argparse
import copy
import hashlib
import json

from kernel_trade import check_definition, digest, lift, psd_details, vector_rank


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mask(points):
    return sum(1 << i for i in points)


def domain(include_inside):
    inside, outside = tuple(range(3)), tuple(range(3,9))
    cross = {mask((*p,q)) for p in combinations(inside,2) for q in outside}
    triples = cross | {mask(p) for p in combinations(outside,3)}
    if include_inside:
        triples.add(mask(inside))
    else:
        triples -= {mask(outside[:3]),mask(outside[3:])}
    members = [0]+sorted({1 << i for i in range(9)} |
                        {mask(p) for p in combinations(range(9),2)} | triples)
    family = {mask(p) for p in combinations(inside,2)} | cross
    if include_inside:
        family.add(mask(inside))
    return members, family


def generators(include_inside):
    swaps = [(0,1),(1,2)]
    swaps += [(i,i+1) for i in range(3,8)] if include_inside else [(3,4),(4,5),(6,7),(7,8)]
    permutations = []
    for i,j in swaps:
        p=list(range(9)); p[i],p[j]=j,i; permutations.append(p)
    if not include_inside:
        permutations.append([0,1,2,6,7,8,3,4,5])
    return permutations


def decode(case):
    include_inside=case['inside_triple_present']
    require(type(include_inside) is bool, 'case parameter is not Boolean')
    members,family=domain(include_inside)
    nonempty=members[1:]; included=set(nonempty)
    def moved(a,p):
        return mask(p[i] for i in range(9) if a >> i & 1)
    maps=[{a:moved(a,p) for a in nonempty} for p in generators(include_inside)]
    require(all(set(mp.values())==included and {mp[a] for a in family}==family for mp in maps),
            'invalid symmetry')
    allowed={(a,b) for a,b in combinations(nonempty,2) if not a & b}
    reps=case['orbit_representatives']; values=case['orbit_values']
    require(len(reps)==len(values), 'orbit table lengths disagree')
    entries={}; orbit_sizes=[]
    for representative,value in zip(reps,values):
        require(len(representative)==2, 'invalid orbit representative')
        seed=tuple(representative)
        require(seed in allowed, 'representative not an allowed pair')
        orbit={seed}; pending=[seed]
        while pending:
            a,b=pending.pop()
            for mp in maps:
                image=tuple(sorted((mp[a],mp[b])))
                if image not in orbit:
                    orbit.add(image); pending.append(image)
        require(orbit <= allowed and not set(entries) & orbit, 'invalid or overlapping orbit')
        entries.update({pair:F(value) for pair in orbit})
        orbit_sizes.append(len(orbit))
    require(set(entries)==allowed, 'incomplete disjoint-pair table')
    s=22 if include_inside else 21
    require(case['s']==s, 'wrong star metadata')
    c=[[F(s-1) if a==b else F(-1) if a & b else
        entries[tuple(sorted((a,b)))] for b in nonempty] for a in nonempty]
    return members,family,s,c,orbit_sizes


def bareiss_psd(matrix):
    """Exact symmetric fraction-free Schur elimination and rank.

    Clear a common positive denominator. Residual entries are the ordinary
    Schur-complement entries multiplied by the previous positive pivot.
    Each positive pivot permits a congruence splitting; a zero diagonal
    requires its residual row to vanish. Python integers cannot overflow.
    """
    n=len(matrix)
    require(all(len(row)==n for row in matrix), 'nonsquare input')
    require(all(matrix[i][j]==matrix[j][i] for i in range(n) for j in range(n)), 'asymmetry')
    denominator=lcm(*(F(x).denominator for row in matrix for x in row))
    a=[[int(F(x)*denominator) for x in row] for row in matrix]
    previous=1; rank=0
    for k in range(n):
        pivot=a[k][k]
        require(pivot>=0, 'negative fraction-free pivot')
        if not pivot:
            require(not any(a[k][j] for j in range(k+1,n)), 'zero pivot with nonzero row')
            continue
        for i in range(k+1,n):
            for j in range(i,n):
                numerator=pivot*a[i][j]-a[i][k]*a[k][j]
                value,remainder=divmod(numerator,previous)
                require(remainder==0, 'nonexact Bareiss division')
                a[i][j]=a[j][i]=value
        previous=pivot; rank+=1
    return rank


def audit(case):
    members,family,s,c,sizes=decode(case)
    n=len(members)
    require(n==case['N']==(85 if case['inside_triple_present'] else 82), 'wrong dimension')
    require(all(a & b for a,b in combinations(family,2)) and len(family)==s,
            'wrong nonstar intersecting family')
    require(not any(all(a >> i & 1 for a in family) for i in range(9)), 'family is a star')
    L=lift(c)
    active,stars,vectors=check_definition(members,s,L)
    require(active==stars==list(range(9)), 'wrong largest stars')
    nonstar=[n*int(a in family)-s for a in members]
    require(vector_rank(vectors+[nonstar])==10, 'forced full kernel dimension differs')
    require(all(sum(x*y for x,y in zip(row,nonstar))==0 for row in L), 'nonstar kernel fails')
    upper=[[F(n*int(i==j)-1)-c[i][j] for j in range(n-1)] for i in range(n-1)]
    ranks=[bareiss_psd(c),bareiss_psd(upper)]
    require(ranks==[n-11,n-1], 'wrong exact PSD ranks')
    require([psd_details(c)['rank'],psd_details(upper)['rank']]==ranks,
            'Fraction and integer PSD checks disagree')
    require(L[0][0]>1, 'certificate unexpectedly centered')
    m=[[F(L[i][j]-s*int(i==j),n-s) for j in range(n)] for i in range(n)]
    require(all(sum(row)==1 for row in m) and
            all(m[i][j]==0 for i,a in enumerate(members) for j,b in enumerate(members) if a & b),
            'decoded M definition fails')
    return {'N':n,'s':s,'inside_triple_present':case['inside_triple_present'],
            'triples':sum(a.bit_count()==3 for a in members),
            'triple_degree':sorted({sum(a.bit_count()==3 and bool(a >> i & 1) for a in members) for i in range(9)}),
            'support_orbits':len(sizes),'disjoint_nonempty_pairs':sum(sizes),
            'core_rank':ranks[0],'full_L_rank':ranks[0]+1,'upper_core_rank':ranks[1],
            'lower_endpoint_multiplicity':10,'unit_eigenvalue_simple':True,
            'maximum_family_count_from_kernel_proof':10,'largest_star_count':9,
            'nonstar_family_masks':sorted(family),
            'C_denominator':lcm(*(x.denominator for row in c for x in row)),
            'M_denominator':lcm(*(x.denominator for row in m for x in row)),
            'L_empty_diagonal':str(L[0][0]),'M_empty_diagonal':str(m[0][0]),
            'minimum_offdiagonal_M_entry':str(min(m[i][j] for i in range(n) for j in range(i+1,n))),
            'core_sha256':digest(c),'L_sha256':digest(L),'M_sha256':digest(m)}


def controls(cases):
    failures=0
    for checker in (bareiss_psd,lambda matrix:psd_details(matrix)['rank']):
        for bad in ([[-1]],[[0,1],[1,0]],[[1,2],[0,1]]):
            try:
                checker(bad)
            except (ValueError,AssertionError):
                failures+=1
            else:
                raise ValueError('invalid matrix control accepted')
        require(checker([[2,0],[0,0]])==1 and checker([[2,1],[1,2]])==2,
                'small PSD rank control failed')
    for duplicate in (False,True):
        damaged=copy.deepcopy(cases[0])
        if duplicate:
            damaged['orbit_representatives'].append(damaged['orbit_representatives'][0])
            damaged['orbit_values'].append(damaged['orbit_values'][0])
        else:
            damaged['orbit_values'][0]=str(F(damaged['orbit_values'][0])+1)
        try:
            audit(damaged)
        except (ValueError,AssertionError):
            failures+=1
        else:
            raise ValueError('damaged certificate accepted')
    return {'indefinite_or_asymmetric_controls_rejected':6,'damaged_orbit_table_controls_rejected':2,
            'positive_and_singular_rank_controls':4,'total_rejections':failures}


def run(certificate):
    raw=certificate.read_bytes(); fixture=json.loads(raw)
    cases=fixture['cases']
    require(len(cases)==2 and [case['N'] for case in cases]==[82,85], 'wrong case coverage')
    return {'agent':'six-downset-3','role':'researcher',
            'scope':'Exact capped H and kernel ranks for two explicit nine-point downsets; product/equality conclusions use the written proof.',
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'cases':[audit(case) for case in cases],'controls':controls(cases)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',type=Path)
    parser.add_argument('--certificate',type=Path,default=Path(__file__).with_name('NINE_POINT_CERTIFICATES.json'))
    args=parser.parse_args()
    result=run(args.certificate)
    if args.check:
        require(result==json.loads(args.check.read_text()), 'expected result mismatch')
        print('exact nine-point certificates and controls match')
    else:
        print(json.dumps(result,indent=2,sort_keys=True))
