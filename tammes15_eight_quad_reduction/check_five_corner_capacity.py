#!/usr/bin/env python3
"""Exact bookkeeping for FIVE_CORNER_CAPACITY.md, CPython>=3.11, stdlib.

Angles/branches and geometric incidence implications are written hand
proofs. No floating angle evaluation or embedding enumeration is used.
"""
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
import sys

import check as base
import check_topology as previous


def trim(p):
    p = tuple(F(x) for x in p)
    while len(p)>1 and not p[-1]:
        p = p[:-1]
    return p


def add(p,q):
    return trim(tuple((p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0)
                      for i in range(max(len(p),len(q)))))


def scale(k,p):
    return trim(tuple(F(k)*v for v in p))


def mul(p,q):
    out = [F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):
            out[i+j] += x*y
    return trim(out)


def symbolic(p,c):
    out = base.Poly(0)
    for i,a in enumerate(p):
        out += a*c**i
    return out


def polynomial_checks():
    one,c = (F(1),),(F(0),F(1))
    c2=mul(c,c); c4=mul(c2,c2)
    A=add(add(one,scale(2,c)),scale(-1,c2))
    B=add(one,scale(2,c))
    g=add(add(one,c),scale(-4,c2))
    P=scale(2,mul(c2,B))
    difference=add(mul(A,A),scale(-4,mul(c4,mul(B,B))))
    factored=mul(mul(add(one,c),g),add(A,P))
    endpoint=add((F(4,25),),mul((F(3,5),F(-1)),(F(7,5),F(4))))
    base.need(difference==factored and g==endpoint, 'exact angle sign factorization')
    base.need(add(A,scale(-1,P))==mul(add(one,c),g), 'first difference-of-squares factor')
    # Cross-multiplied numerator of cos(y)+c/(1+c), after substituting tan^2(x/2).
    K=scale(4,mul(c4,B))
    crossed=add(mul(add(one,c),add(K,scale(-1,mul(A,A)))),
                mul(c,add(K,mul(A,A))))
    base.need(crossed==scale(-1,difference), 'cosine comparison numerator sign')
    # Independently expand with the existing sparse exact symbolic implementation.
    z=base.variable(0)
    Az,Bz=1+2*z-z**2,1+2*z
    identities=(Az**2-4*z**4*Bz**2-(1+z)*(1+z-4*z**2)*(Az+2*z**2*Bz),
                1+z-4*z**2-F(4,25)-(F(3,5)-z)*(4*z+F(7,5)),
                symbolic(difference,z)-(Az**2-4*z**4*Bz**2))
    base.need(all(not p.terms for p in identities), 'independent sparse polynomial identities')
    base.need(sum(a*F(3,5)**i for i,a in enumerate(g))==F(4,25),
              'positive upper endpoint margin')
    base.need(F(7,3)**2-5==F(4,9), 'sqrt-five comparison exact square margin')
    return {'coefficient_order':'ascending powers of c',
            'cosine_gap_positive_numerator':[str(a) for a in difference],
            'first_factor':'(1+c)(1+c-4c^2)',
            'positive_endpoint_identity':'1+c-4c^2=4/25+(3/5-c)(4c+7/5)',
            'positive_endpoint_margin':'4/25','sqrt5_square_margin':'4/9',
            'independent_dense_and_sparse_coefficients_match':True,
            'trigonometric_branches_and_cosine_monotonicity_are_written_proofs':True}


def lin(*a):
    base.need(len(a)==3,'linear angle dimensions')
    return tuple(F(x) for x in a)


def ladd(a,b):
    return tuple(x+y for x,y in zip(a,b))


def lscale(k,a):
    return tuple(F(k)*x for x in a)


def linear_angle_checks():
    pi,alpha,y=lin(1,0,0),lin(0,1,0),lin(0,0,1)
    x,A0=ladd(lscale(2,pi),lscale(-4,alpha)),ladd(lscale(2,pi),lscale(-2,alpha))
    gap=ladd(ladd(y,alpha),lscale(-1,pi))
    two_y_vertex_gap=ladd(ladd(lscale(2,y),lscale(2,alpha)),lscale(-2,pi))
    base.need(two_y_vertex_gap==lscale(2,gap),'two-y-corner vertex contradiction')
    base.need(ladd(ladd(pi,lscale(-1,alpha)),lscale(-1,x))==lin(-1,3,0),
              'pi-alpha exceeds x')
    residuals=(ladd(A0,lscale(-2,x)),
               ladd(ladd(A0,lscale(-1,x)),lscale(-1,y)),
               ladd(lscale(2,y),lscale(-1,A0)))
    base.need(residuals==(lin(-2,6,0),lin(0,2,-1),lscale(2,gap)),
              'ordinary-four two-five-Q sum contradictions')
    return {'formal_variable_order':['pi','alpha','y'],
            'two_y_vertex_gap':[str(a) for a in two_y_vertex_gap],
            'A0_minus_2x':[str(a) for a in residuals[0]],
            'A0_minus_x_minus_y':[str(a) for a in residuals[1]],
            '2y_minus_A0':[str(a) for a in residuals[2]],
            'strict_sign_inputs':['alpha>pi/3','y<2alpha','y>pi-alpha'],
            'zero_three_Q_angle_is_strictly_above_x_is_a_written_angle_sum_proof':True}


