#!/usr/bin/env python3
"""Independent far-root-first two-pair audit by six-reviewer-3.

Only standard-library exact arithmetic. No author program is imported.
The sparse Laurent arithmetic is adapted from this reviewer's public
sendov_two_chart_transition_review3 verifier; the factorization algorithm
and evidence construction below are new independent implementations.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json

NAMES=('v','e','rho','x','f','u0','u1','u2','u3','u4','u5','u6','u7')
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
v,e,rho,x,f=[var(n) for n in NAMES[:5]]
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
def author_ring(p):
    require(all(not any(k[1:2]+k[3:]) for k in p.d),'author ring has only v,rho')
    return [[[k[0],k[2]],[c.numerator,c.denominator]] for k,c in sorted(p.d.items())]
def author_jet(p,n):return [author_ring(p.coeff('e',i)) for i in range(n+1)]

def compute():
    a=1/v-1;b=1-a*a;k=(1+b*x)/2
    # Derive both cleared actual transforms directly from A(a-1/q).
    for s in (e-f,f):
        denominator=4*v**4+2*a*v*v*s;q=x+v
        raw=denominator*((a*q-1)**2+2*(a*q-1)*q+q*q)-2*s*(a*q-1)*q
        eq('literal original-root pair transform',raw,4*v*v*(x*x+s*k))
        product=v*v+a*s/2;total=2*v-b*s/2
        eq('actual opposite-pair energy',2*product-2*v*total+2*v*v,s)
    original=x**4*(x*x+(e-f)*k)*(x*x+f*k)
    character=9*original-(x+v)*original.diff('x')
    k1=(7*a-4)/2
    cubic=x**3+(-8*v+b*e)*x*x+k1*e*x-3*v*e
    J=(1+b*x)*(3*b*x*x+(6*a-1)*x-4*v)/4
    eq('full eight-critical characteristic',character,x**3*(x*x*cubic+f*(e-f)*J))
    eq('endpoint multiplicities',character.at('f',0),x**5*cubic)
    save('full_original_characteristic',original)
    save('full_critical_characteristic',character)
    scaled=character.at('f',e*e*rho)
    C5=[scaled.coeff('x',i+3) for i in range(6)]
    eq('monic quintic',C5[5],1)
    # First remove the far root from the complete quintic. Its constant
    # derivative is 4096v^4, different from the author's external cubic.
    far=8*v
    eq('far collapse',poly_eval(C5,far),0,n=0)
    derivative=sum((i*C5[i]*(8*v)**(i-1) for i in range(1,6)),P())
    eq('full-quintic far derivative',derivative,4096*v**4,n=0)
    for i in range(1,6):far-=poly_eval(C5,far).coeff('e',i)*e**i/(4096*v**4)
    eq('complete far-root residual through5',poly_eval(C5,far))
    quartic=[P() for _ in range(5)];quartic[4]=P(1)
    for i in range(3,-1,-1):quartic[i]=C5[i+1]+far*quartic[i+1]
    eq('synthetic division remainder',C5[0]+far*quartic[0])
    for i in range(6):
        eq('whole far-root removal '+str(i),poly_mul([-far,P(1)],quartic)[i],C5[i])
    # Factor the remaining quartic, not the author's quintic/cubic pair.
    # (x^2+e^2 T x+e^2 P)(x^2+G x+K).
    q0=quartic[0]/e**3;q1=quartic[1]/e**3
    require(all(k[1]>=0 for p in (q0,q1) for k in p.d),'quartic low coefficients divisible by e^3')
    pp=q0.coeff('e',0)/F(3,8)
    G0=quartic[3]/e
    tt=(q1.coeff('e',0)-pp*G0.coeff('e',0))/F(3,8)
    eq('independent auxiliary P limit',pp,rho/3)
    eq('independent auxiliary T limit',tt,-rho*(16*a-7)/(36*v))
    def factors():
        G=quartic[3]-e*e*tt;K=quartic[2]-e*e*pp-e*e*tt*G
        return G,K
    def residuals():
        G,K=factors();return pp*(K/e)-q0,tt*(K/e)+pp*(G/e)-q1
    for i in (1,2):
        residual,_=residuals();pp-=residual.coeff('e',i)*e**i/F(3,8)
        _,residual=residuals();tt-=residual.coeff('e',i)*e**i/F(3,8)
    for residual in residuals():eq('quartic factor IFT jets through2',residual,0,n=2)
    G,K=factors();aux=[e*e*pp,e*e*tt,P(1)];main=[K,G,P(1)]
    for i,p in enumerate(poly_mul(aux,main)):
        eq('quartic product through5 '+str(i),p,quartic[i])
    aux_product=v*v-v*e*e*tt+e*e*pp
    main_product=v*v-v*G+K
    aux_mod=sqrt_series(aux_product,v);main_mod=sqrt_series(main_product,v)
    objective=3*v+2*aux_mod+(v+far)+2*main_mod
    gap=objective-objective.at('rho',0)
    h1=(208-184*v-239*v*v)/(2304*v**5)
    h2=(-245888+771984*v-786792*v*v+246931*v**3)/(4718592*v**8)
    gamma=(4+v)**2/(10368*v**5)
    BQ=(69025-73880*a-66416*a*a)*v**5/12288
    eq('physical split Hessian leading normalization',2*v**8*h1,
       (208*a*a+232*a-215)*v**5/1152)
    eq('complete actual gap through4',gap,e**3*rho*h1+e**4*(rho*h2+rho*rho*(gamma-h1)),n=4)
    for i in range(3):eq('zero lower gap '+str(i),gap.coeff('e',i))
    save('quartic_auxiliary_P_through2',pp);save('quartic_auxiliary_T_through2',tt)
    save('whole_actual_gap_through4',gap.truncate(4))
    save('far_reciprocal_through4',(v+far).truncate(4))
    save('h1',h1);save('h2',h2);save('gamma',gamma)
    ORIGINAL.update({
      'full_eight_original_reciprocal':[author_jet(original.at('f',e*e*rho).coeff('x',i),5) for i in range(9)],
      'full_eight_critical_reciprocal':[author_jet(scaled.coeff('x',i),5) for i in range(9)],
      'rescaled_quintic':[author_jet(p,5) for p in C5],
      'S_energy_jet_through2':author_jet(-tt,2),
      'P_energy_jet_through2':author_jet(pp,2),
      'far_root_energy_through4':author_jet(v+far,4),
      'main_modulus_energy_through4':author_jet(main_mod,4),
      'aux_modulus_energy_through4':author_jet(aux_mod,4),
      'gap_energy_through4':author_jet(gap,4),
      'rho_squared_coefficient':author_ring(gamma-h1)})
    # Whole-family IFT residuals with x=P, f=S, rho=u. Check the full
    # Jacobian, including the off-diagonal entry, in independent symbols.
    U=rho*(1-rho);dc=-3*v+8*v*x;db=k1-x-8*v*f
    low1=x*dc+v*U;low2=-f*dc+x*db-U*5*(2*a-1)/4
    eq('whole-family limiting quadratic',low1,v*(8*x*x-3*x+U))
    eq('whole-family J11',low1.diff('x'),v*(16*x-3))
    eq('whole-family J12',low1.diff('f'),0)
    eq('whole-family J22',low2.diff('f'),v*(3-16*x))
    delta=9-32*rho+32*rho*rho
    det=low1.diff('x')*low2.diff('f')-low1.diff('f')*low2.diff('x')
    eq('whole-family determinant on its limiting conic',det+v*v*delta,-32*v*low1)
    eq('whole-family uniform discriminant floor',delta,1+32*(rho-F(1,2))**2)
    eq('rationalized P0 over u',32*U,(3-(3-16*x))*(3+(3-16*x))+32*(8*x*x-3*x+U))
    Cd=(4+v)**2/(8192*v**5)
    eq('complete endpoint angular entry barrier',64*Cd*rho*rho*(1-rho)**2/9-gamma*rho*rho*delta,
       gamma*rho**3*(14-23*rho))
    save('whole_family_limiting_jacobian',det);save('whole_family_delta',delta)
    # Every vector entry symbolic in all eight original reciprocals, after
    # setting the four collapsed ones equal. No sampled basis inputs.
    us=[var('u'+str(i)) for i in range(8)]
    matrix=[[us[i]*(int(i==j)+1) for j in range(8)] for i in range(8)]
    vectors=[]
    for index in range(3):
        r=[F(0)]*8;r[index+4]=F(1);r[7]=F(-1)
        for side in ('left','right'):
            computed=[sum((r[j]*matrix[j][i] if side=='left' else matrix[i][j]*r[j]
                           for j in range(8)),P()) for i in range(8)]
            for i,p in enumerate(computed):
                for name in ('u4','u5','u6','u7'):p=p.at(name,v)
                eq('symbolic reducing '+side+str((index,i)),p,v*r[i])
            vectors.append([side,index])
    RECORDS['symbolic_full_reducing_vectors']=vectors
    # Exact endpoint signs by rational interval arithmetic and *monotone*
    # threshold isolation, independent of the author's quadratic field code.
    lo,hi=F(3,5),F(5,8)
    g=lambda t:239*t*t+184*t-208
    require(g(lo)<0<g(hi),'positive threshold root isolated')
    for _ in range(80):
        mid=(lo+hi)/2
        if g(mid)<0:lo=mid
        else:hi=mid
    def add(A,B):return (A[0]+B[0],A[1]+B[1])
    def neg(A):return (-A[1],-A[0])
    def mul(A,B):
        z=[a*b for a in A for b in B];return (min(z),max(z))
    def inv(A):
        require(A[0]*A[1]>0,'interval excludes zero');return (1/A[1],1/A[0])
    def interval(p):
        out=(F(0),F(0))
        for k,c in p.d.items():
            require(not any(k[1:]),'endpoint expression only v')
            base=(lo,hi) if k[0]>=0 else inv((lo,hi));term=(c,c)
            for _ in range(abs(k[0])):term=mul(term,base)
            out=add(out,term)
        return out
    h=interval(h2);ga=interval(gamma);sq=interval((239*v+92)/24)
    la=mul(sq,inv(interval(48*v**3)))
    beta=mul(neg(h),inv(mul((F(2),F(2)),ga)))
    gain=mul(mul(h,h),inv(mul((F(4),F(4)),ga)))
    rational=add(mul((F(-11,5),F(-11,5)),h),mul((F(-121,25),F(-121,25)),ga))
    slope=mul(neg(h),inv(la))
    ranges={'gamma':ga,'lambda':la,'minus_h2':neg(h),'beta':beta,'gain':gain,'rational_gain':rational,'curve_slope':slope,
            'mean_stiffness_BQ':interval(BQ),
            'rho6_derivative':add(mul((F(12),F(12)),ga),neg(mul((F(1,5),F(1,5)),la)))}
    for name,I in ranges.items():require(I[0]>0,'strict sign '+name)
    for name,L,U in [('beta',F(2219843,10**6),F(2219844,10**6)),('gain',F(107206,10**6),F(107207,10**6)),
                     ('rational_gain',F(107198,10**6),F(107199,10**6)),('curve_slope',F(112226,10**6),F(112227,10**6))]:
        require(L<ranges[name][0]<=ranges[name][1]<U,'full interval bound '+name)
    # h1(a_-) and its transverse derivative via a polynomial multiple,
    # without accepting any decimal approximation as an identity.
    eq('endpoint leading numerator',208-184*v-239*v*v,-(239*v*v+184*v-208))
    deriv=h1.diff('v')*(-v*v)
    transverse=(239*v+92)/(1152*v**3)
    eq('endpoint transverse identity modulo minimal polynomial',
       deriv-transverse,(239*v*v+184*v-208)*(-F(5,2304))/v**4)
    RECORDS['threshold_interval']=[[q.numerator,q.denominator] for q in (lo,hi)]
    RECORDS['endpoint_intervals']={name:[[q.numerator,q.denominator] for q in I] for name,I in ranges.items()}
    # Meaningful corruptions: missing critical multiplicity, wrong energy,
    # wrong rescaled coefficient, false degeneracy, and broken reducing space.
    damages=[character-x**4*(x*x*cubic+f*(e-f)*J),e+f-e,
             gap.truncate(4)-e**3*rho*h1-e**4*rho*h2,
             delta-32*(rho-F(1,2))**2,
             matrix[4][7].at('u4',v)-0]
    for index,p in enumerate(damages):require(bool(p.d),'damaged math rejected '+str(index))
    RECORDS['damaged_controls']=len(damages)
    return {'schema':'independent-two-pair-review3-v1','agent':'six-reviewer-3',
            'role':'independent mathematical reviewer','method':'complete far quintic root first, synthetic division, remaining quartic factorization',
            'checks':CHECKS,'records':RECORDS,'author_record_names':sorted(ORIGINAL),
            'trust_boundary':'exact algebra/sign evidence; analytic bridges in REVIEW.md'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-fixture',type=Path)
    parser.add_argument('--author-fixture',type=Path,help='optional full literal comparison; never imports author code')
    args=parser.parse_args();result=compute()
    if args.write_fixture:
        args.write_fixture.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        require(args.fixture.is_file(),'mandatory fixture absent')
        require(json.loads(args.fixture.read_text())==result,'complete independent fixture differs')
    if args.author_fixture:
        author=json.loads(args.author_fixture.read_text())['records']
        for name,value in ORIGINAL.items():require(author[name]==value,'complete author record '+name)
    canonical=json.dumps(result,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'agent':result['agent'],'role':result['role'],'checks':len(CHECKS),
      'records':len(RECORDS),'author_records_compared':len(ORIGINAL) if args.author_fixture else 0,
      'damaged_math':RECORDS['damaged_controls'],'sha256':hashlib.sha256(canonical).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
