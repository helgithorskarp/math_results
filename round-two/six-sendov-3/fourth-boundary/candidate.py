#!/usr/bin/env python3
"""six-sendov-3, researcher: exact full twelve-tangent fourth cost.

Finite certificate; arbitrary-competitor completeness is ordinary proof in PROOF.md.
The local arithmetic adapts the author's published cubic kernels, with attribution.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from math import comb
import time

SOURCE=Path(__file__).with_name('arithmetic.py')
spec=importlib.util.spec_from_file_location('cubic_author_arithmetic',SOURCE)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
K,Z=prior.K,prior.Z
N=18; ZERO=(0,)*N; CAP=4
checks=0
started=time.monotonic()

def check(ok,label):
    global checks
    if not ok:raise RuntimeError(label)
    checks+=1

def stage(label):

    if not globals().get('QUIET',False):print(label,flush=True)

class P:
    def __init__(self,value=0):
        if isinstance(value,P):self.a=value.a
        elif isinstance(value,dict):self.a={k:K(v) for k,v in value.items() if K(v)!=0}
        else:self.a={ZERO:K(value)} if K(value)!=0 else {}
    @staticmethod
    def var(j):
        e=list(ZERO);e[j]=1
        return P({tuple(e):K(1)})
    def __bool__(self):return bool(self.a)
    def __add__(self,b):
        a=self.a.copy()
        for e,v in P(b).a.items():
            a[e]=a.get(e,K(0))+v
            if a[e]==0:del a[e]
        return P(a)
    __radd__=__add__
    def __neg__(self):return P({e:-v for e,v in self.a.items()})
    def __sub__(self,b):return self+-P(b)
    def __rsub__(self,b):return P(b)+-self
    def __mul__(self,b):
        a={}
        for e,v in self.a.items():
            for f,w in P(b).a.items():
                key=tuple(x+y for x,y in zip(e,f))
                a[key]=a.get(key,K(0))+v*w
                if a[key]==0:del a[key]
        return P(a)
    __rmul__=__mul__
    def __truediv__(self,b):return self*K(b).inv()
    def __pow__(self,n):
        ans=P(1)
        for _ in range(n):ans=ans*self
        return ans
    def __eq__(self,b):return self.a==P(b).a
    def coef(self,e):return self.a.get(tuple(e),K(0))
    def replace(self,j,v):
        v=P(v);out=P()
        for e,a in self.a.items():
            f=list(e);power=f[j];f[j]=0
            out+=P({tuple(f):a})*v**power
        return out
    def record(self):return [[list(e),v.record()] for e,v in sorted(self.a.items())]
    def digest(self):return sha256(json.dumps(self.record(),separators=(',',':')).encode()).hexdigest()
    def constant(self):
        check(set(self.a)<={ZERO},'polynomial is constant')
        return self.a.get(ZERO,K(0))
    def at(self,values):
        out=K(0)
        for e,a in self.a.items():
            for j,n in enumerate(e):a*=K(values.get(j,0))**n
            out+=a
        return out

class J:
    def __init__(self,values=0):
        if isinstance(values,J):self.a=values.a
        else:
            if not isinstance(values,list):values=[values]
            self.a=[P(values[j]) if j<len(values) else P() for j in range(CAP+1)]
    def __add__(self,b):return J([x+y for x,y in zip(self.a,J(b).a)])
    __radd__=__add__
    def __neg__(self):return J([-a for a in self.a])
    def __sub__(self,b):return self+-J(b)
    def __rsub__(self,b):return J(b)+-self
    def __mul__(self,b):
        b=J(b);out=[P() for _ in self.a]
        for i,x in enumerate(self.a):
            if not x:continue
            for j,y in enumerate(b.a[:CAP+1-i]):
                if y:out[i+j]+=x*y
        return J(out)
    __rmul__=__mul__
    def __truediv__(self,b):return J([a/b for a in self.a])
    def __pow__(self,n):
        ans=J(1)
        for _ in range(n):ans=ans*self
        return ans

eta=J([0,1])
c=K((0,1,0));d=2*c*c-1;v=2*d*d-1
y=1/(3*(1+c));x=K(F(2,3))-y
H=14*y;U0=-8*x;C=K(F(8,3))+y;rho=(c-5)/3;L=-7*(2*c+1)/18
uz=(U0+rho*H)/8;up=uz-rho*H/2;b2=H/2
W=K((F(2512,27),F(5840,9),F(-21392,27)))
D=K((F(-4270,27),F(-29492,27),F(4012,3)))
U2=6*uz**2+2*up**2;gamma=(U2-D)/(2*H)
Bstar=K((F(2311,108),F(4934,27),F(-1976,9)))
C3=K((F(-60800959,17496),F(-307083769,17496),F(10980067,486)))
w4=1/(c+d);w3=K(F(2,3))*(7-(1-d)*w4)
A=[K(F(3,2)),1+c];B=[K(F(3,2)),1-d]
roots=[Z((F(-1,2),0,0,1),q=K(F(3,4))),Z((-c,0,0,1),q=1-c*c)]

t=[P.var(j) for j in range(6)];r=[P.var(j) for j in range(6,12)]
m,theta,n,phi,oddreal,oddmean=[P.var(j) for j in range(12,18)]
St=sum(t,P());Sr=sum(r,P())
xi=[P(gamma)-St/2,-P(gamma)-St/2,*t]
diff=St*(-(rho+3*L)*b2)
nu=[P(W/8)-Sr/2+diff/2,P(W/8)-Sr/2-diff/2,
    *(P(W/8)+a for a in r)]
mean2=St*(-3*L*b2/7)
hs=[1,-1,0,0,0,0,0,0];us=[up,up,*([uz]*6)]
u=[J([us[j],nu[j],m+oddreal*hs[j],n]) for j in range(8)]
h=[J([hs[j],xi[j],theta*hs[j]+mean2,phi*hs[j]+oddmean]) for j in range(8)]
check(sum(xi,P())==0,'balanced first h jet')
check(xi[0]-xi[1]==2*gamma,'forced first h norm jet')
check(sum(nu,P())==W,'forced first u mean jet')
check(nu[0]-nu[1]==diff,'full first mixed constraint')

# All imaginary low moments start at eta^(5/2); their real Newton products
# start at eta^5. Compute every real power sum, including P7 and P8.
powers=[J()]
for k in range(1,9):
    pk=J()
    for j in range(k//2+1):
        exponent=k-j
        if exponent>CAP:continue
        coeff=K((-1)**j*comb(k,2*j))*b2**j
        pk+=eta**exponent*sum((u[a]**(k-2*j)*h[a]**(2*j)
                               for a in range(8)),J())*coeff
    powers.append(pk)
elementary=[J(1)]
for k in range(1,9):
    elementary.append(sum((elementary[k-j]*powers[j]*((-1)**(j-1))
                          for j in range(1,k+1)),J())/k)
primitive={9-j:elementary[j]*K(F(9*(-1)**j,9-j)) for j in range(9)}
anchor=sum((a*(J(1)-eta)**z for z,a in primitive.items()),J())
poly={**primitive,0:-anchor}
jets=[{z:a.a[k] for z,a in poly.items() if a.a[k]} for k in range(CAP+1)]
check(all(set(a.a)<={ZERO} for a in powers[1:3][0].a[:2]),'leading mean constants')
check(all(set(a.a)<={ZERO} for k in [0,1,2] for a in jets[k].values()),
      'first two entire original coefficient jets fixed')
check(sum((a*(J(1)-eta)**z for z,a in poly.items()),J()).a==J().a,
      'full anchored polynomial identity')
stage('generic real critical jets and full eta4 anchored polynomial')

distance=[]
for j in range(8):
    sq=(J(1)-eta*(J(1)+u[j]))**2+eta*h[j]**2*b2
    delta=sq-J(1)
    distance.append(sum((delta**k*coef for k,coef in enumerate(
        [F(1),F(-1,2),F(3,8),F(-5,16),F(35,128)])),J()))
objective=sum(distance,J())
check(objective.a[0]==8 and objective.a[1]==C and objective.a[2]==Bstar,
      'full objective first two constants')

def eval_constant_jet(k,omega,derivative=0):
    out=Z(0,q=omega.q)
    for degree,p in jets[k].items():
        if degree<derivative:continue
        a=p.constant()
        for z in range(derivative):a*=degree-z
        out+=omega**(degree-derivative)*a
    return out

def radial_linear_maps(omega):
    # All root coefficients at orders1 and2 are constant. Higher radial
    # coefficients are affine in p3,p4. Derive both full linear maps.
    q=omega.q;zero=Z(0,q=q)
    f1=eval_constant_jet(1,omega)
    f1p=eval_constant_jet(1,omega,1)
    f1pp=eval_constant_jet(1,omega,2)
    f1ppp=eval_constant_jet(1,omega,3)
    f2=eval_constant_jet(2,omega)
    f2p=eval_constant_jet(2,omega,1)
    f2pp=eval_constant_jet(2,omega,2)
    r1=-f1*omega/9
    r2=-(f2+f1p*r1+36*omega**7*r1*r1)*omega/9
    check((r1*omega.conj()).real_field()==0,'first active tangency')
    check((r2*omega.conj()+r1*r1.conj()/2).real_field()==0,
          'second active tangency')
    r30=-(f2p*r1+f1p*r2+f1pp*r1*r1/2
           +72*omega**7*r1*r2+84*omega**6*r1**3)*omega/9
    r40=-(f2p*r2+f2pp*r1*r1/2+f1p*r30+f1pp*r1*r2
           +f1ppp*r1**3/6+72*omega**7*r1*r30+36*omega**7*r2*r2
           +252*omega**6*r1*r1*r2+126*omega**5*r1**4)*omega/9
    R30=(r30*omega.conj()+r1*r2.conj()).real_field()
    R40=(r40*omega.conj()+r1*r30.conj()+r2*r2.conj()/2).real_field()
    l3={};l4={}
    for degree in range(10):
        delta3=-omega**(degree+1)/9
        delta4=-(f1p*delta3+72*omega**7*r1*delta3
                   +(degree*omega**(degree-1)*r1 if degree else zero))*omega/9
        l3[degree]=(delta3*omega.conj()).real_field()
        l4[degree]=(delta4*omega.conj()+r1*delta3.conj()).real_field()
    R3=P(R30)+sum((p*l3[z] for z,p in jets[3].items()),P())
    R4=P(R40)+sum((p*l3[z] for z,p in jets[4].items()),P())
    R4+=sum((p*l4[z] for z,p in jets[3].items()),P())
    return R3,R4

radials=[radial_linear_maps(w) for w in roots]
def unit(j):
    e=list(ZERO);e[j]=1;return tuple(e)
for j,(R3,R4) in enumerate(radials):
    check(R3.coef(unit(12))==-A[j],'independent m response')
    check(R3.coef(unit(13))==H*B[j]/7,'independent theta response')
    check(R4.coef(unit(14))==-A[j],'independent n response')
    check(R4.coef(unit(15))==H*B[j]/7,'independent phi response')
aa,bb=-A[0],H*B[0]/7;cc,dd=-A[1],H*B[1]/7;det=aa*dd-cc*bb
base3=[a[0].replace(12,0).replace(13,0) for a in radials]
ms=(-base3[0]*dd+base3[1]*bb)/det
ths=(base3[1]*(-aa)+base3[0]*cc)/det
def third_repair(p):return p.replace(12,ms).replace(13,ths)
for R3,R4 in radials:check(third_repair(R3)==0,'whole cubic active cancellation')
check(third_repair(objective.a[3])==C3,'full twelve-variable cubic optimum')
stage('both cubic normals solved and C3 constant on all twelve tangents')

R4=[third_repair(a[1]) for a in radials]
cost=third_repair(objective.a[4])+R4[0]*w3+R4[1]*w4
check(all(not any(e[12:]) for e in cost.a),'all higher normal/odd variables eliminated')
check(all(sum(e)<=2 for e in cost.a),'complete cost has degree at most two')
const=cost.coef(ZERO);lin=cost.coef(unit(6))
aT=cost.coef(tuple(2*x for x in unit(0)))
bt_exp=[x+y for x,y in zip(unit(0),unit(1))]
bT=cost.coef(bt_exp)/2;aT-=bT
aR=cost.coef(tuple(2*x for x in unit(6)))
br_exp=[x+y for x,y in zip(unit(6),unit(7))]
bR=cost.coef(br_exp)/2;aR-=bR
model=P(const)+Sr*lin+sum((a*a for a in t),P())*aT+St*St*bT
model+=sum((a*a for a in r),P())*aR+Sr*Sr*bR
check(cost==model,'full twelve-dimensional two symmetric quadratic blocks')
lo,hi=F(3,4),F(1)
for _ in range(100):
    mid=(lo+hi)/2
    if 8*mid**3-6*mid-1<0:lo=mid
    else:hi=mid
for a,label in [(aT,'imaginary transverse'),(aT+6*bT,'imaginary mean'),
               (aR,'real transverse'),(aR+6*bR,'real mean')]:
    check(a.interval(lo,hi)[0]>0,label+' eigenvalue positive')
rstar=-lin/(2*(aR+6*bR));C4=const-6*lin*lin/(4*(aR+6*bR))
pred=P(C4)+sum((a*a for a in t),P())*aT+St*St*bT
pred+=sum(((a-rstar)**2 for a in r),P())*aR+(Sr-6*rstar)**2*bR
check(cost==pred,'complete square and unique finite minimizer')
values={j:0 for j in range(6)};values.update({j:rstar for j in range(6,12)})
mstar=ms.at(values);thstar=ths.at(values)
bs=[a.at(values) for a in R4]
nstar=(-bs[0]*dd+bs[1]*bb)/det
phstar=(-aa*bs[1]+cc*bs[0])/det
values.update({12:mstar,13:thstar,14:nstar,15:phstar,16:0,17:0})
check(objective.a[4].at(values)==C4,'finite minimizing fourth objective')
for a in R4:check(a.at(values)==0,'finite minimizing fourth active tangency')
check(aR==F(1,2) and bR==F(1,4),'real block coefficients independently identified')
stage('full cost positive, unique minimizer and fourth normals solved')

record={'status':'exact full twelve-tangent fourth cost; analytic completeness is in PROOF.md',
    'agent':'six-sendov-3','role':'researcher','source_arithmetic_commit':'52a408f210846d246b5c8dfd890cc142d480d2c4',
    'checks':checks,'eta_order':CAP,'parameter_count':N,
    'generic_polynomial_terms':[sum(len(p.a) for p in j.values()) for j in jets],
    'cost_terms':len(cost.a),'cost_hash':cost.digest(),'full_cost':cost.record(),
    'constants':{k:a.record() for k,a in [('C4',C4),('cost_at_origin',const),('real_linear',lin),
        ('aT',aT),('bT',bT),('aR',aR),('bR',bR),('rstar',rstar),
        ('nu_zero',W/8+rstar),('nu_pair',W/8-3*rstar),('mstar',mstar),
        ('theta_star',thstar),('nstar',nstar),('phi_star',phstar)]},
    'cubic_repairs':{'m':ms.record(),'theta':ths.record()},
    'embedding_interval':[str(lo),str(hi)],
    'normal_response_determinant':det.record(),
    'limiting_real_polynomial_jets':[[[z,a.at(values).record()] for z,a in sorted(j.items())] for j in jets],
    'trust_boundary':'finite exact identities; uniform analytic bridges are ordinary proof'}