def face_summary(mask):
    base.need(type(mask) is int and 0<=mask<16,'four-corner five mask')
    f=tuple(bool(mask>>i&1) for i in range(4))
    base.need(not any(f[i] and f[(i+1)%4] for i in range(4)),
              'adjacent ordinary fives cannot share Q')
    corners=[i for i in range(4) if not f[i] and (f[i-1] or f[(i+1)%4])]
    count=sum(f)
    base.need(count<=2 and len(corners)==(2 if count else 0),'distinct y-corner count')
    labels=['x' if f[i] else 'y' if i in corners else 'x' if count else 'unfixed'
            for i in range(4)]
    return {'five_corners':count,'five_neighbor_incidences':2*count,
            'distinct_y_corners':corners,'fixed_angle_labels':labels}


def local_checks():
    rows={}
    for mask in range(16):
        f=tuple(bool(mask>>i&1) for i in range(4))
        if not any(f[i] and f[(i+1)%4] for i in range(4)):
            rows[str(mask)]=face_summary(mask)
    base.need(list(map(int,rows))==[0,1,2,4,5,8,10],'all admissible cyclic five masks')
    isolated=[]
    sectors_checked=0
    for tm in range(16):
        if tm.bit_count()>2:
            continue
        for i in range(4):
            if tm>>i&1:
                continue
            sectors_checked+=1
            if tm>>((i-1)%4)&1 and tm>>((i+1)%4)&1:
                row=previous.star(4,tm,0)
                base.need(row['triangle_sectors']==2 and row['Q_fans']==2,
                          'two-five corner must be a separated ordinary-four Q')
                isolated.append([tm,i])
    base.need(isolated==[[5,1],[5,3],[10,0],[10,2]], 'complete isolated Q-sector census')
    return {'four_corner_masks_checked':16,'admissible_five_masks':rows,
            'four_vertex_Q_sectors_checked':sectors_checked,
            'two_five_neighbor_Q_sectors':isolated,
            'two_Qs_with_two_opposite_fives_need_four_distinct_separated_fours':True}


def degree_capacity_checks():
    models=defaultdict(set)
    degree_allocations=0
    direct_count=0
    for r,n4,n5 in product(range(16),repeat=3):
        if r+n4+n5!=15 or 3*r+4*n4+5*n5!=62:
            continue
        for a,p in product(range(n4+1),repeat=2):
            m=n4-a-p
            if m<0 or a+2*m+4*n5!=30:
                continue
            degree_allocations+=1
            base.need(n5==r+2 and n4==13-2*r and a+2*p==4
                      and m==9-2*r+p,'independent degree and T-corner identities')
            for s in range(m+1):
                ends=3*r+4*p+2*a+(m-s)
                if ends%2:
                    continue
                base.need(ends==17+r+p-s,'independent QQ edge-end identity')
                for f1,f2 in product(range(9),repeat=2):
                    if f1+f2>8 or f1+2*f2!=n5:
                        continue
                    if 2*(f1+f2)<=n4-p and 2*f2<=s:
                        base.need(2*n5<=n4-p+s,'capacity follows from separate corner counts')
                        base.need(r<=2,'ordinary-five integer model cannot have r>=3')
                        models[(p,r)].add((s,f1,f2))
                        direct_count+=1
    expected_profile_keys={(p,r) for p in range(3) for r in range(3)}
    base.need(set(models)==expected_profile_keys,'all nine ordinary-five aggregate profiles')
    # A second enumeration uses only the weaker combined capacity inequality.
    weaker=[]
    for p,r in product(range(3),range(16)):
        m=9-2*r+p
        if m<0:
            continue
        for s in range(m+1):
            if s>=4*r+p-9 and (r+p+s)%2==1:
                base.need(r<=2,'capacity plus parity independently forces r<=2')
                weaker.append((p,r,s))
    direct_s={(p,r,s) for (p,r),rows in models.items() for s,_,_ in rows}
    base.need(direct_s<=set(weaker),'direct masks obey combined capacity')
    # Combined capacity omits integrality of f2; record the precise extra relaxation.
    base.need(set(weaker)-direct_s=={(2,2,1)},'integer two-five-face rounding difference')
    rejected_r3=[]
    for p in range(3):
        r,s=3,3+p
        base.need(s==9-2*r+p and s==4*r+p-9 and (r+p+s)%2==0,
                  'r3 extremal capacity and parity contradiction for every p')
        rejected_r3.append({'p':p,'n3':r,'forced_s':s,'QQ_edge_end_count':17+r+p-s,
                            'QQ_edge_end_count_is_odd':True})
    out=[{'p':p,'n3':r,'n4':13-2*r,'n5':r+2,
          'ordinary_fours':9-2*r+p,'admitted_s':sorted({s for s,_,_ in rows}),
          'admitted_five_face_count_vectors':len(rows)}
         for (p,r),rows in sorted(models.items())]
    return {'degree_and_T_corner_allocations_checked':degree_allocations,
            'direct_five_face_capacity_models':direct_count,
            'weaker_capacity_parity_s_models':len(weaker),
            'direct_capacity_s_models':len(direct_s),
            'rounding_difference':[[2,2,1]],'maximum_n3':2,
            'ordinary_five_aggregate_profiles_before_double_zero_exclusion':out,
            'r3_capacity_parity_rejections':rejected_r3}


