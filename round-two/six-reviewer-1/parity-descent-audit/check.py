#!/usr/bin/env python3
"""six-reviewer-1: independent exact corroboration of committed10105.
Companion traces and changing quotient rings, no author executable/CAS.
Ordinary universal positivity/hyperbolicity/chart proofs remain in REVIEW.md.
"""
from fractions import Fraction as F
import json, sys, signal
from itertools import product
signal.alarm(45)

def require(ok, name):
    if not ok: raise ValueError(name)

class P:
    """Sparse Q[E,G,J], exponent triples."""
    def __init__(self, a=0):
        self.a={k:F(v) for k,v in a.items() if v} if isinstance(a,dict) else ({(0,0,0):F(a)} if a else {})
    def __add__(self,b):
        b=b if isinstance(b,P) else P(b); c=dict(self.a)
        for k,v in b.a.items(): c[k]=c.get(k,F(0))+v
        return P(c)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.a.items()})
    def __sub__(self,b):return self+-castp(b)
    def __rsub__(self,b):return castp(b)+-self
    def __mul__(self,b):
        b=castp(b);c={}
        for k,v in self.a.items():
            for l,w in b.a.items():
                t=tuple(k[i]+l[i] for i in range(3));c[t]=c.get(t,F(0))+v*w
        return P(c)
    __rmul__=__mul__
    def __truediv__(self,b):return self*F(1,b)
    def __eq__(self,b):return self.a==castp(b).a
    def diff(self,i):
        c={}
        for k,v in self.a.items():
            if k[i]: l=list(k);l[i]-=1;c[tuple(l)]=v*k[i]
        return P(c)
    def at(self,p):return sum((v*product_value(p,k) for k,v in self.a.items()),F(0))
    def record(self):return [[*k,str(v)] for k,v in sorted(self.a.items())]
def castp(v):return v if isinstance(v,P) else P(v)
def product_value(p,k):
    r=F(1)
    for x,n in zip(p,k):r*=x**n
    return r
E=P({(1,0,0):1});G=P({(0,1,0):1});J=P({(0,0,1):1})

class Jet:
    """Four simultaneous exact first derivatives: E,G,J,c."""
    def __init__(self,v=0,d=None):self.v=F(v);self.d=tuple(map(F,d)) if d is not None else (F(0),)*4
    def __add__(self,b):
        b=jet(b);return Jet(self.v+b.v,[a+c for a,c in zip(self.d,b.d)])
    __radd__=__add__
    def __neg__(self):return Jet(-self.v,[-x for x in self.d])
    def __sub__(self,b):return self+-jet(b)
    def __rsub__(self,b):return jet(b)+-self
    def __mul__(self,b):
        b=jet(b);return Jet(self.v*b.v,[x*b.v+self.v*y for x,y in zip(self.d,b.d)])
    __rmul__=__mul__
    def __truediv__(self,b):
        b=jet(b);require(b.v!=0,'nonzero dual denominator')
        return Jet(self.v/b.v,[(x*b.v-self.v*y)/b.v**2 for x,y in zip(self.d,b.d)])
    def __rtruediv__(self,b):return jet(b)/self
    def __eq__(self,b):b=jet(b);return self.v==b.v and self.d==b.d
    def record(self):return {'value':str(self.v),'derivatives':list(map(str,self.d))}
def jet(v):return v if isinstance(v,Jet) else Jet(v)
def var(v,i):return Jet(v,[int(i==j) for j in range(4)])
def primary(v):return v.v if isinstance(v,Jet) else v

# Independent matrix representation; companion action columns = z*z^j modulo h.
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),0) for j in range(len(b[0]))] for i in range(len(a))]
def trace(a):return sum((a[i][i] for i in range(len(a))),0)
def eye(n):return [[F(int(i==j)) for j in range(n)]for i in range(n)]
def companion(h):
    n=len(h)-1;require(h[-1]==1,'monic modulus');a=[[0]*n for _ in range(n)]
    for j in range(n-1):a[j+1][j]=1
    for i in range(n):a[i][-1]=-h[i]
    return a
def companion_traces(h,n):
    c=companion(h);a=eye(len(h)-1);out=[trace(a)]
    for _ in range(n):a=mm(a,c);out.append(trace(a))
    return out

