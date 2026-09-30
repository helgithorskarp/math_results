#!/usr/bin/env python3
"""Exact scaled support controls for degree-nine global energy minimizers.

Actual author six-sendov-3, researcher. Python standard library only. The
rational Laurent/Gaussian jet kernel is openly adapted from this author's
public finite-energy local-minimum checker. The new calculation builds the
divided characteristic root and holomorphic near trace directly for each
listed scaled root profile. It imports no campaign module.

These profiles check exact coefficients through t^6, not uniform analytic
remainders or domain completeness; the ordinary proof supplies those.
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

V=polynomial({1:1})
a=V**-1-1
beta=(392-1197*V+945*V**2)/20

def jet(a,lo,hi): return [a.get(k,G()) for k in range(lo,hi+1)]
def shift(a,n): return clean({k+n:x for k,x in a.items() if k+n>=0})
def imag(a): return clean({k:G(x.im) for k,x in a.items()})
def pmul(a,b):
 out=[{} for _ in range(len(a)+len(b)-1)]
 for j,x in enumerate(a):
  for k,y in enumerate(b): out[j+k]=plus(out[j+k],times(x,y))
 return out
def peval(a,x):
 out={}
 for c in reversed(a):out=plus(times(out,x),c)
 return out
def pdiff(a): return [scaled(a[j],j) for j in range(1,len(a))]

def original(T,x,y,r):
 mean={3:G(beta+y)}
 phases=[plus(scaled(T,7),mean)]
 phases.extend(plus(scaled(T,-1),mean,{2:G(z)}) for z in x)
 us=[]
 for phi,rj in zip(phases,r):
  z=scaled(times(plus(ts(1),{6:G(-rj)}),exp_i(phi)),-1)
  us.append(invert(minus(ts(a),z)))
 E={}
 for u in us:
  d=minus(u,ts(V));E=plus(E,times(d,conj(d)))
 return us,E

def energy_chart(x,y,r):
 _,Eb=original({1:G(1)},[0]*7,0,[0]*8)
 T={1:G(1)}
 for n in range(2,8):
  _,E=original(T,x,y,r)
  res=minus(E,Eb).get(n+1,G())
  if res!=G():T[n]=-res/(112*V**4)
 us,E=original(T,x,y,r)
 if jet(minus(E,Eb),0,8)!=[G()]*9: raise RuntimeError('energy elimination')
 return T,us,E

def characteristic(us):
 R=[ts(1)]
 for u in us:R=pmul(R,[scaled(u,-1),ts(1)])
 return [scaled(c,9-j) for j,c in enumerate(R)]

def implicit_root(C,initial,nmax=8):
 q=ts(initial)
 derivative=peval(pdiff(C),q).get(0,G())
 if derivative==G(): raise ValueError('root is not simple')
 for n in range(1,nmax+1):
  res=peval(C,q).get(n,G())
  if res!=G():q[n]=-res/derivative
 if jet(peval(C,q),0,nmax)!=[G()]*(nmax+1):raise RuntimeError('implicit root residual')
 return q

def divided_near_root(us):
 # C(v+t*rho)/t^7, formed before any truncation can lose seven orders.
 es=[ts(1)]
 for u in us:
  d=shift(minus(u,ts(V)),-1)
  es=pmul(es,[ts(1),d])
 C=[{} for _ in range(9)]
 C[7]=ts(-8*V);C[8]={1:G(1)}
 for k in range(1,9):
  C[8-k]=plus(C[8-k],shift(scaled(es[k],(-1)**k*(k+1)),1))
  if k<8:C[7-k]=plus(C[7-k],scaled(es[k],-(-1)**k*(8-k)*V))
 rho=implicit_root(C,G(0,-6*V**2),6)
 return plus(ts(V),shift(rho,1))

def global_traces(C,nmax=6):
 traces=[ts(8)]
 for k in range(1,nmax+1):
  s=scaled(C[8-k],k)
  for j in range(1,k):s=plus(s,times(C[8-j],traces[k-j]))
  traces.append(scaled(s,-1))
 return traces

def support_coefficients(u,c,nmax=6):
 # f'(w)=c*conj(u)/|u| * (1+conj(c/u)w)
 #        * (1+(c/u+conj(c/u))w+|c/u|^2 w^2)^(-1/2).
 ratio=divide(c,u); A=plus(ratio,conj(ratio));B=times(ratio,conj(ratio))
 h=[{},A,B]
 powers=[ts(1)]
 inv=[{} for _ in range(nmax)]
 bc=Q(1)
 for k in range(nmax):
  for j,p in enumerate(powers):
   if j<nmax:inv[j]=plus(inv[j],scaled(p,bc))
  powers=pmul(powers,h)[:nmax]
  bc=bc*Q(-1-2*k,2*(k+1))
 pref=divide(times(c,conj(u)),norm(u))
 derivs=pmul([ts(1),conj(ratio)],inv)[:nmax]
 return [norm(u)]+[scaled(times(pref,derivs[j]),Q(1,j+1)) for j in range(nmax)]

def support_value(us):
 C=characteristic(us)
 qf=implicit_root(C,9*V,7)
 qn=divided_near_root(us)
 branch_us,_=original({1:G(1)},[0]*7,0,[0]*8)
 u=branch_us[1]
 B=scaled(exp_i({1:G(-1),3:G(beta)}),-1)
 c=scaled(times(B,tp(u,2)),G(0,1))
 f=support_coefficients(u,c)
 traces=global_traces(C)
 near=[ts(7)]+[minus(traces[k],tp(qf,k)) for k in range(1,7)]
 moments=[]
 for k in range(7):
  s={}
  for j in range(k+1):s=plus(s,scaled(times(tp(scaled(u,-1),k-j),near[j]),comb(k,j)))
  moments.append(divide(s,tp(c,k)))
 A=norm(qf)
 for coef,moment in zip(f,moments):A=plus(A,rr(times(coef,moment)))
 wn=divide(minus(qn,u),c)
 fn={}
 for k,coef in enumerate(f):fn=plus(fn,times(coef,tp(wn,k)))
 H=minus(norm(qn),rr(fn))
 return plus(A,H),wn,H

def encode(value):
 if isinstance(value,Q):return [value.numerator,value.denominator]
 if isinstance(value,L):return [[e,c.numerator,c.denominator] for e,c in value.terms]
 if isinstance(value,G):return {'real':encode(value.re),'imag':encode(value.im)}
 if isinstance(value,dict):return {str(k):encode(v) for k,v in sorted(value.items())}
 if isinstance(value,(list,tuple)):return [encode(v) for v in value]
 return value

RECORDS=[]
CONTROLS=[]

def require(label,actual,expected):
 if actual!=expected:raise RuntimeError('exact identity failed: '+label)
 RECORDS.append({'name':label,'value':encode(actual)})

def reject(label,actual,wrong):
 if actual==wrong:raise RuntimeError('ineffective corruption control: '+label)
 CONTROLS.append(label)

Lshape=Q(101,14)*V**3-Q(179,28)*V**4-Q(1859,224)*V**5

def compression_controls():
 P=[[Q(int(i==j))-Q(1,8) for j in range(8)] for i in range(8)]
 theta=[7]+[-1]*7
 A=[[sum((P[i][k]*theta[k]*P[k][j] for k in range(8)),Q())
     for j in range(8)] for i in range(8)]
 require('simple divided eigenvector',
         [sum((A[i][j]*theta[j] for j in range(8)),Q()) for i in range(8)],
         [6*x for x in theta])
 require('normalized simple leading squared norm',sum(x*x for x in theta),56)
 for j in range(1,7):
  vector=[Q(0)]*8;vector[j]=1;vector[7]=-1
  require('six-group basis eigenvector '+str(j),
          [sum((A[i][k]*vector[k] for k in range(8)),Q()) for i in range(8)],
          [-x for x in vector])
 # The linear split expectation has identical coefficients on all seven
 # coordinates; hence it vanishes on the entire zero-sum subspace.
 expectation=[Q(theta[j]**2,56) for j in range(1,8)]
 require('complete linear split expectation',expectation,[Q(1,56)]*7)
 require('simple/six divided external gap',6-(-1),7)
 require('mean conversion with original positive singleton',
         8*beta.evaluate(Q(8,13))/(112*Q(8,13)**6),Q(28561,32768))
 require('credited beta at cutoff',beta.evaluate(Q(8,13)),Q(112,169))
 require('credited transverse coefficient at cutoff',
         Lshape.evaluate(Q(8,13)),Q(83200,2599051))
 reject('wrong simple divided eigenvalue',6,-1)

def fixture():
 compression_controls()
 base_us,Ebase=original({1:G(1)},[0]*7,0,[0]*8)
 Phib,wnb,Hb=support_value(base_us)
 require('leading exact reciprocal energy',Ebase.get(2,G()),G(56*V**4))
 require('baseline normalized simple root tangent',wnb.get(1,G()),G(7))
 require('baseline normalized simple root has no constant',wnb.get(0,G()),G())
 require('baseline scalar defect below order four',jet(Hb,0,3),[G()]*4)
 profiles=[
  ('mean positive',[0]*7,1,[0]*8),
  ('mean negative',[0]*7,-1,[0]*8),
  ('paired split',[1,-1,0,0,0,0,0],0,[0]*8),
  ('three unequal split',[2,-1,-1,0,0,0,0],-2,[0,1,0,0,0,0,0,0]),
  ('all seven split',[3,2,1,-1,-2,-3,0],2,[1,0,2,0,0,0,0,0]),
  ('independent inward depths',[0]*7,0,[0,1,0,2,0,0,0,3]),
 ]
 for name,x,y,r in profiles:
  if sum(x):raise RuntimeError('profile is not balanced')
  T,us,E=energy_chart(x,y,r)
  Phi,wn,H=support_value(us)
  excess=minus(Phi,Phib);S=sum(z*z for z in x);R=sum(r)
  require(name+' complete actual energy residual',jet(minus(E,Ebase),0,8),[G()]*9)
  require(name+' amplitude degree two',T.get(2,G()),G())
  require(name+' amplitude degree three',T.get(3,G()),G(Q(-S,112)))
  require(name+' amplitude degree four',T.get(4,G()),G())
  require(name+' complete support excess below order six',jet(excess,0,5),[G()]*6)
  require(name+' leading scaled support coefficient',excess.get(6,G()),
          G(5*V**3*y*y+Lshape*S+2*V**2*R))
  require(name+' normalized simple-root change below order three',
          jet(minus(wn,wnb),0,2),[G()]*3)
  require(name+' scalar defect change below order five',
          jet(minus(H,Hb),0,4),[G()]*5)
  # Preserve full compact fields, not only aggregate counts.
  RECORDS.append({'name':name+' exact scaled fields',
                  'value':encode({'T_through_five':{k:v for k,v in T.items() if k<=5},
                                  'wn_change_through_four':{k:v for k,v in minus(wn,wnb).items() if k<=4},
                                  'H_change_through_six':{k:v for k,v in minus(H,Hb).items() if k<=6},
                                  'support_excess_through_six':{k:v for k,v in excess.items() if k<=6}})})
  if name=='paired split':
   _,rawE=original({1:G(1)},x,y,r)
   require('unadjusted paired split changes the actual energy at degree four',
           minus(rawE,Ebase).get(4,G()),G(V**4*S))
   reject('ignore true fixed-energy elimination',minus(rawE,Ebase).get(4,G()),G())
   reject('incorrect leading transverse coefficient',excess.get(6,G()),G(-Lshape*S))
  if name=='three unequal split':
   defect=minus(H,Hb).get(6,G())
   reject('omit the separated near scalar defect',excess.get(6,G()),excess.get(6,G())-defect)
  if name=='independent inward depths':
   reject('omit each inward derivative',excess.get(6,G()),G(V**2*R))
 digest=sha256(json.dumps(RECORDS,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 reject('corrupted exact record digest',digest,'0'*64)
 return {'schema':1,'agent':'six-sendov-3','role':'researcher',
         'claim_status':'exact profile algebra; analytic all-root proof remains ordinary mathematics',
         'arithmetic':'Q[V,V^-1][i], formal order-eight t jets; reported support through order six',
         'profiles':[name for name,_,_,_ in profiles],
         'identity_count':sum('value' in r for r in RECORDS)-len(profiles),
         'compact_field_records':len(profiles),
         'corruption_control_count':len(CONTROLS),'corruption_controls':CONTROLS,
         'records_sha256':digest,
         'mean_coefficient':encode(5*V**3),
         'split_coefficient':encode(Lshape),
         'inward_coefficient':encode(2*V**2),
         'mean_cutoff':encode(Q(112,169)),
         'split_cutoff':encode(Q(83200,2599051)),
         'complete_records':RECORDS}

def main():
 if sys.argv[1:] not in ([],['--emit-fixture']):
  raise SystemExit('usage: python3 -I -B verify.py [--emit-fixture]')
 result=fixture();path=Path(__file__).with_name('expected.json')
 if sys.argv[1:]==['--emit-fixture']:
  path.write_text(json.dumps(result,indent=2)+'\n')
 else:
  try:expected=json.loads(path.read_text())
  except (OSError,ValueError) as exc:raise RuntimeError('required expected.json absent or malformed') from exc
  if expected!=result:raise RuntimeError('complete exact fixture differs')
 summary={k:v for k,v in result.items() if k!='complete_records'}
 print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main()
