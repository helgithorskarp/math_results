#!/usr/bin/env python3
"""six-reviewer-1: independent cyclotomic/Lagrange fourth-boundary audit.
Standard library only; no imports of researcher source. See REVIEW.md for the
ordinary degree/symmetry and uniform analytic bridges behind finite checks.
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
U0=-8*(Q(2,3)-1/(3*(1+c)));uz=(U0+rho*H)/8;up=uz-rho*H/2
Wstar=realfield((Q(2512,27),Q(5840,9),Q(-21392,27)))
Dstar=realfield((Q(-4270,27),Q(-29492,27),Q(4012,3)))
gamma=(6*uz**2+2*up**2-Dstar)/(2*H)
d=2*c*c-1;v=2*d*d-1
A=[E(Q(3,2)),1+c];B=[E(Q(3,2)),1-d]
w4=1/(c+d);w3=Q(2,3)*(7-(1-d)*w4);weights=[w3,w4]
C=Q(8,3)+1/(3*(1+c));Bstar=realfield((Q(2311,108),Q(4934,27),Q(-1976,9)))
C3=realfield((Q(-60800959,17496),Q(-307083769,17496),Q(10980067,486)))
C4=realfield((Q(340367352475,839808),Q(808137564635,419904),Q(-1052841914857,419904)))
q0=realfield((Q(183619658945,2519424),Q(444829186913,1259712),Q(-288729410449,629856)))
ell=realfield((Q(50960,243),Q(1218245,972),Q(-125944,81)))
aT=realfield((Q(-11564,405),Q(-20482,81),Q(123284,405)))
bT=realfield((Q(49,180),Q(-105889,486),Q(305123,1215)))
rstar=-ell/4;alpha=Wstar/8+rstar;beta=Wstar/8-3*rstar
mstar=realfield((Q(-18681113,8748),Q(-23084270,2187),Q(3318742,243)))
thetastar=realfield((Q(-6128723,23328),Q(-33473077,23328),Q(173445991,93312)))
nstar=realfield((Q(69179489551,629856),Q(82217239787,157464),Q(-214144521727,314928)))
phistar=realfield((Q(100267260167,17915904),Q(269718907597,8957952),Q(-42812814917,1119744)))


def moments_poly(h,u):
    """Real Newton coefficients; imaginary products begin at eta5 on this chart."""
    N=len(h[0])-1;one=series([1],N);powers=[series(N=N)]
    for k in range(1,9):
        p=series(N=N)
        for j in range(k//2+1):
            exponent=k-j
            if exponent<=N:
                term=sumseries([mul(power(u[a],k-2*j),power(h[a],2*j)) for a in range(8)],N)
                p=add(p,scale(shift(term,exponent),(-1)**j*comb(k,2*j)*b2**j))
        powers.append(p)
    es=[one]
    for k in range(1,9):
        es.append(scale(sumseries([scale(mul(es[k-j],powers[j]),(-1)**(j-1)) for j in range(1,k+1)],N),Q(1,k)))
    poly={9-j:scale(es[j],Q(9*(-1)**j,9-j)) for j in range(9)}
    marked=series([1,-1],N)
    poly[0]=neg(sumseries([mul(a,power(marked,z)) for z,a in poly.items()],N))
    f=series(N=N)
    for j in range(8):
        sq=add(power(add(one,neg(shift(add(one,u[j]),1))),2),scale(shift(power(h[j],2),1),b2))
        sq[0]-=1;f=add(f,binomial(sq,Q(-1,2)))
    return poly,f

def sumseries(items,N):
    out=series(N=N)
    for item in items:out=add(out,item)
    return out


def lagrange(poly,k,N=4,residual=False):
    """p(w^k(1+s),eta)=g(s)s+delta; formal Lagrange inversion."""
    omega=WP[k];R=series([Q(1,9)],N-1)
    for n in range(1,N):R[n]=-sum((comb(9,j+1)*R[n-j] for j in range(1,n+1)),E())/9
    D=[series(N=N-1)]
    for n in range(1,N+1):
        f=series(N=N-1)
        for z,a in poly.items():
            if n<len(a) and a[n]:
                for j in range(min(z,N-1)+1):f[j]+=a[n]*omega**z*comb(z,j)
        D.append(mul(f,R))
    # eta convolution of the Lagrange powers, truncated in s as well.
    current=[series([1],N-1)]+[series(N=N-1) for _ in range(N)]
    sn=[E() for _ in range(N+1)]
    for m in range(1,N+1):
        nxt=[series(N=N-1) for _ in range(N+1)]
        for i in range(N+1):
            for j in range(1,N+1-i):
                if any(current[i]) and any(D[j]):nxt[i+j]=add(nxt[i+j],mul(current[i],D[j]))
        current=nxt
        for n in range(m,N+1):sn[n]+=current[n][m-1]*Q((-1)**m,m)
    root=scale(series([1]+sn[1:],N),omega)
    rad=[]
    for n in range(1,N+1):
        rad.append(sn[n].real()+sum((sn[j]*sn[n-j].conj() for j in range(1,n)),E())/2)
        rad[-1].rec()
    if residual:
        val=series(N=N)
        for z in range(9,-1,-1):val=add(mul(val,root),poly.get(z,series(N=N)))
        need(not any(val),'complete Lagrange root residual '+str(k))
    return root,rad


def canonical(t,r,m=0,theta=0):
    N=4;S=sum(t,E());R=sum(r,E());diff=-(rho+3*L)*b2*S;kappa=-3*L*b2*S/7
    xi=[gamma-S/2,-gamma-S/2,*t]
    nu=[Wstar/8-R/2+diff/2,Wstar/8-R/2-diff/2,*[Wstar/8+a for a in r]]
    hs=[1,-1,0,0,0,0,0,0];us=[up,up,*[uz]*6]
    h=[series([hs[j],xi[j],theta*hs[j]+kappa],N) for j in range(8)]
    u=[series([us[j],nu[j],m],N) for j in range(8)]
    return moments_poly(h,u)


def finite_cost(t,r,check_residual=False):
    pol,f=canonical(t,r)
    baseline=[lagrange(pol,k)[1] for k in (3,4)]
    p,q=[a[2] for a in baseline]
    determinant=(-A[0])*(H*B[1]/7)-(-A[1])*(H*B[0]/7)
    m=((-p)*(H*B[1]/7)-(-q)*(H*B[0]/7))/determinant
    theta=((-A[0])*(-q)-(-A[1])*(-p))/determinant
    pol,f=canonical(t,r,m,theta)
    rr=[lagrange(pol,k,residual=check_residual)[1] for k in (3,4)]
    need(all(a==0 for rad in rr for a in rad[:3]),'three active contact coefficients')
    need(f[:4]==[E(8),C,Bstar,C3],'four fixed objective coefficients')
    cost=f[4]+sum((w*rad[3] for w,rad in zip(weights,rr)),E())
    S=sum(t,E());R=sum(r,E())
    model=q0+ell*R+aT*sum((a*a for a in t),E())+bT*S*S+sum((a*a for a in r),E())/2+R*R/4
    need(cost==model,'independent finite quadratic cost')
    return cost,m,theta,pol,f



def invariant_coefficients(values):
    """Degree/symmetry completeness is proved separately in REVIEW.md."""
    o,tm,tp,tt,rp,rm,rr=values
    need(tm==tp,'even imaginary invariant')
    td=tm-o;to=(tt-o-2*td)/2
    rl=(rp-rm)/2;rd=(rp+rm)/2-o;ro=(rr-o-2*rl-2*rd)/2
    terms={}
    def put(coords,value):
        if value:
            ex=[0]*18
            for i in coords:ex[i]+=1
            terms[tuple(ex)]=value
    put([],o)
    for j in range(6):
        put([j,j],td);put([j+6],rl);put([j+6,j+6],rd)
        for k in range(j+1,6):put([j,k],2*to);put([j+6,k+6],2*ro)
    return [[list(e),a.rec()] for e,a in sorted(terms.items())]

def family(real_split_order=None,compensated=False):
    """Full factor-defined conjugation-invariant polynomial, eta through5."""
    N=5;one=series([1],N);eta=series([0,1],N)
    L0=series([0,uz,alpha,mstar,nstar,1000],N)
    Lp=series([0,up,beta,mstar,nstar,1000],N)
    opening=series([1,gamma,thetastar,phistar+(1/H if compensated else 0)],N)
    # Polynomials in z with eta-series coefficients, coefficientwise products.
    def zmul(a,b):
        out={}
        for i,x in a.items():
            for j,y in b.items():out[i+j]=add(out.get(i+j,series(N=N)),mul(x,y))
        return out
    def zpower(a,n):
        out={0:one}
        for _ in range(n):out=zmul(out,a)
        return out
    realfactor={1:one,0:neg(L0)}
    real=zpower(realfactor,6)
    if real_split_order:
        split=zpower(realfactor,2);split[0]=add(split[0],neg(shift(one,real_split_order)))
        real=zmul(zpower(realfactor,4),split)
    pair=zpower({1:one,0:neg(Lp)},2)
    pair[0]=add(pair[0],scale(mul(eta,power(opening,2)),b2))
    derivative={z:scale(a,9) for z,a in zmul(real,pair).items()}
    pol={z+1:scale(a,Q(1,z+1)) for z,a in derivative.items()}
    marked=series([1,-1],N);pol[0]=neg(sumseries([mul(a,power(marked,z)) for z,a in pol.items()],N))
    base=add(marked,neg(L0));delta=base.copy();delta[0]-=1
    freal=scale(binomial(delta,Q(-1)),6)
    if real_split_order:
        # 1/(a-e)+1/(a+e)-2/a = 2 e^2/a^3+O(e^4).
        freal=add(freal,scale(shift(binomial(delta,Q(-3)),real_split_order),2))
    sq=add(power(add(marked,neg(Lp)),2),scale(shift(power(opening,2),1),b2));sq[0]-=1
    f=add(freal,scale(binomial(sq,Q(-1,2)),2))
    branches=[]
    for k in range(9):
        root,rad=lagrange(pol,k,N=5,residual=True)
        need(root[0]==WP[k],'root base index '+str(k))
        if k==0:need(root==series([1,-1],N),'exact marked branch')
        elif k in (1,2,7,8):need(interval(rad[0])[1]<0,'inactive first inward '+str(k))
        else:
            need(all(a==0 for a in rad[:4]),'active contact through fourth '+str(k))
            need(interval(rad[4])[1]<0,'active fifth inward '+str(k))
        branches.append({'index':k,'radial':[a.rec() for a in rad]})
    return pol,f,branches


def higher_traces():
    N=4;hs=[1,-1,0,0,0,0,0,0];us=[up,up,*[uz]*6]
    base,f0=moments_poly([series([a],N) for a in hs],[series([a],N) for a in us])
    records=[]
    directions=[]
    # 6 imaginary zero-sum/norm-tangent directions, 7 real zero-sum.
    for j in range(6):
        a=[E(-Q(1,2)),E(-Q(1,2)),*[E(i==j) for i in range(6)]];directions.append(('tangent_h',a,[E()]*8,2))
    for j in range(7):
        a=[E(i==j) for i in range(8)];a[7]-=1;directions.append(('tangent_u',[E()]*8,a,2))
    # All8+8 third normals; linearity proves every combination.
    for j in range(8):
        a=[E(i==j) for i in range(8)];directions.append(('normal_h',a,[E()]*8,3))
        directions.append(('normal_u',[E()]*8,a,3))
    for kind,dh,du,order in directions:
        h=[series([hs[j]],N) for j in range(8)];u=[series([us[j]],N) for j in range(8)]
        for j in range(8):h[j][order]=dh[j];u[j][order]=du[j]
        pol,f=moments_poly(h,u)
        need(all(pol.get(z,series(N=N))[:4]==base.get(z,series(N=N))[:4] for z in set(pol)|set(base)),'lower polynomial higher trace '+kind)
        need(f[:4]==f0[:4],'lower objective higher trace '+kind)
        delta={z:pol.get(z,series(N=N))[4]-base.get(z,series(N=N))[4] for z in set(pol)|set(base)}
        response=f[4]-f0[4]-sum((wt*sum((a*WP[k]**z for z,a in delta.items()),E()).real()/9 for wt,k in zip(weights,(3,4))),E())
        need(response==0,'full independent higher dual trace '+kind)
        records.append({'kind':kind,'polynomial_delta4':[[z,a.rec()] for z,a in sorted(delta.items()) if a],'objective_delta4':(f[4]-f0[4]).rec(),'dual_delta4':response.rec()})
    return records


def build():
    need(WP[9%9]==1 and W**6+W**3+1==0,'cyclotomic relation')
    need(8*c**3-6*c-1==0,'embedded cubic relation')
    need(w3*A[0]/8+w4*A[1]/8==1 and w3*B[0]/7+w4*B[1]/7==1,'dual normalizations')
    for a in (H,w3,w4,aT,aT+6*bT):need(interval(a)[0]>0,'positive inherited or finite weight')
    need(C4==q0-3*ell*ell/4,'completed square coefficient')
    need(Q('-233.920855886')<interval(C4)[0]<=interval(C4)[1]<Q('-233.920855885'),'C4 enclosure')
    # Seven values fix all six coefficients after the separately proved
    # degree<=2, S6 symmetry, and simultaneous t->-t invariance.
    points=[([0]*6,[0]*6),([1,0,0,0,0,0],[0]*6),([-1,0,0,0,0,0],[0]*6),([1,1,0,0,0,0],[0]*6),([0]*6,[1,0,0,0,0,0]),([0]*6,[-1,0,0,0,0,0]),([0]*6,[1,1,0,0,0,0])]
    finite=[]
    for i,(t,r) in enumerate(points):
        value,m,theta,pol,f=finite_cost(list(map(E,t)),list(map(E,r)),check_residual=i==0)
        finite.append({'t':t,'r':r,'cost':value.rec(),'m':m.rec(),'theta':theta.rec()})
    _,m,theta,pol,f=finite_cost([E()]*6,[rstar]*6)
    need(m==mstar and theta==thetastar,'independent optimal cubic normals')
    radial4=[lagrange(pol,k)[1][3] for k in (3,4)]
    determinant=-A[0]*(H*B[1]/7)+A[1]*(H*B[0]/7)
    nn=(-radial4[0]*(H*B[1]/7)+radial4[1]*(H*B[0]/7))/determinant
    pp=(A[0]*radial4[1]-A[1]*radial4[0])/determinant
    need(nn==nstar and pp==phistar,'independent optimal quartic normals')
    need(f[4]+sum((wt*lagrange(pol,k)[1][3] for wt,k in zip(weights,(3,4))),E())==C4,'optimal finite cost')
    branches={};families={}
    for name,split,comp in [('attaining',None,False),('sharp_next_profile',5,False),('sharp_coercivity',4,True)]:
        p,ff,rr=family(split,comp);branches[name]=rr;families[name]=[a.rec() for a in ff]
        expected=[E(8),C,Bstar,C3,C4+(1 if comp else 0)]
        need(ff[:5]==expected,'full objective through fourth '+name)
        if name=='attaining':
            need(all(p[z][:4]==pol.get(z,series(N=4))[:4] for z in p),'factor versus independent lower moment coefficients')
            for z in p:
                shift4=(-9*nstar if z==8 else Q(9,7)*H*phistar if z==7 else 9*nstar-Q(9,7)*H*phistar if z==0 else E())
                need(p[z][4]-pol.get(z,series(N=4))[4]==shift4,'full quartic normal response')
            basep=p;basef=ff
        elif name=='sharp_next_profile':
            need(ff[5]-basef[5]==2,'split fifth objective response')
            need(all(p[z][:5]==basep[z][:5] for z in p),'fifth split lower polynomial jets')
            for z in p:need(p[z][5]-basep[z][5]==(-Q(9,7) if z==7 else Q(9,7) if z==0 else 0),'entire split fifth polynomial response')
        else:
            need(all(p[z][:5]==basep[z][:5] for z in p),'compensated real split all quartic polynomial jets')
    # Two invariant imaginary modes, with the exact Euclidean chart metric.
    gapT=aT-b2/2
    meanmetric=4*b2+3*(rho+3*L)**2*b2**2
    gapS=aT+6*bT-meanmetric/2
    need(interval(gapT)[0]>0 and interval(gapS)[0]>0,'sharp half coercivity positive imaginary blocks')
    # Pure-real first jets have Qgap=.5 E^2, so the endpoint is sharp.
    t=[E()]*6;r=[rstar+1,rstar-1,*[rstar]*4]
    value,_,_,_,_=finite_cost(t,r)
    need(value-C4==1,'finite sharp half equality direction')
    higher=higher_traces()
    interpolation={key:invariant_coefficients([realfield(point[key]) for point in finite]) for key in ('cost','m','theta')}
    damages=[]
    def reject(ok,label):
        if ok:raise Failure('unrejected damage '+label)
        damages.append(label)
    reject(C4+1==q0-3*ell*ell/4,'fourth coefficient')
    reject(finite[1]['cost']==(q0+aT+bT+1).rec(),'imaginary quadratic coefficient')
    reject(finite[4]['cost']==(q0+ell+Q(3,4)+1).rec(),'real quadratic coefficient')
    reject(interval(realfield(branches['attaining'][3]['radial'][4]))[0]>0,'active fifth radial sign')
    reject(families['sharp_next_profile'][5]==families['attaining'][5],'fifth split response')
    reject(all(realfield(x['dual_delta4'])==1 for x in higher),'higher tangent cancellation')
    reject(gapT==0,'half-coercivity imaginary block')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','method':'single cyclotomic field; formal Lagrange inversion; proved degree/symmetry reduction; full29 higher-trace basis directions; three factor-defined full families','checks':CHECKS,'damage_controls':damages,'c_embedding_interval':[str(LO),str(HI)],'constants':{k:a.rec() for k,a in {'C4':C4,'q0':q0,'ell':ell,'aT':aT,'bT':bT,'rstar':rstar,'alpha':alpha,'beta':beta,'mstar':mstar,'thetastar':thetastar,'nstar':nstar,'phistar':phistar,'coercivity_transverse_gap':gapT,'coercivity_mean_gap':gapS}.items()},'finite_cost_points':finite,'full_invariant_records':interpolation,'family_objectives':families,'all_nine_root_radials':branches,'higher_trace_basis':higher,'trust_boundary':'Exact standard-library rational arithmetic. Analytic arbitrary-competitor reduction, degree/symmetry completeness, disk collar, optimal-rate quantifiers and literature status are ordinary proofs in REVIEW.md; no formal kernel or effective collar.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit-fixture',action='store_true');args=parser.parse_args()
    fixture=None
    if not args.emit_fixture:
        try:fixture=json.loads(args.fixture.read_text())
        except (OSError,ValueError) as e:raise Failure('required fixture unavailable or malformed') from e
        if not isinstance(fixture,dict):raise Failure('fixture must be a complete object')
    result=build();encoded=json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    if args.emit_fixture:print(encoded,end='')
    else:
        need(fixture==result,'complete fresh record versus fixture')
        print('PASS:',result['checks'],'exact checks;',len(result['damage_controls']),'damages rejected; 27 root branches; 29 higher trace directions.')
        print('Complete record SHA256:',sha256(encoded.encode()).hexdigest())
if __name__=='__main__':main()