def solve(a,b):
    n=len(b);r=[list(a[i])+[b[i]]for i in range(n)]
    for k in range(n):
        j=next((j for j in range(k,n)if primary(r[j][k])!=0),None)
        require(j is not None,'nonsingular linear system');r[k],r[j]=r[j],r[k]
        pivot=r[k][k];r[k]=[x/pivot for x in r[k]]
        for i in range(n):
            if i!=k:
                v=r[i][k];r[i]=[x-v*y for x,y in zip(r[i],r[k])]
    return [r[i][-1]for i in range(n)]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),0)
def mv(a,v):return [dot(r,v)for r in a]
def transpose(a):return list(map(list,zip(*a)))

# Univariate coefficients low to high; changing quotient ring includes root motion.
def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return p
def add(a,b):return trim([(a[i]if i<len(a)else 0)+(b[i]if i<len(b)else 0)for i in range(max(len(a),len(b)))])
def neg(a):return [-x for x in a]
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def divmodp(a,b):
    a=trim(a);b=trim(b);require(b!=[0],'polynomial divisor');q=[0]*max(1,len(a)-len(b)+1)
    while a!=[0]and len(a)>=len(b):
        i=len(a)-len(b);v=a[-1]/b[-1];q[i]+=v
        a=add(a,neg([0]*i+[v*x for x in b]))
    return trim(q),a
def rem(a,h):return divmodp(a,h)[1]
def der(a):return trim([i*a[i]for i in range(1,len(a))])
def qmul(a,b,h):return rem(mul(a,b),h)
def qtrace(p,h):
    t=companion_traces(h,len(p)-1);return dot(p,t)
def square_mass(f,h):
    n=len(h)-1;hp=der(h);columns=[]
    for i in range(n):columns.append(rem([0]*i+hp,h)+[0]*n)
    a=[[columns[j][i]for j in range(n)]for i in range(n)]
    rhs=rem([-8*x for x in f],h);rhs+= [0]*(n-len(rhs))
    p=solve(a,rhs);return qtrace(qmul(p,p,h),h),p

def sturm_count(p):
    p=trim(list(map(F,p)));seq=[p,der(p)]
    while seq[-1]!=[0]:
        r=neg(divmodp(seq[-2],seq[-1])[1])
        if r==[0]:break
        seq.append(r)
    def variations(positive):
        signs=[]
        for q in seq:
            v=q[-1]if positive else q[-1]*(-1)**(len(q)-1)
            if v:signs.append(1 if v>0 else -1)
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return variations(False)-variations(True)
def pencil(e,g,j,c):return [c,8*j,4*g,0,2*e,0,-F(1,2),0,F(1)], [j,g,0,e,0,-F(3,8),0,F(1)]
def center(e,g,j):
    _,h=pencil(e,g,j,F(0));t=companion_traces(h,11);nu=[F(1),F(0),F(3,8)-8*e,F(0),F(9,64)-4*e-24*g,-56*j]
    m=[[t[i+k]for k in range(6)]for i in range(6)];beta=solve(m,nu)
    c=(F(27,512)-F(15,8)*e+8*e*e-10*g-dot(beta,t[6:12]))/8
    return c,t,nu,m,beta

# Whole coefficient identities via companion powers (no Newton implementation).
f,h=pencil(E,G,J,P(0));tau=companion_traces(h,11)
written=[7,0,F(3,4),0,F(9,32)-4*E,0,F(27,256)-F(9,4)*E-6*G,-7*J,
 F(81,2048)-F(9,8)*E+4*E*E-3*G,-F(27,8)*J,
 F(243,16384)-F(135,256)*E+F(15,4)*E*E-F(45,32)*G+10*E*G,
 11*E*J-F(99,64)*J]
for i,(a,b)in enumerate(zip(tau,written)):require(a==b,'whole trace '+str(i))
# Original-power chart checked by a DIFFERENT degree-eight companion action.
original_mu=companion_traces(f,7)
for exponent,value in [(1,0),(2,1),(3,0),(4,F(1,2)-8*E),(5,0),(7,-56*J)]:
    require(original_mu[exponent]==value,'whole original normalization/moment '+str(exponent))
# Expand resolvent numerator/h at infinity; c first appears in moment6.
c=P(0);numerator=[-8*c,-56*J,-24*G,0,-8*E,0,P(1)]
series=[]
for k in range(7):
    n=numerator[6-k]if k<7 else 0
    series.append(n-sum((h[7-r]*series[k-r]for r in range(1,min(k,7)+1)),0))
