"""Exact conditional-kernel obstruction; no negative actual beta is claimed.

Two representations: Taylor coefficients through degree four, and a direct
polynomial substitution. Only Python integer/Fraction operations are used.
"""
from fractions import Fraction as F
from math import factorial,prod
import json,hashlib
from pathlib import Path
D=7;LIMIT=4;ZERO=(0,)*D

def clean(p):return {a:c for a,c in p.items() if c}
def add(p,q):
 r=dict(p)
 for a,c in q.items():r[a]=r.get(a,F(0))+c
 return clean(r)
def scale(p,c):return clean({a:v*c for a,v in p.items()})
def mul(p,q,limit=LIMIT):
 r={}
 for a,u in p.items():
  for b,v in q.items():
   ab=tuple(x+y for x,y in zip(a,b))
   if sum(ab)<=limit:r[ab]=r.get(ab,F(0))+u*v
 return clean(r)
def var(i):
 a=list(ZERO);a[i]=1
 return {tuple(a):F(1)}
def const(c):return {ZERO:F(c)} if c else {}
def power(p,n):
 out=const(1)
 for _ in range(n):out=mul(out,p)
 return out

def geometry():
 x=[(0,0,0)]
 for j in range(3):
  for s in [1,-1]:
   z=[0]*3;z[j]=s;x.append(tuple(z))
 y=[tuple(abs(v) for v in z) for z in x]
 z=[xx+yy for xx,yy in zip(x,y)]
 mean=tuple(F(z[1][k]+z[2][k],2) for k in range(6))
 w=[tuple(F(v)-a for v,a in zip(zz,mean)) for zz in z]
 for i in range(7):
  for j in range(i):
   dx=sum((a-b)**2 for a,b in zip(x[i],x[j]));dy=sum((a-b)**2 for a,b in zip(y[i],y[j]))
   if dx<dy:raise ArithmeticError('not a contraction')
 v=[tuple(wi[k]-w[0][k] for k in range(6)) for wi in w[1:]]
 if any(sum(a*b for a,b in zip(v[i],v[j]))!=(2 if i==j else 0) for i in range(6) for j in range(6)):raise ArithmeticError('affine basis')
 return x,y,w

def expansion(w,alpha=F(5,2)):
 xs=[var(i) for i in range(D)];S={}
 for a in xs:S=add(S,a)
 diag=[sum(v*v for v in wi) for wi in w]
 gram=[[sum(a*b for a,b in zip(u,v)) for v in w] for u in w]
 inverse={};pref={};rising=F(1)
 for k in range(5):
  sk=power(S,k)
  inverse=add(inverse,scale(sk,F((-1)**k,2**(k+1))))
  if k:rising*=alpha+k-1
  pref=add(pref,scale(sk,(-1)**k*rising/F(factorial(k)*2**k)))
 linear={};quad={}
 for i in range(D):
  linear=add(linear,scale(xs[i],-diag[i]/2))
  for j in range(D):quad=add(quad,scale(mul(xs[i],xs[j]),gram[i][j]/2))
 exponent=add(linear,mul(quad,inverse));expo={}
 for k in range(5):expo=add(expo,scale(power(exponent,k),F(1,factorial(k))))
 series=mul(pref,expo)
 return {a:(-1)**sum(a)*prod(factorial(k) for k in a)*v for a,v in series.items()},gram

def witness():
 ys=[var(i) for i in range(D)]
 p=scale(ys[0],4)
 for i in range(1,D):p=add(p,scale(power(add(const(1),add(ys[0],scale(ys[i],-1))),2),-1))
 return p

def substitution_check(w,p):
 # Variables here are formal R,Z_1,...,Z_6. This is NOT a probability
 # distribution for R. Its gamma-shape moments are a formal linear map.
 R=var(0);zs=[var(i) for i in range(1,D)];ys=[]
 for wi in w:
  yy=R
  for z,c in zip(zs,wi):yy=add(yy,scale(power(add(z,const(-c)),2),F(1,2)))
  ys.append(yy)
 out={}
 for a,c in p.items():
  term=const(c)
  for yy,k in zip(ys,a):term=mul(term,power(yy,k))
  out=add(out,term)
 if out!=scale(R,4):raise ArithmeticError('P(Y)=4R reconstruction fails')
 return out

def compute():
 x,y,w=geometry();mom,G=expansion(w);p=witness();sq=mul(p,p)
 value=sum(c*mom.get(a,0) for a,c in sq.items())
 sub=substitution_check(w,p)
 if value!=F(-1):raise ArithmeticError(('negative square failed',value))
 mons=[a for a in mom if sum(a)<=2]
 # Include all degree<=2 monomials whether or not an individual moment vanishes.
 from itertools import product
 mons=sorted(a for a in product(range(3),repeat=7) if sum(a)<=2)
 matrix=[[mom.get(tuple(a+b for a,b in zip(i,j)),F(0)) for j in mons] for i in mons]
 v=[p.get(a,F(0)) for a in mons]
 rayleigh=sum(v[i]*matrix[i][j]*v[j] for i in range(36) for j in range(36))
 if rayleigh!=value:raise ArithmeticError('matrix evaluation mismatch')
 controls=[]
 for alpha,expected in [(F(3),F(0)),(F(7,2),F(3))]:
  alternate,_=expansion(w,alpha)
  got=sum(c*alternate.get(a,0) for a,c in sq.items())
  if got!=expected:raise ArithmeticError('effective-dimension control failed')
  controls.append({'alpha':str(alpha),'square_value':str(got)})
 raw=json.dumps([[str(v) for v in row] for row in matrix],separators=(',',':')).encode()
 return {'status':'EXACT_CONDITIONAL_JOINT_MOMENT_OBSTRUCTION','source':x,'target':y,'base_pair':[1,2],'p':2,'t':'1/2','variance':'1/2','w':[[str(v) for v in row] for row in w],'moment_terms_through_degree4':len(mom),'moment_matrix_dimension':len(mons),'moment_matrix_sha256':hashlib.sha256(raw).hexdigest(),'witness_terms':[{'powers':a,'coefficient':str(c)} for a,c in sorted(p.items())],'negative_square_value':str(value),'formal_residual_shape':'-1/2','formal_residual_rate':'2','formal_residual_second_moment':'-1/16','algebraic_substitution':'P(Y)=4R','effective_dimension_controls':controls,'trust':'Written Gaussian/formal-series identification and multivariate Bernstein theorem; no negative actual beta or explicit negative conditional kernel index supplied'}

def check_record(record):
 # JSON normalization converts coordinate/exponent tuples to portable lists.
 if record!=json.loads(json.dumps(compute())):raise ArithmeticError('certificate mismatch')

def damage_controls(record):
 for field,value in [('negative_square_value','0'),('moment_matrix_sha256','0'*64)]:
  damaged=json.loads(json.dumps(record));damaged[field]=value
  try:check_record(damaged)
  except ArithmeticError:continue
  raise ArithmeticError('damaged certificate accepted')
 damaged=json.loads(json.dumps(record));damaged['witness_terms'][0]['coefficient']='0'
 try:check_record(damaged)
 except ArithmeticError:return 3
 raise ArithmeticError('damaged witness accepted')

if __name__=='__main__':
 record=json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
 check_record(record);n=damage_controls(record)
 print(json.dumps({'status':record['status'],'moment_matrix_dimension':36,
                   'moment_matrix_sha256':record['moment_matrix_sha256'],
                   'negative_square_value':record['negative_square_value'],
                   'damage_controls':n,'effective_dimension_controls':2},indent=2))
