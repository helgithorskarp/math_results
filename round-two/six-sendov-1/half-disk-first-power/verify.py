#!/usr/bin/env python3
"""Finite exact algebra for the written degree-nine half-disk proof.

Author six-sendov-1, researcher. Same-author checking, not formalization
or independent review. Standard-library CPython3.10+. No network/data input.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
GAMMA=Q(63,80)
A_CELLS=((Q(2,5),Q(9,20)),(Q(9,20),Q(1,2)))
T_CELLS=((Q(0),Q(1,2),Q(2,3)),(Q(1,2),Q(1),Q(1)),
         (Q(1),Q(3,2),Q(7,6)),(Q(3,2),Q(2),Q(4,3)),
         (Q(2),Q(5,2),Q(3,2)),(Q(5,2),Q(3),Q(5,3)),
         (Q(3),Q(56,9),Q(7,3)))

def require(ok,message):
    if not ok:raise ValueError(message)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def add(a,b):
    c=[Q(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return c
def scale(a,x):return [v*x for v in a]
def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c
def power(a,n):
    c=[Q(1)]
    for _ in range(n):c=mul(c,a)
    return c
def area(a):return sum(v/Q(i+1) for i,v in enumerate(a))
def value(a,x):
    y=Q(0)
    for c in reversed(a):y=y*x+c
    return y
def pad(a,n):return list(a)+[Q(0)]*(n-len(a))
def interpolate(values):
    """Full coefficient recovery from degree+1 integer nodes."""
    n=len(values)-1
    out=[Q(0)]*(n+1)
    for i,v in enumerate(values):
        basis=[Q(1)];den=Q(1)
        for j in range(n+1):
            if i!=j:
                basis=mul(basis,[-Q(j),Q(1)])
                den*=i-j
        out=add(out,scale(basis,v/den))
    return out
def p_record(a):return [str(x) for x in a]

def moments(A,B):
    return [sum(Q(comb(8,l))*A**(8-l)*B**l/Q(l+j+1)
                for l in range(9)) for j in range(5)]

def certificate(damage=None):
    budgets=[]
    def bound(name,lhs,rhs,strict=True):
        require(lhs<rhs if strict else lhs<=rhs,'failed '+name)
        budgets.append(dict(id=name,lhs=str(lhs),rhs=str(rhs),strict=strict))
    bound('sqrt3',Q(3),Q(7,4)**2)
    bound('small-origin-endpoint',Q(53,100),Q(3,4)**2)
    bound('small-origin-ninth',Q(3,4)*Q(53,100)**4,Q(1,16))
    bound('common-phase-floor',Q(2,5),Q(9,20))
    bound('last-a-boundary',Q(9,20),Q(1,2))
    require(A_CELLS[0][0]==Q(2,5) and A_CELLS[-1][1]==Q(1,2),
            'entire a interval endpoints')
    require(A_CELLS[0][1]==A_CELLS[1][0],'a interval gap')
    require(T_CELLS[0][0]==0 and T_CELLS[-1][1]==Q(56,9),
            'entire T interval endpoints')
    require(all(T_CELLS[i][1]==T_CELLS[i+1][0] for i in range(6)),
            'T interval gap')
    cells=[]
    for ai,(lo,hi) in enumerate(A_CELLS):
        B=1-hi**2
        for ti,(L,U,d) in enumerate(T_CELLS):
            bound(f'disk-deviation-{ai}-{ti}',Q(7,8)*U,d*d,False)
            P=max(Q(0),(3-U)/2)
            M=hi+B
            N=hi+(1-lo**2)*(1+d)
            k1=lo*(1-lo**2)*P/N**2
            k2=B**2*L/(2*M*N)
            K=[Q(0),k1,k2]
            major=add(add([Q(1)],scale(K,-1)),scale(mul(K,K),Q(1,2)))
            polynomial=mul(power([hi,B],8),major)
            if damage=='last-polar-coefficient' and ai==1 and ti==6:
                polynomial[-1]+=1
            direct=interpolate([(hi+B*i)**8*(1-(k1*i+k2*i*i)
                                      +(k1*i+k2*i*i)**2/2)
                                for i in range(13)])
            require(pad(polynomial,13)==direct,'whole degree12 polar identity')
            m=moments(hi,B)
            second=m[0]-k1*m[1]+(-k2+k1*k1/2)*m[2]+k1*k2*m[3]+k2*k2*m[4]/2
            require(area(polynomial)==second,'binomial whole integration')
            bound(f'polar-cell-{ai}-{ti}',second,Q(199,200))
            cells.append(dict(a=[str(lo),str(hi)],T=[str(L),str(U)],d=str(d),
                              P=str(P),k1=str(k1),k2=str(k2),
                              coefficients=p_record(direct),integral=str(second)))
    scalar=[]
    for name,A,B in [('small-a',Q(2,5),Q(21,25)),
                     ('radius-mass',Q(1,2),Q(3,4)*Q(39,40))]:
        pol=power([A,B],8)
        other=[Q(comb(8,l))*A**(8-l)*B**l for l in range(9)]
        require(pol==other,'full scalar binomial coefficients')
        require(area(pol)==moments(A,B)[0],'full scalar integral')
        bound(name,area(pol),Q(1))
        scalar.append(dict(id=name,coefficients=p_record(pol),integral=str(area(pol))))
    c=[Q(1),Q(0)]
    for l in range(2,9):c.append(sum(c[l-k] for k in range(2,l+1))/l)
    if damage=='newton-eighth-bound':c[8]=0
    require(c==[Q(1),Q(0),Q(1,2),Q(1,3),Q(3,8),Q(11,30),
                 Q(53,144),Q(103,280),Q(2119,5760)],'all Newton majorants')
    beta=[Q(1),-GAMMA,Q(1,4)]
    origin=[];R=Q(0)
    for l in range(2,9):
        h=power(beta,(8-l)//2)
        if l%2:h=mul(h,scale(add([Q(1)],beta),Q(1,2)))
        energy=Q(3)**(l//2)*(Q(7,4) if l%2 else 1)
        pol=scale([Q(0)]*l+h,9*Q(1,2)**l*c[l]*energy)
        if damage=='origin-drop-eighth' and l==8:pol=[Q(0)]*len(pol)
        # Independently form each beta power by multinomial coefficients.
        def beta_multinomial(n):
            out=[Q(0)]*(2*n+1)
            for i in range(n+1):
                for j in range(n-i+1):
                    out[i+2*j]+=Q(comb(n,i)*comb(n-i,j))*(-GAMMA)**i*Q(1,4)**j
            return out
        m=(8-l)//2
        h2=beta_multinomial(m)
        if l%2:h2=scale(add(h2,beta_multinomial(m+1)),Q(1,2))
        pol2=scale([Q(0)]*l+h2,9*Q(1,2)**l*c[l]*energy)
        require(pad(pol,len(pol2))==pol2,'full centered origin polynomial')
        R+=area(pol)
        origin.append(dict(l=l,c=str(c[l]),energy=str(energy),
                           coefficients=p_record(pol),integral=str(area(pol))))
    require(R==Q(795509283,917504000),'seven-term exact origin sum')
    bound('whole-origin-remainder',R,Q(111,128))
    # Whole monotonicity polynomial, including its positive global floor.
    monotone=[Q(2),-10*GAMMA,Q(8)]
    square=add(scale(power([-Q(63,128),Q(1)],2),Q(8)),[Q(127,2048)])
    if damage=='monotone-square':square[0]-=1
    require(monotone==square,'entire monotonicity square completion')
    bound('monotone-floor',Q(0),Q(127,2048))
    bound('final-origin-gap',Q(1),Q(15,8)-Q(111,128))
    newton=newton_maps(damage)
    controls=gaussian_controls(damage)
    return dict(schema='sendov-half-disk-exact-v1',agent='six-sendov-1',role='researcher',
                claim='F>8 at every marked root |a|<=1/2 for actual complex degree nine',
                actual_domains=dict(originals='all9 closed disk',critical='all8 with multiplicity',
                                    denominator_zero='infinity',conjugation=False,
                                    separation=False,second_moment_premise=False),
                polar_cells=cells,scalar_integrals=scalar,origin_terms=origin,
                origin_sum=str(R),monotonicity=p_record(monotone),
                newton=newton,gaussian_controls=controls,budgets=budgets,
                global_first_power_resolved=False,formalized=False,
                independent_review=False)

# Generic eight-variable sparse polynomials; no imposed symmetry or balance.
ZERO=(0,)*8
def sadd(a,b,f=Q(1)):
    c=dict(a)
    for k,v in b.items():
        c[k]=c.get(k,Q(0))+f*v
        if c[k]==0:del c[k]
    return c
def smul(a,b):
    c={}
    for k,v in a.items():
        for h,w in b.items():
            key=tuple(x+y for x,y in zip(k,h))
            c[key]=c.get(key,Q(0))+v*w
    return {k:v for k,v in c.items() if v}
def sparse_record(a):return [[list(k),str(v)] for k,v in sorted(a.items())]
def newton_maps(damage):
    variables=[]
    for j in range(8):
        k=list(ZERO);k[j]=1;variables.append({tuple(k):Q(1)})
    e=[{ZERO:Q(1)}]+[{} for _ in range(8)]
    for var in variables:
        for l in range(8,0,-1):e[l]=sadd(e[l],smul(e[l-1],var))
    p=[{}]
    for l in range(1,9):
        p.append({tuple(l if i==j else 0 for i in range(8)):Q(1) for j in range(8)})
    ids=[]
    for l in range(1,9):
        route={}
        for k in range(1,l+1):route=sadd(route,smul(e[l-k],p[k]),Q((-1)**(k-1),l))
        if damage=='newton-last-sign' and l==8:route=sadd(route,p[8],Q(1,4))
        require(route==e[l],'full generic Newton identity '+str(l))
        ids.append(dict(l=l,e=sparse_record(e[l]),power_sum=sparse_record(p[l]),
                        complete_residual=sparse_record(sadd(route,e[l],-1))))
    return ids

# Exact Gaussian rational arithmetic, separate subset and convolution routes.
def ca(z,w):return z[0]+w[0],z[1]+w[1]
def cs(z,x):return z[0]*x,z[1]*x
def cm(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def norm2(z):return z[0]**2+z[1]**2
def c_record(z):return [str(z[0]),str(z[1])]
def complex_coeff(q,c,b):
    out=[(Q(1),Q(0))]
    for z in q:
        new=[(Q(0),Q(0))]*(len(out)+1)
        for i,v in enumerate(out):
            new[i]=ca(new[i],cs(v,c))
            new[i+1]=ca(new[i+1],cs(cm(v,z),b))
        out=new
    return out
def subset_coeff(q,c,b):
    out=[]
    for l in range(9):
        acc=(Q(0),Q(0))
        for subset in itertools.combinations(range(8),l):
            term=(Q(1),Q(0))
            for j in subset:term=cm(term,q[j])
            acc=ca(acc,term)
        out.append(cs(acc,c**(8-l)*b**l))
    return out
def complex_area(poly):
    result=(Q(0),Q(0))
    for i,z in enumerate(poly):result=ca(result,cs(z,Q(1,i+1)))
    return result
def gaussian_controls(damage):
    controls=[]
    for index in range(4):
        a=(Q(9,20),Q(19,40),Q(1,2),Q(1,2))[index]
        radii=([Q(9,8)]+[Q(55,56)]*7 if index<3
               else [Q(3,2)]+[Q(13,14)]*7)
        q=[]
        for j,r in enumerate(radii):
            t=Q((j+1)*(index+1),2000)
            q.append((r*(1-t*t)/(1+t*t),r*2*t/(1+t*t)))
        require(sum(radii)==8 and all(norm2(z)==r*r for z,r in zip(q,radii)),
                'exact Gaussian radii and first power')
        require(sum(norm2(z) for z in q)>8,'controls outside quadratic sublevel')
        require(all((1-a*a)*norm2(z)+2*a*z[0]>=1 for z in q),'whole critical disks')
        coefficients=[];integrals=[]
        for c,b in ((Q(1),-a),(a,1-a*a)):
            left=complex_coeff(q,c,b);right=subset_coeff(q,c,b)
            if damage=='gaussian-last-coefficient' and index==3:
                right[8]=ca(right[8],(Q(1),Q(0)))
            require(left==right,'all nine Gaussian coefficients')
            coefficients.append(left);integrals.append(complex_area(left))
        O=cs(integrals[0],Q(9));J=integrals[1]
        require(norm2(J)>1 and norm2(O)>Q(129,128)**2,'entire abstract controls')
        mu=cs(tuple(map(sum,zip(*q))),Q(1,8))
        w=[ca(z,cs(mu,-1)) for z in q]
        e=[(Q(1),Q(0))]+[(Q(0),Q(0))]*8
        for z in w:
            for l in range(8,0,-1):e[l]=ca(e[l],cm(e[l-1],z))
        centered=[(Q(0),Q(0))]*9
        for l in range(9):
            diagonal=complex_coeff([mu]*(8-l),Q(1),-a)
            for i,z in enumerate(diagonal):
                centered[i+l]=ca(centered[i+l],cs(cm(e[l],z),(-a)**l))
        require(centered==coefficients[0],'full centered eight-factor expansion')
        controls.append(dict(a=str(a),q=[c_record(z) for z in q],r=[str(r) for r in radii],
                             all_nine_origin_coefficients=[c_record(z) for z in coefficients[0]],
                             all_nine_polar_coefficients=[c_record(z) for z in coefficients[1]],
                             O=c_record(O),J=c_record(J),outside_second_moment=True,
                             original_disk_feasibility_asserted=False))
    return controls

def typed_equal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--damage',choices=('last-polar-coefficient','newton-eighth-bound',
                                          'origin-drop-eighth','monotone-square',
                                          'newton-last-sign','gaussian-last-coefficient'))
    args=parser.parse_args()
    if not args.emit:
        manifest=json.loads((HERE/'MANIFEST.json').read_text())
        for name,info in manifest['files'].items():
            data=(HERE/name).read_bytes()
            require(len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256'],
                    'source pin '+name)
    record=certificate(args.damage)
    if args.emit:
        print(json.dumps(record,indent=2,sort_keys=True));return
    expected=json.loads(args.expected.read_text())
    require(typed_equal(record,expected),'entire typed exact record')
    print(json.dumps(dict(result='PASS',agent='six-sendov-1',role='researcher',
                          record_sha256=digest(record),polar_cells=14,full_newton_identities=8,
                          full_origin_terms=7,gaussian_controls=4,
                          rational_budgets=len(record['budgets']),
                          global_first_power_resolved=False)))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
