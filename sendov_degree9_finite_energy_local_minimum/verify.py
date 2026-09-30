#!/usr/bin/env python3
"""Exact local-variation controls for degree-nine reciprocal energy.

Actual author six-sendov-3, researcher. Standard-library rational algebra;
no CAS, floating input, graph access or campaign imports. The small Laurent/
Gaussian kernel is openly adapted from this author's preceding public
second-order-energy checker. Written analytic arguments in PROOF.md establish
all-root coverage, lower support and local coercivity; this file does not
formalize those arguments or enumerate admissible polynomials.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial, isqrt, comb
from pathlib import Path
import json
import sys

ORDER = 8


@dataclass(frozen=True)
class L:
    terms: tuple = ()

    def __add__(self, other):
        other = laurent(other)
        terms = dict(self.terms)
        for exponent, coefficient in other.terms:
            terms[exponent] = terms.get(exponent, Q(0)) + coefficient
        return polynomial(terms)

    __radd__ = __add__

    def __neg__(self):
        return L(tuple((e, -c) for e, c in self.terms))

    def __sub__(self, other):
        return self + -laurent(other)

    def __rsub__(self, other):
        return laurent(other) + -self

    def __mul__(self, other):
        other = laurent(other)
        terms = {}
        for e, c in self.terms:
            for f, d in other.terms:
                terms[e+f] = terms.get(e+f, Q(0)) + c*d
        return polynomial(terms)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = laurent(other)
        if len(other.terms) != 1:
            raise ValueError('Division requires a nonzero Laurent monomial')
        f, d = other.terms[0]
        return L(tuple((e-f, c/d) for e, c in self.terms))

    def __pow__(self, power):
        if not isinstance(power, int):
            raise TypeError('Integer exponent required')
        if power < 0:
            return laurent(1) / self**(-power)
        total = laurent(1)
        for _ in range(power):
            total = total*self
        return total

    def evaluate(self, value):
        return sum((c*value**e for e, c in self.terms), Q(0))

    def derivative(self):
        return polynomial({e-1: e*c for e, c in self.terms if e})


def polynomial(terms):
    return L(tuple(sorted((e, Q(c)) for e, c in terms.items() if c)))


def laurent(value):
    return value if isinstance(value, L) else polynomial({0: Q(value)})


@dataclass(frozen=True)
class G:
    re: L = L()
    im: L = L()

    def __post_init__(self):
        object.__setattr__(self, 're', laurent(self.re))
        object.__setattr__(self, 'im', laurent(self.im))

    def __add__(self, other):
        other = gaussian(other)
        return G(self.re+other.re, self.im+other.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, other):
        return self + -gaussian(other)

    def __rsub__(self, other):
        return gaussian(other) + -self

    def __mul__(self, other):
        other = gaussian(other)
        return G(self.re*other.re-self.im*other.im,
                 self.re*other.im+self.im*other.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = gaussian(other)
        norm = other.re**2+other.im**2
        numerator = self*G(other.re, -other.im)
        return G(numerator.re/norm, numerator.im/norm)

    def conjugate(self):
        return G(self.re, -self.im)


def gaussian(value):
    return value if isinstance(value, G) else G(value)



# Exact formal t jets with rational Laurent coefficients in V=(1+a)^-1.
# MAX=8 inputs suffice for the reported mean t^6 and shape t^2 jets.
# Shape denominators have total t valuation at most two; see README.md.
MAX=8

def ts(value=0):
 g=gaussian(value)
 return {0:g} if g!=G() else {}

def clean(a): return {k:x for k,x in a.items() if x!=G() and k<=MAX}
def plus(*values):
 r={}
 for a in values:
  for k,x in a.items(): r[k]=r.get(k,G())+x
 return clean(r)
def times(*values):
 r=ts(1)
 for a in values:
  n={}
  for k,x in r.items():
   for l,y in a.items():
    if k+l<=MAX:n[k+l]=n.get(k+l,G())+x*y
  r=clean(n)
 return r
def scaled(a,x):return clean({k:y*x for k,y in a.items()})
def minus(a,b):return plus(a,scaled(b,-1))
def invert(a):
 m=min(a); shifted={k-m:x for k,x in a.items()}; b={0:G(1)/shifted[0]}
 for k in range(1,MAX+m+1):
  b[k]=-sum((shifted.get(j,G())*b.get(k-j,G()) for j in range(1,k+1)),G())/shifted[0]
 return clean({k-m:x for k,x in b.items()})
def divide(a,b):return times(a,invert(b))
def tp(a,n):
 if n<0:return tp(invert(a),-n)
 r=ts(1)
 for _ in range(n):r=times(r,a)
 return r
def conj(a):return {k:x.conjugate() for k,x in a.items()}
def rr(a):return clean({k:G(x.re) for k,x in a.items()})
def sqrt_t(a):
 if min(a)!=0 or a[0].im!=L() or len(a[0].re.terms)!=1:raise ValueError('positive monomial constant required')
 e,c=a[0].re.terms[0]; p,q=c.numerator,c.denominator; ip,iq=isqrt(p),isqrt(q)
 if e%2 or c<=0 or ip*ip!=p or iq*iq!=q:raise ValueError('nonrational sqrt')
 b={0:G(polynomial({e//2:Q(ip,iq)}))}
 for k in range(1,MAX+1):
  b[k]=(a.get(k,G())-sum((b[j]*b[k-j] for j in range(1,k)),G()))/(2*b[0])
 return clean(b)
def norm(a):return sqrt_t(times(a,conj(a)))
def deriv(a):return clean({k-1:k*x for k,x in a.items() if k})
def exp_i(phi):
 iphi=scaled(phi,G(0,1)); power=ts(1); total={}
 for k in range(MAX+1):
  total=plus(total,scaled(power,Q(1,factorial(k))));power=times(power,iphi)
 return total

RECORDS = []
CONTROLS = []

def encode(value):
 if isinstance(value, Q): return [value.numerator, value.denominator]
 if isinstance(value, L): return [[e,c.numerator,c.denominator] for e,c in value.terms]
 if isinstance(value, G): return {'real':encode(value.re),'imag':encode(value.im)}
 if isinstance(value, dict): return {str(k):encode(v) for k,v in sorted(value.items())}
 if isinstance(value, (list,tuple)): return [encode(v) for v in value]
 if isinstance(value, (str,int,bool)) or value is None: return value
 raise TypeError('unsupported exact record type: '+str(type(value)))

def require(label,actual,expected):
 if actual!=expected: raise RuntimeError('exact identity failed: '+label)
 RECORDS.append({'name':label,'value':encode(actual)})

def reject(label,actual,corruption):
 if actual==corruption: raise RuntimeError('corruption control was ineffective: '+label)
 CONTROLS.append(label)

def jet(a,lo,hi): return [a.get(k,G()) for k in range(lo,hi+1)]


V=polynomial({1:1}); a=V**-1-1; kappa=V**-2-Q(13,8)*V**-1
K1=(516*V**-5-528*V**-4-393*V**-3)/7168
v0=Q(8,13)


def profile(beta):
 marked=ts(a)
 A=scaled(exp_i({1:G(7),3:G(beta)}),-1)
 B=scaled(exp_i({1:G(-1),3:G(beta)}),-1)
 ua=invert(minus(marked,A));ub=invert(minus(marked,B))
 tr=plus(scaled(ua,2),scaled(ub,8));det=scaled(times(ua,ub),9)
 discr=sqrt_t(minus(tp(tr,2),scaled(det,4)))
 qn=scaled(minus(tr,discr),Q(1,2));qf=scaled(plus(tr,discr),Q(1,2))
 F=plus(scaled(norm(ub),6),norm(qn),norm(qf));gap=minus(F,ts(16*V))
 da=minus(ua,ts(V));db=minus(ub,ts(V))
 energy=plus(times(da,conj(da)),scaled(times(db,conj(db)),7))
 rem=plus(minus(gap,scaled(energy,kappa)),scaled(tp(energy,2),K1))
 for n in range(6): require('family '+str(beta)+' quartic baseline t^'+str(n),rem.get(n,G()),G())
 return A,B,ua,ub,qn,qf,gap,energy,rem


def pmul(a,b):
 """Polynomial convolution; coefficients are formal t jets."""
 out=[{} for _ in range(len(a)+len(b)-1)]
 for j,x in enumerate(a):
  for k,y in enumerate(b): out[j+k]=plus(out[j+k],times(x,y))
 return out

def ppow(a,n):
 out=[ts(1)]
 for _ in range(n): out=pmul(out,a)
 return out

def pplus(a,b):
 return [plus(a[j] if j<len(a) else {},b[j] if j<len(b) else {})
         for j in range(max(len(a),len(b)))]

def pscale(a,c): return [times(x,c) for x in a]
def pdiff(a): return [scaled(a[j],j) for j in range(1,len(a))]
def peval(a,x):
 out={}
 for c in reversed(a): out=plus(times(out,x),c)
 return out

def reciprocal_numerator(dp):
 """q^8 dp(a-1/q), derived directly by the binomial theorem."""
 out=[{} for _ in range(9)]
 for j,c in enumerate(dp):
  for k in range(j+1):
   out[8-k]=plus(out[8-k],scaled(c,(-1)**k*comb(j,k)*a**(j-k)))
 return out

def mean_checks():
 profiles={b:profile(b) for b in (0,-1,1,2)}
 P0=profiles[0][-1][6].re
 linear=(profiles[1][-1][6].re-profiles[-1][-1][6].re)/2
 quad=(profiles[1][-1][6].re+profiles[-1][-1][6].re)/2-P0
 require('generic sextic mean constant',P0,
         Q(931,2)*V**3+Q(15897,8)*V**4-Q(168525,32)*V**5
         -Q(9639,8)*V**6+Q(678993,128)*V**7)
 require('generic sextic mean linear',linear,
         -196*V**3+Q(1197,2)*V**4-Q(945,2)*V**5)
 require('generic sextic mean quadratic',quad,5*V**3)
 require('fourth mean value checks degree-two interpolation',
         profiles[2][-1].get(6,G()),G(P0+2*linear+4*quad))
 for b,p in profiles.items():
  require('mean profile '+str(b)+' leading exact energy',p[-2].get(2,G()),G(56*V**4))
  require('mean profile '+str(b)+' conjugation parity',
          [p[-2].get(k,G()) for k in (1,3,5,7)], [G()]*4)
  require('mean profile '+str(b)+' sextic real',p[-1][6].im,L())
 beta=-linear/(10*V**3)
 require('analytic leading stationary mean',beta,(392-1197*V+945*V**2)/20)
 require('stationary quadratic completion',linear+10*V**3*beta,L())
 require('mean coefficient at cutoff',beta.evaluate(v0),Q(112,169))
 require('mean coefficient at a=0',beta.evaluate(Q(1)),Q(7))
 require('mean coefficient at a=1',beta.evaluate(Q(1,2)),Q(119,80))
 require('mean formula in original marked radius',
         beta*20*(a+1)**2,392*a**2-413*a+140)
 Dcut=(P0-linear**2/(20*V**3)).evaluate(v0)/(56**3*v0**12)
 require('credited cutoff sextic baseline reproduced',Dcut,
         Q(520320727875,6734508720128))
 require('credited quartic at cutoff',K1.evaluate(v0),Q(560235,8388608))
 reject('incorrect stationary mean sign',beta,-beta)
 return profiles

def characteristic_checks(p):
 A,B,ua,u,qn,qf,_,_,_=p
 zm=[scaled(ts(a),-1),ts(1)]
 za=[scaled(A,-1),ts(1)];zb=[scaled(B,-1),ts(1)]
 p0=pmul(pmul(zm,za),ppow(zb,7))
 # Paired angular direction has S=2, hence this is p_epsilon's eps^2 term.
 p2=pscale(pmul(pmul(pmul([{},ts(1)],zm),za),ppow(zb,5)),B)
 dp0=pdiff(p0);dp2=pdiff(p2);normal=peval(dp0,ts(a))
 C0=pscale(reciprocal_numerator(dp0),invert(normal))
 C2=pplus(pscale(reciprocal_numerator(dp2),invert(normal)),
          pscale(C0,scaled(divide(peval(dp2,ts(a)),normal),-1)))
 w=[scaled(u,-1),ts(1)]
 qpoly=[{},ts(1)]
 qr=[scaled(times(ua,u),9),scaled(plus(scaled(ua,2),scaled(u,8)),-1),ts(1)]
 up=scaled(times(B,tp(u,2)),G(0,1))
 upp=plus(scaled(times(B,tp(u,2)),-1),scaled(times(tp(B,2),tp(u,3)),-2))
 c2=tp(up,2)
 # From C=(8q-9ua) PB - q(q-ua) PB', with PB=(q-u)^7.
 R=pscale(pplus(
       pmul([scaled(ua,-9),ts(8)],pplus(pscale(ppow(w,2),upp),pscale(w,c2))),
       pscale(pmul(pmul(qpoly,[scaled(ua,-1),ts(1)]),
                  pplus(pscale(w,scaled(upp,6)),[scaled(c2,5)])),ts(-1))),ts(Q(-1,2)))
 R=R+[{}]*(4-len(R))
 for j,(x,y) in enumerate(zip(C0,pmul(ppow(w,6),qr))):
  require('original derivative versus reciprocal C0 q^'+str(j),jet(x,0,8),jet(y,0,8))
 expected_C2=pscale(pmul(ppow(w,4),R),ts(2))
 expected_C2 += [{}]*(len(C2)-len(expected_C2))
 for j,(x,y) in enumerate(zip(C2,expected_C2)):
  require('original derivative versus reciprocal C2 q^'+str(j),jet(x,0,8),jet(y,0,8))
 # Values/residues are checked only through order two after Laurent division.
 Q0=scaled(times(u,minus(ua,u)),7)
 Qp=plus(scaled(ua,-2),scaled(u,-6))
 R0=scaled(times(c2,u,minus(u,ua)),Q(5,2))
 Rp=plus(scaled(times(upp,u,minus(u,ua)),3),times(c2,plus(u,scaled(ua,2))))
 require('reciprocal residue numerator R(u)',jet(peval(R,u),0,6),jet(R0,0,6))
 require('reciprocal residue numerator derivative Rprime(u)',
         jet(peval(pdiff(R),u),0,6),jet(Rp,0,6))
 Ccl_alt=scaled(minus(divide(Rp,Q0),divide(times(R0,Qp),tp(Q0,2))),-1)
 squared_alt=scaled(divide(R0,Q0),-2)
 require('first cluster squared trace from reciprocal polynomial',
         jet(squared_alt,0,2),jet(scaled(c2,Q(5,7)),0,2))
 return R,qr,Ccl_alt

def shape_checks(p,tag,independent=None):
 A,B,ua,u,qn,qf,gap,energy,_=p
 Ccl=plus(scaled(times(B,tp(u,2)),-Q(3,7)),
          scaled(divide(times(tp(B,2),tp(u,2)),minus(B,A)),-Q(1,49)),
          scaled(times(tp(B,2),tp(u,3)),-Q(34,49)))
 if independent:
  R,qr,Ccl_alt=independent
  require('cluster original residue versus reciprocal residue',
          jet(Ccl,-2,2),jet(Ccl_alt,-2,2))
 variance=scaled(times(norm(u),tp(rr(times(B,u)),2)),Q(5,14))
 F2=plus(divide(rr(times(Ccl,conj(u))),norm(u)),variance)
 simple=[]
 for label,q in [('near',qn),('far',qf)]:
  z=minus(ts(a),invert(q));H=times(minus(z,ts(a)),minus(z,A))
  Qprime=minus(scaled(z,18),plus(scaled(plus(ts(a),A),8),scaled(B,2)))
  dq=scaled(divide(times(B,tp(q,2),H,plus(z,B)),times(tp(minus(z,B),2),Qprime)),Q(1,2))
  simple.append(dq)
  if independent:
   alt=scaled(divide(peval(R,q),times(tp(minus(q,u),2),peval(pdiff(qr),q))),-1)
   require(label+' simple root original versus reciprocal coefficient',
           jet(dq,-2,2),jet(alt,-2,2))
  F2=plus(F2,divide(rr(times(dq,conj(q))),norm(q)))
 up=scaled(times(B,tp(u,2)),G(0,1))
 upp=plus(scaled(times(B,tp(u,2)),-1),scaled(times(tp(B,2),tp(u,3)),-2))
 require('total reciprocal second trace '+tag,
         jet(plus(Ccl,*simple),-2,2),jet(upp,-2,2))
 E2=plus(times(up,conj(up)),rr(times(minus(u,ts(V)),conj(upp))))
 lagrange=divide(deriv(gap),deriv(energy))
 shape=minus(F2,times(lagrange,E2))
 require('constrained shape lower cancellations '+tag,jet(shape,-2,1),[G()]*4)
 expected=Q(101,14)*V**3-Q(179,28)*V**4-Q(1859,224)*V**5
 require('generic transverse leading coefficient '+tag,shape.get(2,G()),G(expected))
 if tag=='zero mean':
  require('transverse coefficient at cutoff',expected.evaluate(v0),Q(83200,2599051))
  require('transverse formula in original marked radius',
          expected*224*(1+a)**5,1616*a**2+1800*a-1675)
  require('curvature below cutoff at a=3/5',
          (1616*a**2+1800*a-1675).evaluate(Q(5,8)),Q(-331,25))
  require('curvature numerator at a=5/8',
          (1616*a**2+1800*a-1675).evaluate(v0),Q(325,4))
  require('unique positive threshold discriminant',
          1800**2+4*1616*1675,6400*2198)
  require('positive derivative formula',-V**2*expected.derivative(),
          (10175-3968*a-4848*a**2)/(224*(1+a)**6))
  require('derivative numerator lower endpoint at a=1',
          Q(10175)-3968-4848,Q(1359))
  reject('omit cluster modulus curvature',shape.get(2,G()),minus(shape,variance).get(2,G()))
  reject('omit fixed-energy multiplier',shape.get(0,G()),F2.get(0,G()))
  reject('flip cluster residue sign',jet(shape,-1,2),
         jet(minus(shape,scaled(divide(rr(times(Ccl,conj(u))),norm(u)),2)),-1,2))
 return expected

def compression_checks():
 # P=I-J/7 on the seven-root coordinates. Verify the complete coefficient
 # matrix of tr(P diag(eta) P)^2, not a finite random direction sample.
 P=[[Q(int(i==j))-Q(1,7) for j in range(7)] for i in range(7)]
 square=[[sum((P[i][k]*P[k][j] for k in range(7)),Q()) for j in range(7)] for i in range(7)]
 require('orthogonal compression projector idempotent',square,P)
 require('compression kills the common vector',[sum(row) for row in P],[Q()]*7)
 require('six-dimensional compression trace',sum(P[j][j] for j in range(7)),Q(6))
 gram=[[P[i][j]**2 for j in range(7)] for i in range(7)]
 wanted=[[Q(5,7)*int(i==j)+Q(1,49) for j in range(7)] for i in range(7)]
 require('full squared-trace coefficient matrix',gram,wanted)
 require('compression first trace balanced identity',[P[j][j] for j in range(7)],[Q(6,7)]*7)
 reject('wrong cluster variance dimension factor',Q(5,7),Q(6,7))

def radial_collapse_checks():
 # Here the formal variable is the inward depth s, not the balanced angle t.
 # One original root is -1+s and the other seven are -1. The two residual
 # critical reciprocals stay analytic with positive constants V,9V.
 A={0:G(-1),1:G(1)};B=ts(-1)
 ua=invert(minus(ts(a),A));u=invert(minus(ts(a),B))
 tr=plus(scaled(ua,2),scaled(u,8));det=scaled(times(ua,u),9)
 disc=sqrt_t(minus(tp(tr,2),scaled(det,4)))
 qn=scaled(minus(tr,disc),Q(1,2));qf=scaled(plus(tr,disc),Q(1,2))
 F=plus(scaled(norm(u),6),norm(qn),norm(qf))
 energy=times(minus(ua,ts(V)),conj(minus(ua,ts(V))))
 require('actual inward original-root reciprocal derivative',ua.get(1,G()),G(V**2))
 require('actual inward critical near derivative',qn.get(1,G()),G(Q(7,8)*V**2))
 require('actual inward critical far derivative',qf.get(1,G()),G(Q(9,8)*V**2))
 require('actual inward true objective derivative at collapse',F.get(1,G()),G(2*V**2))
 require('actual inward energy derivative at collapse',energy.get(1,G()),G())
 require('actual inward energy quadratic at collapse',energy.get(2,G()),G(V**4))

def integral(a,constant):
 return plus(ts(constant),{k+1:x/Q(k+1) for k,x in a.items() if 0<=k<MAX})

def scalar_support_checks():
 # Exact jets in the real argument x; analyticity/harmonicity in the written
 # proof gives the inequalities. These controls check both matched first
 # derivatives and the positive normal curvature identity.
 for name,q0,c in [('3+4i',G(3,4),G(2,-1)),
                   ('5-12i',G(5,-12),G(-3,2)),
                   ('formal positive V',G(V),G(0,V**2))]:
  p={0:q0,1:c};pref={0:q0.conjugate(),1:c.conjugate()}
  r=sqrt_t(times(p,pref));fp=divide(scaled(pref,c),r)
  f=integral(fp,r[0]);ny=divide(rr(scaled(pref,G(0,1)*c)),r)
  require('scalar support line value '+name,jet(rr(f),0,6),jet(r,0,6))
  require('scalar support normal first derivative '+name,
          jet(rr(scaled(fp,G(0,1))),0,6),jet(ny,0,6))
  normyy=minus(divide(ts(c.re**2+c.im**2),r),divide(tp(ny,2),r))
  require('scalar support positive normal curvature '+name,
          jet(plus(normyy,rr(deriv(fp))),0,5),
          jet(divide(ts(c.re**2+c.im**2),r),0,5))
  if name=='3+4i':
   wrong=divide(scaled(pref,c.conjugate()),r)
   reject('wrong holomorphic derivative conjugation',fp.get(0,G()),wrong.get(0,G()))
 # Universal Laplacian numerator identity as sparse polynomials in x,y,u,v.
 def add(a,b):
  d=dict(a)
  for m,c in b.items():d[m]=d.get(m,0)+c
  return {m:c for m,c in d.items() if c}
 def mul(a,b):
  d={}
  for m,c in a.items():
   for n,e in b.items():
    z=tuple(i+j for i,j in zip(m,n));d[z]=d.get(z,0)+c*e
  return {m:c for m,c in d.items() if c}
 x,y,u,v=[{tuple(int(j==i) for j in range(4)):1} for i in range(4)]
 dot=add(mul(x,u),mul(y,v))
 cross=add(mul(y,u),{m:-c for m,c in mul(x,v).items()})
 left=add(mul(dot,dot),mul(cross,cross))
 right=mul(add(mul(x,x),mul(y,y)),add(mul(u,u),mul(v,v)))
 # Tuple dictionary keys are encoded as readable exponent strings explicitly.
 require('universal scalar Laplacian numerator',
         {','.join(map(str,k)):v for k,v in left.items()},
         {','.join(map(str,k)):v for k,v in right.items()})

def fixture():
 profiles=mean_checks()
 independent=characteristic_checks(profiles[0])
 for beta,tag in [(0,'zero mean'),(-1,'negative cubic mean'),(1,'positive cubic mean')]:
  shape_checks(profiles[beta],tag,independent if beta==0 else None)
 compression_checks();radial_collapse_checks();scalar_support_checks()
 # Seventh control checks that the pinned evidence cannot silently change.
 digest=sha256(json.dumps(RECORDS,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 reject('record digest corruption',digest,'0'*64)
 return {'schema':1,'agent':'six-sendov-3','role':'researcher',
         'status':'exact algebra controls; analytic proof remains ordinary written proof',
         'arithmetic':'Q[V,V^-1][i], exact formal t jets with order-eight input',
         'mean_profiles':[0,-1,1,2],'transverse_profiles':[0,-1,1],
         'identity_count':len(RECORDS),'corruption_control_count':len(CONTROLS),
         'corruption_controls':CONTROLS,'record_sha256':digest,
         'beta_cutoff':[112,169],'Dstar_baseline':[520320727875,6734508720128],
         'transverse_cutoff':[83200,2599051],
         'a_star_polynomial':[1616,1800,-1675],
         'reported_curvature_L_of_V':encode(Q(101,14)*V**3-Q(179,28)*V**4-Q(1859,224)*V**5)}

def main():
 if sys.argv[1:] not in ([],['--emit-fixture']):
  raise SystemExit('usage: python3 -I -B verify.py [--emit-fixture]')
 result=fixture();path=Path(__file__).with_name('expected.json')
 if sys.argv[1:]==['--emit-fixture']:
  path.write_text(json.dumps(result,indent=2)+'\n')
 else:
  try: expected=json.loads(path.read_text())
  except (OSError,ValueError) as exc: raise RuntimeError('required complete expected.json is absent or malformed') from exc
  if expected!=result: raise RuntimeError('complete expected fixture mismatch')
 print(json.dumps(result,sort_keys=True))

if __name__=='__main__': main()
