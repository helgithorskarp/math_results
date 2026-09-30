#!/usr/bin/env python3
"""Exact independent two-block quartic audit; no researcher implementation imports.

Coefficient domain: Q[m,r,h,1/m,1/(3m+2),1/(m+1)], Gaussian extension i^2=-1.
Two simple quadratic roots are expanded implicitly, then each modulus separately.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import factorial
from pathlib import Path
from time import monotonic
import argparse
import json

HERE = Path(__file__).resolve().parent
ZERO_EXP = (0,0,0)

def demand(ok,message):
    if not ok: raise ValueError(message)

class P:
    """Sparse polynomial in m,r,h with exact rational coefficients."""
    def __init__(self,terms=0):
        self.t = ({e:F(c) for e,c in terms.items() if c}
                  if isinstance(terms,dict) else ({ZERO_EXP:F(terms)} if terms else {}))
    def __add__(self,other):
        other = other if isinstance(other,P) else P(other)
        out = dict(self.t)
        for e,c in other.t.items(): out[e] = out.get(e,F(0))+c
        return P(out)
    __radd__ = __add__
    def __neg__(self): return P({e:-c for e,c in self.t.items()})
    def __sub__(self,other): return self + -(other if isinstance(other,P) else P(other))
    def __mul__(self,other):
        other = other if isinstance(other,P) else P(other)
        out = defaultdict(F)
        for e,c in self.t.items():
            for f,d in other.t.items(): out[tuple(a+b for a,b in zip(e,f))] += c*d
        return P(out)
    __rmul__ = __mul__
    def __pow__(self,n):
        demand(type(n) is int and n>=0,'invalid polynomial power')
        ans,base = P(1),self
        while n:
            if n&1: ans = ans*base
            base,n = base*base,n//2
        return ans
    def divide_linear(self,a,b):
        """Try exact division by a*m+b, coefficient by coefficient in r,h."""
        slices = defaultdict(dict)
        for (j,k,l),c in self.t.items(): slices[k,l][j] = c
        out = {}
        for (k,l),row in slices.items():
            while row and max(row)>=1:
                j = max(row);c = row[j]/a
                out[j-1,k,l] = c
                row[j] -= a*c
                if not row[j]: del row[j]
                row[j-1] = row.get(j-1,F(0))-b*c
                if not row[j-1]: del row[j-1]
            if row: return None
        return P(out)
    def evaluate(self,m,r,h=0):
        return sum(c*F(m)**e[0]*F(r)**e[1]*F(h)**e[2] for e,c in self.t.items())
    def rows(self): return [[*e,c.numerator,c.denominator] for e,c in sorted(self.t.items())]

UNITS = (P({(1,0,0):1}),P({(1,0,0):3,ZERO_EXP:2}),P({(1,0,0):1,ZERO_EXP:1}))
UNIT_LINEAR = ((F(1),F(0)),(F(3),F(2)),(F(1),F(1)))

@lru_cache(None)
def unit_power(j,n): return UNITS[j]**n

class R:
    """Rational function whose only denominator factors are m,3m+2,m+1."""
    def __init__(self,num=0,den=(0,0,0)):
        num = num if isinstance(num,P) else P(num)
        demand(len(den)==3 and all(type(e) is int and e>=0 for e in den),'invalid denominator')
        den = list(den)
        if not num.t: den = [0,0,0]
        for j,(a,b) in enumerate(UNIT_LINEAR):
            while den[j] and num.t:
                divided = num.divide_linear(a,b)
                if divided is None: break
                num,den[j] = divided,den[j]-1
        self.num,self.den = num,tuple(den)
    @staticmethod
    def cast(x): return x if isinstance(x,R) else R(x)
    def __add__(self,other):
        other = R.cast(other)
        den = tuple(max(a,b) for a,b in zip(self.den,other.den))
        def lifted(x):
            out = x.num
            for j,(a,b) in enumerate(zip(den,x.den)):
                if a>b: out = out*unit_power(j,a-b)
            return out
        return R(lifted(self)+lifted(other),den)
    __radd__ = __add__
    def __neg__(self): return R(-self.num,self.den)
    def __sub__(self,other): return self+-R.cast(other)
    def __rsub__(self,other): return R.cast(other)+-self
    def __mul__(self,other):
        other = R.cast(other)
        return R(self.num*other.num,tuple(a+b for a,b in zip(self.den,other.den)))
    __rmul__ = __mul__
    def __truediv__(self,x):
        demand(isinstance(x,(int,F)) and x!=0,'only exact constant division allowed')
        return R(self.num*F(1,x),self.den)
    def __pow__(self,n):
        demand(type(n) is int and n>=0,'invalid rational power')
        return R(self.num**n,tuple(e*n for e in self.den))
    def zero(self): return not self.num.t
    def evaluate(self,m,r,h=0):
        demand(m!=0 and 3*m+2!=0 and m+1!=0,'exceptional specialization')
        return self.num.evaluate(m,r,h)/(F(m)**self.den[0]*F(3*m+2)**self.den[1]*F(m+1)**self.den[2])
    def record(self): return {'numerator':self.num.rows(),'denominator_powers':list(self.den)}

class G:
    def __init__(self,re=0,im=0): self.re,self.im = R.cast(re),R.cast(im)
    @staticmethod
    def cast(x): return x if isinstance(x,G) else G(x)
    def __add__(self,x):
        x=G.cast(x);return G(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self): return G(-self.re,-self.im)
    def __sub__(self,x): return self+-G.cast(x)
    def __mul__(self,x):
        x=G.cast(x);return G(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__
    def conj(self): return G(self.re,-self.im)
    def zero(self): return self.re.zero() and self.im.zero()

M = R(UNITS[0]); RR = R(P({(0,1,0):1})); H = R(P({(0,0,1):1}))
DI = R(1,(0,1,0)); MI = R(1,(1,0,0)); NI = R(1,(0,0,1))
D = 3*M+2; N=M+1; S=M-RR; K=RR*S; AA=(M+2)*MI/2; V=2*M*DI
CHECKS=[]

def identity(label,a,b=0):
    a,b=G.cast(a),G.cast(b)
    demand((a-b).zero(),'identity failed: '+label)
    CHECKS.append(label)

def constant(x,L): return [G(x)]+[G() for _ in range(L)]
def add(a,b): return [x+y for x,y in zip(a,b)]
def neg(a): return [-x for x in a]
def scale(a,x): return [z*x for z in a]
def mul(a,b):
    return [sum((a[j]*b[k-j] for j in range(k+1)),G()) for k in range(len(a))]
def conjugate(a): return [x.conj() for x in a]

def exponential(slope,L):
    values=[];power=R(1)
    for j in range(L+1):
        coefficient=power/factorial(j)
        values.append((G(coefficient),G(0,coefficient),G(-coefficient),G(0,-coefficient))[j%4])
        power=power*slope
    return values

def reciprocal(a,inv0,label):
    values=[G(inv0)]+[G() for _ in a[1:]]
    for k in range(1,len(a)):
        values[k]=-sum((a[j]*values[k-j] for j in range(1,k+1)),G())*inv0
    for k,z in enumerate(mul(a,values)): identity(label+' inverse '+str(k),z,int(k==0))
    return values

def modulus(a,base,inv_twice_base,label):
    norm2=mul(a,conjugate(a)); values=[G(base)]+[G() for _ in a[1:]]
    for k in range(1,len(a)):
        values[k]=(norm2[k]-sum((values[j]*values[k-j] for j in range(1,k)),G()))*inv_twice_base
    for k,z in enumerate(mul(values,values)): identity(label+' norm square '+str(k),z,norm2[k])
    for k,z in enumerate(values): identity(label+' real norm '+str(k),z.im)
    return values

def root_series(A,B,base,inv_derivative,label):
    values=constant(base,len(A)-1)
    for k in range(1,len(A)):
        residual=add(mul(A,mul(values,values)),neg(mul(B,values)))
        values[k]=-residual[k]*inv_derivative
    residual=add(add(mul(A,mul(values,values)),neg(mul(B,values))),constant(N,len(A)-1))
    for k,z in enumerate(residual): identity(label+' quadratic residual '+str(k),z)
    return values

def calculate(slope_x,slope_y,L,label):
    x,y=exponential(slope_x,L),exponential(slope_y,L)
    ax,ay=add(constant(AA,L),x),add(constant(AA,L),y)
    A=mul(ax,ay)
    B=add(constant((M+2)*AA,L),add(scale(x,S+1),scale(y,RR+1)))
    # Direct substitution in the quadratic produced by the product rule.
    c0=add(mul(x,y),neg(scale(add(scale(y,RR),scale(x,S)),AA)))
    c1=add(add(scale(x,S+1),scale(y,RR+1)),constant(-M*AA,L))
    transformed_A=add(add(c0,scale(c1,AA)),constant(N*AA**2,L))
    transformed_B=add(c1,constant(2*N*AA,L))
    for k in range(L+1):
        identity(label+' transformed A '+str(k),transformed_A[k],A[k])
        identity(label+' transformed B '+str(k),transformed_B[k],B[k])
    ux,uy=reciprocal(ax,V,label+' x'),reciprocal(ay,V,label+' y')
    qlo=root_series(A,B,V,-2*DI,label+' small')
    qhi=root_series(A,B,N*V,2*DI,label+' large')
    # The two implicit derivatives are -D/2,+D/2, never zero for m>=3.
    identity(label+' small derivative',2*A[0]*V-B[0],-D/2)
    identity(label+' large derivative',2*A[0]*N*V-B[0],D/2)
    invsmall=D*MI/4; invlarge=D*MI*NI/4
    nx=modulus(ux,V,invsmall,label+' x')
    ny=modulus(uy,V,invsmall,label+' y')
    nl=modulus(qlo,V,invsmall,label+' small')
    nh=modulus(qhi,N*V,invlarge,label+' large')
    total=add(add(scale(nx,RR-1),scale(ny,S-1)),add(nl,nh))
    dx,dy=add(ux,constant(-V,L)),add(uy,constant(-V,L))
    energy=add(scale(mul(dx,conjugate(dx)),RR),scale(mul(dy,conjugate(dy)),S))
    for k,z in enumerate(total): identity(label+' real F '+str(k),z.im)
    for k,z in enumerate(energy): identity(label+' real E '+str(k),z.im)
    return [z.re for z in total],[z.re for z in energy]

def finite_coefficient(m,r):
    s=m-r;d=F(3*m+2,2*m)
    return F((m+2)*(3*m+2)**3,256*m**7)*(F(m*m*(m*m-4*m-4),r*s)-(m-6)*(3*m+2))

class C:
    """A separate Gaussian-rational arithmetic layer for finite controls."""
    def __init__(self,re=0,im=0):self.re,self.im=F(re),F(im)
    @staticmethod
    def cast(x):return x if isinstance(x,C) else C(x)
    def __add__(self,x):
        x=C.cast(x);return C(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self):return C(-self.re,-self.im)
    def __sub__(self,x):return self+-C.cast(x)
    def __mul__(self,x):
        x=C.cast(x);return C(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__
    def conj(self):return C(self.re,-self.im)
    def same(self,x):
        x=C.cast(x);return self.re==x.re and self.im==x.im

def finite_oracle(m,r,slope_x,slope_y,alpha=0,beta=0):
    """Expand the branch-free quadratic modulus SUM, unlike the main checker.

    Angles are slope*t+curvature*t^2. Only Fraction arithmetic is used;
    this secondary route checks implementation, not the universal quantifier.
    """
    L=4;s=m-r;n=m+1;a=F(m+2,2*m);d=1+a;v=1/d
    def const(x):return [C(x)]+[C() for _ in range(L)]
    def plus(*seq):return [sum(row,C()) for row in zip(*seq)]
    def times(x,y):return [sum((x[j]*y[k-j] for j in range(k+1)),C()) for k in range(L+1)]
    def scaled(x,k):return [z*k for z in x]
    def conjugated(x):return [z.conj() for z in x]
    def invert(x):
        demand(x[0].im==0 and x[0].re!=0,'finite inverse base')
        out=const(1/x[0].re)
        for k in range(1,L+1):out[k]=-sum((x[j]*out[k-j] for j in range(1,k+1)),C())*(1/x[0].re)
        demand(all(z.same(int(k==0)) for k,z in enumerate(times(x,out))),'finite inverse residual')
        return out
    def square_root(x,base):
        demand(base>0 and x[0].same(base*base),'finite square-root base')
        out=const(base)
        for k in range(1,L+1):out[k]=(x[k]-sum((out[j]*out[k-j] for j in range(1,k)),C()))*F(1,2*base)
        demand(all(z.same(w) for z,w in zip(times(out,out),x)),'finite square-root residual')
        return out
    def phase(slope,curvature):
        exponent=[C(),C(0,slope),C(0,curvature),C(),C()]
        out=const(1);power=const(1)
        for j in range(1,L+1):power=times(power,exponent);out=plus(out,scaled(power,F(1,factorial(j))))
        return out
    x,y=phase(slope_x,alpha),phase(slope_y,beta)
    ax,ay=plus(const(a),x),plus(const(a),y)
    A=times(ax,ay);B=plus(const((m+2)*a),scaled(x,s+1),scaled(y,r+1))
    delta=plus(times(B,B),scaled(A,-4*n))
    norm_A=square_root(times(A,conjugated(A)),d*d)
    norm_delta=square_root(times(delta,conjugated(delta)),F((3*m+2)**2,4))
    squared=scaled(plus(times(B,conjugated(B)),norm_delta,scaled(norm_A,4*n)),F(1,2))
    qsum=times(square_root(squared,(m+2)*d),invert(norm_A))
    ux,uy=invert(ax),invert(ay)
    nx,ny=square_root(times(ux,conjugated(ux)),v),square_root(times(uy,conjugated(uy)),v)
    total=plus(qsum,scaled(nx,r-1),scaled(ny,s-1))
    dx,dy=plus(ux,const(-v)),plus(uy,const(-v))
    energy=plus(scaled(times(dx,conjugated(dx)),r),scaled(times(dy,conjugated(dy)),s))
    demand(all(z.im==0 for z in total+energy),'finite real coefficients')
    return [z.re for z in total],[z.re for z in energy]

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    start=monotonic()
    gap,energy=calculate(S,-RR,4,'balanced')
    f4=M**3*(M+2)*K*DI**5*(-M**2*(M**2-4*M-4)+(M-6)*D*K)
    e2=M*K*V**4
    for j in range(4): identity('balanced F coefficient '+str(j),gap[j],2*M*V if j==0 else 0)
    identity('balanced F fourth coefficient',gap[4],f4)
    for j in (0,1,3): identity('balanced E zero '+str(j),energy[j])
    identity('balanced E second coefficient',energy[2],e2)
    identity('balanced E fourth coefficient',energy[4],M*K*(M**2-3*K)*(AA*V**6-V**4/12))
    kk=(M+2)*D**3*MI**7/256*(M**2*(M**2-4*M-4)-(M-6)*D*K)
    identity('energy-normalized K times k',gap[4]*K+kk*energy[2]**2)
    general,general_energy=calculate(S+H,-RR+H,2,'common shift')
    identity('common shift Hessian',general[2],M*AA*V**3*H**2)
    identity('common shift energy',general_energy[2],(M*K+M*H**2)*V**4)
    polynomial=M**4-9*M**3+13*M**2-13*M-6
    identity('positivity T at m=5+h',(H+5)**2-4*(H+5)-4,H**2+6*H+1)
    identity('positive lower bracket',4*(M**2-4*M-4)-(M-6)*D,M**2-4)
    identity('k lower gap',K-(M-1),(RR-1)*(M-RR-1))
    identity('k upper gap',M**2-4*K,(M-2*RR)**2)
    pair=(M+2)*(M**3-4*M**2+13*M+18)*D**3*MI**7/512
    # Multiply comparison by m-1 to avoid adding any unlisted denominator unit.
    extreme_times_mminus1=(M+2)*D**3*MI**7/256*(M**2*(M**2-4*M-4)-(M-6)*D*(M-1))
    identity('comparison polynomial',extreme_times_mminus1-pair*(M-1),(M+2)*D**3*MI**7*polynomial/512)
    shifted=(H+8)**4-9*(H+8)**3+13*(H+8)**2-13*(H+8)-6
    identity('comparison positivity at m=8+h',shifted,H**4+23*H**3+181*H**2+515*H+210)
    profiles=0;finite_entries=0
    for m in range(3,25):
        values=[finite_coefficient(m,r) for r in range(1,m)]
        demand(all(v>0 for v in values),'nonpositive coefficient')
        maximizing=[r for r,v in enumerate(values,1) if v==max(values)]
        demand(maximizing==([1,2] if m==3 else [2] if m==4 else [1,m-1]),'wrong finite extremizer')
        for r in range(1,m):
            demand(-gap[4].evaluate(m,r)/energy[2].evaluate(m,r)**2==values[r-1],'specialization differs')
            ff,ee=finite_oracle(m,r,m-r,-r)
            for original,independent in ((ff,gap),(ee,energy)):
                for j in range(5):
                    demand(original[j]==independent[j].evaluate(m,r),'finite branch-free coefficient differs')
                    finite_entries+=1
            profiles+=1
        pair_m=pair.evaluate(m,1)
        demand((max(values)>pair_m)==(m>=8),'wrong finite comparison threshold')
    demand(finite_coefficient(3,1)==F(6655,373248),'m3 exception')
    demand(finite_coefficient(4,2)==F(3087,65536),'m4 exception')
    max9=finite_coefficient(8,1);pair9=pair.evaluate(8,1)
    demand(max9==F(560235,8388608) and max9-pair9==F(164775,33554432),'degree9 coefficient')
    demand([polynomial.evaluate(m,0) for m in (5,6,7)]==[-246,-264,-146],'small degree polynomial')
    nonlinear_cases=0;hessian_cases=0
    for m,r in ((4,2),(8,1),(8,3)):
        s=m-r;d=F(3*m+2,2*m);a=d-1
        for h in (-2,-1,0,1,2):
            ff,ee=finite_oracle(m,r,s+h,-r+h)
            demand(ff[2]==general[2].evaluate(m,r,h),'finite common-shift Hessian differs')
            demand(ee[2]==general_energy[2].evaluate(m,r,h),'finite common-shift energy differs')
            hessian_cases+=1
        for lam in (F(1),F(1,2),F(-2)):
            for alpha,beta in ((0,0),(1,1),(1,-1),(7,-1),(0,1)):
                ff,ee=finite_oracle(m,r,s*lam,-r*lam,alpha,beta)
                prediction=lam**4*gap[4].evaluate(m,r)+a*F((r*alpha+s*beta)**2,m)/d**3
                demand(ff[:3]==[2*m/d,0,0] and ff[3]==0 and ff[4]==prediction,'finite nonlinear quartic differs')
                demand(ee[2]==lam**2*energy[2].evaluate(m,r),'finite nonlinear energy differs')
                nonlinear_cases+=1
    # Reject concrete incorrect all-degree coefficients, not numerical fit variants.
    rejected=0
    for bad in (f4+1,f4-1,-f4,2*f4,f4+M*K*DI**5):
        if not (gap[4]-bad).zero():rejected+=1
    demand(rejected==5,'coefficient mutation accepted')
    symbolic={'F_coefficients':[z.record() for z in gap],'E_coefficients':[z.record() for z in energy],
              'common_shift_F2':general[2].record(),'common_shift_E2':general_energy[2].record()}
    output={'reviewer':'six-reviewer-3','role':'independent mathematical reviewer','status':'ALL-DEGREE TWO-BLOCK QUARTIC AND HESSIAN IDENTITIES VERIFIED',
            'coefficient_domain':'Q[m,r,h,1/m,1/(3m+2),1/(m+1)][i]/(i^2+1)',
            'symbolic_identities':len(CHECKS),'identity_labels_sha256':sha256(('\n'.join(CHECKS)+'\n').encode()).hexdigest(),
            'coefficient_digest_sha256':sha256(json.dumps(symbolic,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'finite_profiles':profiles,'finite_degrees':list(range(3,25)),'rejected_coefficient_mutations':rejected,
            'independent_finite_branch_free_entries':finite_entries,'finite_hessian_cases':hessian_cases,
            'finite_nonlinear_jet_cases':nonlinear_cases,
            'degree9_maximum':[max9.numerator,max9.denominator],'degree9_moving_pair':[pair9.numerator,pair9.denominator],
            'degree9_excess':[(max9-pair9).numerator,(max9-pair9).denominator],
            'nonlinear_refinement':'Quadratic Taylor term is a/(m*d^3)*(r*theta_x+s*theta_y)^2; balanced first jet with nonzero scale lambda and second coefficients alpha,beta has deficit limit K-a*d^5*(r*alpha+s*beta)^2/(lambda^4*m^3*r^2*s^2).'}
    raw=json.dumps(output,sort_keys=True,indent=2)+'\n'
    if args.write:(HERE/'expected.json').write_text(raw)
    else:demand(json.loads((HERE/'expected.json').read_text())==output,'compact expected manifest mismatch')
    print(raw,end='');print('Elapsed seconds:',round(monotonic()-start,3))

if __name__=='__main__':main()
