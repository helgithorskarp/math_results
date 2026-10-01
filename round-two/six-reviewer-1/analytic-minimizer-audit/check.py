#!/usr/bin/env python3
"""six-reviewer-1, independent exact analytic-minimizer audit.
Standard library only. Reuses this reviewer's published cyclotomic arithmetic
kernel (fourth-boundary-audit, commit7bf51b77755026292db72084d8338698e2f43925).
Fresh moment parity, nine-root, univariate polarization and spectrum checks;
never imports researcher proof source or prior review source at runtime.
Ordinary analytic arguments and trust boundaries are in REVIEW.md.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
from hashlib import sha256
import argparse,json

class Failure(RuntimeError):pass
CHECKS=0
def need(ok,label):
    global CHECKS
    if not ok:raise Failure(label)
    CHECKS+=1

class E:
    """Q[w]/(w^6+w^3+1), w=exp(2*pi*i/9), a single field for all roots."""
    __slots__=('a',)
    def __init__(self,x=0):
        if isinstance(x,E):self.a=x.a
        elif isinstance(x,(tuple,list)):
            if len(x)!=6:raise Failure('cyclotomic normal form')
            self.a=tuple(Q(v) for v in x)
        else:self.a=(Q(x),Q(0),Q(0),Q(0),Q(0),Q(0))
    def __bool__(self):return any(self.a)
    def __eq__(self,x):return self.a==E(x).a
    def __add__(self,x):return E(tuple(a+b for a,b in zip(self.a,E(x).a)))
    __radd__=__add__
    def __neg__(self):return E(tuple(-v for v in self.a))
    def __sub__(self,x):return self+-E(x)
    def __rsub__(self,x):return E(x)+-self
    def __mul__(self,x):
        x=E(x); out=[Q(0)]*11
        for i,a in enumerate(self.a):
            if a:
                for j,b in enumerate(x.a):
                    if b:out[i+j]+=a*b
        for j in range(10,5,-1):
            out[j-3]-=out[j];out[j-6]-=out[j]
        return E(out[:6])
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=E(1);a=self
        while n:
            if n&1:out=out*a
            a=a*a;n//=2
        return out
    def inv(self):
        if not any(self.a[1:]):return E(1/self.a[0])
        cols=[(self*E(tuple(int(i==j) for i in range(6)))).a for j in range(6)]
        rows=[[cols[j][i] for j in range(6)]+[Q(i==0)] for i in range(6)]
        for j in range(6):
            pivot=next((i for i in range(j,6) if rows[i][j]),None)
            if pivot is None:raise Failure('noninvertible cyclotomic element')
            rows[j],rows[pivot]=rows[pivot],rows[j]
            rows[j]=[v/rows[j][j] for v in rows[j]]
            for i in range(6):
                if i!=j:
                    a=rows[i][j];rows[i]=[v-a*b for v,b in zip(rows[i],rows[j])]
        return E(tuple(rows[i][6] for i in range(6)))
    def __truediv__(self,x):
        x=E(x)
        if not any(x.a[1:]):return E(tuple(v/x.a[0] for v in self.a))
        return self*x.inv()
    def __rtruediv__(self,x):return E(x)*self.inv()
    def conj(self):return sum((v*WP[(-j)%9] for j,v in enumerate(self.a)),E())
    def real(self):return (self+self.conj())/2
    def rec(self):
        # Invert the explicitly embedded real basis {1,c,c^2}.
        t=4*self.a[1];b=-2*self.a[4];a=self.a[0]-t/2
        if self != realfield((a,b,t)):raise Failure('real subfield decoding')
        return [str(a),str(b),str(t)]

W=E((0,1,0,0,0,0));WP=[W**j for j in range(9)]
c=-(WP[4]+WP[5])/2

def realfield(a):return E(a[0])+E(a[1])*c+E(a[2])*c*c

def isolated():
    lo,hi=Q(3,4),Q(1)
    for _ in range(110):
        mid=(lo+hi)/2
        if 8*mid**3-6*mid-1<0:lo=mid
        else:hi=mid
    need(8*lo**3-6*lo-1<0<8*hi**3-6*hi-1 and 24*lo**2-6>0,'isolated c')
    return lo,hi
LO,HI=isolated()
def interval(a):
    a=list(map(Q,E(a).rec()));out=[a[0],a[0]]
    for k in (1,2):
        v=(a[k]*LO**k,a[k]*HI**k);out[0]+=min(v);out[1]+=max(v)
    return out

def series(a=(),N=5):return [E(a[i]) if i<len(a) else E() for i in range(N+1)]
def add(a,b):return [x+y for x,y in zip(a,b)]
def neg(a):return [-v for v in a]
def scale(a,b):return [v*b for v in a]
def mul(a,b):
    out=series(N=len(a)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b[:len(a)-i]):
                if y:out[i+j]+=x*y
    return out
def power(a,n):
    out=series([1],len(a)-1)
    for _ in range(n):out=mul(out,a)
    return out
def shift(a,n):return [E()]*n+a[:len(a)-n]
def ipow(a,k):
    # Series in the formal Lagrange variable s, sharing the eta series kernel.
    return power(a,k)
def binomial(a,p):
    out=series(N=len(a)-1);q=Q(1);term=series([1],len(a)-1)
    for j in range(len(a)):
        if j:q=q*(p-j+1)/j;term=mul(term,a)
        out=add(out,scale(term,q))
    return out

H=14/(3*(1+c));b2=H/2;rho=(c-5)/3;L=-7*(2*c+1)/18
U=-8*(Q(2,3)-1/(3*(1+c)));uz=(U+rho*H)/8;up=uz-rho*H/2
d=2*c*c-1;v=2*d*d-1
w4=1/(c+d);w3=Q(2,3)*(7-(1-d)*w4)
sigma=E(Q(3,8))-(Q(3,2)*w3+(1-v)*w4)/20
K0=realfield((Q(-2609,405),Q(-2000,81),Q(12964,405)))
Bstar=realfield((Q(2311,108),Q(4934,27),Q(-1976,9)))
aT=realfield((Q(-11564,405),Q(-20482,81),Q(123284,405)))
bT=realfield((Q(49,180),Q(-105889,486),Q(305123,1215)))

# At odd epsilon degree the coefficient denotes i times the stored value.
# Multiplying two odd coefficients introduces -1. Moments/anchor are lifted
# directly; epsilon itself is not a generator in this parity representation.
NAMES=['eps','z','U','H','V','M','J3','J21','J4','W','D']
ZERO=(0,)*len(NAMES)
def pc(a=0):return {ZERO:E(a)} if E(a) else {}
def pv(name):
    k=list(ZERO);k[NAMES.index(name)]=1;return {tuple(k):E(1)}
def pa(*items):
    out={}
    for p in items:
        for k,a in p.items():out[k]=out.get(k,E())+a
    return {k:a for k,a in out.items() if a}
def ps(p,a):return {k:v*E(a) for k,v in p.items() if v*E(a)}
def pm(a,b):
    out={}
    for ka,va in a.items():
        for kb,vb in b.items():
            k=tuple(x+y for x,y in zip(ka,kb))
            if k[0]<=4:out[k]=out.get(k,E())+va*vb*(-1 if ka[0]%2 and kb[0]%2 else 1)
    return {k:a for k,a in out.items() if a}
def pp(a,n):
    out=pc(1)
    for _ in range(n):out=pm(out,a)
    return out
def lift(n,p):
    out={}
    for k,a in p.items():
        if k[0]:raise Failure('lift expects epsilon-free expression')
        k=list(k);k[0]=n;out[tuple(k)]=a
    return out
def pz_eval(p,z):
    out={}
    for k,a in p.items():
        n=k[1];kk=list(k);kk[1]=0
        out=pa(out,pm({tuple(kk):a},pp(z,n)))
    return out
def peval(p,z,values):
    out=E()
    for k,a in p.items():
        if k[0]:raise Failure('epsilon-free evaluation expected')
        out+=a*z**k[1]*prod(values[name]**k[i] for i,name in enumerate(NAMES) if i>=2)
    return out
def prod(items):
    out=E(1)
    for a in items:out*=a
    return out
def prec(p):return [[list(k),[str(a) for a in value.a]] for k,value in sorted(p.items())]

def generic(normalization=9,anchor_odd=False):
    z,uu,hh,vv,mm,j3,j21,j4,ww,dd=[pv(n) for n in NAMES[1:]]
    moments={1:pa(lift(2,uu),lift(3,vv),lift(4,ww)),
             2:pa(lift(2,ps(hh,-1)),lift(3,ps(mm,2)),lift(4,dd)),
             3:pa(lift(3,ps(j3,-1)),lift(4,ps(j21,-3))),4:lift(4,j4)}
    elementary=[pc(1)]
    for k in range(1,9):
        elementary.append(ps(pa(*(ps(pm(elementary[k-j],moments.get(j,{})),(-1)**(j-1))
                                   for j in range(1,k+1))),Q(1,k)))
    primitive=pa(*(ps(pm(elementary[k],pp(z,9-k)),Q(normalization*(-1)**k,9-k)) for k in range(9)))
    derivative=pa(*(ps(pm(elementary[k],pp(z,8-k)),normalization*(-1)**k) for k in range(9)))
    anchor=pa(pc(1),lift(2,pc(-1)),lift(3,pc(1)) if anchor_odd else {})
    p=pa(primitive,ps(pz_eval(primitive,anchor),-1))
    zm=lambda n:pa(pp(z,n),pc(-1))
    g2=pa(pc(9),ps(pm(uu,zm(8)),Q(-9,8)),ps(pm(hh,zm(7)),Q(9,14)))
    odd=pa(ps(pm(vv,zm(8)),Q(-9,8)),ps(pm(mm,zm(7)),Q(-9,7)),ps(pm(j3,zm(6)),Q(1,2)))
    g4=pa(pc(-36),ps(uu,-9),ps(hh,Q(9,2)),ps(pm(ww,zm(8)),Q(-9,8)),
          ps(pm(pa(pp(uu,2),ps(dd,-1)),zm(7)),Q(9,14)),
          pm(pa(ps(pm(uu,hh),Q(-3,4)),ps(j21,Q(3,2))),zm(6)),
          pm(pa(ps(pp(hh,2),Q(9,40)),ps(j4,Q(-9,20))),zm(5)))
    expected=pa(zm(9),lift(2,g2),lift(3,odd),lift(4,g4))
    return p,expected,derivative,anchor,g2,odd,g4

def tangent(direction,denominator=2,real_weight=Q(1,2)):
    # Exact Taylor coefficients of the literal chart along tau*direction.
    ts=direction[:6];rs=direction[6:];S=sum(ts);T2=sum(q*q for q in ts);R=sum(rs)
    mh=series([0,-Q(S,2)],2)
    correction=Q(T2,4)+Q(S*S,8)
    sh=series([1,0,-correction],2);invsh=series([1,0,correction],2)
    hs=[add(mh,sh),add(mh,neg(sh))]+[series([0,q],2) for q in ts]
    J3=sumseries([power(q,3) for q in hs],2)
    mu=series([up,-Q(R,2)],2)
    small=[series([uz,q],2) for q in rs]
    num=add(add(scale(J3,L*b2),scale(mul(mh,mu),-2)),
            neg(sumseries([mul(q,u) for q,u in zip(hs[2:],small)],2)))
    du=scale(mul(num,invsh),Q(1,denominator))
    us=[add(mu,du),add(mu,neg(du))]+small
    mixed=sumseries([mul(q,u) for q,u in zip(hs,us)],2)
    checks=[sumseries(hs,2),add(sumseries([power(q,2) for q in hs],2),series([-2],2)),
            add(sumseries(us,2),series([-U],2)),add(mixed,neg(scale(J3,L*b2)))]
    cost=add(series([K0],2),add(scale(sumseries([power(q,2) for q in us],2),real_weight),
             add(scale(sumseries([mul(power(q,2),u) for q,u in zip(hs,us)],2),rho*b2),
                 scale(sumseries([power(q,4) for q in hs],2),sigma*b2*b2))))
    return cost,checks
def sumseries(items,N):
    out=series(N=N)
    for a in items:out=add(out,a)
    return out

def build():
    start=CHECKS
    need(WP[0]==1 and W**9==1 and W**3!=1,'cyclotomic embedding')
    need(8*c**3-6*c-1==0,'cubic relation')
    need(interval(b2)[0]>0,'positive pair scale')
    need(6*uz+2*up==U,'reference mean')
    need(Q(3,2)*w3/8+(1+c)*w4/8==1,'dual U')
    need(Q(3,2)*w3/14+(1-d)*w4/14==Q(1,2),'dual H')
    for w in (w3,w4):need(interval(w)[0]>0,'positive slack weight')
    p,expected,derivative,anchor,g2,odd,g4=generic()
    need(p==expected,'complete generic anchored fourth jet')
    need(not pz_eval(p,anchor),'exact generic anchor')
    need(not any(k[0]==1 for k in p),'no epsilon first term')
    diff={}
    for k,a in p.items():
        if k[1]:
            kk=list(k);kk[1]-=1;diff[tuple(kk)]=a*k[1]
    need(diff==derivative,'monic integrated derivative normalization')
    values={n:E(0) for n in NAMES[2:]};values.update(U=U,H=H)
    radials={};even=[];oddrows=[];quartic=[]
    for k,omega in enumerate(WP):
        need(omega**9==1,'ninth root branch')
        gv=peval(g2,omega,values);t2=-gv*omega/9
        radial=(omega.conj()*t2).real()
        A=1-omega.real();B=1-(omega**2).real()
        need(radial==-1-A*U/8+B*H/14,'generic leading radial')
        if k in (3,4,5,6):need(radial==0,'active radial')
        else:need(interval(radial)[1]<0,'strict inactive or marked radial')
        radials[str(k)]=radial.rec()
        if k not in (3,4):continue
        even.append([-A/8,B/14])
        row=[]
        for name in ('V','M','J3'):
            vi={n:E(0) for n in NAMES[2:]};vi[name]=E(1)
            coef=(peval(odd,omega,vi)-peval(odd,omega.conj(),vi))/(9*(omega-omega.conj()))
            row.append(coef)
        oddrows.append(row)
        g2p=-9*U*omega**7+Q(9,2)*H*omega**6
        q=-1 if k==3 else -2*c;s=Q(3,4) if k==3 else 1-c*c
        y=H/14;x=-U/8
        curvature=-(Q(7,2)*x*x+6*x*y*q+Q(5,2)*y*y*q*q)*s
        C6=1-(omega**6).real();C5=1-(omega**5).real()
        T0=4+U-H/2+B*U*U/14-C6*U*H/12+C5*H*H/40+curvature
        coefficients=[]
        # g4 is affine in these four parameters. Checking the constant and
        # four basis columns proves its complete affine identity.
        for name in (None,'W','D','J21','J4'):
            vi=dict(values)
            if name:vi[name]=E(1)
            t4=-(peval(g4,omega,vi)+g2p*t2+36*omega**7*t2*t2)*omega/9
            second=(omega.conj()*t4).real()+(t2*t2.conj())/2
            expect=T0-A*vi['W']/8-B*vi['D']/14+C6*vi['J21']/6-C5*vi['J4']/20
            need(second==expect,'complete active affine root curvature')
            coefficients.append(second if name is None else second-T0)
        quartic.append(coefficients)
    need(oddrows[0]==[E(Q(1,8)),E(Q(-1,7)),E(0)],'inner odd row')
    need(oddrows[1]==[E(Q(1,8)),-2*c/7,(1-4*c*c)/18],'outer odd row')
    detE=even[0][0]*even[1][1]-even[0][1]*even[1][0]
    detO=oddrows[0][0]*oddrows[1][1]-oddrows[0][1]*oddrows[1][0]
    need(detE==3*(c+d)/224 and interval(detE)[0]>0,'even normal invertibility')
    need(detO==(1-2*c)/56 and interval(detO)[1]<0,'odd normal invertibility')
    need(L==-oddrows[1][2]/(oddrows[1][1]+Q(1,7)),'mixed constraint solution')
    base=8+2*U-Q(3,2)*H+w3*quartic[0][0]+w4*quartic[1][0]
    need(base==K0,'finite cost constant')
    need(Q(-3,2)+w3*quartic[0][3]+w4*quartic[1][3]==rho,'finite mixed cost')
    need(Q(3,8)+w3*quartic[0][4]+w4*quartic[1][4]==sigma,'finite fourth moment cost')
    # Full quadratic reconstruction needs only twelve axis directions and
    # all66 pair sums; degree<=2 follows from literal truncated operations.
    axes=[[int(j==i) for j in range(12)] for i in range(12)]
    directions=axes+[list(map(sum,zip(axes[i],axes[j]))) for i in range(12) for j in range(i+1,12)]
    costs=[]
    for direction in directions:
        cost,constraints=tangent(direction)
        for eq in constraints:need(all(x==0 for x in eq),'literal tangent chart constraint')
        need(cost[0]==Bstar and cost[1]==0,'stationary reference cost')
        t=direction[:6];r=direction[6:]
        wanted=aT*sum(x*x for x in t)+bT*sum(t)**2+Q(1,2)*sum(x*x for x in r)+Q(1,4)*sum(r)**2
        need(cost[2]==wanted,'complete polarized tangent coefficient')
        costs.append(cost[2])
    matrix=[[E(0) for _ in range(12)] for _ in range(12)]
    for i in range(12):matrix[i][i]=costs[i]
    offset=12
    for i in range(12):
        for j in range(i+1,12):
            matrix[i][j]=matrix[j][i]=(costs[offset]-costs[i]-costs[j])/2;offset+=1
    for i in range(12):
        for j in range(12):
            expected=(aT*int(i==j)+bT if i<6 and j<6 else
                      E(Q(1,2)*int(i==j)+Q(1,4)) if i>=6 and j>=6 else E(0))
            need(matrix[i][j]==expected,'full tangent matrix entry')
    raw_imag=[2*aT/b2,2*(aT+6*bT)/b2]
    for eigenvalue in raw_imag:need(interval(eigenvalue)[0]>1,'imaginary Hessian exceeds real minimum')
    need(2*Q(1,2)==1 and 2*(Q(1,2)+6*Q(1,4))==4,'real Hessian exact spectrum')
    need(interval((aT+bT)/b2)[0]>0,'small imaginary direction positive')
    centered=[0]*12;centered[6]=1;centered[7]=-1
    cost,_=tangent(centered)
    need(cost[2]==1 and sum(x*x for x in centered)==2,'sharp raw centered-real quotient one half')
    damage=[]
    def reject(ok,label):
        try:need(ok,label)
        except Failure:damage.append(label)
        else:raise Failure('damaged check accepted: '+label)
    bad=generic(normalization=8);reject(bad[0]==bad[1],'wrong derivative normalization')
    bad=generic(anchor_odd=True);reject(bad[0]==bad[1],'wrong third-order anchor')
    reject(oddrows[0][1]/2==Q(-1,7),'odd mixed half omitted')
    omega=WP[3];t2=-peval(g2,omega,values)*omega/9
    reject(quartic[0][0]-(t2*t2.conj())/2==quartic[0][0],'radial modulus square omitted')
    test=[0]*12;test[0]=1
    cost,constraints=tangent(test,denominator=1)
    reject(all(x==0 for x in constraints[-1]),'mixed reconstruction denominator changed')
    cost,_=tangent(centered,real_weight=1)
    reject(cost[2]==1,'finite real square doubled')
    cost,_=tangent(test)
    reject(cost[2]==aT,'imaginary rank-one coupling omitted')
    reject(matrix[6][7]==0,'real rank-one coupling omitted')
    reject(raw_imag[0]==1,'imaginary eigenvalue replaced by one')
    reject(costs[6]*2==1,'raw real diagonal mistaken for least eigenvalue')
    # Distance jet in two real variables: a standalone second derivative
    # uses q=-2eta(1+u)+eta*h^2+eta^2(1+u)^2 and 1-q/2+3q^2/8.
    u,h2=pv('U'),pv('H');aa=pa(pc(1),u)
    dq=pa(lift(2,pa(ps(aa,-2),h2)),lift(4,pp(aa,2)))
    distance=pa(pc(1),ps(dq,Q(-1,2)),ps(pm(dq,dq),Q(3,8)))
    dist_expected=pa(pc(1),lift(2,pa(aa,ps(h2,Q(-1,2)))),
                     lift(4,pa(pp(aa,2),ps(pm(aa,h2),Q(-3,2)),ps(pp(h2,2),Q(3,8)))))
    need(distance==dist_expected,'complete reciprocal distance second jet')
    bad=pa(pc(1),ps(dq,Q(-1,2)),ps(pm(dq,dq),Q(1,3)))
    reject(bad==dist_expected,'reciprocal binomial changed')
    return dict(schema='independent-analytic-minimizer-v1',agent='six-reviewer-1',role='independent mathematical reviewer',
                arithmetic='single Q[w]/(w^6+w^3+1) and univariate chart polarization',
                embedding_interval=[str(LO),str(HI)],
                constants={n:E(x).rec() for n,x in dict(H=H,U=U,uz=uz,up=up,rho=rho,L=L,w3=w3,w4=w4,sigma=sigma,K0=K0,Bstar=Bstar).items()},
                generic_variables=NAMES,generic_polynomial=prec(p),generic_derivative=prec(derivative),
                leading_radials=radials,even_rows=[[x.rec() for x in row] for row in even],
                odd_rows=[[x.rec() for x in row] for row in oddrows],normal_determinants=[detE.rec(),detO.rec()],
                active_second_affine=[[x.rec() for x in row] for row in quartic],
                tangent_axes_and_pairs=len(directions),tangent_matrix=[[x.rec() for x in row] for row in matrix],
                tangent_a=aT.rec(),tangent_b=bT.rec(),raw_imaginary_hessian_eigenvalues=[x.rec() for x in raw_imag],
                raw_real_hessian_eigenvalues=['1','4'],raw_eigenvalue_multiplicities=[5,1,5,1],
                sharp_limiting_quadratic_gap='1/2',sharp_limiting_individual_radial_weights=[(w3/2).rec(),(w4/2).rec()],
                small_imaginary_cost=((aT+bT)/b2).rec(),exact_checks=CHECKS-start,damage_labels=damage,
                trust_boundary='Finite algebra only; ordinary analytic chart, coverage and continuation in REVIEW.md')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write',action='store_true',help='Development only; does not validate changed evidence')
    args=parser.parse_args();record=build();record=json.loads(json.dumps(record))
    raw=(json.dumps(record,sort_keys=True,indent=2)+'\n').encode()
    if args.write:args.fixture.write_bytes(raw)
    else:
        try:expected=json.loads(args.fixture.read_text())
        except (OSError,ValueError) as exc:raise Failure('Missing/malformed exact fixture') from exc
        need(expected==record,'complete frozen record')
    print('PASS: '+str(record['exact_checks'])+' exact checks; '+str(len(record['damage_labels']))+' mathematical damages rejected; all78 tangent directions.')
    print('Record SHA256 '+sha256(raw).hexdigest())
    print('Smallest raw Hessian eigenvalue exactly1; sharp limiting gap1/2. Analytic bridges are ordinary proof.')
if __name__=='__main__':main()
