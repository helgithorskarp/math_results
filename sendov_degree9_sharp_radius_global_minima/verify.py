#!/usr/bin/env python3
"""Exact coefficient certificate; analytic completeness is in PROOF.md.

Sparse Gaussian/Laurent arithmetic adapts six-reviewer-1's public audit
kernel (source2901643, with credit); the unbalanced secular/word-trace
calculation is performed here, with no parent executable or fixture import.
The eleven quoted coefficient targets retain six-reviewer-3/7707 credit.
"""
import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction as Q
from pathlib import Path

NAMES = ('s','v','x','Y','A','I','X2','Y2','XY','XY2','Y3','Y4',
         'theta','m','r','R','mu2','mu3','mu4','Psi','X','eta',
         'Delta','Gamma','a','i')
NV = len(NAMES)
ZERO = (0,) * NV
checks, signs, damages = [], [], []
records = {}

class P:
    def __init__(self, terms=None):
        if isinstance(terms, (int,Q)):
            terms = {ZERO: Q(terms)}
        self.d = {k: Q(v) for k,v in (terms or {}).items() if v}
    def __add__(self,b):
        b=as_p(b); d=self.d.copy()
        for k,v in b.d.items(): d[k]=d.get(k,Q(0))+v
        return P(d)
    __radd__=__add__
    def __neg__(self): return P({k:-v for k,v in self.d.items()})
    def __sub__(self,b): return self+-as_p(b)
    def __rsub__(self,b): return as_p(b)+-self
    def __mul__(self,b):
        b=as_p(b); d={}
        for k,v in self.d.items():
            for l,w in b.d.items():
                m=tuple(a+c for a,c in zip(k,l))
                if m[0]>4: continue
                js=m[-1]; m=m[:-1]+(js%2,)
                value=v*w*(-1 if (js//2)%2 else 1)
                d[m]=d.get(m,Q(0))+value
        return P(d)
    __rmul__=__mul__
    def __pow__(self,n):
        if not isinstance(n,int) or n<0: raise ValueError('nonnegative exponent required')
        out=P(1)
        for _ in range(n): out=out*self
        return out
    def __truediv__(self,b): return self*inverse(as_p(b))
    def conj(self): return P({k:(-v if k[-1] else v) for k,v in self.d.items()})
    def real(self): return P({k:v for k,v in self.d.items() if not k[-1]})
    def imag(self): return P({k[:-1]+(0,):v for k,v in self.d.items() if k[-1]})
    def coef(self,n): return P({(0,)+k[1:]:v for k,v in self.d.items() if k[0]==n})
    def wire(self):
        return {'terms':[[[[n,e] for n,e in zip(NAMES,k) if e],
                          [v.numerator,v.denominator]] for k,v in sorted(self.d.items())]}

def as_p(x): return x if isinstance(x,P) else P(x)
def var(name,power=1):
    k=[0]*NV; k[NAMES.index(name)]=power
    return P({tuple(k):Q(1)})
def inverse(a):
    a0=P({k:v for k,v in a.d.items() if not k[0]})
    if len(a0.d)!=1: raise ValueError('series inverse requires monomial constant')
    k,c=next(iter(a0.d.items()))
    kk=tuple(-e for e in k[:-1])+(k[-1],)
    ainv=P({kk:Q(-1 if k[-1] else 1)/c})
    z=(a-a0)*ainv
    if any(not k[0] for k in z.d): raise ValueError('nonpositive valuation')
    return ainv*sum(((-z)**j for j in range(5)),P())
def equal(name,a,b):
    if (as_p(a)-b).d: raise RuntimeError(name+' mismatch '+json.dumps((as_p(a)-b).wire()))
    checks.append(name)
def record(name,value):
    if name in records: raise RuntimeError('duplicate record '+name)
    records[name]=wire(value)
def positive(name,value):
    ok=value.sign()>0 if isinstance(value,Field) else Q(value)>0
    if not ok: raise RuntimeError('nonpositive '+name)
    signs.append(name); record('positive '+name,value)
def damaged(name,a,b):
    difference=as_p(a)-b
    if not difference.d: raise RuntimeError('damaged expression was accepted: '+name)
    damages.append(name); record('rejected '+name,difference)
def wire(value):
    if isinstance(value,P): return value.wire()
    if isinstance(value,Field): return {'rational':wire(value.p),'sqrt1614':wire(value.q)}
    if isinstance(value,(int,Q)): return [Q(value).numerator,Q(value).denominator]
    if isinstance(value,dict): return {str(k):wire(v) for k,v in sorted(value.items())}
    if isinstance(value,(list,tuple)): return [wire(v) for v in value]
    if isinstance(value,str): return value
    raise TypeError(type(value).__name__)

class Field:
    """Q(sqrt1614), with the positive real radical and exact signs."""
    def __init__(self,p=0,q=0): self.p,self.q=Q(p),Q(q)
    def __add__(self,b):
        b=b if isinstance(b,Field) else Field(b)
        return Field(self.p+b.p,self.q+b.q)
    __radd__=__add__
    def __neg__(self): return Field(-self.p,-self.q)
    def __sub__(self,b): return self+- (b if isinstance(b,Field) else Field(b))
    def __rsub__(self,b): return Field(b)+-self
    def __mul__(self,b):
        b=b if isinstance(b,Field) else Field(b)
        return Field(self.p*b.p+1614*self.q*b.q,self.p*b.q+self.q*b.p)
    __rmul__=__mul__
    def __pow__(self,n):
        if not isinstance(n,int) or n<0: raise ValueError('nonnegative field power')
        out=Field(1)
        for _ in range(n):out=out*self
        return out
    def __truediv__(self,b):
        b=b if isinstance(b,Field) else Field(b)
        norm=b.p*b.p-1614*b.q*b.q
        if not norm: raise ZeroDivisionError('zero field norm')
        return self*Field(b.p/norm,-b.q/norm)
    def sign(self):
        if not self.q:return (self.p>0)-(self.p<0)
        if not self.p:return (self.q>0)-(self.q<0)
        if self.p*self.q>0:return (self.p>0)-(self.p<0)
        comparison=self.p*self.p-1614*self.q*self.q
        if not comparison: return 0
        return ((self.p>0)-(self.p<0))*((comparison>0)-(comparison<0))

s,v,x,Y,A,I,X2,Y2,XY,XY2,Y3,Y4,th,m,r,R,mu2,mu3,mu4,psi,X,eta,Delta,Gamma,a,ii=(var(n) for n in NAMES)
d=var('v',-1)

def aggregate_unbalanced(poly):
    moments={(0,0):8,(1,0):A,(0,1):I,(2,0):X2,(0,2):Y2,
             (1,1):XY,(1,2):XY2,(0,3):Y3,(0,4):Y4}
    jx,jy=NAMES.index('x'),NAMES.index('Y');out=P()
    for k,c in poly.d.items():
        pair=k[jx],k[jy]
        if pair not in moments:raise RuntimeError('unretained point moment '+str(pair))
        kk=list(k);kk[jx]=kk[jy]=0
        out=out+P({tuple(kk):c})*moments[pair]
    return out

def aggregate_circle(poly):
    jt,jr=NAMES.index('theta'),NAMES.index('r');out=P()
    for k,c in poly.d.items():
        exponent,rad=k[jt],k[jr];kk=list(k);kk[jt]=kk[jr]=0
        if rad:
            if rad!=1 or exponent:raise RuntimeError('unretained radial point monomial')
            factor=R
        elif exponent==0:factor=8
        elif exponent==1:continue
        elif exponent in (2,3,4):factor={2:mu2,3:mu3,4:mu4}[exponent]
        else:raise RuntimeError('unretained circle moment')
        out=out+P({tuple(kk):c})*factor
    return out

def word_trace(power,powers):
    """All 2^power words in D+u1^T; cyclic run identity is universal."""
    out=P()
    for word in itertools.product((0,1),repeat=power):
        if not any(word):out=out+powers[power];continue
        start=word.index(1)
        rotated=word[start:]+word[:start]
        runs=[];run=0
        for letter in rotated[1:]+(1,):
            if letter:runs.append(run+1);run=0
            else:run+=1
        term=P(1)
        for length in runs:term=term*powers[length]
        out=out+term
    return out

def traces_and_near(u,aggregate,prefix):
    powers={k:aggregate(u**k) for k in range(1,5)}
    qf=9*v
    for degree in range(1,5):
        residual=aggregate(u/(qf-u))-1
        qf=qf+8*v*residual.coef(degree)*s**degree
    equal(prefix+' far secular equation',aggregate(u/(qf-u)),1)
    p1,p2,p3,p4=(powers[k] for k in range(1,5))
    quoted={1:2*p1,2:p1**2+3*p2,3:p1**3+3*p1*p2+4*p3,
            4:p1**4+4*p1**2*p2+2*p2**2+4*p1*p3+5*p4}
    traces={0:P(8)}
    for k in range(1,5):
        traces[k]=word_trace(k,powers)
        equal(prefix+' full cyclic word trace '+str(k),traces[k],quoted[k])
    near={}
    for k in range(1,5):
        shifted=sum((Q(math.comb(k,j))*(-v)**(k-j)*traces[j]
                     for j in range(k+1)),P())
        near[k]=shifted-(qf-v)**k
        record(prefix+' near moment '+str(k),near[k])
    record(prefix+' far jet',qf)
    return powers,qf,near

# Weighted real x degree2, imaginary Y degree1; all joint moments symbolic.
u=v+x*s**2+ii*Y*s
powers,qfar,near=traces_and_near(u,aggregate_unbalanced,'unbalanced')
lower=2*A*s**2-near[2].real()/(2*v)+near[3].real()/(6*v**2)-near[4].real()/(8*v**3)+near[1].real()**2/(14*v)
energy=Y2*s**2+X2*s**4
quartic=lower-2*A*s**2-Q(3,8)*d*energy-I**2/(128*v)*s**2
equal('unbalanced degree two removed',quartic.coef(2),0)
equal('unbalanced odd coefficient one',lower.coef(1),0)
equal('unbalanced odd coefficient three',lower.coef(3),0)
targets=[('Y4',-Q(59,512)*d**3,Y4,Q(59,64)),
         ('XY2',-Q(47,64)*d**2,XY2,Q(47,16)),
         ('Y2^2',-Q(83,14336)*d**3,Y2**2,Q(83,1792)),
         ('X2',-Q(3,4)*d,X2,Q(3,2)),
         ('I Y3',-Q(59,4096)*d**3,I*Y3,Q(177,512)),
         ('I XY',Q(7,128)*d**2,I*XY,Q(21,32)),
         ('I^2 Y2',Q(1277,229376)*d**3,I**2*Y2,Q(1277,3584)),
         ('I^4',-Q(677,1835008)*d**3,I**4,Q(677,3584)),
         ('A Y2',Q(23,512)*d**2,A*Y2,Q(23,128)),
         ('A I^2',-Q(1,128)*d**2,A*I**2,Q(1,4)),
         ('A^2',Q(3,64)*d,A**2,Q(3,32))]
quoted=sum((c*monomial for name,c,monomial,bound in targets),P())
equal('all eleven unbalanced coefficients',quartic,quoted*s**4)
record('full unbalanced lower functional',lower)
record('full eleven coefficient polynomial',quartic.coef(4))
record('eleven absolute coefficient majorants',{name:bound for name,c,monomial,bound in targets})
bound=sum((bound for name,c,monomial,bound in targets),Q(0))
if bound!=Q(26795,3584):raise RuntimeError('majorant sum differs')
positive('quartic majorant slack below eight',8-bound)
record('quartic majorant sum',bound)
equal('comparison-driven real coordinate completion',1-a**2+(1+a)*(a-Q(5,8))/2,
      Q(361,512)-(a-Q(3,16))**2/2)
positive('real coordinate slack below one',1-Q(489,512))
record('real coordinate upper after B E<=1/2',Q(489,512))

# Complete nonlinear mean/inward quartic, independently reconstructed by words.
phase=s*th+s**2*m
exponential=sum(((ii*phase)**k/Q(math.factorial(k)) for k in range(5)),P())
denominator=d+(1-s**4*r)*exponential-1
uc=inverse(denominator)
equal('literal original reciprocal inverse',uc*denominator,1)
pc,qfc,nc=traces_and_near(uc,aggregate_circle,'circle mean radial')
c2=v**2/2-v**3;cR=c2+9*v**3/8
real_square=c2**2*(mu4/2+mu2**2/32)+2*c2*cR*(mu4/8-mu2**2/64)+cR**2*psi
ec=aggregate_circle((uc-v)*(uc-v).conj())
far_loss=qfc.imag().coef(2)**2/(18*v)*s**4
Fjet=2*pc[1].real()-16*v-nc[2].real()/(2*v)+real_square/(2*v)*s**4+nc[3].real()/(6*v**2)-nc[4].real()/(8*v**3)+far_loss
kappa=d**2-Q(13,8)*d
Ac=(48*d**5-40*d**4-53*d**3)/512
Bc=(16*d**5-104*d**4+203*d**3)/8192
Cc=(16*d**5+8*d**4+d**3)/8192
want=(-v**8*Ac*mu4-v**8*Bc*mu2**2+64*v**8*Cc*psi+5*v**3*m**2+2*v**2*R)*s**4
equal('complete mean inward angular coefficient',Fjet-kappa*ec,want)
equal('far mean modulus loss',far_loss,Q(9,2)*v**3*m**2*s**4)
record('complete mean inward angular quartic',(Fjet-kappa*ec).coef(4))
record('full circle energy jet',ec)
record('near real square limiting expression',real_square)
record('far mean modulus loss',far_loss)
K1=(516*d**5-528*d**4-393*d**3)/7168
Sg=(2768*d**5-2456*d**4-3187*d**3)/30720
X0=Q(43,56)-Delta
eta0=(56*X0-13)/30+Gamma
equal('sharp all radius angular deficit',K1-(Ac*X0+Bc-Cc*eta0),Sg*Delta+Cc*Gamma)
record('angular gap factor',Sg)
record('K1',K1)

# Exact domain signs and positive shifted angular-gap coefficients.
ag=Field(Q(-385,692),Q(20,692))
PG=lambda z:2768*z**2+3080*z-2875
if PG(ag).sign():raise RuntimeError('aG is not a root')
record('aG',ag)
record('PG(aG)',PG(ag))
positive('aG above151/250',ag-Q(151,250))
positive('aG below5/8',Field(Q(5,8))-ag)
positive('L numerator at151/250',1616*Q(151,250)**2+1800*Q(151,250)-1675)
equal('L monotonic derivative positive decomposition',-4848*(1-a)**2-3968*(1-a)+10175,
      1359+8816*a+4848*a*(1-a))
positive('L derivative floor',1359)
shifted={k:Field(0) for k in range(1,6)}
for j in range(4):
    pref=Q(math.comb(3,j),30720)*(1+ag)**(3-j)
    shifted[j+1]=shifted[j+1]+pref*(5536*ag+3080)
    shifted[j+2]=shifted.get(j+2,Field(0))+pref*2768
for k in range(1,6):positive('S(aG+q) coefficient degree'+str(k),shifted[k])
record('S(aG+q) positive polynomial coefficients',shifted)
for q in (Q(0),Q(1,16),Q(1,8),Q(1,4),Q(1,2),Q(1)):
    computed=sum((shifted[k]*q**k for k in range(1,6)),Field(0))
    direct=(1+ag+q)**3*PG(ag+q)/30720
    if (computed-direct).sign():raise RuntimeError('degree-five shifted gap identity differs')
    checks.append('degree-five shifted gap exact control '+str(q))
    record('degree-five shifted gap control '+str(q),computed)
# Both expressions have degree at most five; these six distinct exact
# points also give a complete scalar polynomial identity control.
positive('global angular rounding coefficient',Q(1,125))
# The global rounding implication uses Delta>=1/100 and dist^2<=5/4:
if Q(1,125)*Q(5,4)!=Q(1,100):raise RuntimeError('global rounding cutoff mismatch')
record('global angular distance coefficient',Q(1,125))
positive('radial coarse half cost',Q(1,4))
positive('mean coarse half cost',Q(5,16))

# Literal Gaussian matrix traces, with a separate integer backend.
def ga(a,b):return a[0]+b[0],a[1]+b[1]
def gm(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def gs(values):
    z=(0,0)
    for a in values:z=ga(z,a)
    return z
def gp(a,n):
    z=(1,0)
    for _ in range(n):z=gm(z,a)
    return z
def scale(a,n):return n*a[0],n*a[1]
def mm(a,b):return [[gs(gm(a[i][k],b[k][j]) for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
literal_count=0
for n in (1,2,3,8):
    for seed in range(3):
        us=[((j+2)*(seed+1)-3,(2*j+seed)%5-2) for j in range(n)]
        mat=[[scale(us[i],1+(i==j)) for j in range(n)] for i in range(n)]
        power=[[(int(i==j),0) for j in range(n)] for i in range(n)]
        ps={k:gs(gp(z,k) for z in us) for k in range(1,5)}
        p1,p2,p3,p4=(ps[k] for k in range(1,5))
        ts=[scale(p1,2),ga(gp(p1,2),scale(p2,3)),
            gs([gp(p1,3),scale(gm(p1,p2),3),scale(p3,4)]),
            gs([gp(p1,4),scale(gm(gp(p1,2),p2),4),scale(gp(p2,2),2),scale(gm(p1,p3),4),scale(p4,5)])]
        for k in range(1,5):
            power=mm(power,mat)
            got=gs(power[j][j] for j in range(n))
            if got!=ts[k-1]:raise RuntimeError('literal word trace mismatch')
            literal_count+=1
record('literal Gaussian trace control count',literal_count)

# Full eight-coordinate basis establishes every linear compression entry.
q7=[[Q(int(i==j))-Q(1,7) for j in range(7)] for i in range(7)]
nvec=[Q(7)]+[Q(-1)]*7; fvec=[Q(1)]*8
def matmul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Q(0)) for j in range(len(b[0]))] for i in range(len(a))]
def row_times(row,mat):return [sum((row[i]*mat[i][j] for i in range(len(row))),Q(0)) for j in range(len(mat[0]))]
def matrix_equal(name,left,right):
    if left!=right:raise RuntimeError('linear compression mismatch '+name)
    checks.append(name)
embed=[[Q(0)]*7]+q7
left=q7
compression_count=0
for basis in range(8):
    us=[Q(int(j==basis)) for j in range(8)]
    N=[[us[i]*(1+int(i==j)) for j in range(8)] for i in range(8)]
    block=matmul(N,embed)
    nc=matmul(N,[[nvec[j],fvec[j]] for j in range(8)])
    ub=us[1:];u0=sum(ub,Q(0))/7;ua=us[0]
    An=matmul(q7,block[1:])
    Aw=matmul(matmul(q7,[[ub[i]*int(i==j) for j in range(7)] for i in range(7)]),q7)
    matrix_equal('compression basis'+str(basis)+' A',An,Aw)
    Bt=matmul(q7,nc[1:]);qu=[sum((q7[i][j]*ub[j] for j in range(7)),Q(0)) for i in range(7)]
    matrix_equal('compression basis'+str(basis)+' B',Bt,[[-z,9*z] for z in qu])
    Dt=[row_times([z/56 for z in nvec],block),row_times([z/8 for z in fvec],block)]
    uq=[sum((ub[j]*q7[j][i] for j in range(7)),Q(0)) for i in range(7)]
    matrix_equal('compression basis'+str(basis)+' D',Dt,[[-z/56 for z in uq],[z/8 for z in uq]])
    Ct=[row_times([z/56 for z in nvec],nc),row_times([z/8 for z in fvec],nc)]
    matrix_equal('compression basis'+str(basis)+' C',Ct,[[(7*ua+u0)/8,9*(ua-u0)/8],[7*(ua-u0)/8,9*(ua+7*u0)/8]])
    compression_count+=1
record('linear compression complete coordinate basis count',compression_count)
c0=-ii*v**2
kn=Q(1,392);kf=-c0/(56*v)
equal('near graph row cancellation',-c0/56+7*c0*kn,0)
equal('far graph row cancellation',c0/8+7*c0*kn+8*v*kf,0)
equal('normalized leading graph shear',-c0*kn/c0,-Q(1,392))
record('leading graph kn scalar',kn)
record('leading graph kf scalar',kf)

# Mutations are mathematical failures, distinct from fixture corruption.
damaged('alter one unbalanced quartic basis coefficient',quartic,quoted*s**4+d**3*Y2**2*s**4/14336)
damaged('omit leading reciprocal mean cost',lower,lower-I**2*s**2/(128*v))
damaged('omit far nonlinear mean modulus loss',Fjet-far_loss-kappa*ec,want)
damaged('halve independent inward cost',Fjet-kappa*ec,want-v**2*R*s**4)
damaged('replace mean cost by nine halves',Fjet-kappa*ec,want-v**3*m**2*s**4/2)
damaged('replace real-coordinate upper bound by one half',P(Q(489,512)),Q(1,2))
damaged('wrong fine graph far denominator64',c0/8+7*c0*kn+8*v*(-c0/(64*v)),0)
damaged('omit sharp angular Gamma',K1-(Ac*X0+Bc-Cc*eta0),Sg*Delta)

record('mathematical damage names',damages)
record('checked identity names',checks)
record('strict sign names',signs)
encoded=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
payload={'schema':'sendov-sharp-radius-global-v1','agent':'six-sendov-3','role':'researcher',
         'status':'exact algebra/sign certificate; analytic bridges are in PROOF.md',
         'identity_count':len(checks),'strict_sign_count':len(signs),
         'literal_gaussian_trace_count':literal_count,'linear_compression_basis_count':compression_count,
         'unbalanced_quartic_basis_count':len(targets),'damaged_math_count':len(damages),
         'record_count':len(records),'record_sha256':hashlib.sha256(encoded).hexdigest(),
         'records':records}
parser=argparse.ArgumentParser()
parser.add_argument('--write-fixture',type=Path)
parser.add_argument('--check',type=Path,default=Path(__file__).with_name('expected.json'))
args=parser.parse_args()
if args.write_fixture:
    if args.write_fixture.exists():raise RuntimeError('refuse to overwrite existing complete fixture')
    args.write_fixture.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
else:
    expected=json.loads(args.check.read_text())
    if expected!=payload:raise RuntimeError('complete expected fixture differs')
print(json.dumps({k:v for k,v in payload.items() if k!='records'},sort_keys=True))