nu_written=[1,0,F(3,8)-8*E,0,F(9,64)-4*E-24*G,-56*J,F(27,512)-F(15,8)*E+8*E*E-10*G]
for i,(a,b)in enumerate(zip(series,nu_written)):require(a==b,'whole resolvent moment '+str(i))
order=[0,2,4,1,3,5];gram=[[tau[i+j]for j in range(6)]for i in range(6)]
u_coupling=[[0,0,0],[0,0,-7],[0,-7,-F(27,8)]]
for i in range(3):
    for j in range(3):
        require(gram[order[i]][order[j+3]]==J*u_coupling[i][j],'complete cross parity block')
        require(castp(gram[order[i]][order[j]]).diff(2)==0,'even block J independent')
        require(castp(gram[order[i+3]][order[j+3]]).diff(2)==0,'odd block J independent')
# Eliminated first two normal equations imply the full mismatch polynomial.
a=F(3,4);b=castp(tau[4]);t=castp(tau[6]);d=F(3,8)-8*E;k=b-a*a/7;ell=t-a*b/7
require(d-a/7-8*k==-3*(d+F(1,14)),'exact mismatch normal-equation elimination')
q1=ell/7-F(27,392)*k
require(q1==t/7-F(33,392)*b+F(243,43904),'refined q1 identity')
# Correlated bound t<=a*b and the exact b bound; strict rational budget.
low=-F(33,392)*F(9,16)+F(243,43904)
high=(a/7-F(33,392))*F(9,16)+F(243,43904)
require(low==-F(459,10976)and high==F(405,21952),'q1 endpoints')
qnorm=low*low+F(27,392)**2;traceB=a+a**3+a**5
require(qnorm==F(782217,120472576)and traceB==F(1443,1024),'whole rational budget')
require(qnorm*traceB<F(1,100),'strict H>900 budget')
require(F(900)*F(2,7)>256 and F(900)*F(2,7)/4>64,'integral and actual-gradient strengthening')

# Own deterministic controls: bounded exact selection of a feasible centered even spectrum.
trials=0;chosen=None
for r1 in range(1,10):
    for r2 in range(r1+1,15):
        r3=30-r1-r2
        if r3<=r2:continue
        trials+=1
        if trials>80:raise ValueError('bounded control selection exhausted (not nonexistence)')
        r=list(map(lambda x:F(x,80),[r1,r2,r3]));e=r[0]*r[1]+r[0]*r[2]+r[1]*r[2];g=-r[0]*r[1]*r[2]
        c,*_=center(e,g,F(0));ff,hh=pencil(e,g,F(0),c)
        if sturm_count(ff)==8:chosen=(e,g);break
    if chosen is not None:break
require(chosen is not None,'no feasible control (bounded search, no universal inference)')
controls=[]
for j in [F(0),F(1,10**7),-F(1,10**7)]:
    e,g=chosen;c,tr,nu,m,beta=center(e,g,j);ff,hh=pencil(e,g,j,c)
    require(sturm_count(ff)==8 and sturm_count(hh)==7,'actual centered control reality')
    variables=[var(x,i)for i,x in enumerate([e,g,j,c])];fd,hd=pencil(*variables)
    eta,p=square_mass(fd,hd);D=F(3,8)-8*variables[0];C=(1-eta)/D
    tjet=companion_traces(hd,11);nujet=[jet(1),jet(0),F(3,8)-8*variables[0],jet(0),F(9,64)-4*variables[0]-24*variables[1],-56*variables[2]]
    mj=[[tjet[i+k]for k in range(6)]for i in range(6)];betaj=solve(mj,nujet);bar=(1-dot(nujet,betaj))/D
    require(C==bar,'all four changing-ring center derivatives')
    # Explicit closed reduced gradient, including EVERY moving-node Gram entry.
    grad=[]
    for dim in range(3):
        dn=[castp(x).diff(dim).at([e,g,j])for x in series[:6]]
        dm=[[castp(x).diff(dim).at([e,g,j])for x in row]for row in gram]
        dr=2*dot(beta,dn)-dot(beta,mv(dm,beta))
        grad.append(((8*bar.v if dim==0 else 0)-dr)/(F(3,8)-8*e))
    require(C.d[:3]==tuple(grad)and C.d[3]==0,'complete reduced moving-node gradient')
    # The fully retained Schur identity and x derivative at each control.
    A=[[tr[order[i]+order[k]]for k in range(3)]for i in range(3)]
    B=[[tr[order[i+3]+order[k+3]]for k in range(3)]for i in range(3)]
    y=solve(A,[nu[i]for i in order[:3]]);w=[v-uy for v,uy in zip([0,0,-56],mv(transpose(u_coupling),y))]
    Q=mm(transpose(u_coupling),transpose([solve(A,col)for col in transpose(u_coupling)]))
    S=[[B[i][k]-j*j*Q[i][k]for k in range(3)]for i in range(3)]
    r=dot([nu[i]for i in order[:3]],y)+j*j*dot(w,solve(S,w))
    require(r==dot(nu,beta),'entire Schur value')
    sw=solve(S,w);H=dot(sw,mv(B,sw));dv=F(3,8)-8*e
    require(H>900*(dv+F(1,14))**2,'improved coercivity at control')
    require(C.d[2]==-2*j*H/dv,'Schur J derivative')
    if j:require(j*C.d[2]/8<-64*j*j,'strict signed actual gradient')
    # Freeze only the critical modulus, while differentiating f and h'; deliberately wrong.
    frozenh=[jet(primary(x))for x in hd]
    n=len(hh)-1;cols=[]
    for i in range(n):cols.append(rem([0]*i+der(hd),frozenh)+[0]*n)
    mp=[[cols[k][i]for k in range(n)]for i in range(n)]
    rhs=rem([-8*x for x in fd],frozenh);rhs+=[0]*(n-len(rhs))
    p_frozen=solve(mp,rhs);eta_frozen=qtrace(qmul(p_frozen,p_frozen,frozenh),frozenh)
    frozenC=(1-eta_frozen)/D
    if j:require(frozenC.d[2]!=C.d[2],'reject omitted critical-root motion')
    controls.append({'E':str(e),'G':str(g),'J':str(j),'cstar':str(c),'original_real_roots':8,'critical_real_roots':7,'C':C.record(),'H':str(H),'frozen_J_derivative':str(frozenC.d[2])})
