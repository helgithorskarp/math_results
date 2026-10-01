#!/usr/bin/env python3
"""Independent far-root-first transverse split audit by six-reviewer-3.

Only standard-library exact arithmetic. No author program is imported.
The sparse Laurent arithmetic is adapted from this reviewer's public
sendov_two_chart_transition_review3 verifier; the factorization algorithm
and evidence construction below are new independent implementations.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json

NAMES=('v','e','rho','x','f','g','u0','u1','u2','u3','u4','u5','u6','u7')
Z=(0,)*len(NAMES)
CAP=5
CHECKS=[]; RECORDS={}; ORIGINAL={}
def require(ok, text):
    if not ok: raise ValueError(text)

class P:
    def __init__(self, value=0):
        self.d=({k:F(c) for k,c in value.items() if c and k[1]<=CAP}
                if isinstance(value,dict) else ({Z:F(value)} if value else {}))
    @staticmethod
    def cast(x): return x if isinstance(x,P) else P(x)
    def __add__(self,x):
        d=dict(self.d)
        for k,c in P.cast(x).d.items(): d[k]=d.get(k,F(0))+c
        return P(d)
    __radd__=__add__
    def __neg__(self): return P({k:-c for k,c in self.d.items()})
    def __sub__(self,x): return self+-P.cast(x)
    def __rsub__(self,x): return P.cast(x)+-self
    def __mul__(self,x):
        d=defaultdict(F)
        for k,c in self.d.items():
            for h,b in P.cast(x).d.items():
                if k[1]+h[1]<=CAP: d[tuple(i+j for i,j in zip(k,h))]+=c*b
        return P(d)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=P.cast(x);require(len(x.d)==1,'nonzero monomial divisor')
        h,b=next(iter(x.d.items()))
        return P({tuple(i-j for i,j in zip(k,h)):c/b for k,c in self.d.items()})
    def __rtruediv__(self,x): return P.cast(x)/self
    def __pow__(self,n):
        if n<0: return P(1)/(self**(-n))
        result=P(1)
        while n:
            if n&1: result*=self
            self=self*self;n//=2
        return result
    def coeff(self,name,n):
        i=NAMES.index(name);d={}
        for k,c in self.d.items():
            if k[i]==n:
                h=list(k);h[i]=0;d[tuple(h)]=c
        return P(d)
    def diff(self,name):
        i=NAMES.index(name);d={}
        for k,c in self.d.items():
            if k[i]:
                h=list(k);h[i]-=1;d[tuple(h)]=k[i]*c
        return P(d)
    def at(self,name,value):
        i=NAMES.index(name);out=P()
        for k,c in self.d.items():
            h=list(k);h[i]=0;out+=P({tuple(h):c})*P.cast(value)**k[i]
        return out
    def truncate(self,n): return P({k:c for k,c in self.d.items() if k[1]<=n})
    def wire(self):
        return [[[[name,power] for name,power in zip(NAMES,k) if power],
                 [c.numerator,c.denominator]] for k,c in sorted(self.d.items())]

def var(name):
    k=list(Z);k[NAMES.index(name)]=1;return P({tuple(k):1})
v,e,rho,x,f,g=[var(n) for n in NAMES[:6]]
def eq(name,value,expected=0,n=CAP):
    require(not (P.cast(value)-expected).truncate(n).d,name);CHECKS.append(name)
def save(name,p): RECORDS[name]=P.cast(p).wire()
def jet_div(numerator,denominator,n=CAP):
    c=denominator.coeff('e',0);inv=[P(1)/c]
    for i in range(1,n+1):
        inv.append(-sum((denominator.coeff('e',j)*inv[i-j]
                         for j in range(1,i+1)),P())/c)
    return sum((sum((numerator.coeff('e',j)*inv[i-j] for j in range(i+1)),P())*e**i
                for i in range(n+1)),P())
def sqrt_series(squared,constant,n=4):
    c=[P.cast(constant)];eq('sqrt constant',c[0]*c[0],squared.coeff('e',0))
    for i in range(1,n+1):
        c.append((squared.coeff('e',i)-sum((c[j]*c[i-j] for j in range(1,i)),P()))/(2*c[0]))
    root=sum((c[i]*e**i for i in range(n+1)),P())
    eq('all square coefficients',root*root,squared,n=n);return root
def poly_mul(a,b):
    out=[P() for _ in range(len(a)+len(b)-1)]
    for i,p in enumerate(a):
        for j,q in enumerate(b):out[i+j]+=p*q
    return out
def poly_eval(a,z):
    out=P()
    for p in reversed(a):out=out*z+p
    return out
def poly_diff(a):return [i*a[i] for i in range(1,len(a))]
def poly_add(a,b):
    return [(a[i] if i<len(a) else P())+(b[i] if i<len(b) else P()) for i in range(max(len(a),len(b)))]
def old_full(p):
    require(all(not(k[2] or k[3] or any(k[6:])) for k in p.d),"full comparison has only v,e,f,g")
    return [[[k[0],k[1],k[4],k[5]],[c.numerator,c.denominator]] for k,c in sorted(p.d.items())]
def old_ring(p):
    require(all(not any(k[1:2]+k[3:]) for k in p.d),"coefficient has only v,rho")
    return [[[k[0],k[2]],[c.numerator,c.denominator]] for k,c in sorted(p.d.items())]
def old_jet(p,n=2):return [old_ring(p.coeff('e',i)) for i in range(n+1)]
def compute():
    a=1/v-1;b=1-a*a;k=(1+b*x)/2
    # Full physical transform, before using any perturbation or jet.
    energies=(e-f-g,f,g)
    original=x*x
    for s in energies:
        denominator=4*v**4+2*a*v*v*s;q=x+v
        raw=denominator*((a*q-1)**2+2*(a*q-1)*q+q*q)-2*s*(a*q-1)*q
        eq('literal actual pair transform',raw,4*v*v*(x*x+s*k))
        eq('literal pair energy',2*(v*v+a*s/2)-2*v*(2*v-b*s/2)+2*v*v,s)
        original*=x*x+s*k
    character=9*original-(x+v)*original.diff('x')
    # These stages have total energy degree at most3, so the generic
    # e^6 jet cap cannot discard anything in the untruncated stage.
    require(all(sum(t[i] for i in (1,4,5))<=3 for p in (original,character) for t in p.d),"full-stage energy degree bound")
    eq('one persistent critical reciprocal',character.coeff('x',0),0)
    C7=[character.coeff('x',i+1) for i in range(8)]
    C5=[character.at('g',0).coeff('x',i+3) for i in range(6)]
    eq('monic complete quintic',C5[5],1)
    derivative=[p.diff('g').at('g',0) for p in C7]
    pi=P(F(1,4));sigma=(8*a+1)/(16*v)
    # Solve the two lowest first-variation coefficient identities,
    # and derive the remaining external quintic by exact division.
    num=poly_add(derivative,[-pi*p for p in C5])
    num=poly_add(num,[P()]+[sigma*p for p in C5])
    eq('new quadratic constant identity',num[0]);eq('new quadratic linear identity',num[1])
    L5=num[2:]
    full=poly_add([pi*p for p in C5],[P()]+[-sigma*p for p in C5])
    full=poly_add(full,[P(),P()]+L5)
    for i in range(8):eq('entire differentiated septic coefficient '+str(i),full[i],derivative[i])
    ORIGINAL.update({'full_eight_original_reciprocal':[old_full(original.coeff('x',i)) for i in range(9)],
        'full_eight_critical_reciprocal':[old_full(character.coeff('x',i)) for i in range(9)],
        'complete_septic':[old_full(p) for p in C7],
        'new_pair_product_derivative':old_full(pi),
        'new_pair_sum_derivative':old_full(sigma),
        'full_external_quintic_derivative':[old_full(p) for p in L5]})
    save('full_original_reciprocal',original);save('full_critical_reciprocal',character)
    # An identity of physical families alone would not identify a limiting
    # derivative at a collision. Verify the exact factor derivative at
    # rho=0, before any energy truncation, as a separate bridge.
    s=(16*a-7)/(36*v)
    C3=[-3*v*e,(7*a-4)*e/2,-8*v+b*e,P(1)]
    J=[-v,5*(2*a-1)/4,b*(3*a+1)/2,3*b*b/4]
    U=s-sigma;V=P(F(1,12))
    Ap=s;Bp=e*J[3]+s*C3[2]-F(1,3)
    Cp=e*J[2]+s*C3[1]-C3[2]/3
    rhozero=poly_add(poly_mul([V,-U],C3),[P(),P(),Cp,Bp,Ap])
    for i,p in enumerate(rhozero):eq('full rho-zero quintic factor derivative '+str(i),p,L5[i].at('f',0))
    eq('exact combined rho-zero sum derivative',sigma+U,s)
    eq('exact combined rho-zero product derivative',pi+V,F(1,3))
    RECORDS['full_rho_zero_cubic_variation']=[p.wire() for p in [Cp,Bp,Ap]]
    # Independent order: remove the far root from the full quintic,
    # differentiate that removal, and only then factor its quartic.
    C5=[p.at('f',e*e*rho) for p in C5];L5=[p.at('f',e*e*rho) for p in L5]
    far=8*v
    eq('far-root collapse',poly_eval(C5,far),0,n=0)
    eq('full-quintic far derivative',poly_eval(poly_diff(C5),far),4096*v**4,n=0)
    for i in range(1,6):
        far-=poly_eval(C5,far).coeff('e',i)*e**i/(4096*v**4)
    eq('whole far root residual',poly_eval(C5,far))
    quartic=[P() for _ in range(5)];quartic[4]=P(1)
    for i in range(3,-1,-1):quartic[i]=C5[i+1]+far*quartic[i+1]
    eq('whole far division remainder',C5[0]+far*quartic[0])
    farprime=jet_div(-poly_eval(L5,far),poly_eval(poly_diff(C5),far))
    eq('whole far derivative equation',farprime*poly_eval(poly_diff(C5),far)+poly_eval(L5,far))
    quarticprime=[P() for _ in range(5)]
    for i in range(3,-1,-1):
        quarticprime[i]=L5[i+1]+farprime*quartic[i+1]+far*quarticprime[i+1]
    productprime=poly_add(poly_mul([-farprime,P()],quartic),poly_mul([-far,P(1)],quarticprime))
    for i in range(6):eq('whole differentiated far factor '+str(i),productprime[i],L5[i])
    q0=quartic[0]/e**3;q1=quartic[1]/e**3
    pp=q0.coeff('e',0)/F(3,8)
    tt=(q1.coeff('e',0)-pp*(quartic[3]/e).coeff('e',0))/F(3,8)
    s=(16*a-7)/(36*v)
    eq('quartic pair product limit',pp,rho/3);eq('quartic pair sum limit',tt,-rho*s)
    def base():
        alpha=e*e*tt;beta=e*e*pp
        G=quartic[3]-alpha;K=quartic[2]-beta-alpha*G
        return alpha,beta,G,K
    def residual():
        alpha,beta,G,K=base()
        return pp*(K/e)-q0,tt*(K/e)+pp*(G/e)-q1
    for i in (1,2):
        rp,_=residual();pp-=rp.coeff('e',i)*e**i/F(3,8)
        _,rt=residual();tt-=rt.coeff('e',i)*e**i/F(3,8)
    for p in residual():eq('quartic base normalized equations',p,0,n=2)
    alpha,beta,G,K=base()
    aux=[beta,alpha,P(1)];main=[K,G,P(1)]
    for i,p in enumerate(poly_mul(aux,main)):eq('whole quartic base product '+str(i),p,quartic[i])
    # Different normalized system from the author's quintic/cubic IFT.
    # The two diagonal pivots are3/8, after removing the far root.
    alphaprime=P();betaprime=P()
    def prime():
        gp=quarticprime[3]-alphaprime
        kp=quarticprime[2]-betaprime-alphaprime*G-alpha*gp
        return gp,kp
    def primeresidual():
        gp,kp=prime()
        return (betaprime*K+beta*kp-quarticprime[0])/e, \
               (alphaprime*K+alpha*kp+betaprime*G+beta*gp-quarticprime[1])/e
    for i in range(3):
        rp,_=primeresidual();betaprime-=rp.coeff('e',i)*e**i/F(3,8)
        _,rt=primeresidual();alphaprime-=rt.coeff('e',i)*e**i/F(3,8)
    for p in primeresidual():eq('normalized derivative equation through2',p,0,n=2)
    eq('independent product derivative limit',betaprime.coeff('e',0),F(1,12))
    eq('independent signed sum derivative limit',alphaprime.coeff('e',0),sigma-s)
    gp,kp=prime()
    qp=poly_add(poly_mul([betaprime,alphaprime,P()],main),poly_mul(aux,[kp,gp,P()]))
    for i,p in enumerate(qp):eq('entire quartic factor derivative '+str(i),p,quarticprime[i],n=3)
    auxmod=sqrt_series(v*v-v*alpha+beta,v)
    mainmod=sqrt_series(v*v-v*G+K,v)
    H4=sigma+pi/v+jet_div(-v*alphaprime+betaprime,auxmod)+farprime+jet_div(-v*gp+kp,mainmod)
    h1=(208-184*v-239*v*v)/(2304*v**5)
    h2=(-245888+771984*v-786792*v*v+246931*v**3)/(4718592*v**8)
    gamma=(4+v)**2/(10368*v**5);mu=-h1-F(7,4)*gamma
    eq('whole H4 energy coefficients',H4,h1*e+(h2+rho*mu)*e*e,n=2)
    eq('full rho cross identity',mu,(-3856+3256*v+4295*v*v)/(41472*v**5))
    ORIGINAL.update({'existing_pair_sum_derivative_through2':old_jet(-alphaprime),
        'existing_pair_product_derivative_through2':old_jet(betaprime),
        'H4_energy_through2':old_jet(H4),'rho_cross_coefficient':old_ring(mu),
        'far_root_derivative_through2':old_jet(farprime),'far_root_through2':old_jet(v+far)})
    save('H4_complete_rho_polynomial_through2',H4.truncate(2))
    save('quartic_sum_derivative_through2',alphaprime.truncate(2))
    save('quartic_product_derivative_through2',betaprime.truncate(2))
    save('main_quadratic_derivative_through2',(-v*gp+kp).truncate(2))
    # Exact rho-zero identification against the physical two-pair family.
    # This is the full (untruncated) physical identity T(f=0,g)=R(g).
    orig0=original.at('f',0)
    two=x**4*(x*x+(e-g)*k)*(x*x+g*k)
    eq('full physical rho-zero family identity',orig0,two)
    # Universal reducing and angular-compression identities in all
    # independent external reciprocals and phase variations.
    us=[var('u'+str(i)) for i in range(8)]
    collapsed=us[:4]+[v]*4
    N=[[collapsed[i]*(int(i==j)+1) for j in range(8)] for i in range(8)]
    Q=[[F(int(i==j))-F(1,4) if i>=4 and j>=4 else F(0) for j in range(8)] for i in range(8)]
    def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(8)),P()) for j in range(8)] for i in range(8)]
    for label,A in [('right',mm(N,Q)),('left',mm(Q,N)),('idempotence',mm(Q,Q))]:
        for i in range(8):
            for j in range(8):eq('full symbolic '+label+str((i,j)),A[i][j],Q[i][j] if label=='idempotence' else v*Q[i][j])
    angular=[[us[i]*(int(i==j)+1) for j in range(8)] for i in range(8)]
    diagonal=[[us[i]*int(i==j) for j in range(8)] for i in range(8)]
    compression=mm(mm(Q,angular),Q);simple=mm(mm(Q,diagonal),Q)
    for i in range(8):
        for j in range(8):
            eq('whole symbolic compression'+str((i,j)),compression[i][j],simple[i][j])
            eq('whole symbolic symmetric compression'+str((i,j)),simple[i][j],simple[j][i])
    RECORDS['whole_symbolic_phase_compression']=[[p.wire() for p in row] for row in simple]
    # Independent raw rational intervals, rather than the author's
    # quadratic-field reduction, certify the endpoint signs.
    lo,hi=F(3,5),F(5,8);threshold=lambda t:239*t*t+184*t-208
    require(threshold(lo)<0<threshold(hi),"threshold branch isolated")
    for _ in range(80):
        mid=(lo+hi)/2
        if threshold(mid)<0:lo=mid
        else:hi=mid
    def mul(A,B):
        vals=[a*b for a in A for b in B];return min(vals),max(vals)
    def inv(A):
        require(A[0]*A[1]>0,"interval excludes zero");return 1/A[1],1/A[0]
    def interval(p):
        out=(F(0),F(0))
        for t,c in p.d.items():
            require(not any(t[1:]),"endpoint expression only v")
            power=(lo,hi) if t[0]>=0 else inv((lo,hi));term=(c,c)
            for _ in range(abs(t[0])):term=mul(term,power)
            out=(out[0]+term[0],out[1]+term[1])
        return out
    lam=(239*v+92)/(1152*v**3)
    signs={'gamma':interval(gamma),'lambda':interval(lam),'minus_h2':interval(-h2),
           'relative_H4_coefficient':interval(F(15,8)*lam),
           'endpoint_minus_H4_coefficient':interval(-F(15,8)*h2),
           'balanced_split_leading_coefficient':interval(F(15,4)*v**4*lam),
           'compact_descent_coefficient':interval(F(15,32)*v**4*lam)}
    for name,I in signs.items():require(I[0]>0,"positive "+name)
    RECORDS['strict_endpoint_interval_bounds']={name:[str(z) for z in I] for name,I in signs.items()}
    RECORDS['isolated_v_interval']=[str(lo),str(hi)]
    # Endpoint relations use polynomial divisibility by the defining
    # quadratic, not Q[v]/g arithmetic.
    relation=239*v*v+184*v-208
    eq('h1 factorization',2304*v**5*h1,-relation)
    eq('mu endpoint relation',mu+F(7,4)*gamma,-h1)
    eq('general branch coefficient relative identity',2*gamma*lam-lam*mu-F(15,4)*gamma*lam,lam*h1)
    damages=[H4.coeff('e',2)-h2,H4.coeff('e',1)-2*h1,mu+h1+F(3,2)*gamma,
             character-original,compression[4][4],betaprime.coeff('e',0)-F(1,4)]
    require(all(p.d for p in damages),"six damaged mathematical controls are nonzero")
    return {'actual_author':'six-reviewer-3','role':'independent mathematical reviewer',
            'method':'far quintic root then differentiated quartic; normalized pivots3/8; universal symbolic reducing/compression identities; raw rational interval signs',
            'identities':CHECKS,'records':RECORDS,'damaged_math':len(damages),'author_complete_records':ORIGINAL}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-fixture',type=Path);parser.add_argument('--author-fixture',type=Path)
    args=parser.parse_args();result=compute()
    if args.write_fixture:args.write_fixture.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        require(args.fixture.is_file(),"mandatory full fixture absent")
        require(json.loads(args.fixture.read_text())==result,"entire mandatory fixture comparison")
    if args.author_fixture:
        rows=json.loads(args.author_fixture.read_text())['records']
        for key,value in ORIGINAL.items():require(rows[key]==value,"entire independently reconstructed author record "+key)
    print(json.dumps({'status':'PASS_INDEPENDENT' if not args.write_fixture else 'FIXTURE_GENERATED',
        'identities':len(CHECKS),'records':len(RECORDS),'whole_author_record_comparisons':len(ORIGINAL) if args.author_fixture else 0,
        'damaged_math':result['damaged_math'],'canonical_result_sha256':hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
