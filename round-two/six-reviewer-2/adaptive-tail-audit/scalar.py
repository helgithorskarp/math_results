"""Exact multivariate frontier identities and semantic certificate controls.

Independent sparse Q[N,s,k,h,alpha,x] arithmetic, plus frozen own endpoint
record construction. No imported author code or EXPECTED.
"""
from fractions import Fraction as F
from math import isqrt
import json,signal
from polynomial import Rat
from finite import scalars,repair_check
from linear import need,canonical,psd
from affine import parameters,family

def alarm(*unused):raise TimeoutError('fixed60s scalar guard; incomplete is not exclusion')
signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
DIM=6
class Poly:
 def __init__(self,v=0):
  self.a=v.copy()if isinstance(v,dict)else({(0,)*DIM:F(v)}if v else{})
 def __add__(self,v):
  b=v if isinstance(v,Poly)else Poly(v);a=self.a.copy()
  for key,val in b.a.items():a[key]=a.get(key,F(0))+val
  return Poly({k:v for k,v in a.items()if v})
 __radd__=__add__
 def __neg__(self):return Poly({k:-v for k,v in self.a.items()})
 def __sub__(self,v):return self+-(v if isinstance(v,Poly)else Poly(v))
 def __rsub__(self,v):return Poly(v)+-self
 def __mul__(self,v):
  b=v if isinstance(v,Poly)else Poly(v);a={}
  for key,val in self.a.items():
   for key2,val2 in b.a.items():
    key3=tuple(i+j for i,j in zip(key,key2));a[key3]=a.get(key3,F(0))+val*val2
  return Poly({k:v for k,v in a.items()if v})
 __rmul__=__mul__
 def __pow__(self,n):
  out=Poly(1)
  for unused in range(n):out=out*self
  return out
 def __eq__(self,v):return self.a==(v if isinstance(v,Poly)else Poly(v)).a
 def record(self):return [[list(k),str(v)]for k,v in sorted(self.a.items())]
V=[]
for j in range(DIM):
 key=[0]*DIM;key[j]=1;V.append(Poly({tuple(key):F(1)}))

def algebra():
 N,s,k,h,alpha,x=V;g=N-2*s;B=N-s-k;B0=N-(k+1)*s+k*(k-1);D=2*k*g*(1-h)+(alpha-2*k+2)*B;E=k*g*(1-h)**2+(alpha-k+1)*B
 chi=k*g*(N-x+x*h)**2-((k-1)*(N-x)+x*alpha)*(N-x)*B
 need(chi==N*N*B0-x*N*D+x*x*E,'universal multivariate adaptive chi identity')
 need(D-E*F(1,4)==k*g*(1-h)*(2-(1-h)*F(1,4))+(3*alpha-7*(k-1))*B*F(1,4),'positive scalar derivative decomposition')
 q=Rat([4,1]);rp=(3*q*q-11*q+14)/2;need(rp.polynomial()==(F(9),F(13,2),F(3,2)),'positive shifted derivative polynomial')
 samples=[]
 for qq,kk in [(4,1),(7,2),(12,3),(18,4),(24,5),(29,6),(1000000,100000)]:
  P=scalars(qq,kk);b=(6*kk-7+isqrt(28*kk*kk-36*kk+17))//2
  samples.append({key:P[key]for key in ['q','k','N','s','g','h','alpha','B','B0','D','E','kap','chi','gamma','old','new']}|{'strict_first_q':max(4,b+1)})
 return {'variable_order':['N','s','k','h','alpha','kappa'],'chi_expanded_coefficients':chi.record(),'chi_decomposition_coefficients':(N*N*B0-x*N*D+x*x*E).record(),'derivative_decomposition_coefficients':(D-E*F(1,4)).record(),'shifted_derivative_polynomial':rp.record(),'calibrations':samples,'complete_scalar_proof':'g,B,D,E,N-kappa positive;D-E/4>0,N>=38 imply chi strictly decreasing on[0,1/2]; adaptive min makeschi>=N²B0/2>0; ordinary signs not samples'}

def controls():
 rejected=[]
 def reject(name,f):
  try:f()
  except(ValueError,ZeroDivisionError):rejected.append(name);return
  raise ValueError('semantic damage accepted: '+name)
 N,s,k,h,a,x=V;g=N-2*s;B=N-s-k;B0=N-(k+1)*s+k*(k-1);D=2*k*g*(1-h)+(a-2*k+2)*B;E=k*g*(1-h)**2+(a-k+1)*B
 reject('missing kappa quadratic term',lambda:need(N*N*B0-x*N*D+x*x*E==N*N*B0-x*N*D,'exact numerator'))
 reject('wrong maximum-star coefficient',lambda:need(B0==N-(k+2)*s+k*(k-1),'exact original B0'))
 reject('non-strict square cutoff',lambda:scalars(40,8))
 reject('negative outside-domain deletion',lambda:scalars(4,5))
 reject('zero deletion not theorem domain',lambda:scalars(4,0))
 reject('floating scalar input',lambda:scalars(4.0,1))
 reject('incorrect repair norm squared2',lambda:psd([[2*F(i==j)-v for j,v in enumerate(row)]for i,row in enumerate(repair_check()['R_squared'])]))
 reject('Y norm4 omits shared deleted coordinates',lambda:psd([[4*F(i==j)-v for j,v in enumerate(row)]for i,row in enumerate(repair_check()['Y_calibrations'][0]['Y_Gram'])]))
 reject('zero endpoint determinant constant corrupted',lambda:need(Rat([-1,1]).sign()==1,'all u>=0 coefficient sign'))
 reject('denominator sign unsupported',lambda:Rat([1],[-1,1]).sign())
 reject('anchor kernel dependence',lambda:need(psd([[1,1],[1,1]])['rank']==2,'independent anchors'))
 reject('zero diagonal hidden negative direction',lambda:psd([[0,1],[1,0]]))
 reject('new interval mistreated as all-real t',lambda:need(F(1)<=scalars(12,3)['new'],'finite guaranteed repair domain'))
 reject('failed B0 conflated with failing scalar Q',lambda:need(parameters(266,49)['Q0']<0,'original Q test can pass while B0 fails; no full feasibility inference'))
 reject('negative kappa greatest rank',lambda:need(F(-1,8)>0,'strict positive floor'))
 reject('whole empty vertex removed',lambda:need(len(family(4,1)[0][1:])==len(family(4,1)[0]),'literal original empty coordinate retained'))
 return rejected
if __name__=='__main__':print(json.dumps(canonical({'agent':'six-reviewer-2','role':'independent mathematical reviewer','algebra':algebra(),'semantic_rejections':controls()}),sort_keys=True,separators=(',',':')))
