#!/usr/bin/env python3
"""Whole finite analytic checks. Standard-library rational arithmetic, same author.

All coefficients and integrals are compared before any extrema/fingerprint.
The compact expected record is a change detector, not the proof of coverage.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import comb, factorial, isqrt
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
LOW=Q(11,20); H=Q(3,5); C=Q(13,20)
BM=Q(16,25); BX=Q(279,400); AB=Q(3069,8000); TM=Q(63,8)
ENERGY=Q(17,4); MASS=Q(186,25); GAMMA=Q(1063,1600); TARGET=Q(257,256)
ROOT=(LOW,H,GAMMA,Q(1),Q(0),ENERGY/8)
PINS=('.gitignore','PROOF.md','LITERATURE.md','README.md','verify.py',
      'validate.py','COVER.json','EXPECTED.json')

def require(ok,message):
    if not ok: raise ValueError(message)
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x): return sha256(canonical(x)).hexdigest()
def add(a,b):
    out=[Q(0)]*max(len(a),len(b))
    for j,x in enumerate(a):out[j]+=x
    for j,x in enumerate(b):out[j]+=x
    return out
def scale(a,c):return [x*c for x in a]
def mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for j,x in enumerate(a):
        for k,y in enumerate(b):out[j+k]+=x*y
    return out
def power(a,n):
    out=[Q(1)]
    for _ in range(n):out=mul(out,a)
    return out
def integral(a):return sum((x/Q(j+1) for j,x in enumerate(a)),Q(0))
def strings(a):return [str(x) for x in a]
def ceiling(x,den):
    require(x>=0,'nonnegative square operand')
    n=isqrt(x.numerator*den*den//x.denominator)
    if Q(n,den)**2<x:n+=1
    r=Q(n,den)
    require(r*r>=x and (n==0 or Q(n-1,den)**2<x),'complete rational ceiling')
    return r

def typed_equal(x,y,where='expected'):
    require(type(x) is type(y),'type '+where)
    if isinstance(x,dict):
        require(set(x)==set(y),'keys '+where)
        for k in x:typed_equal(x[k],y[k],where+'.'+k)
    elif isinstance(x,list):
        require(len(x)==len(y),'length '+where)
        for k,(a,b) in enumerate(zip(x,y)):typed_equal(a,b,where+'.'+str(k))
    else:require(x==y,'value '+where)

def floor_root(x,den):
    require(x>=0,'nonnegative lower square operand')
    n=isqrt(x.numerator*den*den//x.denominator);r=Q(n,den)
    require(r*r<=x<(r+Q(1,den))**2,'complete rational lower root')
    return r

def polar_cell(k,damage):
    L=Q(k,8);U=Q(k+1,8);P=max(Q(0),(ENERGY-U)/2)
    delta=floor_root(L/56,1024);d=ceiling(Q(7,8)*U,256)
    if damage=='radial-lower-cap' and k==12:delta+=Q(1,1024)
    require(delta**2<=L/56<(delta+Q(1,1024))**2,'radial lower square payment '+str(k))
    require(0<=delta<=Q(3,8) and C-BM*delta>0,'radial positivity '+str(k))
    MC=H+BX*(1+d);nu=BX*(1+d)/MC
    require(0<=nu<1,'geometric convergence')
    # Derivation 1: convolution of all radial and reciprocal-series factors.
    g=[Q(0)]
    for n in range(5):
        coefficient=(n+1)*nu**n/MC**2
        if damage=='drop-polar-series' and k==12 and n==4:coefficient=Q(0)
        g=add(g,scale(power([Q(1),-Q(1)],n),coefficient))
    K=scale([Q(0)]+g,AB*P)
    radial=mul([H,C+7*BM*delta],power([H,C-BM*delta],7))
    if damage=='radial-coefficient' and k==12:radial[-1]+=Q(1,1000)
    full=mul(radial,add(add([Q(1)],scale(K,-1)),scale(mul(K,K),Q(1,2))))
    if damage=='last-polar-coefficient' and k==62:full[-1]+=1
    # Derivation 2: binomial radial vector; all kernel terms/ordered pairs.
    factors=[]
    for i in range(9):
        value=Q(0)
        if i<=7:value+=comb(7,i)*H**(8-i)*(C-BM*delta)**i
        if i>=1:value+=(C+7*BM*delta)*comb(7,i-1)*H**(8-i)*(C-BM*delta)**(i-1)
        factors.append(value)
    require(radial==factors,'whole radial Hermite payment '+str(k))
    terms=[(1,n,AB*P*(n+1)*nu**n/MC**2) for n in range(5)]
    weighted=[(0,0,Q(1))]+[(r,n,-v) for r,n,v in terms]
    weighted += [(r+s,n+m,v*w/2) for r,n,v in terms for s,m,w in terms]
    other=[Q(0)]*19;beta_area=Q(0)
    for r,n,v in weighted:
        for i,f in enumerate(factors):
            for j in range(n+1):other[i+r+j]+=f*v*comb(n,j)*(-1)**j
            beta_area+=f*v*Q(factorial(i+r)*factorial(n),factorial(i+r+n+1))
    require(len(full)==19 and full==other,'whole polar coefficients cell '+str(k))
    area=integral(full)
    require(area==beta_area,'full coefficient/beta integration '+str(k))
    require(area<Q(9999,10000),'strict polar payment '+str(k))
    return dict(k=k,L=str(L),U=str(U),P=str(P),d=str(d),delta=str(delta),
                integral=str(area),all19_coefficients_sha256=digest(strings(full)),
                all_coefficients=strings(full))

def multinomial_quadratic(a,n):
    # Count how many linear and quadratic choices occur in the product.
    out=[Q(0)]*(2*n+1)
    for j in range(n+1):
        for k in range(n-j+1):
            i=n-j-k
            out[j+2*k]+=Q(factorial(n),factorial(i)*factorial(j)*factorial(k))*a[0]**i*a[1]**j*a[2]**k
    return out

def origin_leaf(path,box,constants,damage):
    al,ah,ul,uh,wl,wh=box
    sm=min(Q(1),uh**2+wh);SM=ENERGY-8*((1-uh)**2+wl)
    if damage=='uncouple-energy' and path=='00000000':SM=ENERGY
    require(SM==ENERGY-8*((1-uh)**2+wl),'exact centered energy identity '+path)
    require(SM>=0 and sm>=ul*ul,'nonempty-leaf conservative energy '+path)
    beta=[Q(1),-2*al*ul,al*al*sm];b1=sum(beta)
    require(ul>al*sm and 0<b1<1 and 1-al*ul>0,'whole beta/denominator signs '+path)
    ds=ceiling(sm,1024);db=ceiling(b1,1024);dS=ceiling(SM,1024)
    numerator=1-db*b1**4
    require(numerator>0 and ah*ds>0,'diagonal bound signs '+path)
    D=numerator/(ah*ds)
    root=[Q(1),-al*ul,al**2*(sm-ul**2)/(2*(1-al*ul))]
    if damage=='origin-odd-root' and path=='00000000':root[-1]*=2
    alternate_root=[Q(1),-al*ul,(beta[2]-beta[1]**2/4)/(2+beta[1])]
    require(root==alternate_root,'complete odd root expression '+path)
    rows=[];R=Q(0)
    for l in range(2,9):
        pol=power(beta,(8-l)//2)
        if l%2:pol=mul(pol,root)
        factor=9*ah**l*constants[l]*SM**(l//2)*(dS if l%2 else 1)
        pol=[Q(0)]*l+scale(pol,factor)
        alternate=multinomial_quadratic(beta,(8-l)//2)
        if l%2:
            # Full three-shift formula, no polynomial convolution.
            raw=[Q(0)]*(len(alternate)+2)
            for j,v in enumerate(alternate):
                raw[j]+=v;raw[j+1]+=v*(-al*ul);raw[j+2]+=v*alternate_root[2]
            alternate=raw
        alternate=[Q(0)]*l+[v*factor for v in alternate]
        require(pol==alternate,'whole origin coefficients '+path+' order '+str(l))
        area=integral(pol)
        # Separate exact integration from multinomial term choices, before
        # expanding in t or collecting coefficients.
        other=Q(0);n=(8-l)//2
        for j in range(n+1):
            for k in range(n-j+1):
                i=n-j-k
                v=Q(factorial(n),factorial(i)*factorial(j)*factorial(k))*beta[0]**i*beta[1]**j*beta[2]**k
                base=l+j+2*k+1
                payment=Q(1,base)
                if l%2:payment+=(-al*ul)/Q(base+1)+alternate_root[2]/Q(base+2)
                other+=factor*v*payment
        require(area==other,'full integrated origin order '+str(l)+' '+path)
        if damage=='origin-drop-eighth' and path=='00000000' and l==8:continue
        require(area>=0,'positive integrated remainder '+path)
        rows.append(dict(l=l,integral=str(area),coefficients_sha256=digest(strings(pol)),all_coefficients=strings(pol)))
        R+=area
    require([r['l'] for r in rows]==list(range(2,9)),'all seven orders retained '+path)
    require(D-R>TARGET,'strict origin leaf '+path)
    return dict(path=path,box=strings(box),smax=str(sm),Smax=str(SM),
                dmean=str(ds),dbeta=str(db),dS=str(dS),beta=strings(beta),
                odd_root=strings(root),D=str(D),R=str(R),score=str(D-R),terms=rows)

def compute(damage):
    require(TM==56*Q(3,8)**2 and BM==1-H*H and BX==1-LOW*LOW,'analytic endpoint budgets')
    require(AB==min(LOW*(1-LOW**2),H*(1-H**2)) and LOW>0,'concave ab endpoint minimum')
    require(GAMMA==MASS/8-ENERGY/16 and GAMMA>H,'uniform mean monotonicity budgets')
    require(Q(479,512)**2>=Q(7,8) and Q(478,512)**2<Q(7,8),'centered coordinate root upper cap')
    # Full affine identity in the independent a,x variables.
    left={(0,0):H,(1,0):-Q(1),(0,1):C-1,(2,1):Q(1)}
    right={(0,0):H,(1,0):-Q(1),(0,1):Q(1,4)-H,(2,1):Q(1)}
    require(left==right,'safe affine identity in two independent variables')
    mass=power([H,C*MASS/8],8)
    independent=[comb(8,i)*H**(8-i)*(C*MASS/8)**i for i in range(9)]
    require(mass==independent,'all nine mass coefficients')
    mass_area=integral(mass)
    require(mass_area==Q(250634863328462439487299369,256000000000000000000000000) and mass_area<1,'mass floor')
    polar=[polar_cell(k,damage) for k in range(63)]
    require(Q(polar[0]['L'])==0 and Q(polar[-1]['U'])==TM,'closed polar endpoints')
    require(all(Q(x['U'])==Q(y['L']) for x,y in zip(polar,polar[1:])),'complete polar cover')
    rho=ceiling(Q(7,8),1024);tau=ceiling(Q(1,8),1024)
    require(rho==Q(479,512) and tau==Q(363,1024),'two complete centered root caps')
    c=[Q(1),Q(0)];constant_rows=[]
    for l in range(2,9):
        # Coordinate/power-sum bound fed into the complete Newton recurrence.
        factors={k:Q(7,8)**((k-2)//2)*(rho if k%2 else 1) for k in range(2,l+1)}
        newton=sum((c[l-k]*factors[k] for k in range(2,l+1)),Q(0))/l
        cs=Q(comb(8,l),8**(l//2))*(tau if l%2 else 1)
        chosen=min(newton,cs)
        if damage=='centered-third' and l==3:chosen+=Q(1,1000)
        if damage=='newton-eighth' and l==8:chosen+=Q(1,1000)
        c.append(chosen)
        constant_rows.append(dict(l=l,power_caps={str(k):str(v) for k,v in factors.items()},
                                  newton=str(newton),cauchy_maclaurin=str(cs),chosen=str(chosen)))
    require(c==[Q(1),Q(0),Q(1,2),Q(479,1536),Q(11,32),Q(2541,8192),Q(7,128),Q(363,65536),Q(1,4096)],'all finite-cardinality centered constants')
    cover=json.loads((HERE/'COVER.json').read_text())
    require(set(cover)=={'root','splits','leaves'},'complete cover schema')
    typed_equal(cover['root'],strings(ROOT),'root')
    splits=cover['splits'];leaves=cover['leaves'][:]
    if damage=='omit-leaf':leaves.pop()
    require(isinstance(splits,dict) and isinstance(leaves,list),'cover types')
    require(all(type(k) is str and type(v) is int and 0<=v<=2 for k,v in splits.items()),'split axis types')
    require(all(type(x) is str for x in leaves) and len(set(leaves))==len(leaves),'leaf path types')
    require(not(set(splits)&set(leaves)),'internal/leaf disjointness')
    visited=set();rows=[]
    def walk(path,box):
        require(path not in visited and len(path)<=18,'finite path census')
        visited.add(path)
        require(all(ROOT[2*j]<=box[2*j]<box[2*j+1]<=ROOT[2*j+1] for j in range(3)),'whole closed box containment')
        if path in splits:
            axis=splits[path];mid=(box[2*axis]+box[2*axis+1])/2
            lo=list(box);hi=list(box);lo[2*axis+1]=mid;hi[2*axis]=mid
            require(lo[2*axis+1]==hi[2*axis] and lo[2*axis]==box[2*axis] and hi[2*axis+1]==box[2*axis+1],'no split boundary omitted')
            walk(path+'0',tuple(lo));walk(path+'1',tuple(hi))
        else:
            require(path in leaves,'missing cover leaf '+path)
            rows.append(origin_leaf(path,box,c,damage))
    walk('',ROOT)
    require(visited==set(splits)|set(leaves),'no unreachable cover entry')
    require(len(splits)==271 and len(leaves)==272 and len(visited)==543,'complete fixed origin census')
    whole=dict(mass_coefficients=strings(mass),mass_integral=str(mass_area),
               centered_constants=strings(c),constant_derivations=constant_rows,polar_cells=polar,origin_leaves=rows,
               cover=cover,trust='ordinary analytic bridges; same-author exact cross-method coefficients')
    worst=dict(max(polar,key=lambda r:Q(r['integral'])));worst.pop('all_coefficients')
    least=dict(min(rows,key=lambda r:Q(r['score'])));least['terms']=[{k:v for k,v in term.items() if k!='all_coefficients'} for term in least['terms']]
    expected=dict(agent='six-sendov-1',role='researcher',result='PASS',
                  full_checked_record_sha256=digest(whole),polar_cells=63,origin_leaves=272,
                  internal_splits=271,polar_strict_target='9999/10000',origin_strict_target='257/256',
                  mass_integral=str(mass_area),worst_polar=worst,least_origin=least,
                  all_coefficients_checked=True,all_closed_cells_checked=True,
                  independent_review=False,formalized=False)
    return expected,whole

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--damage',default='',choices=['','last-polar-coefficient','drop-polar-series','newton-eighth','origin-drop-eighth','origin-odd-root','uncouple-energy','omit-leaf','radial-lower-cap','radial-coefficient','centered-third'])
    parser.add_argument('--record',type=Path,help='Optional verbose PRIVATE regenerated record; never an imported premise')
    args=parser.parse_args()
    if not args.emit:
        manifest=json.loads((HERE/'MANIFEST.json').read_text())
        actual={name:dict(bytes=len((HERE/name).read_bytes()),sha256=sha256((HERE/name).read_bytes()).hexdigest()) for name in PINS}
        typed_equal(actual,manifest['files'],'manifest')
    expected,whole=compute(args.damage)
    if args.emit:
        require(not args.damage and args.expected==HERE/'EXPECTED.json','explicit author emit only')
        args.expected.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:typed_equal(expected,json.loads(args.expected.read_text()))
    if args.record:
        require(HERE not in args.record.resolve().parents,'verbose record must remain outside publication directory')
        args.record.write_text(json.dumps(whole,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(result='PASS',record_sha256=expected['full_checked_record_sha256'],
                         polar_cells=63,origin_leaves=272,whole_coefficients_cross_checked=True)))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,ZeroDivisionError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
