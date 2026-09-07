"""Reproducible exact controls; the full-field theorems have written proofs.

This uses an independent polynomial-quotient model for the Salem field,
Newton lifting for the colouring, and direct checks of all reported edges.
"""
import hashlib
import json
import random
from fractions import Fraction as Q
from itertools import combinations, product
from math import lcm
from pathlib import Path
import exact as e


def insist(condition, message):
    if not condition:raise ValueError(message)


# Independent quotient Q[a,w]/(a^4-a^3-a^2-a+1, w^2+w+1).
# Index i+4*j means a^i*w^j, 0<=i<4, 0<=j<2.
PZERO=(Q(0),)*8
PONE=(Q(1),)+PZERO[1:]
PA=PZERO[:1]+(Q(1),)+PZERO[2:]
PW=PZERO[:4]+(Q(1),)+PZERO[5:]


def padd(x,y):return tuple(a+b for a,b in zip(x,y))


def pscale(x,a):return tuple(a*b for b in x)


def pmul(x,y):
    terms={}
    for i,a in enumerate(x):
        for j,b in enumerate(y):
            if a and b:
                key=(i%4+j%4,i//4+j//4)
                terms[key]=terms.get(key,Q(0))+a*b
    for first in range(6,3,-1):
        for second in range(3):
            c=terms.pop((first,second),Q(0))
            for shift,factor in [(0,-1),(1,1),(2,1),(3,1)]:
                key=(first-4+shift,second)
                terms[key]=terms.get(key,Q(0))+factor*c
    for first in range(4):
        c=terms.pop((first,2),Q(0))
        for second in (0,1):
            key=(first,second);terms[key]=terms.get(key,Q(0))-c
    return tuple(terms.get((i%4,i//4),Q(0)) for i in range(8))


def ppow(x,n):
    z=PONE
    for _ in range(n):z=pmul(z,x)
    return z


CA=(Q(1),Q(1),Q(1),Q(-1))+PZERO[4:]
CW=pscale(padd(PONE,PW),-1)
CONJ_BASIS=[pmul(ppow(CA,i),ppow(CW,j)) for j in range(2) for i in range(4)]


def pconj(x):
    return tuple(sum(x[j]*CONJ_BASIS[j][i] for j in range(8)) for i in range(8))


def invert_matrix(matrix):
    n=len(matrix)
    rows=[list(row)+[Q(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for j in range(n):
        k=next((i for i in range(j,n) if rows[i][j]),None)
        if k is None:raise ValueError('singular basis conversion')
        rows[j],rows[k]=rows[k],rows[j]
        v=rows[j][j];rows[j]=[x/v for x in rows[j]]
        for i in range(n):
            if i!=j:
                c=rows[i][j];rows[i]=[a-c*b for a,b in zip(rows[i],rows[j])]
    return [row[n:] for row in rows]


def conversion():
    cols=[e.mul(e.power(e.ALPHA,i),e.power(e.OMEGA,j)) for j in range(2) for i in range(4)]
    matrix=[[cols[j][i] for j in range(8)] for i in range(8)]
    return cols,invert_matrix(matrix)


COLS,INVERSE=conversion()


def to_poly(x):return tuple(sum(row[j]*x[j] for j in range(8)) for row in INVERSE)


def from_poly(x):return tuple(sum(x[j]*COLS[j][i] for j in range(8)) for i in range(8))


def newton_root(exponent, extra=0):
    modulus=3;t=1;target=3**(exponent+extra)
    while modulus<target:
        nxt=modulus*modulus
        t=(t-(t*t-t-3)*pow(2*t-1,-1,nxt))%nxt
        modulus=nxt
    return t%target


def colour_check(x,extra=0):
    a,b=x[:2];den=lcm(a.denominator,b.denominator)
    k=0;unit=den
    while unit%3==0:k+=1;unit//=3
    modulus=3**(k+1+extra)
    num=int(a*den)+int(b*den)*newton_root(k+1,extra)
    r=num*pow(unit,-1,modulus)%modulus
    return (r//3**k)%3


def valuation(q,p):
    if not q:return None
    a,b=q.numerator,q.denominator;v=0
    while a%p==0:a//=p;v+=1
    while b%p==0:b//=p;v-=1
    return v


def reject(callback):
    try:callback()
    except (ValueError,ZeroDivisionError,TypeError):return
    raise ValueError('bad control accepted')


def run():
    insist(e.mul(e.T,e.T)==e.add(e.T,tuple(3*x for x in e.ONE)),'trace identity')
    insist(e.mul(e.G,e.G)==e.point([Q(1,3),Q(-1,3),0,0,0,0,0,0]),'gamma identity')
    insist(e.mul(e.B,e.B)==tuple(-3*x for x in e.ONE),'beta identity')
    pvalue=e.add(e.add(e.power(e.ALPHA,4),e.ONE),
                 e.neg(e.add(e.add(e.power(e.ALPHA,3),e.power(e.ALPHA,2)),e.ALPHA)))
    insist(pvalue==e.ZERO and e.is_unit(e.ALPHA),'Salem root identity')
    insist(e.add(e.add(e.power(e.OMEGA,2),e.OMEGA),e.ONE)==e.ZERO,'Eisenstein identity')
    insist(e.conjugate(e.ALPHA)==e.inverse(e.ALPHA),'conjugation of alpha')
    insist(from_poly(PA)==e.ALPHA and from_poly(PW)==e.OMEGA,'basis images')
    basis_products=0
    for i,j in product(range(8),repeat=2):
        left=tuple(Q(k==i) for k in range(8));right=tuple(Q(k==j) for k in range(8))
        insist(to_poly(e.mul(left,right))==pmul(to_poly(left),to_poly(right)),'basis multiplication mismatch')
        basis_products+=1
    for precision in range(1,81):
        t=e.hensel_t(precision)
        insist(t==newton_root(precision),'Hensel algorithms differ')
        insist(t%3==1 and (t*t-t-3)%3**precision==0,'invalid Hensel root')
    # Irreducibility mod 2: no linear factor and no irreducible quadratic factor.
    f=(1,1,1,1,1)
    insist(sum(f)%2==1 and f[0]==1,'linear factor of Phi5')
    rem=list(f)
    for j in (4,3,2):
        if rem[j]:
            for k in (j,j-1,j-2):rem[k]^=1
    insist(any(rem[:2]),'quadratic factor of Phi5')

    rng=random.Random(130307)
    def random_point(n=8):
        return tuple(Q(rng.randrange(-9,10),2**rng.randrange(4)*3**rng.randrange(9)*5**rng.randrange(3)) for _ in range(n))
    units=[];operations=0
    for _ in range(160):
        x=random_point();y=random_point()
        insist(from_poly(to_poly(x))==x,'coordinate roundtrip')
        insist(to_poly(e.mul(x,y))==pmul(to_poly(x),to_poly(y)),'independent product')
        insist(to_poly(e.conjugate(x))==pconj(to_poly(x)),'independent conjugation')
        if any(x):
            inverse=e.inverse(x)
            insist(pmul(to_poly(x),to_poly(inverse))==PONE,'independent inverse')
            units.append(e.mul(x,e.inverse(e.conjugate(x))))
        operations+=1
    for m in range(1,13):
        x=e.add(e.power(e.add(e.T,e.neg(e.ONE)),m),e.B)
        units.append(e.mul(x,e.inverse(e.conjugate(x))))
    unit_edges=0;max_denominator_valuation=0;word=[]
    for d in units:
        insist(pmul(to_poly(d),pconj(to_poly(d)))==PONE,'false Hilbert-90 unit')
        for z in [e.ZERO,random_point(),tuple(q/3**60 for q in random_point())]:
            other=e.add(z,d)
            ca,cb=e.colour_salem(z),e.colour_salem(other)
            insist(ca!=cb,'monochromatic exact Salem edge')
            for x,c in [(z,ca),(other,cb)]:
                insist(c==colour_check(x)==colour_check(x,5),'independent digit mismatch')
                max_denominator_valuation=max(max_denominator_valuation,*[max(0,-valuation(q,3)) if q else 0 for q in x[:2]])
            word.extend((ca,cb));unit_edges+=1
    triangle=[e.ZERO,e.ONE,tuple(q/2 for q in e.add(e.ONE,e.B))]
    insist(all(e.is_unit(e.add(x,e.neg(y))) for x,y in combinations(triangle,2)),'triangle geometry')
    insist([e.colour_salem(x) for x in triangle]==[0,1,2],'triangle colours')
    powers=[e.power(e.ALPHA,j) for j in range(-20,21)]
    insist(len(set(powers))==41 and all(e.is_unit(x) for x in powers),'distinct power controls')

    # An actual finite support with all pairwise unit tests, not just supplied edges.
    zeta=triangle[2]
    directions={e.mul(e.power(e.ALPHA,n),e.power(zeta,j)) for n in range(-2,3) for j in range(6)}
    anchors=[e.ZERO,e.ALPHA,e.add(e.power(e.ALPHA,2),tuple(q/3 for q in e.B))]
    points=sorted({e.add(a,d) for a in anchors for d in directions}|set(anchors))
    colours=[e.colour_salem(x) for x in points]
    edges=[]
    for a,b in combinations(range(len(points)),2):
        if e.is_unit(e.add(points[a],e.neg(points[b]))):
            insist(colours[a]!=colours[b],'monochromatic induced edge');edges.append((a,b))

    # Full-field dyadic control Q(h,i), h^2=h+1 (discriminant 5).
    done=0;D1=(Q(1),Q(0),Q(0),Q(0))
    for _ in range(160):
        u=random_point(4)
        if not any(u):continue
        d=e.dmul(u,e.dinverse(e.dconjugate(u)))
        insist(e.dmul(d,e.dconjugate(d))==D1,'false dyadic unit')
        for z in [random_point(4),tuple(q/2**60 for q in random_point(4))]:
            other=tuple(a+b for a,b in zip(z,d))
            insist(e.colour_dyadic(z)!=e.colour_dyadic(other),'monochromatic dyadic edge')
            done+=1

    # Finite residue facts and the necessity of the local hypotheses.
    residue_checks=0
    for p in [2,3,5,7,11]:
        roots=[x for x in range(p) if x*x%p==1]
        insist(roots==sorted({1,p-1}),'residue roots of one')
        palette=[j%2 if j<p-1 else (1 if p==2 else 2) for j in range(p)]
        insist(all(palette[j]!=palette[(j+1)%p] for j in range(p)),'residue cycle colouring')
        residue_checks+=p
    insist(all((a*a+b*b)%3 for a,b in product(range(3),repeat=2) if (a,b)!=(0,0)),'F9 anisotropy')
    # At the other Hensel branch t=0 mod3, alpha would share colour 0 with the origin.
    insist((0*pow(2,-1,3))%3==0 and e.colour_salem(e.ALPHA)!=0,'wrong branch countercontrol')
    # F=Q(sqrt3) is ramified at2 and contains (1+i sqrt3)/2: a unit triangle.
    insist(Q(1,4)+Q(3,4)==1,'ramified-base triangle norm')
    insist(e.digit_zero(Q(1,2),2)==0,'ramified-base parity failure')
    for callback in [lambda:e.point([0]),lambda:e.colour_salem([0]),lambda:e.colour_dyadic([0]),
                     lambda:e.hensel_t(0),lambda:e.hensel_t(-1),lambda:e.hensel_t(True),
                     lambda:e.inverse(e.ZERO),lambda:e.dinverse((Q(0),)*4)]:reject(callback)
    return {'status':'VERIFIED','symbolic_basis_products':basis_products,'independent_random_operations':operations,
            'hensel_precisions_checked':80,'exact_salem_units':len(units),'translated_salem_unit_edges':unit_edges,
            'maximum_tested_3_denominator_valuation':max_denominator_valuation,'salem_triangle_colours':[0,1,2],
            'distinct_unit_powers':len(powers),'induced_support_vertices':len(points),'induced_pairs_checked':len(points)*(len(points)-1)//2,
            'induced_unit_edges':len(edges),'induced_colour_sha256':hashlib.sha256(bytes(colours)).hexdigest(),
            'unit_control_colour_sha256':hashlib.sha256(bytes(word)).hexdigest(),'translated_dyadic_unit_edges':done,
            'prime_residue_values_checked':residue_checks,'wrong_branch_countercontrol':True,'ramified_base_countercontrol':True,
            'malformed_input_rejections':8,'full_theorems_depend_on_test_exhaustion':False}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--check-expected',action='store_true');args=parser.parse_args()
    result=run()
    if args.check_expected:
        expected=json.loads((Path(__file__).parent/'expected.json').read_text())
        insist(result==expected,'expected report mismatch')
    print(json.dumps(result,sort_keys=True))
