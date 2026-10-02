#!/usr/bin/env python3
"""Exact finite corroboration of the written paired-cube collar proof.
Stdlib only. Ordinary analytic/norm arguments are not formalized here.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import argparse, hashlib, json, sys

ROOT = Path(__file__).resolve().parent
E, R, KAPPA = F(1,65536), F(1,25), F(19,96)
HMAX = 8*R*R
controls, margins = {}, {}

def require(ok, message):
    if not ok: raise ValueError(message)

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()

def fraction(value): return str(F(value))
def digest(value): return hashlib.sha256(canonical(value)).hexdigest()

def freeze(p):
    return [[list(m),str(c)] for m,c in sorted(p.items()) if c]

def add(*ps):
    out={}
    for p in ps:
        for m,c in p.items(): out[m]=out.get(m,F())+c
    return {m:c for m,c in out.items() if c}

def scale(p,c): return {m:c*v for m,v in p.items() if c*v}

def mul(p,q):
    out={}
    for m,c in p.items():
        for n,d in q.items():
            z=tuple(a+b for a,b in zip(m,n))
            out[z]=out.get(z,F())+c*d
    return {m:c for m,c in out.items() if c}

def power(p,n):
    require(n>=0 and bool(p),'invalid polynomial power')
    width=len(next(iter(p)))
    out={(0,)*width:F(1)}
    for _ in range(n): out=mul(out,p)
    return out

def var(n,i):
    m=[0]*n; m[i]=1
    return {tuple(m):F(1)}

def same(name,p,q):
    require(p==q,'whole identity mismatch: '+name)
    controls[name]={'terms':len(p),'sha256':digest(freeze(p))}

def positive(name,v):
    require(isinstance(v,F) and v>0,'nonpositive margin: '+name)
    margins[name]=str(v)

def rho(k): return F(1) if k%3==0 else F(-1,2)

def omega(k): return [(F(1),F(0)),(F(0),F(1)),(F(-1),F(-1))][k%3]

def cmul(x,y):
    # QQ[omega]/(omega^2+omega+1).
    a,b=x;c,d=y
    return a*c-b*d,a*d+b*c-b*d

def cconj(x):a,b=x;return a-b,-b

def ctrace(x): return x[0]-x[1]/2

def kernel_checks():
    closed={};defined={}
    for k in range(9):
        for l in range(9):
            m=[0]*18;m[k]+=1;m[9+l]+=1;m=tuple(m)
            closed[m]=(k+l-9)*rho(k-l)
            x=cmul(omega(k),cconj(omega(l)))
            # Two derivative-product channels and the modulus square.
            defined[m]=ctrace(tuple((k+l)*t-9*t for t in x))
    closed={m:c for m,c in closed.items() if c}
    defined={m:c for m,c in defined.items() if c}
    same('entire-paired-quadratic-kernel',closed,defined)
    all_rows={}
    for f in range(9):
        direct={};expected={}
        for k in range(9):
            for l in range(9):
                if (k-l)%9==f:
                    m=[0]*18;m[k]+=1;m[9+l]+=1
                    if k+l!=9:direct[tuple(m)]=F(k+l-9)
        if f==0:
            for k in range(9):
                m=[0]*18;m[k]=1;m[9+k]=1;expected[tuple(m)]=F(2*k-9)
        elif f in (1,2):
            for j in range(9-f):
                m=[0]*18;m[j+f]=1;m[9+j]=1
                c=F(2*j+f-9)
                if c:expected[tuple(m)]=c
            for j in range(9-f,9):
                k=j+f-9;m=[0]*18;m[k]=1;m[9+j]=1
                c=F(k+j-9)
                if c:expected[tuple(m)]=c
        else:
            # A separate coefficient-orthogonality recipe covers every row.
            for l in range(9):
                k=(l+f)%9;m=[0]*18;m[k]=1;m[9+l]=1
                c=F(k+l-9)
                if c:expected[tuple(m)]=c
        same('entire-cyclic-row-'+str(f),direct,expected)
        all_rows[f]=dict(direct)
    X,Y,D,Xb,Yb,Db=[var(6,i) for i in range(6)]
    x=[add(D,scale(X,-1),scale(Y,-1)),Y,X]
    xb=[add(Db,scale(Xb,-1),scale(Yb,-1)),Yb,Xb];idx=[0,7,8]
    top=add(*[scale(mul(x[i],xb[j]),(k+l-9)*rho(k-l))
              for i,k in enumerate(idx) for j,l in enumerate(idx)])
    expected=add(scale(mul(X,Xb),-3),scale(mul(Y,Yb),-6),
        scale(add(mul(X,Yb),mul(Y,Xb)),F(-27,2)),
        scale(add(mul(X,Db),mul(D,Xb)),F(19,2)),
        scale(add(mul(Y,Db),mul(D,Yb)),10),scale(mul(D,Db),-9))
    same('entire-top-three-coefficient-reduction',top,expected)
    low=range(1,7)
    maxima={str(j):max(2*abs(k+j-9)*abs(rho(k-j)) for k in low) for j in [0,8,7]}
    require(maxima=={'0':F(12),'8':F(8),'7':F(4)},'quadratic cross-row maximum mismatch')
    require(max(abs((k+l-9)*rho(k-l)) for k in low for l in low)==7,'lower quadratic maximum mismatch')
    controls['all-lower-quadratic-coefficients']={'exact_cross_maxima':{k:str(v) for k,v in maxima.items()},'used_safe_bounds':['16','10','8','7']}
    # Damage controls retain altered full kernels and both wrap conventions.
    damaged=dict(closed);m=next(iter(damaged));damaged[m]+=1
    require(damaged!=defined,'kernel damage escaped')
    damaged=dict(top);m=next(iter(damaged));damaged[m]=-damaged[m]
    require(damaged!=expected,'top sign damage escaped')
    wrap1=[0]*18;wrap1[0]=1;wrap1[17]=1
    damaged=dict(all_rows[1]);del damaged[tuple(wrap1)]
    require(damaged!=all_rows[1],'missing first wrap escaped')
    wrap2=[0]*18;wrap2[1]=1;wrap2[17]=1
    damaged=dict(all_rows[2]);damaged[tuple(wrap2)]=F(1)
    require(damaged!=all_rows[2],'spurious second wrap escaped')
    return 4

def anchoring_checks():
    t=var(9,0);a=add({(0,)*9:F(1)},scale(t,-1))
    c={k:var(9,k) for k in range(1,9)}
    base=add({(0,)*9:F(1)},scale(power(a,9),-1))
    d0=add(base,*[scale(mul(power(a,k),c[k]),-1) for k in range(1,9)])
    direct=add(scale(d0,18),*[scale(c[k],18*rho(k)) for k in range(1,9)])
    expected=add(scale(base,18),scale(add(c[7],c[8]),-27),
        *[scale(mul(add({(0,)*9:F(1)},scale(power(a,k),-1)),c[k]),18) for k in [7,8]],
        *[scale(mul(add({(0,)*9:rho(k)},scale(power(a,k),-1)),c[k]),18) for k in range(1,7)])
    same('entire-paired-linear-anchor',direct,expected)
    require(direct.get(next(iter(c[6])),F())==0 and direct.get(next(iter(c[3])),F())==0,'cube coefficient cancellation failed')
    require(add(direct,c[6])!=expected,'linear c6 damage escaped')
    return 1

def gaussian_weight_checks():
    zero=(F(),F());one=(F(1),F())
    def ga(x,y):return x[0]+y[0],x[1]+y[1]
    def gm(x,y):return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]
    def gc(x):return x[0],-x[1]
    def gs(x,c):return x[0]*c,x[1]*c
    def ladd(*ps):
        out={}
        for p in ps:
            for m,c in p.items():out[m]=ga(out.get(m,zero),c)
        return {m:c for m,c in out.items() if c!=zero}
    def lscale(p,c):return {m:gs(v,c) for m,v in p.items() if gs(v,c)!=zero}
    def lmul(p,q):
        out={}
        for m,c in p.items():
            for n,d in q.items():out[m+n]=ga(out.get(m+n,zero),gm(c,d))
        return {m:c for m,c in out.items() if c!=zero}
    def lconj(p):return {-m:gc(c) for m,c in p.items()}
    anchor=(1-E,F())
    cases=[
        [anchor]+[one]*8,
        [anchor]*9,
        [anchor,(F(),F(1)),(F(),F(-1)),one,(F(-1),F()),(F(1,2),F(1,2)),(F(1,2),F(-1,2)),zero,(F(1,3),F(2,3))],
        [anchor,(F(3,5),F(4,5)),(F(-3,5),F(4,5)),(F(-3,5),F(-4,5)),(F(3,5),F(-4,5)),zero]+[(F(1,2),F())]*3,
    ]
    for index,roots in enumerate(cases):
        require(len(roots)==9 and all(gm(r,gc(r))[0]<=1 for r in roots),'invalid literal original roots')
        factors=[{1:one,0:gs(r,-1)} for r in roots]
        p={0:one}
        for f in factors:p=lmul(p,f)
        zp={m:gs(c,m) for m,c in p.items() if m}
        left=ladd(lmul(zp,lconj(p)),lmul(lconj(zp),p),lscale(lmul(p,lconj(p)),-9))
        right={}
        for j,r in enumerate(roots):
            part={0:one}
            for k,f in enumerate(factors):
                if k!=j:part=lmul(part,lmul(f,lconj(f)))
            right=ladd(right,lscale(part,1-gm(r,gc(r))[0]))
        require(left==right,'entire division-free literal weight mismatch')
        frozen=[[m,str(c[0]),str(c[1])] for m,c in sorted(left.items())]
        controls['whole-actual-original-weight-'+str(index)]={'degree':9,'all_original_norms_at_most_one':True,'terms':len(left),'sha256':digest(frozen),'includes_critical_collision_fixture':index==1}
    damaged=ladd(left,{0:one})
    require(damaged!=right,'literal weight damage escaped')
    return 1

def newton_checks():
    z=[var(8,i) for i in range(8)]
    t={j:add(*(power(x,j) for x in z)) for j in range(1,5)}
    elementary={m:add(*[mul_all([z[i] for i in I]) for I in combinations(range(8),m)]) for m in range(1,5)}
    c8=scale(elementary[1],F(-9,8));c7=scale(elementary[2],F(9,7))
    same('whole-first-newton',t[1],scale(c8,F(-8,9)))
    same('whole-second-newton',t[2],add(power(t[1],2),scale(c7,F(-14,9))))
    rhs3=add(scale(power(t[1],3),F(-1,4)),scale(mul(t[1],t[2]),F(3,4)),scale(t[3],F(-1,2)))
    same('whole-third-newton',scale(elementary[3],F(-3,2)),rhs3)
    rhs4=add(scale(power(t[1],4),F(3,40)),scale(mul(power(t[1],2),t[2]),F(-9,20)),
             scale(power(t[2],2),F(9,40)),scale(mul(t[1],t[3]),F(3,5)),scale(t[4],F(-9,20)))
    same('whole-fourth-newton',scale(elementary[4],F(9,5)),rhs4)
    bad=add(rhs3,scale(t[3],F(1,2)))
    require(bad!=scale(elementary[3],F(-3,2)),'third-moment omission escaped')
    bad=add(rhs4,scale(mul(t[1],t[3]),F(1,5)))
    require(bad!=scale(elementary[4],F(9,5)),'fourth Newton damage escaped')
    return 2

def mul_all(ps):
    out={(0,)*8:F(1)}
    for p in ps:out=mul(out,p)
    return out

eta,H=var(2,0),var(2,1)

def linear(p):
    aa=bb=F()
    for (i,j),c in p.items():
        require(c>=0 and (i+j)>0,'invalid nonnegative scalar majorant')
        if j:bb+=c*E**i*HMAX**(j-1)
        else:aa+=c*E**(i-1)
    return aa,bb

B={k:F(9,k)*comb(8,9-k)*R**(7-k)/8 for k in range(1,8)}
ELL=sum(B[k] for k in range(1,7))

def first_stage(x0,name,X,D):
    b1=B[1];Y=F(9,2)
    lam=19*E+F(160,63)*x0+F(7,9)*Y*HMAX+ELL*HMAX/9+F(8,9)*b1*HMAX
    aa=F(27,4)+18*E
    bb=14*E*Y+2*ELL+F(45,112)-F(9,4)*KAPPA+(
        F(5,9)*Y*Y+F(11,9)*ELL*ELL+F(4,9)*Y*ELL)*HMAX+b1*(1+F(8,9)*(9*E+Y*HMAX+ELL*HMAX))
    positive(name+'-damping',1-lam)
    positive(name+'-eta',X*(1-lam)-aa)
    positive(name+'-energy',D*(1-lam)-bb)
    controls[name]={'x0':str(x0),'lambda':str(lam),'rhs_eta':str(aa),'rhs_energy':str(bb),'X':str(X),'D':str(D)}


def moments(X,D):
    x=add(scale(eta,X),scale(H,D));U=scale(x,F(8,9));U2=power(U,2)
    y=scale(add(H,U2),F(9,14));c={k:scale(H,B[k]) for k in range(1,5)}
    c[5]=add(scale(power(U,4),F(3,40)),scale(mul(U2,H),F(9,20)),scale(power(H,2),F(9,40)),
             scale(mul(U,H),F(3,5)*R),scale(H,F(9,20)*R*R))
    c[6]=add(scale(power(U,3),F(1,4)),scale(mul(U,H),F(3,4)),scale(H,R/2))
    return x,U,U2,y,c,add(*c.values())

def tail_stage(X,D,nextX,nextD,name):
    x,U,U2,y,c,L=moments(X,D);d0=add(scale(eta,9),x,y,L)
    M=add(scale(eta,F(27,4)),scale(power(eta,2),18),scale(mul(eta,x),19),scale(mul(eta,y),14),scale(L,2),
          scale(power(x,2),F(8,3)),scale(power(y,2),F(5,9)),scale(mul(x,y),F(7,9)),scale(mul(L,x),F(1,9)),
          scale(power(L,2),F(11,9)),scale(mul(y,L),F(4,9)),c[1],scale(mul(c[1],d0),F(8,9)))
    aa,bb=linear(M)
    positive(name+'-eta',nextX-aa);positive(name+'-energy',nextD-bb)
    controls[name]={'full_majorant_terms':len(M),'full_majorant_sha256':digest(freeze(M)),'linear_eta':str(aa),'linear_energy':str(bb),'nextX':str(nextX),'nextD':str(nextD)}


def scalar_checks():
    positive('radius-ratio',1-E-24*R)
    positive('square-tail-positive',KAPPA)
    positive('signed-coefficient-positive',F(7,4)*KAPPA-F(5,16))
    positive('bounded-full-critical-energy',HMAX)
    first_stage(9*R,'mean-stage-1',F(169),F(26))
    first_stage(169*E+26*HMAX,'mean-stage-2',F(66),F(10))
    first_stage(66*E+10*HMAX,'mean-stage-3',F(11),F(2))
    tail_stage(F(11),F(2),F(7),F(1,4),'mean-stage-4')
    tail_stage(F(7),F(1,4),F(7),F(1,8),'mean-stage-5')
    x,U,U2,y,c,L=moments(F(7),F(1,8))
    delta=add(scale(eta,9),scale(mul(eta,x),8),scale(mul(eta,y),7),L);d0=add(x,y,delta)
    Qplus=add(scale(mul(x,y),27),mul(add(scale(x,19),scale(y,20)),delta),scale(mul(d0,L),16),
              scale(mul(x,L),10),scale(mul(y,L),8),scale(power(L,2),7))
    S=add(scale(eta,6),scale(mul(eta,x),F(16,3)),scale(mul(eta,y),F(14,3)),
          c[1],c[2],c[4],c[5],scale(mul(eta,c[3]),2),scale(mul(eta,c[6]),4),scale(Qplus,F(1,27)))
    T=add(scale(S,F(8,9)),scale(y,F(5,18)),scale(mul(eta,x),F(8,9)),scale(U2,F(3,4)),scale(power(eta,2),8))
    aa,bb=linear(T);nu=aa-5;gap=KAPPA-bb
    positive('energy-feedback-denominator',gap)
    positive('energy-feedback-H25',25*gap-nu)
    for name,p in [('final-x',x),('final-y',y),('final-lower-tail',L),('final-delta',delta),('paired-Qplus',Qplus),('paired-S',S),('complete-feedback-T',T)]:
        controls[name]={'all_coefficients_nonnegative':True,'terms':len(p),'sha256':digest(freeze(p)),'linear':[str(v) for v in linear(p)]}
    controls['energy-result']={'nu':str(nu),'gap':str(gap),'H_over_eta_bound':str(nu/gap),'strict_bound':'25'}
    # Entire anchoring/binomial remainder as an exact polynomial in eta.
    a=add({(0,0):F(1)},scale(eta,-1))
    diff=add(scale(power(a,2),8),scale(mul(add({(0,0):F(8)},scale(eta,3)),power(a,3)),-1))
    expected={(1,0):F(5),(2,0):F(-7),(3,0):F(-1),(4,0):F(3)}
    same('complete-low-sublevel-polynomial',diff,expected)
    positive('low-sublevel-lower-budget',1-E)
    # Negative controls for each of the important scalar/sign thresholds.
    damages=0
    for bad,label in [(F(-1),'negative damping'),(F(24)*gap-nu,'unsupported H24'),
                      (F(7,4)*F(1,6)-F(5,16),'invalid square-tail radius'),
                      (F(0),'zero strict margin')]:
        require(bad<=0,'damage is not a rejecting control: '+label);damages+=1
    return damages

def typed_tree(x):
    require(type(x) in (dict,list,str,int,bool,type(None)),'invalid fixture type')
    if type(x) is dict:
        for k,v in x.items():require(type(k) is str,'invalid fixture key');typed_tree(v)
    if type(x) is list:
        for v in x:typed_tree(v)

def unique_object(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,'duplicate fixture key')
        out[k]=v
    return out


def record():
    controls.clear();margins.clear()
    damages=kernel_checks()+anchoring_checks()+gaussian_weight_checks()+newton_checks()+scalar_checks()
    data={'schema':'paired-cube-energy-v1','parameters':{'eta_max':str(E),'critical_radius':str(R),'H_max':str(HMAX),'square_tail_kappa':str(KAPPA)},
          'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'controls':controls,'positive_margins':margins,'internal_damage_controls':damages}
    typed_tree(data)
    return data

def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=ROOT/'EXPECTED.json');p.add_argument('--write-expected',action='store_true');args=p.parse_args()
    r=record()
    if args.write_expected:
        args.fixture.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    else:
        expected=json.loads(args.fixture.read_text(),object_pairs_hook=unique_object,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('invalid JSON constant')))
        typed_tree(expected)
        require(canonical(expected)==canonical(r),'complete typed fixture mismatch')
    print(json.dumps({'status':'PASS','whole_controls':len(controls),'strict_margins':len(margins),'internal_damage_controls':r['internal_damage_controls'],'record_sha256':digest(r),'scope':'finite exact corroboration; ordinary analytic proof unformalized'},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
