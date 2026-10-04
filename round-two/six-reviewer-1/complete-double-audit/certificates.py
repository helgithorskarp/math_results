"""Fresh rational clearing and complete reversible Bernstein certificates.

Written rectangles were exposed. No producer programs or tensors are inputs.
The sparse ring and original spectral model are this reviewer's published core.
"""
from fractions import Fraction as Q
from math import comb
from ring import constant,add,scale,mul,power,shift,degree,exact_divide_axis

def positive_q0(P,side):
    I=degree(P)[0]; kappa=9 if side==1 else 16
    # J=j/K. All common denominators are retained in the returned scale.
    K=240 if side==1 else 420
    j={(0,0,0):35,(1,0,0):-180,(2,0,0):-800} if side==1 else {(0,0,0):59,(1,0,0):-612,(2,0,0):-560}
    a={(0,0,0):1,(1,0,0):8*side}
    av=scale(a,Q(1,8));bv=add(constant(Q(1,4)),scale(av,-1));h2={(2,0,0):1}
    derived=mul(bv,add(scale(av,Q(19,3)),scale(bv,3))) if side==1 else add(scale(mul(av,add(add(av,scale(bv,Q(1,3))),constant(Q(4,35)))),4),scale(h2,-4))
    if scale(j,Q(1,K))!=derived:raise ValueError('whole rational J polynomial identity')
    dn=add(scale(shift(j,(2,0,0)),8),{(4,1,0):-4*K})
    un=scale(shift(add(j,{(2,1,0):4*K}),(4,0,1)),-1)
    ap=[power(a,n)for n in range(I+9)];jp=[power(j,n)for n in range(9)]
    dp=[power(dn,n)for n in range(degree(P)[1]+1)];up=[power(un,n)for n in range(6)]
    cleared={}
    for (i,d,u),c in P.items():
        if d+u>8:raise ValueError('joint degree clearing denominator')
        term=mul(mul(ap[i+8-u],jp[8-d-u]),mul(dp[d],up[u]))
        cleared=add(cleared,scale(term,c*kappa**(8-u)*8**(I-i+u)))
    if any(e[0]<10 for e in cleared):raise ValueError('whole h10 factor')
    S={(i-10,r,v):c for (i,r,v),c in cleared.items()}
    if shift(S,(10,0,0))!=cleared or degree(S)!=(31,8,5) or len(S)!=965:
        raise ValueError('whole positive-q0 reduced identity and census')
    return S,64**12*8**(I+8)*K**8

def real_q0(P,kappa):
    I=degree(P)[0];cleared={}
    for (i,j,k),c in P.items():
        n=i+5-k
        if n<0:raise ValueError('A clearing exponent')
        for a in range(n+1):
            for b in range(3*k+1):
                e=(2*j+4*k+a,10-2*k+a+2*b,k)
                v=c*kappa**(5-k)*8**(I-i+k)*24**j*(-216)**k*comb(n,a)*8**a*comb(3*k,b)*(-1)**(3*k-b)
                cleared[e]=cleared.get(e,0)+v
    cleared={e:c for e,c in cleared.items()if c}
    if any(e[0]<10 for e in cleared):raise ValueError('whole q10 factor')
    S={(i-10,j,k):c for (i,j,k),c in cleared.items()}
    S=exact_divide_axis(S,{0:1,2:-2,4:1},1)
    if shift(mul(S,{(0,0,0):1,(0,2,0):-2,(0,4,0):1}),(10,0,0))!=cleared or degree(S)!=(12,28,5):
        raise ValueError('whole real-q0 reverse factor identity')
    return S,64**12*8**(I+5)

def affine(poly,bounds):
    out={}
    for e,c in poly.items():
        terms={ (0,0,0):Q(c) }
        for axis,(lo,hi) in enumerate(bounds):
            one={tuple(n if j==axis else 0 for j in range(3)):comb(e[axis],n)*lo**(e[axis]-n)*(hi-lo)**n for n in range(e[axis]+1)}
            terms=mul(terms,{f:v for f,v in one.items()if v})
        out=add(out,terms)
    return out

def bernstein(poly,deg):
    if any(any(e[i]>deg[i]for i in range(3))for e in poly):raise ValueError('degree overflow')
    work={e:Q(c)for e,c in poly.items()}
    for axis,n in enumerate(deg):
        out={}
        for e,c in work.items():
            for k in range(e[axis],n+1):
                f=list(e);f[axis]=k;f=tuple(f)
                out[f]=out.get(f,Q(0))+c*Q(comb(k,e[axis]),comb(n,e[axis]))
        work={e:c for e,c in out.items()if c}
    controls=work
    if len(controls)!=(deg[0]+1)*(deg[1]+1)*(deg[2]+1)or min(controls.values())<=0:
        raise ValueError('complete strict coefficient positivity')
    for axis,n in enumerate(deg):
        out={}
        for e,c in work.items():
            for k in range(e[axis],n+1):
                f=list(e);f[axis]=k;f=tuple(f)
                out[f]=out.get(f,Q(0))+c*comb(n,k)*comb(k,e[axis])*(-1)**(k-e[axis])
        work={e:c for e,c in out.items()if c}
    if work!=poly:raise ValueError('entire inverse Bernstein identity')
    return controls

QUARTIC_BOXES=[(Q(0),Q(1,10),Q(1,4),Q(3,8)),(Q(0),Q(1,20),Q(3,8),Q(7,16)),
 (Q(0),Q(1,20),Q(7,16),Q(1,2)),(Q(1,20),Q(1,10),Q(3,8),Q(1,2)),
 (Q(1,10),Q(1,5),Q(1,4),Q(3,8)),(Q(1,10),Q(3,20),Q(3,8),Q(1,2)),
 (Q(3,20),Q(7,40),Q(3,8),Q(7,16)),(Q(7,40),Q(1,5),Q(3,8),Q(13,32)),
 (Q(7,40),Q(1,5),Q(13,32),Q(7,16)),(Q(3,20),Q(1,5),Q(7,16),Q(1,2))]

def quartic():
    # T4(-y) after D is replaced by its permitted upper endpoint 5/141.
    R={(0,4,0):Q(3),(1,3,0):Q(-2),(2,2,0):Q(4),(0,2,0):Q(-1),
       (1,1,0):Q(1,2),(3,1,0):Q(-2),(4,0,0):Q(3),(2,0,0):Q(-1),(0,0,0):Q(3,32)-Q(5,564)}
    xs=sorted({v for box in QUARTIC_BOXES for v in box[:2]});ys=sorted({v for box in QUARTIC_BOXES for v in box[2:]})
    if xs[0]!=0 or xs[-1]!=Q(1,5)or ys[0]!=Q(1,4)or ys[-1]!=Q(1,2):raise ValueError('quartic enclosing rectangle')
    for l,r in zip(xs,xs[1:]):
        for b,t in zip(ys,ys[1:]):
            if sum(al<=l and r<=ar and bl<=b and t<=br for al,ar,bl,br in QUARTIC_BOXES)!=1:
                raise ValueError('quartic complete tiling coverage')
    records=[]
    for al,ar,bl,br in QUARTIC_BOXES:
        p=affine(R,[(al,ar),(bl,br),(Q(0),Q(1))]);controls=bernstein(p,(4,4,0))
        records.append((p,controls))
    return R,records
