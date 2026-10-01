#!/usr/bin/env python3
"""Exact actual-family jets and comparison-boundary certificates.

Actual author six-sendov-3, role researcher. Standard library only.
All coefficient algebra is exact. Uniform analytic arguments and cited
all-balanced geometry remain ordinary written mathematics in PROOF.md.
The literal original-polynomial route adapts the credited local review;
the supplementary far secular route adapts the full-radius review.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from math import factorial, comb
from pathlib import Path

class L:
 def __init__(self,x=0):
  self.d=dict(x.d) if isinstance(x,L) else {int(k):Q(v) for k,v in x.items()} if isinstance(x,dict) else {0:Q(x)}
  self.d={k:v for k,v in self.d.items() if v}
 def __add__(self,x):
  if isinstance(x,(G,J)):return NotImplemented
  x=L(x);d=dict(self.d)
  for k,v in x.d.items():d[k]=d.get(k,Q(0))+v
  return L(d)
 __radd__=__add__
 def __neg__(self):return L({k:-v for k,v in self.d.items()})
 def __sub__(self,x):
  if isinstance(x,(G,J)):return NotImplemented
  return self+-L(x)
 def __rsub__(self,x):return L(x)+-self
 def __mul__(self,x):
  if isinstance(x,(G,J)):return NotImplemented
  x=L(x);d={}
  for k,v in self.d.items():
   for j,w in x.d.items():d[k+j]=d.get(k+j,Q(0))+v*w
  return L(d)
 __rmul__=__mul__
 def inv(self):
  if len(self.d)!=1:raise RuntimeError('only monomial Laurent inverses supported')
  k,v=next(iter(self.d.items()));return L({-k:1/v})
 def __truediv__(self,x):
  if isinstance(x,(G,J)):return NotImplemented
  return self*L(x).inv()
 def __rtruediv__(self,x):return L(x)*self.inv()
 def __pow__(self,n):
  if n<0:return self.inv()**(-n)
  r=L(1)
  for _ in range(n):r*=self
  return r
 def __bool__(self):return bool(self.d)
 def __eq__(self,x):return self.d==L(x).d
 def encode(self):return [[k,v.numerator,v.denominator] for k,v in sorted(self.d.items())]
 def __repr__(self):return str(self.encode())

class G:
 def __init__(self,re=0,im=0):
  if isinstance(re,G):self.re,self.im=re.re,re.im
  else:self.re,self.im=L(re),L(im)
 def __add__(self,x):
  if isinstance(x,J):return NotImplemented
  x=G(x);return G(self.re+x.re,self.im+x.im)
 __radd__=__add__
 def __neg__(self):return G(-self.re,-self.im)
 def __sub__(self,x):
  if isinstance(x,J):return NotImplemented
  return self+-G(x)
 def __rsub__(self,x):return G(x)+-self
 def __mul__(self,x):
  if isinstance(x,J):return NotImplemented
  x=G(x);return G(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
 __rmul__=__mul__
 def __truediv__(self,x):
  if isinstance(x,J):return NotImplemented
  x=G(x)
  if x.im:raise RuntimeError('only real Gaussian divisors needed')
  return G(self.re/x.re,self.im/x.re)
 def conjugate(self):return G(self.re,-self.im)
 def __bool__(self):return bool(self.re) or bool(self.im)
 def __eq__(self,x):x=G(x);return self.re==x.re and self.im==x.im
 def encode(self):return {'re':self.re.encode(),'im':self.im.encode()}

class J:
 N=6
 def __init__(self,x=0):
  data=list(x.c) if isinstance(x,J) else list(x) if isinstance(x,(tuple,list)) else [x]
  self.c=[G(y) for y in data[:self.N+1]]+[G() for _ in range(max(0,self.N+1-len(data)))]
 def __add__(self,x):x=J(x);return J([a+b for a,b in zip(self.c,x.c)])
 __radd__=__add__
 def __neg__(self):return J([-a for a in self.c])
 def __sub__(self,x):return self+-J(x)
 def __rsub__(self,x):return J(x)+-self
 def __mul__(self,x):
  x=J(x);return J([sum((self.c[j]*x.c[k-j] for j in range(k+1)),G()) for k in range(self.N+1)])
 __rmul__=__mul__
 def inverse(self):
  b=[G(1)/self.c[0]]
  for k in range(1,self.N+1):b.append(-sum((self.c[j]*b[k-j] for j in range(1,k+1)),G())/self.c[0])
  return J(b)
 def __truediv__(self,x):return self*J(x).inverse()
 def __rtruediv__(self,x):return J(x)*self.inverse()
 def __pow__(self,n):
  r=J(1)
  for _ in range(n):r*=self
  return r
 def conjugate(self):return J([x.conjugate() for x in self.c])
 def sqrt(self,constant):
  b=[G(constant)]
  if b[0]*b[0]!=self.c[0]:raise RuntimeError('wrong square-root constant')
  for k in range(1,self.N+1):b.append((self.c[k]-sum((b[j]*b[k-j] for j in range(1,k)),G()))/(2*constant))
  return J(b)
 def modulus(self):
  if self.c[0].im:raise RuntimeError('nonreal initial reciprocal')
  return (self*self.conjugate()).sqrt(self.c[0].re)
 def __eq__(self,x):return self.c==J(x).c
 def encode(self):return [x.encode() for x in self.c]

def exp_i(phi):
 r=J();term=J(1)
 for k in range(J.N+1):
  r+=term/factorial(k);term*=G(0,1)*phi
 return r

def evaluate(cs,x):
 out=J()
 for c in reversed(cs):out=out*x+c
 return out

def implicit(cs,const):
 root=J(const);dc=[j*cs[j] for j in range(1,len(cs))];linear=evaluate(dc,root).c[0]
 if not linear:raise RuntimeError('vanishing simple implicit derivative')
 for k in range(1,J.N+1):root.c[k]=-evaluate(cs,root).c[k]/linear
 if evaluate(cs,root)!=J():raise RuntimeError('complete implicit residual failed')
 return root

def real(x):
 if x.im:raise RuntimeError('uncancelled imaginary coefficient')
 return x.re

def polynomial_product(a,b):
 out=[J() for _ in range(len(a)+len(b)-1)]
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out

CHECKS=[]
SIGNS=[]
RECORDS={}

def demand(condition, message):
 if not condition:raise RuntimeError(message)

def wire(value):
 if isinstance(value,(str,int)):return value
 if hasattr(value,'encode'):return value.encode()
 if isinstance(value,Q):return [value.numerator,value.denominator]
 if isinstance(value,(list,tuple)):return [wire(x) for x in value]
 return value

def record(name,value):
 demand(name not in RECORDS,'duplicate record '+name)
 RECORDS[name]=wire(value)

def equal(name,value,wanted):
 demand(value==wanted,'exact identity failed: '+name)
 CHECKS.append(name)

def reciprocal_polynomial(physical,a):
 """q^n D(a-1/q)/D(a), normalized with no omitted coefficient."""
 n=len(physical)-1
 normalization=evaluate(physical,J(a))
 out=[J() for _ in range(n+1)]
 for k,coef in enumerate(physical):
  for ell in range(k+1):
   out[n-ell]+=coef*(comb(k,ell)*a**(k-ell)*(-1)**ell)
 return [coef/normalization for coef in out]

def constants():
 v=L({1:1});d=v**-1;a=d-1
 kappa=d*d-Q(13,8)*d
 A=(48*d**5-40*d**4-53*d**3)/512
 B=(16*d**5-104*d**4+203*d**3)/8192
 C=(16*d**5+8*d**4+d**3)/8192
 K1=(516*d**5-528*d**4-393*d**3)/7168
 Kpair=(784*d**5-856*d**4-443*d**3)/16384
 S=(2768*d**5-2456*d**4-3187*d**3)/30720
 PG=2768*a*a+3080*a-2875
 return v,d,a,kappa,A,B,C,K1,Kpair,S,PG

def moving_pair():
 J.N=3
 v,d,a,kappa,A,B,C,K1,Kpair,S,PG=constants()
 e=J([0,1]);x=d**4*e/(4+2*a*d*d*e);c=1-x
 h=v*v+a*e/2;j=2*v+(a*a-1)*e/2
 equal('moving-pair reciprocal product',h,(d*d-2*a*x).inverse())
 equal('moving-pair reciprocal sum',j,2*(d-x)/(d*d-2*a*x))
 energy=2*h-2*v*j+2*v*v
 equal('moving-pair exact energy inverse',energy,e)
 pair=[J(1),2*c,J(1)]
 base=polynomial_product([J(1),J(1)],pair)
 cross=polynomial_product([J(1),J(1)],[2*c,J(2)])
 bracket=[6*p+q for p,q in zip(pair,cross)]
 term=polynomial_product([J(-a),J(1)],bracket)
 physical=[p+q for p,q in zip(base,term)]
 cubic=reciprocal_polynomial(physical,a)
 expected=[-9*v*h,3*h+8*v*j,-2*j-7*v,J(1)]
 for k in range(4):equal('physical reciprocal cubic coefficient '+str(k),cubic[k],expected[k])
 # Credited all-degree moving-pair equation (7328), specialized to m=8.
 # This baseline is reproduced, not claimed as a new construction.
 denominator=d*d-2*a*x
 earlier=[J(-9),16*(a+c)+3*d,-7*denominator-4*d*(a+c),d*denominator]
 earlier=[coef/(d*denominator) for coef in earlier]
 for k in range(4):equal('credited moving-pair normalized cubic '+str(k),cubic[k],earlier[k])
 cutoff=sum((coef*Q(8,13)**power for power,coef in Kpair.d.items()),Q())
 equal('credited moving-pair cutoff coefficient',cutoff,Q(2076165,33554432))
 record('credited earlier moving-pair full reciprocal cubic',earlier)
 record('credited earlier moving-pair cutoff coefficient',cutoff)
 far=implicit(cubic,9*v)
 equal('complete physical far residual',evaluate(cubic,far),J())
 # A different far-root equation, with the same literal original reciprocals.
 def secular(q):return (j*q-2*h)/(q*q-j*q+h)+6*v/(q-v)-1
 qs=J(9*v)
 den=qs*qs-j*qs+h;num=j*qs-2*h
 derivative=j/den-num*(2*qs-j)/(den*den)-6*v/((qs-v)*(qs-v))
 linear=G(-Q(1,8)/v)
 equal('far secular collapse derivative',derivative.c[0],linear)
 for k in range(1,J.N+1):qs.c[k]=-secular(qs).c[k]/linear
 equal('complete far secular residual',secular(qs),J())
 equal('physical versus secular far jet',far,qs)
 product=9*v*h/far
 near_norm=product.sqrt(v)
 F=5*v+far+2*near_norm
 discriminant=(2*j+7*v-far)**2-4*product
 equal('near discriminant constant',discriminant.c[0],G())
 equal('near discriminant linear coefficient',discriminant.c[1],G(Q(-3,2)))
 equal('moving-pair collapsed objective',F.c[0],G(16*v))
 equal('moving-pair linear objective',F.c[1],G(kappa))
 equal('moving-pair quartic objective',F.c[2],G(-Kpair))
 CQ=Q(1127,65536)*d**8-Q(6855,131072)*d**7+Q(52737,1048576)*d**6-Q(28853,2097152)*d**5
 equal('moving-pair cubic energy coefficient',real(F.c[3]),CQ)
 for name,val in [('energy inverse',x),('reciprocal product',h),('reciprocal sum',j),
                  ('physical residual polynomial',physical),('reciprocal residual cubic',cubic),
                  ('far jet',far),('secular far jet',qs),('near product',product),
                  ('near modulus',near_norm),('near discriminant',discriminant),
                  ('energy',energy),('objective',F),('cubic coefficient',CQ)]:
  record('moving pair '+name,val)
 # Actual failure mode: retaining only the linear part of the energy inverse.
 wrong_x=d**4*e/4
 wrong_h=(d*d-2*a*wrong_x).inverse()
 wrong_j=2*(d-wrong_x)*wrong_h
 wrong_cubic=[-9*v*wrong_h,3*wrong_h+8*v*wrong_j,-2*wrong_j-7*v,J(1)]
 wrong_far=implicit(wrong_cubic,9*v)
 wrong_F=5*v+wrong_far+2*(9*v*wrong_h/wrong_far).sqrt(v)
 return CQ,real(F.c[0]-5*v),real(wrong_F.c[3])

def stationary_profile(mean_coefficient):
 v,d,a,kappa,A,B,C,K1,Kpair,S,PG=constants()
 t=J([0,1]);m=mean_coefficient*t**3
 alpha=-exp_i(7*t+m);b=-exp_i(-t+m)
 ua=(J(a)-alpha).inverse();ub=(J(a)-b).inverse()
 prod=polynomial_product([-alpha,J(1)],[-b,J(1)])
 cross=polynomial_product([J(-a),J(1)],[-b-7*alpha,J(8)])
 physical=[p+q for p,q in zip(prod,cross)]
 quadratic=reciprocal_polynomial(physical,a)
 wanted=[9*ua*ub,-2*ua-8*ub,J(1)]
 equal('stationary physical quadratic at mean '+str(mean_coefficient),quadratic,wanted)
 far=implicit(quadratic,9*v);near=2*ua+8*ub-far
 radical=((2*ua+8*ub)**2-36*ua*ub).sqrt(8*v)
 equal('stationary far quadratic radical '+str(mean_coefficient),far,(2*ua+8*ub+radical)/2)
 equal('stationary near quadratic radical '+str(mean_coefficient),near,(2*ua+8*ub-radical)/2)
 equal('stationary complete near residual '+str(mean_coefficient),evaluate(quadratic,near),J())
 F=6*ub.modulus()+near.modulus()+far.modulus()
 E=(ua-v)*(ua-v).conjugate()+7*(ub-v)*(ub-v).conjugate()
 equal('stationary collapsed objective '+str(mean_coefficient),F.c[0],G(16*v))
 equal('stationary energy leading coefficient '+str(mean_coefficient),E.c[2],G(56*v**4))
 equal('stationary quadratic cancellation '+str(mean_coefficient),F.c[2],kappa*E.c[2])
 equal('stationary quartic cancellation '+str(mean_coefficient),F.c[4]-kappa*E.c[4],-K1*E.c[2]*E.c[2])
 for k in (1,3,5):
  equal('stationary objective parity '+str(mean_coefficient)+'/'+str(k),F.c[k],G())
  equal('stationary energy parity '+str(mean_coefficient)+'/'+str(k),E.c[k],G())
 residual=F-kappa*E+K1*E*E
 for k in range(6):equal('stationary remainder divisibility '+str(mean_coefficient)+'/'+str(k),residual.c[k],G(16*v) if k==0 else G())
 return F,E,real(residual.c[6]),{'physical quadratic':physical,'reciprocal quadratic':quadratic,'far':far,'near':near,'objective':F,'energy':E,'reduced residual':residual}

def stationary():
 J.N=6
 v,d,a,kappa,A,B,C,K1,Kpair,S,PG=constants()
 beta=(392-1197*v+945*v*v)/20
 F,E,sextic,profile=stationary_profile(beta)
 CP=(F.c[6]-kappa*E.c[6]+2*K1*E.c[2]*E.c[4])/(E.c[2]*E.c[2]*E.c[2])
 CP=real(CP)
 wanted=-Q(297,35840)*d**9+Q(78387,1003520)*d**8-Q(741429,4014080)*d**7+Q(15471,100352)*d**6-Q(15303,458752)*d**5
 equal('stationary cubic energy coefficient',CP,wanted)
 vals={}
 for w in (0,-1,1,2):
  _,_,vals[w],data=stationary_profile(L(w))
  record('mean-control '+str(w)+' full residual',data['reduced residual'])
 p0=vals[0];linear=(vals[1]-vals[-1])/2;quadratic=(vals[1]+vals[-1])/2-p0
 known0=Q(931,2)*v**3+Q(15897,8)*v**4-Q(168525,32)*v**5-Q(9639,8)*v**6+Q(678993,128)*v**7
 known1=-196*v**3+Q(1197,2)*v**4-Q(945,2)*v**5
 equal('credited independent mean constant',p0,known0)
 equal('credited independent mean linear coefficient',linear,known1)
 equal('credited independent mean quadratic coefficient',quadratic,5*v**3)
 equal('fourth complete mean value',vals[2],p0+2*linear+4*quadratic)
 equal('stationary mean coefficient',beta,-linear/(10*v**3))
 equal('stationary sextic mean substitution',sextic,p0+linear*beta+quadratic*beta*beta)
 equal('independent mean-elimination cubic route',CP,(p0-5*v**3*beta*beta)/(56**3*v**12))
 for name,val in profile.items():record('stationary '+name,val)
 for name,val in [('beta',beta),('mean constant',p0),('mean linear',linear),('mean quadratic',quadratic),('cubic coefficient',CP)]:record('stationary '+name,val)
 return CP,p0/(56**3*v**12),real(F.c[0]-6*v)

def matrix_product(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Q()) for j in range(len(b[0]))] for i in range(len(a))]
def matrix_vector(a,b):return [sum((x*y for x,y in zip(row,b)),Q()) for row in a]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q())

def angular_controls():
 v,d,a,kappa,A,B,C,K1,Kpair,S,PG=constants()
 equal('singleton angular coefficient',A*Q(43,56)+B-C,K1)
 equal('moving-pair angular coefficient',A/2+B-C/2,Kpair)
 equal('moving-pair exact quartic gap',K1-Kpair,d**3*PG/114688)
 equal('global angular slope sign polynomial',S,d**3*PG/30720)
 equal('angular spectral weight coefficient',C,d**3*(4*d+1)**2/8192)
 # Full affine identity: constant, X and eta coefficients separately.
 equal('angular deficit constant',K1-B,S*Q(43,56)+C*Q(13,30))
 equal('angular deficit X coefficient',-A,-S-C*Q(56,30))
 equal('angular deficit eta coefficient',C,C)
 theta=[Q(1),Q(-1)]+[Q()]*6
 P=[[Q(int(i==j))-Q(1,8) for j in range(8)] for i in range(8)]
 D=[[theta[i]*int(i==j) for j in range(8)] for i in range(8)]
 H=matrix_product(matrix_product(P,D),P);H2=matrix_product(H,H)
 H3=matrix_product(H2,H);projection=[[Q(4,3)*x for x in row] for row in H2]
 equal('moving-pair balance',sum(theta),Q())
 equal('moving-pair full compression preserves theta',matrix_vector(P,theta),theta)
 equal('moving-pair full operator polynomial',H3,[[Q(3,4)*x for x in row] for row in H])
 equal('moving-pair active projector idempotence',matrix_product(projection,projection),projection)
 equal('moving-pair active rank',sum(projection[j][j] for j in range(8)),Q(2))
 equal('moving-pair active trace',sum(H[j][j] for j in range(8)),Q())
 equal('moving-pair coupling support',matrix_vector(projection,theta),theta)
 equal('moving-pair first weighted moment',dot(theta,matrix_vector(H,theta)),Q())
 equal('moving-pair second weighted moment',matrix_vector(H2,theta),[Q(3,4)*x for x in theta])
 mu2=dot(theta,theta);mu4=sum(x**4 for x in theta)
 eta=64*(2*(mu2/16)**2)/mu2**2
 equal('moving-pair scalar invariant X',mu4/mu2**2,Q(1,2))
 equal('moving-pair full-eigenspace invariant eta',eta,Q(1,2))
 equal('moving-pair Gram equality',eta-(56*mu4/mu2**2-13)/30,Q())
 equal('moving-pair moment deficit',Q(43,56)-mu4/mu2**2,Q(15,56))
 for name,val in [('compression',H),('active projector',projection),('X',Q(1,2)),('eta',eta),('Delta',Q(15,56)),('Gamma',Q())]:record('credited moving-pair '+name,val)
 for name,val in [('A',A),('B',B),('C',C),('K1',K1),('Kpair',Kpair),('S',S),('radius sign polynomial',PG),('quartic objective gap',Kpair-K1)]:record('angular '+name,val)

def equality_controls():
 # The formal symbols in these records are explicitly bound to Delta,h
 # and, in the scalar records, s=mu3,x. No numerical profile sampling.
 J.N=2
 delta=L({1:1});h=J([0,1]);X=Q(43,56)-delta
 z=Q(12,5)*(X-Q(1,2))+h
 D=Q(3,4)*delta-Q(25,48)*h;N=delta-Q(5,6)*h
 B=Q(1,7)+Q(4,3)*z;lower=(56*X-13)/30
 certificate=(B-lower)*D+N*N
 equal('credited full Gram equality certificate',certificate,delta*h/36)
 record('equality Gram variable binding','L exponent=Delta; J degree=h')
 record('equality Gram certificate',certificate)
 J.N=4
 s=L({1:1});x=J([0,1]);X0=Q(1,2)+Q(5,12)*s*s
 c4=Q(1,8)-X0/4
 equal('scalar equality constant coefficient',c4,-Q(5,48)*s*s)
 fourth=1680*x**4-180*x*x-40*s*x+24*c4
 reverse=J([1680,0,-180,-40*s,24*c4])
 derivative=J([k*reverse.c[k] for k in range(1,5)])
 equal('reversed quartic repeated-derivative factor',derivative,-10*x*(s*x+6)**2)
 zero_s=J([G(coef.re.d.get(0,Q()),coef.im.d.get(0,Q())) for coef in fourth.c])
 equal('zero-third-moment double-root factor',zero_s,x*x*(1680*x*x-180))
 record('equality scalar variable binding','L exponent=s=mu3; J degree=x; mu2=1 and h=0')
 record('equality fourth derivative',fourth)
 record('equality reversed derivative',derivative)
 record('equality zero-third-moment quartic',zero_s)
 return derivative,derivative+10*s*s*x**3

class Field:
 """Q(sqrt(1614)), with the positive real square root and exact signs."""
 def __init__(self,a=0,b=0):
  if isinstance(a,Field):self.a,self.b=a.a,a.b
  else:self.a,self.b=Q(a),Q(b)
 def __add__(self,x):x=Field(x);return Field(self.a+x.a,self.b+x.b)
 __radd__=__add__
 def __neg__(self):return Field(-self.a,-self.b)
 def __sub__(self,x):return self+-Field(x)
 def __rsub__(self,x):return Field(x)+-self
 def __mul__(self,x):x=Field(x);return Field(self.a*x.a+1614*self.b*x.b,self.a*x.b+self.b*x.a)
 __rmul__=__mul__
 def inverse(self):
  den=self.a*self.a-1614*self.b*self.b
  demand(den!=0,'zero quadratic-field divisor')
  return Field(self.a/den,-self.b/den)
 def __truediv__(self,x):return self*Field(x).inverse()
 def __pow__(self,n):
  if n<0:return self.inverse()**(-n)
  out=Field(1)
  for _ in range(n):out*=self
  return out
 def __eq__(self,x):x=Field(x);return self.a==x.a and self.b==x.b
 def sign(self):
  sa=(self.a>0)-(self.a<0);sb=(self.b>0)-(self.b<0)
  if not sb:return sa
  if not sa:return sb
  if sa==sb:return sa
  difference=self.a*self.a-1614*self.b*self.b
  demand(difference!=0,'unexpected rational sqrt(1614)')
  return sa if difference>0 else sb
 def encode(self):return [[self.a.numerator,self.a.denominator],[self.b.numerator,self.b.denominator]]

def positive(name,value):
 value=Field(value)
 demand(value.sign()==1,'strict exact sign failed: '+name)
 SIGNS.append({'name':name,'value':value.encode(),'sign':1})

def field_evaluate(p,v):return sum((v**k*c for k,c in p.d.items()),Field())

def threshold_controls(CP,CQ):
 ag=Field(Q(-385,692),Q(5,173));d=1+ag;v=d.inverse()
 positive('positive square-root lower bound',1614-40**2)
 positive('positive square-root upper bound',41**2-1614)
 equal('sharp radius minimal polynomial',2768*ag*ag+3080*ag-2875,Field())
 positive('sharp radius lower bound',ag-Q(604757,1000000))
 positive('sharp radius upper bound',Q(604758,1000000)-ag)
 positive('sharp radius below five eighths',Q(5,8)-ag)
 pg=lambda a:2768*a*a+3080*a-2875
 ls=lambda a:1616*a*a+1800*a-1675
 positive('rational radius above local threshold',ls(Q(151,250)))
 positive('rational radius below angular threshold',-pg(Q(151,250)))
 positive('radius sign increasing lower bound',3080)
 cg=field_evaluate(CP-CQ,v)
 derivative=-d**3*(5536*ag+3080)/114688
 slope=-cg/derivative
 positive('quartic-tie cubic difference',cg)
 positive('quartic-tie cubic lower bound',cg-Q(30800,1000000))
 positive('quartic-tie cubic upper bound',Q(30802,1000000)-cg)
 positive('comparison derivative strictly negative',-derivative)
 positive('comparison slope strictly positive',slope)
 positive('comparison slope lower bound',slope-Q(132978,1000000))
 positive('comparison slope upper bound',Q(132979,1000000)-slope)
 positive('uniform gap constant from quartic distance',(2768*ag+3080)/(4*114688)-Q(77,10000))
 positive('uniform gap constant from cubic tie',cg/4-Q(77,10000))
 equal('comparison slope implicit derivative',derivative*slope+cg,Field())
 for name,val in [('radius',ag),('v',v),('stationary cubic',field_evaluate(CP,v)),('moving-pair cubic',field_evaluate(CQ,v)),('cubic difference',cg),('comparison a derivative',derivative),('equal-value curve slope',slope)]:record('threshold '+name,val)
 return cg,derivative,slope

def reject_damage(name,value,wanted):
 demand(value!=wanted,'damaged mathematical expression was accepted: '+name)
 return name

def make_result():
 CHECKS.clear();SIGNS.clear();RECORDS.clear()
 CQ,Qmissing,Qwrongenergy=moving_pair()
 CP,Pwrongmean,Pmissing=stationary()
 angular_controls()
 correct_equality,damaged_equality=equality_controls()
 cg,derivative,slope=threshold_controls(CP,CQ)
 record('cubic objective gap',CP-CQ)
 controls=[
  reject_damage('omit five within-block critical reciprocals',Qmissing,L({1:16})),
  reject_damage('omit six within-block critical reciprocals',Pmissing,L({1:16})),
  reject_damage('replace stationary mean by zero at cubic order',Pwrongmean,CP),
  reject_damage('truncate the nonlinear moving-pair energy inverse',Qwrongenergy,CQ),
  reject_damage('discard cubic comparison at quartic tie',Field(),cg),
  reject_damage('reverse the comparison curve slope',-slope,slope),
  reject_damage('use negative radical for the marked radius',Field(Q(-385,692),-Q(5,173)).sign(),1),
  reject_damage('omit the scalar equality quartic constant term',damaged_equality,correct_equality),
 ]
 return {'schema':1,'agent':'six-sendov-3','role':'researcher',
  'proof_status':'ordinary written author proof; exact coefficient checks are not independent review or a formalization',
  'arithmetic':'Q[v,v^-1][i] actual original-root jets through moving-pair energy degree3 and stationary angle degree6; Q(sqrt(1614)) exact signs',
  'identity_count':len(CHECKS),'strict_sign_count':len(SIGNS),'record_count':len(RECORDS),
  'matrix_profile_count':1,'damaged_expression_count':len(controls),
  'identities':CHECKS,'strict_signs':SIGNS,'damaged_expressions':controls,
  'record_sha256':hashlib.sha256(json.dumps(RECORDS,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
  'records':RECORDS}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--check',type=Path,default=Path(__file__).with_name('expected.json'))
 parser.add_argument('--write-fixture',action='store_true')
 args=parser.parse_args()
 result=make_result()
 if args.write_fixture:args.check.write_text(json.dumps(result,indent=2)+'\n')
 else:
  try:expected=json.loads(args.check.read_text())
  except (OSError,ValueError) as error:raise RuntimeError('required complete fixture missing or malformed') from error
  demand(result==expected,'required complete fixture mismatch')
 print(json.dumps({k:result[k] for k in ['agent','role','identity_count','strict_sign_count','record_count','matrix_profile_count','damaged_expression_count','record_sha256']},indent=2))

if __name__=='__main__':main()