# Exact stated feasibility obstruction, not an inferred continuation of actual originals.
e=F(7,160);g=-F(1,640);c,*_=center(e,g,F(0));require(c==F(1,7040),'center obstruction value')
f0,h0=pencil(e,g,F(0),F(3,20000));fc,_=pencil(e,g,F(0),c)
require(sturm_count(f0)==8 and sturm_count(fc)==4 and sturm_count(h0)==7,'actual/unconstrained obstruction counts')
record={'agent':'six-reviewer-1','role':'independent mathematical reviewer','algorithm':'companion multiplication traces; Q[E,G,J] full coefficient maps; independent changing Q[epsilon_1,...,epsilon_4]/(epsilon_i epsilon_j)[z]/h mass square; exact Sturm controls',
 'trace_polynomials':[castp(x).record()for x in tau],
 'original_moments':[castp(x).record()for x in original_mu],
 'coupling_moments_c0':[castp(x).record()for x in series],
 'gram':[[castp(x).record()for x in row]for row in gram],
 'gram_derivatives':[[[castp(x).diff(dim).record()for x in row]for row in gram]for dim in range(3)],
 'coupling_derivatives':[[castp(x).diff(dim).record()for x in series]for dim in range(3)],
 'improved_budget':{'q1_interval':[str(low),str(high)],'q_norm_square_cap':str(qnorm),'B_trace_cap':str(traceB),'strict_product_below_1_over_100':True,'H_factor':900,'rounded_gradient_factor':64,'rounded_J_square_penalty':256,'mu7_square_penalty':'4/49'},
 'controls':controls,'own_control_selection_trials':trials,
 'feasibility_obstruction':{'actual_c':'3/20000','center_c':str(c),'actual_original_count':8,'center_original_count':4,'critical_count':7},
 'universal_trust_boundary':'Ordinary real Gram/Schur positivity, hyperbolicity continuation, least-squares, local chart and credited even/continuity proofs; finite controls are corroboration, not a universal enumeration or formalization.'}
text=json.dumps(record,sort_keys=True,indent=2)+'\n'
if '--record' in sys.argv:print(text,end='')
else:
    import hashlib
    print(json.dumps({'whole_record_sha256':hashlib.sha256(text.encode()).hexdigest(),'whole_record_bytes':len(text.encode()),'controls':len(controls),'control_trials':trials,'trace_entries':12,'gram_entries':36,'gram_derivative_entries':108,'coupling_entries':7,'coupling_derivative_entries':21,'improved_penalty':'4/49 * mu7^2','ordinary_not_formal':True},sort_keys=True))