def cover():
    old=previous.cover()
    retained=[deepcopy(p) for p in old['profiles'] if p['n3']<=2]
    removed=[deepcopy(p) for p in old['profiles'] if p['n3']>2]
    direct=[]
    for row in old['distributions']:
        if not row['allowed_H_codes']:
            continue
        for n3,n4,n5 in product(range(16),repeat=3):
            if (n3<=2 and n3+n4+n5==15 and 3*n3+4*n4+5*n5==62
                    and n4>=row['d41']+row['d42']):
                direct.append({'d41':row['d41'],'d42':row['d42'],'d51':row['d51'],
                               'n3':n3,'n4':n4,'n5':n5,'H_codes':row['allowed_H_codes'][:]})
    base.need(retained==direct,'entry-level independent six-profile generation')
    base.need(len(removed)==1 and (removed[0]['d41'],removed[0]['d42'],removed[0]['n3'])==(4,0,3),
              'sole newly removed largest profile')
    rows=deepcopy(old['distributions'])
    for row in rows:
        row['surviving_degree_profiles']=sum(
            all(p[k]==row[k] for k in ('d41','d42','d51')) for p in retained)
    base.need(len(retained)==6 and sum(len(row['allowed_H_codes']) for row in rows)==11,
              'six profiles and unchanged eleven global auxiliary types')
    return {'previous_degree_profiles':7,'remaining_degree_profiles':6,
            'previous_colored_H_types':11,'remaining_colored_H_types':11,
            'remaining_deficit_distributions':2,'removed_profiles':removed,
            'distributions':rows,'profiles':retained,
            'restriction':'At most two degree threes in the ordinary-five branch',
            'capacity_inequality':'2n5 <= n4-p+s',
            'extra_incidence_restrictions':['No degree-three Q contains an ordinary five',
                                          'An ordinary four meets at most one Q containing a five']}


def selftest():
    controls=0
    def test(value,message):
        nonlocal controls
        base.need(value,message)
        controls+=1
    for mask in (-1,16,True,3,7,15):
        try:
            face_summary(mask)
        except ValueError:
            controls+=1
        else:
            raise ValueError('invalid or adjacent-five face mask accepted')
    test(face_summary(5)['five_neighbor_incidences']==4
         and len(face_summary(5)['distinct_y_corners'])==2,'opposite fives count two y corners')
    test(face_summary(1)['five_neighbor_incidences']==2
         and len(face_summary(1)['distinct_y_corners'])==2,'single five counts two y corners')
    test(face_summary(0)['distinct_y_corners']==[],'zero-five face supplies no counted corner')
    test(mul((1,1),(1,-1))==(1,0,-1),'dense polynomial convolution')
    test(trim((0,0,0))==(0,),'zero polynomial normalization')
    test(F(4,25)>0 and F(4,9)>0,'strict rational margins')
    test(4*3-9==3 and 9-2*3==3 and (3+3)%2==0,
         'r3 at capacity equality still fails QQ parity')
    test(2*(2+2)<=9-0+1,'r2 all-one-deficit is retained by capacity')
    test(2*(2+2)==9-1+0,'mixed r2 s0 equality is retained')
    return controls


def main():
    base.need(sys.argv[1:] in ([],['--selftest']),
              'usage: check_five_corner_capacity.py [--selftest]')
    algebra,angles,local,degrees,remaining=(polynomial_checks(),linear_angle_checks(),
                                          local_checks(),degree_capacity_checks(),cover())
    if sys.argv[1:]:
        print(json.dumps({'status':'PASS','controls':selftest(),'degree_profiles':6,
                          'colored_H_types':11,'maximum_n3':2},sort_keys=True))
    else:
        print(json.dumps({'agent':'six-tammes-1','role':'researcher',
                          'scope':'exact sign/incidence bookkeeping; geometric angle bridges written separately',
                          'polynomial_checks':algebra,'linear_angle_checks':angles,
                          'local_corner_checks':local,'degree_capacity_checks':degrees,
                          'cover':remaining},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
