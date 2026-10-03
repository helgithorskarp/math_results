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
H=Q(11,20); C=Q(7,10); BM=Q(279,400); TM=Q(6776,961)
GAMMA=Q(61,80); TARGET=Q(257,256)
ROOT=(Q(1,2),H,GAMMA,Q(1),Q(0),Q(3,8))
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

def polar_cell(k,damage):
    L=Q(k,8);U=min(Q(k+1,8),TM);P=max(Q(0),(3-U)/2)
    d=ceiling(Q(7,8)*U,256);MB=Q(5,4);MC=H+Q(3,4)*(1+d)
    alpha=C/MB;nu=Q(3,4)*(1+d)/MC
    require(0<=alpha<1 and 0<=nu<1,'geometric convergence')
    # Derivation 1: product of the two truncated reciprocal power series.
    g1=[Q(0)];g2=[Q(0)]
    for n in range(5):
        z=power([Q(1),-Q(1)],n)
        coefficient=sum((alpha**j*nu**(n-j) for j in range(n+1)),Q(0))
        if damage=='drop-polar-series' and k==56 and n==4:coefficient=Q(0)
        g1=add(g1,scale(z,coefficient/(MB*MC)))
        g2=add(g2,scale(z,(n+1)*nu**n/MC**2))
    K=add(scale([Q(0),Q(0)]+g1,BM*BM*L/2),
          scale([Q(0)]+g2,Q(3,8)*P))
    full=mul(power([H,C],8),add(add([Q(1)],scale(K,-1)),scale(mul(K,K),Q(1,2))))
    if damage=='last-polar-coefficient' and k==56:full[-1]+=1
    # Derivation 2: expand all t^r(1-t)^n kernel terms and all ordered pairs.
    terms=[]
    for n in range(5):
        terms.append((2,n,BM**2*L/(2*MB*MC)*
                      sum((alpha**j*nu**(n-j) for j in range(n+1)),Q(0))))
        terms.append((1,n,Q(3,8)*P*(n+1)*nu**n/MC**2))
    factors=[comb(8,i)*H**(8-i)*C**i for i in range(9)]
    other=[Q(0)]*21
    beta_area=Q(0)
    weighted=[(0,0,Q(1))]+[(r,n,-v) for r,n,v in terms]
    weighted += [(r+s,n+m,v*w/2) for r,n,v in terms for s,m,w in terms]
    for r,n,v in weighted:
        for i,f in enumerate(factors):
            for j in range(n+1):other[i+r+j]+=f*v*comb(n,j)*(-1)**j
            beta_area+=f*v*Q(factorial(i+r)*factorial(n),factorial(i+r+n+1))
    require(len(full)==21 and full==other,'whole polar coefficients cell '+str(k))
    area=integral(full)
    require(area==beta_area,'full coefficient/beta integration '+str(k))
    require(area<Q(999,1000),'strict polar payment '+str(k))
    return dict(k=k,L=str(L),U=str(U),P=str(P),d=str(d),
                integral=str(area),all21_coefficients_sha256=digest(strings(full)))

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
    sm=min(Q(1),uh**2+wh);SM=3-8*((1-uh)**2+wl)
    if damage=='uncouple-energy' and path=='0000':SM=Q(3)
    require(SM==3-8*((1-uh)**2+wl),'exact centered energy identity '+path)
    require(SM>=0 and sm>=ul*ul,'nonempty-leaf conservative energy '+path)
    beta=[Q(1),-2*al*ul,al*al*sm];b1=sum(beta)
    require(ul>al*sm and 0<b1<1 and 1-al*ul>0,'whole beta/denominator signs '+path)
    ds=ceiling(sm,1024);db=ceiling(b1,1024);dS=ceiling(SM,1024)
    numerator=1-db*b1**4
    require(numerator>0 and ah*ds>0,'diagonal bound signs '+path)
    D=numerator/(ah*ds)
    root=[Q(1),-al*ul,al**2*(sm-ul**2)/(2*(1-al*ul))]
    if damage=='origin-odd-root' and path=='0000':root[-1]*=2
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
        if damage=='origin-drop-eighth' and path=='0000' and l==8:continue
        require(area>=0,'positive integrated remainder '+path)
        rows.append(dict(l=l,integral=str(area),coefficients_sha256=digest(strings(pol))))
        R+=area
    require([r['l'] for r in rows]==list(range(2,9)),'all seven orders retained '+path)
    require(D-R>TARGET,'strict origin leaf '+path)
    return dict(path=path,box=strings(box),smax=str(sm),Smax=str(SM),
                dmean=str(ds),dbeta=str(db),dS=str(dS),beta=strings(beta),
                odd_root=strings(root),D=str(D),R=str(R),score=str(D-R),terms=rows)

def compute(damage):
    require(TM==56*Q(11,31)**2 and BM==1-H*H,'analytic endpoint budgets')
    require(H**2<Q(1,3) and GAMMA>H,'uniform monotonicity budgets')
    # Full coefficient identities: h+cx-[a+(1-a^2)x].
    left={(0,0):H,(1,0):-Q(1),(0,1):C-1,(2,1):Q(1)}
    right={(0,0):H,(1,0):-Q(1),(0,1):Q(1,4)-H,(2,1):Q(1)}
    require(left==right,'safe affine identity in two independent variables')
    mass=power([H,Q(133,200)],8)
    independent=[comb(8,i)*H**(8-i)*Q(133,200)**i for i in range(9)]
    require(mass==independent,'all mass coefficients')
    mass_area=integral(mass)
    require(mass_area==Q(22195148562855892471,23040000000000000000) and mass_area<1,'mass floor')
    polar=[polar_cell(k,damage) for k in range(57)]
    require(Q(polar[0]['L'])==0 and Q(polar[-1]['U'])==TM,'closed polar endpoints')
    require(all(Q(x['U'])==Q(y['L']) for x,y in zip(polar,polar[1:])),'complete polar cover')
    c=[Q(1),Q(0)]
    for l in range(2,9):c.append(sum((c[l-k] for k in range(2,l+1)),Q(0))/l)
    if damage=='newton-eighth':c[8]+=Q(1,1000)
    require(c==[Q(1),Q(0),Q(1,2),Q(1,3),Q(3,8),Q(11,30),Q(53,144),Q(103,280),Q(2119,5760)],'all centered Newton constants')
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
    require(len(splits)==47 and len(leaves)==48 and len(visited)==95,'complete fixed origin census')
    whole=dict(mass_coefficients=strings(mass),mass_integral=str(mass_area),
               newton_constants=strings(c),polar_cells=polar,origin_leaves=rows,
               cover=cover,trust='ordinary analytic bridges; same-author exact cross-method coefficients')
    worst=max(polar,key=lambda r:Q(r['integral']));least=min(rows,key=lambda r:Q(r['score']))
    expected=dict(agent='six-sendov-1',role='researcher',result='PASS',
                  full_checked_record_sha256=digest(whole),polar_cells=57,origin_leaves=48,
                  internal_splits=47,polar_strict_target='999/1000',origin_strict_target='257/256',
                  mass_integral=str(mass_area),worst_polar=worst,least_origin=least,
                  all_coefficients_checked=True,all_closed_cells_checked=True,
                  independent_review=False,formalized=False)
    return expected,whole

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--damage',default='',choices=['','last-polar-coefficient','drop-polar-series','newton-eighth','origin-drop-eighth','origin-odd-root','uncouple-energy','omit-leaf'])
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
                         polar_cells=57,origin_leaves=48,whole_coefficients_cross_checked=True)))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,ZeroDivisionError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
