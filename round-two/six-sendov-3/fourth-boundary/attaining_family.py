#!/usr/bin/env python3
"""six-sendov-3 researcher: candidate fourth family, all-nine-root eta5 check.

This certifies only the explicit construction, not a universal fourth lower.
"""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import importlib.util,json,time
SOURCE=Path(__file__).with_name('arithmetic.py')
spec=importlib.util.spec_from_file_location('family_arithmetic',SOURCE)
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
p.KORDER=5
K,Z=p.K,p.Z;C=lambda v:p.kpc(v)
add,mul,pow,scale=p.kadd,p.kmul,p.kpower,p.kscale
eta,z=p.kpv(0),p.kpv(1)
candidate=globals().get('CANDIDATE_RECORD')
if not isinstance(candidate,dict):raise RuntimeError('fresh computed candidate record required')
vals={k:K(v) for k,v in candidate['constants'].items()}
c=K((0,1,0));d=2*c*c-1;v=2*d*d-1;y=1/(3*(1+c));x=K(F(2,3))-y
H=14*y;U0=-8*x;rho=(c-5)/3;uz=(U0+rho*H)/8;up=uz-rho*H/2
W=K((F(2512,27),F(5840,9),F(-21392,27)))
D=K((F(-4270,27),F(-29492,27),F(4012,3)))
gamma=(6*uz**2+2*up**2-D)/(2*H)
marked=add(C(1),scale(eta,-1));checks=0;t0=time.monotonic()
def check(a,b,label):
    global checks
    if a!=b:raise RuntimeError(label)
    checks+=1
def family(repair):
    common=add(scale(pow(eta,3),vals['mstar']),scale(pow(eta,4),vals['nstar']),
               scale(pow(eta,5),repair))
    L0=add(scale(eta,uz),scale(pow(eta,2),vals['nu_zero']),common)
    Lp=add(scale(eta,up),scale(pow(eta,2),vals['nu_pair']),common)
    opening=add(C(1),scale(eta,gamma),scale(pow(eta,2),vals['theta_star']),
                scale(pow(eta,3),vals['phi_star']))
    der=scale(mul(pow(add(z,scale(L0,-1)),6),
        add(pow(add(z,scale(Lp,-1)),2),scale(mul(eta,pow(opening,2)),H/2))),9)
    primitive=p.kintegrate(der)
    pol=add(primitive,scale(p.ksubstitute(primitive,1,marked),-1))
    return L0,Lp,opening,der,pol

root1=Z((d,0,0,1),q=1-d*d);root2=Z((v,0,0,1),q=1-v*v)
root3=Z((F(-1,2),0,0,1),q=K(F(3,4)));root4=Z((-c,0,0,1),q=1-c*c)
roots=[Z(1,q=0),root1,root2,root3,root4,root4.conj(),root3.conj(),root2.conj(),root1.conj()]
base=family(0);A=[K(F(3,2)),1+c]
base_radials=[p.residual_roots(base[4],w,0,0)[2] for w in [root3,root4]]
for a in base_radials:check(a[:4],[K(0)]*4,'active tangency through eta4')
lo,hi=map(F,candidate['embedding_interval'])
repair=1
while any((repair*A[j]-base_radials[j][4]).interval(lo,hi)[0]<=0 for j in range(2)):
    repair*=10
    if repair>1000000:raise RuntimeError('bounded repair search incomplete')
L0,Lp,opening,der,pol=family(repair)
check(p.ksubstitute(pol,1,marked),{},'full defining polynomial anchor')
check(p.kcoefficient(pol,0),add(pow(z,9),C(-1)),'limiting nonagon')
jet=candidate['limiting_real_polynomial_jets']
for k in range(5):
    actual={e[1]:a for e,a in pol.items() if e[0]==k}
    expected={degree:K(a) for degree,a in jet[k]}
    check(actual,expected,'independent factor vs twelve-jet Newton coefficient '+str(k))

def taylor_root(omega):
    zero=lambda:[Z(0,q=omega.q) for _ in range(6)]
    def vmul(a,b):
        out=zero()
        for i,x in enumerate(a):
            for j,y in enumerate(b[:6-i]):out[i+j]+=x*y
        return out
    delta=zero();r=[omega]
    # Direct derivative expansion around omega, separate from whole-polynomial
    # Horner residual solving. Exact binomial Taylor coefficients, no sampling.
    for order in range(1,6):
        powers=[zero()];powers[0][0]=Z(1,q=omega.q)
        for j in range(1,order+1):powers.append(vmul(powers[-1],delta))
        residual=Z(0,q=omega.q)
        for (k,b,mm,tt),a in pol.items():
            if k>order:continue
            for j in range(min(b,order-k)+1):
                residual+=powers[j][order-k]*omega**(b-j)*(a*__import__('math').comb(b,j))
        rn=-residual*omega/9;delta[order]=rn;r.append(rn)
    return r

branches=[]
for j,omega in enumerate(roots):
    r,residual,rad,evaluate=p.residual_roots(pol,omega,0,0)
    check(omega**9,1,'ninth root '+str(j))
    check(residual,[Z(0,q=omega.q)]*6,'full polynomial residual '+str(j))
    check(r,taylor_root(omega),'two complete fifth root routes '+str(j))
    if j==0:check(r,[omega,Z(-1,q=0)]+[Z(0,q=0)]*4,'exact marked branch')
    elif j in [1,2,7,8]:check((-rad[0]).interval(lo,hi)[0]>0,True,'inactive first inward '+str(j))
    else:
        check(rad[:4],[K(0)]*4,'active tangency through fourth '+str(j))
        check((-rad[4]).interval(lo,hi)[0]>0,True,'active fifth inward '+str(j))
    branches.append({'index':j,'radial':[a.record() for a in rad],
        'root_hash':sha256(json.dumps([a.record() for a in r],separators=(',',':')).encode()).hexdigest()})
for j in range(2):
    actual=p.residual_roots(pol,[root3,root4][j],0,0)[2][4]
    check(actual,base_radials[j][4]-repair*A[j],'independent fifth repair response')

delta=add(add(marked,scale(L0,-1)),C(-1))
inverse=add(*(scale(pow(delta,j),(-1)**j) for j in range(6)))
sq=add(pow(add(marked,scale(Lp,-1)),2),scale(mul(eta,pow(opening,2)),H/2))
delta=add(sq,C(-1))
inverse_sqrt=add(*(scale(pow(delta,j),a) for j,a in enumerate(
    [F(1),F(-1,2),F(3,8),F(-5,16),F(35,128),F(-63,256)])))
objective=add(scale(inverse,6),scale(inverse_sqrt,2))
check(p.kcoefficient(objective,4),C(vals['C4']),'actual critical-distance fourth coefficient')
record={'agent':'six-sendov-3','role':'researcher','status':'explicit all-nine-root fourth upper family, verified through fifth inward order',
    'checks':checks,'eta_order':5,'common_eta5_inward_repair':repair,
    'family_hash':p.kphash(pol),'derivative_hash':p.kphash(der),'objective_hash':p.kphash(objective),
    'all_nine_root_branches':branches,'objective_coefficients':[[k,p.kcoefficient(objective,k).get(p.KZERO,K(0)).record()] for k in range(6)]}
