#!/usr/bin/env python3
"""Independent far-root and full-trace derivation; exact Laurent algebra."""
import argparse, hashlib, json, math
from fractions import Fraction as Q

# Q[i][v,v^-1,theta,y,r,R,mu2,mu3,mu4,Psi,s]/(s^5).
NAMES=('s','v','theta','y','r','R','mu2','mu3','mu4','Psi','i')
NV=len(NAMES); ZERO=(0,)*NV; checks=[]; records={}
class P:
    def __init__(self,terms=None):
        if isinstance(terms,(int,Q)):terms={ZERO:Q(terms)}
        self.d={k:Q(v) for k,v in (terms or {}).items() if v}
    def __add__(self,b):
        b=as_p(b);d=self.d.copy()
        for k,v in b.d.items():d[k]=d.get(k,Q(0))+v
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.d.items()})
    def __sub__(self,b):return self+-as_p(b)
    def __rsub__(self,b):return as_p(b)+-self
    def __mul__(self,b):
        b=as_p(b);d={}
        for k,v in self.d.items():
            for l,w in b.d.items():
                m=tuple(a+c for a,c in zip(k,l))
                if m[0]>4:continue
                js=m[-1];m=m[:-1]+(js%2,)
                value=v*w*(-1 if (js//2)%2 else 1)
                d[m]=d.get(m,Q(0))+value
        return P(d)
    __rmul__=__mul__
    def __pow__(self,n):
        if not isinstance(n,int) or n<0:raise ValueError('nonnegative polynomial power required')
        z=P(1)
        for _ in range(n):z=z*self
        return z
    def __truediv__(self,b):return self*inverse(as_p(b))
    def conj(self):return P({k:(-v if k[-1] else v) for k,v in self.d.items()})
    def real(self):return P({k:v for k,v in self.d.items() if not k[-1]})
    def imag(self):return P({k[:-1]+(0,):v for k,v in self.d.items() if k[-1]})
    def coef(self,n):return P({(0,)+k[1:]:v for k,v in self.d.items() if k[0]==n})
    def subvar(self,name,value):
        j=NAMES.index(name);value=as_p(value);out=P()
        for k,v in self.d.items():
            if k[j]<0:raise ValueError('negative substitution degree')
            kk=list(k);power=kk[j];kk[j]=0
            out=out+P({tuple(kk):v})*value**power
        return out
    def wire(self):
        return {'terms':[[[[n,e] for n,e in zip(NAMES,k) if e],[v.numerator,v.denominator]] for k,v in sorted(self.d.items())]}
def as_p(x):return x if isinstance(x,P) else P(x)
def var(name,power=1):
    k=[0]*NV;k[NAMES.index(name)]=power;return P({tuple(k):Q(1)})
def inverse(a):
    a0=P({k:v for k,v in a.d.items() if not k[0]})
    if len(a0.d)!=1:raise ValueError('series inverse requires monomial constant')
    k,c=next(iter(a0.d.items()));kk=tuple(-e for e in k[:-1])+(k[-1],)
    ainv=P({kk:(-1 if k[-1] else 1)/c})
    z=(a-a0)*ainv
    if any(not k[0] for k in z.d):raise ValueError('nonpositive series valuation')
    return ainv*sum(((-z)**j for j in range(5)),P())
def ensure_equal(name,a,b):
    if (as_p(a)-b).d:raise RuntimeError(name+' mismatch '+json.dumps((as_p(a)-b).wire()))
    checks.append(name)
def record(name,p):records[name]=p.wire()
def aggregate(a):
    """Sum point jets: mu1=0, mu0=8, sum r_j=R."""
    out=P();jt=NAMES.index('theta');jr=NAMES.index('r')
    for k,c in a.d.items():
        e=k[jt];rad=k[jr];kk=list(k);kk[jt]=kk[jr]=0
        if rad:
            if rad!=1 or e:raise RuntimeError('unexpected retained radial monomial')
            kk[NAMES.index('R')]+=1
        elif e==0:c*=8
        elif e==1:continue
        elif e in (2,3,4):kk[NAMES.index('mu'+str(e))]+=1
        else:raise RuntimeError('unexpected retained moment')
        out=out+P({tuple(kk):c})
    return out
s,v,th,y,r,R,m2,m3,m4,psi,ii=(var(n) for n in NAMES)
vminus=var('v',-1)
phase=s*th+s*s*y
exponential=sum(((ii*phase)**k/Q(math.factorial(k)) for k in range(5)),P())
u=inverse(vminus+exponential-1-s**4*r*exponential)
delta=u-v
ensure_equal('literal reciprocal inverse',u*(vminus+exponential-1-s**4*r*exponential),1)
c2=v**2/2-v**3;c3=v**2/6-v**3+v**4;c4=-v**2/24+7*v**3/12-3*v**4/2+v**5
ensure_equal('reciprocal jet',delta,-ii*v**2*th*s+(c2*th**2-ii*v**2*y)*s**2+(ii*c3*th**3+2*c2*th*y)*s**3+(c4*th**4+c2*y*y+3*ii*c3*th**2*y+v**2*r)*s**4)
powers={k:aggregate(u**k) for k in range(1,5)}
# Solve the simple far root by the rank-one secular equation, degree by degree.
qfar=9*v
for degree in range(1,5):
    defect=aggregate(u/(qfar-u))-1
    qfar=qfar+8*v*defect.coef(degree)*s**degree
ensure_equal('far secular equation',aggregate(u/(qfar-u)),1)
record('far reciprocal jet',qfar)
# Exact word traces for D + u1^T, derived from cyclic word types.
p1,p2,p3,p4=(powers[k] for k in range(1,5))
traces={0:P(8),1:2*p1,2:p1**2+3*p2,3:p1**3+3*p1*p2+4*p3,4:p1**4+4*p1**2*p2+2*p2**2+4*p1*p3+5*p4}
near={}
for k in range(1,5):
    shifted=sum((Q(math.comb(k,j))*(-v)**(k-j)*traces[j] for j in range(k+1)),P())
    near[k]=shifted-(qfar-v)**k
    record('near shifted moment '+str(k),near[k])
cR=c2+9*v**3/8
square=c2**2*(m4/2+m2**2/32)+2*c2*cR*(m4/8-m2**2/64)+cR**2*psi
energy=aggregate(delta*delta.conj())
ensure_equal('energy jet',energy,v**4*m2*s**2+((c2**2-2*v**2*c3)*m4+8*v**4*y**2)*s**4)
far_loss=qfar.imag().coef(2)**2/(18*v)*s**4
Fjet=2*p1.real()-16*v-near[2].real()/(2*v)+square/(2*v)*s**4+near[3].real()/(6*v**2)-near[4].real()/(8*v**3)+far_loss
kappa=vminus**2-Q(13,8)*vminus
excess=Fjet-kappa*energy
A=(48*vminus**5-40*vminus**4-53*vminus**3)/512
B=(16*vminus**5-104*vminus**4+203*vminus**3)/8192
C=(16*vminus**5+8*vminus**4+vminus**3)/8192
want=(-v**8*A*m4-v**8*B*m2**2+64*v**8*C*psi+5*v**3*y**2+2*v**2*R)*s**4
ensure_equal('complete mean inward spectral quartic',excess,want)
for name,p in [('complete quartic',excess.coef(4)),('near real square',square),('far nonlinear mean loss',far_loss.coef(4)),('energy jet',energy)]:record(name,p)
# Radius-parametric optimizer and range identities, no author fixture read.
x=var('theta'); eta=var('r')
K1=(516*vminus**5-528*vminus**4-393*vminus**3)/7168
S=(2768*vminus**5-2456*vminus**4-3187*vminus**3)/30720
ensure_equal('angular exact deficit',K1-(A*x+B-C*eta),S*(Q(43,56)-x)+C*(eta-(56*x-13)/30))
ensure_equal('four four minimum',A/8+B-C,3*vminus**3*(vminus-1)**2/256)
ensure_equal('singleton maximum',A*Q(43,56)+B-C,K1)
Ktr=(3792*vminus**5-7728*vminus**4+2991*vminus**3)/28672
ensure_equal('true versus trace quartic improvement',Ktr-K1,Q(27,448)*vminus**3*(vminus-Q(13,8))**2)
# Polynomial positivity and exact uniform refinements in a-5/8 >= 0.
q=var('theta');d=Q(13,8)+q
polynomials={
 'S sign polynomial':2768*d**2-2456*d-3187,
 'A sign polynomial':48*d**2-40*d-53,
 'K1 sign polynomial':516*d**2-528*d-393,
 'L numerator':1616*(d-1)**2+1800*(d-1)-1675,
 'L increasing derivative at a=1-q':-4848*(1-q)**2-3968*(1-q)+10175}
for name,p in polynomials.items():record(name,p)
ensure_equal('S shifted sign',polynomials['S sign polynomial'],Q(525,4)+6540*q+2768*q**2)
ensure_equal('A shifted sign',polynomials['A sign polynomial'],Q(35,4)+116*q+48*q**2)
ensure_equal('K1 shifted sign',polynomials['K1 sign polynomial'],Q(1785,16)+1149*q+516*q**2)
ensure_equal('L shifted sign',polynomials['L numerator'],Q(325,4)+3820*q+1616*q**2)
# Derivative numerator on 0<=q<=3/8:1359+13664q-4848q^2.
# Since q<=3/8, it is >=1359+(13664-1818)q>0.
ensure_equal('L derivative certificate',polynomials['L increasing derivative at a=1-q'],1359+13664*q-4848*q**2)
Smin=Q(13,8)**3*Q(525,4)/30720
Cmin=Q(13,8)**3*Q(15,2)**2/8192
Lmin=Q(325,4)/(224*Q(13,8)**5)

# Literal integer Gaussian matrix controls use a separate arithmetic backend.
def ga(a,b):return (a[0]+b[0],a[1]+b[1])
def gm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def gs(values):
    z=(0,0)
    for value in values:z=ga(z,value)
    return z
def gpow(a,n):
    z=(1,0)
    for _ in range(n):z=gm(z,a)
    return z
def gscale(a,n):return (n*a[0],n*a[1])
def gmatrix(a,b):return [[gs(gm(a[i][k],b[k][j]) for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
controls=0
for n in (1,2,3,8):
    for seed in range(3):
        us=[((k+2)*(seed+1)-3,(2*k+seed)%5-2) for k in range(n)]
        mat=[[gscale(us[i],1+(i==j)) for j in range(n)] for i in range(n)]
        power=[[(int(i==j),0) for j in range(n)] for i in range(n)]
        ps={k:gs(gpow(z,k) for z in us) for k in range(1,5)}
        a,b,c,e=(ps[k] for k in range(1,5))
        ts=[gscale(a,2),ga(gpow(a,2),gscale(b,3)),gs([gpow(a,3),gscale(gm(a,b),3),gscale(c,4)]),gs([gpow(a,4),gscale(gm(gpow(a,2),b),4),gscale(gpow(b,2),2),gscale(gm(a,c),4),gscale(e,5)])]
        for k in range(1,5):
            power=gmatrix(power,mat)
            if gs(power[j][j] for j in range(n))!=ts[k-1]:raise RuntimeError('literal Gaussian trace control')
            # Also cross-check the independent sparse Gaussian arithmetic.
            literal=ts[k-1]
            ensure_equal('literal trace n'+str(n)+' seed'+str(seed)+' power'+str(k),sum(((P(z[0])+ii*P(z[1]))**k for z in us),P()),P(ps[k][0])+ii*P(ps[k][1]))
            controls+=1

# Eight full coordinate basis matrices establish every linear compression entry.
nvec=[Q(7)]+[Q(-1)]*7;fvec=[Q(1)]*8
q7=[[Q(int(i==j))-Q(1,7) for j in range(7)] for i in range(7)]
def rmm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def rmv(a,x):return [sum(row[j]*x[j] for j in range(len(x))) for row in a]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
block_controls=0
for coordinate in range(8):
    us=[Q(int(j==coordinate)) for j in range(8)];ub=us[1:];ua=us[0]
    mat=[[us[i]*(1+(i==j)) for j in range(8)] for i in range(8)]
    nf=[nvec,fvec];dual=[ [v/Q(56) for v in nvec],[v/Q(8) for v in fvec] ]
    complement=[[dot(left,rmv(mat,right)) for right in nf] for left in dual]
    wantc=[[(49*ua+sum(ub))/56,9*(7*ua-sum(ub))/56],[(7*ua-sum(ub))/8,9*(ua+sum(ub))/8]]
    if complement!=wantc:raise RuntimeError('complementary compression mismatch')
    b_actual=[rmv(q7,rmv(mat,x)[1:]) for x in nf]
    b_want=[[-z for z in rmv(q7,ub)],[9*z for z in rmv(q7,ub)]]
    if b_actual!=b_want:raise RuntimeError('outgoing compression mismatch')
    a_actual=[];d_actual=[[],[]]
    for j in range(7):
        w=[Q(0)]+[q7[k][j] for k in range(7)];mw=rmv(mat,w)
        a_actual.append(rmv(q7,mw[1:]))
        for k in range(2):d_actual[k].append(dot(dual[k],mw))
    diag=[[ub[i]*int(i==j) for j in range(7)] for i in range(7)]
    wanta=rmm(rmm(q7,diag),q7)
    if a_actual!=[list(col) for col in zip(*wanta)]:raise RuntimeError('core compression mismatch')
    urow=rmv(q7,ub)
    if d_actual!=[[-z/56 for z in urow],[z/8 for z in urow]]:raise RuntimeError('return compression mismatch')
    block_controls+=1
ensure_equal('graph near leading row',-Q(1,56)+7*Q(1,392),0)
ensure_equal('graph far leading row',Q(1,8)+7*Q(1,392)-Q(1,7),0)
ensure_equal('complete Hermitian feedback trace',6*y+6*m2/112-m2/392,6*y+5*m2/98)
rejected=0
for name,a,b in [
 ('missing far mean modulus term',excess-far_loss,want),
 ('missing radial contribution',excess-2*v**2*R*s**4,want),
 ('missing energy correction',Fjet,want),
 ('wrong spectral real-square weight',excess-cR**2*psi/(2*v)*s**4,want),
 ('wrong optimizer slope',(S+1)*(Q(43,56)-x)+C*(eta-(56*x-13)/30),K1-(A*x+B-C*eta))]:
    if not (a-b).d:raise RuntimeError('failed negative-control rejection '+name)
    rejected+=1

def validate_fixture(payload,wanted):
    if payload!=wanted:raise RuntimeError('complete independent expected output mismatch')

def main():
    payload={'schema':'sendov-full-radius-fartrace-review1-v1','agent':'six-reviewer-1','role':'independent mathematical reviewer','status':'COMPLETE exact coefficient derivation; analytic bridges proved separately','algebra':'Q[i][v,v^-1,theta,y,r,R,mu2,mu3,mu4,Psi,s]/(s^5); mu1=0','identity_checks':len(checks),'literal_trace_controls':controls,'full_linear_compression_basis_controls':block_controls,'damaged_math_inputs_rejected':rejected,'records':records,'uniform_refinements':{'S_min':str(Smin),'C_min':str(Cmin),'L_min':str(Lmin),'angular_orbit_cost':str(Smin/125),'coarse_physical_inward_cost':'1/4','coarse_physical_mean_cost':'5/16','coarse_physical_split_cost':str(Lmin/2),'K1_max':'615/896','full_first_power_small_energy':'F>=8+3(1-a)+E/2 with a common existential positive energy threshold'},'author_code_imported':False,'author_fixture_read':False}
    args=argparse.ArgumentParser();args.add_argument('--check');ns=args.parse_args()
    if ns.check:validate_fixture(json.loads(open(ns.check).read()),payload)
    print(json.dumps(payload,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
