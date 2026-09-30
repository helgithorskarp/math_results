"""Exact polar proof, origin identities and obstruction for critical7+1.

Author six-sendov-1, researcher. Python3.10+ standard library only.
The origin kernel is regenerated as a reduction, with no global sign
assertion. Gaussian controls and evaluator reuse author source
 d02716775d595df93bb338e533323db8717b3185, with fresh 7+1 constants.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod,lcm,comb
import hashlib,importlib.util,json,copy
ROOT=Path(__file__).resolve().parent

def module(name,file):
 spec=importlib.util.spec_from_file_location(name,ROOT/file)
 obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
A=module('critical71_algebra','algebra.py')
B=module('critical71_bernstein','certificate.py')
P=module('critical71_polar','polar.py')
def require(condition,message):
 if not condition:raise ArithmeticError(message)
def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tensor_hash(values,den):
 h=hashlib.sha256()
 for v in values:h.update((str(F(v,den))+'\n').encode())
 return h.hexdigest()

def gadd(z,w):return z[0]+w[0],z[1]+w[1]
def gscale(z,k):return z[0]*k,z[1]*k
def gmul(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def gnorm(z):return z[0]*z[0]+z[1]*z[1]
def gpower(z,n):
 out=(F(1),F(0))
 for _ in range(n):out=gmul(out,z)
 return out
def grecip(z):return z[0]/gnorm(z),-z[1]/gnorm(z)

def direct_integral(u,v,start=F(1),slope=F(-1),factor=F(9)):
 coeff=[(F(1),F(0))]
 for z in [u]*7+[v]:
  out=[(F(0),F(0))]*(len(coeff)+1)
  for i,k in enumerate(coeff):
   out[i]=gadd(out[i],gscale(k,start))
   out[i+1]=gadd(out[i+1],gscale(gmul(k,z),slope))
  coeff=out
 out=(F(0),F(0))
 for i,k in enumerate(coeff):out=gadd(out,gscale(k,factor/F(i+1)))
 return out

def exact_evaluator(p):
 degrees=[max(e[j] for e in p) for j in range(4)]
 denominator=lcm(*(v.denominator for v in p.values()))
 terms=[(e,v.numerator*(denominator//v.denominator)) for e,v in p.items()]
 def value(values):
  require(len(values)==4,'Wrong exact-evaluation variable count')
  powers=[[v.numerator**i*v.denominator**(n-i) for i in range(n+1)] for v,n in zip(values,degrees)]
  total=0
  for e,k in terms:
   for j in range(4):k*=powers[j][e[j]]
   total+=k
  return F(total,denominator*prod(v.denominator**n for v,n in zip(values,degrees)))
 return value

def gaussian_controls(E,J):
 ev=exact_evaluator(E);jv=exact_evaluator(J)
 (u0,u1),(v0,v1)=A.gauss_lucas()
 gu0,gu1,gv0,gv1=map(exact_evaluator,[u0,u1,v0,v1])
 phases=[(F(1,2),F(1,2),F(3,5),F(4,5)),
  (F(1,5),F(2,5),F(5,13),F(12,13)),
  (F(4,5),F(2,5),F(99,101),F(20,101)),
  (F(0),F(0),F(0),F(1)),(F(1),F(0),F(3,5),F(4,5)),
  (F(1),F(0),F(1),F(0))]
 rows=[];references=0
 for c,d0,x,y0 in phases:
  require(d0*d0==c*(1-c) and x*x+y0*y0==1,'Bad rational phase control')
  for K in [F(-1,8),F(0),F(3,4),F(7,8)]:
   q=K*K+(1-K*K)*c;R=F(4,7)**14*F(4)**2*(1+K)**14*(1-K)**2
   for sd in [-1,1]:
    delta=sd*d0
    u=(F(4,7)*(q+K),F(4,7)*(1-K*K)*delta)
    v=(F(4)*(q-K),F(-4)*(1-K*K)*delta)
    require(gadd(gscale(u,7),v)==(8*q,F(0)),'Weighted mean-coordinate identity fails')
    require(gnorm(u)==q*F(4,7)**2*(1+K)**2 and gnorm(v)==q*F(4)**2*(1-K)**2,'Phase norm-coordinate identity fails')
    for sy in [-1,1]:
     y=sy*y0;w=(x,y);lam=-delta*y
     for t in [F(0),F(1,3),F(1)]:
      tx=t*x;values=[t,c,x,K]
      original=gnorm(direct_integral(gscale(gmul(w,u),tx),gscale(gmul(w,v),tx)))-R
      modeled=ev(values)+lam*jv(values)-R
      if len(rows) in {5,17,71,119,167,215,263,287}:
       require(A.evaluate(E,values)+lam*A.evaluate(J,values)-R==modeled,'Fraction/shared-denominator evaluation mismatch')
       references+=1
      require(original==modeled,'Signed Gaussian integral/norm mismatch')
      # This is an identity control, not an origin sign assertion.
      r=F(4,7)*(1+K);s=4*(1-K)
      gu=(1-t*t*q*x*x)*r*r+2*t*x*gmul(w,u)[0]-1
      gv=(1-t*t*q*x*x)*s*s+2*t*x*gmul(w,v)[0]-1
      require(gu==gu0(values)+lam*gu1(values) and gv==gv0(values)+lam*gv1(values),'Normalized Gauss-Lucas identities fail')
      rows.append([str(z) for z in [t,c,x,K,delta,y,original]])
 require(len(rows)==288 and references==8,'Wrong Gaussian/reference control count')
 # An exact nondegenerate bridge to original reciprocal phase coordinates.
 K=F(0);rho=F(3,5);q=rho*rho;c=q;delta=F(12,25)
 t=F(3,4);x=F(3,5);y=F(4,5);b=t*rho*x
 require(x*x+y*y==1 and delta*delta==c*(1-c),'Bad bridge phase control')
 u=gscale(gmul((x,y),(F(3,5),F(4,5))),F(4,7))
 v=gscale(gmul((x,y),(F(3,5),F(-4,5))),F(4))
 raw=gnorm(direct_integral(u,v,slope=-b))
 modeled=ev([t,c,x,K])-delta*y*jv([t,c,x,K])
 require(raw==modeled and b==F(27,100),'Original reciprocal-coordinate bridge fails')
 return {'count':len(rows),'fraction_reference_checks':references,'sha256':digest(rows),
  'original_coordinate_bridge_b':'27/100','original_coordinate_bridge_norm':str(raw)}

def polynomial_control():
 a=F(3,4);z1=(F(0),F(1,20));z2=(F(1,40),F(1,40))
 coeff=[(F(1),F(0))]
 for z in [z1]*7+[z2]:
  out=[(F(0),F(0))]*(len(coeff)+1)
  for i,k in enumerate(coeff):
   out[i]=gadd(out[i],gscale(gmul(k,z),-1));out[i+1]=gadd(out[i+1],k)
  coeff=out
 primitive=[(F(0),F(0))]+[gscale(k,F(9,i+1)) for i,k in enumerate(coeff)]
 value=(F(0),F(0))
 for i,k in enumerate(primitive):value=gadd(value,gscale(k,a**i))
 primitive[0]=gscale(value,-1)
 check=(F(0),F(0))
 for i,k in enumerate(primitive):check=gadd(check,gscale(k,a**i))
 require(check==(F(0),F(0)) and primitive[-1]==(F(1),F(0)),'Primitive/root control fails')
 require([gscale(k,i) for i,k in enumerate(primitive) if i]==[gscale(k,9) for k in coeff],'Multiplicity/derivative control fails')
 bound=sum(abs(k[0])+abs(k[1]) for k in primitive[:-1])
 require(bound<1,'Polynomial Rouche bound fails')
 u=grecip((a-z1[0],-z1[1]));v=grecip((a-z2[0],-z2[1]))
 qp=gmul(gpower(u,7),v)
 original=direct_integral(u,v,slope=-a)
 require(original==gscale(gmul(primitive[0],qp),-1/a),'Polynomial origin identity control fails')
 polar=direct_integral(u,v,start=a,slope=1-a*a,factor=F(1))
 atfar=(F(0),F(0));atprime=(F(0),F(0))
 for i,k in enumerate(primitive):
  atfar=gadd(atfar,gscale(k,(1/a)**i))
  if i:atprime=gadd(atprime,gscale(k,i*a**(i-1)))
 require(polar==gscale(gmul(atfar,grecip(atprime)),a**9/(1-a*a)),'Polynomial polar identity control fails')
 require(gnorm(polar)>=1,'Disk-root polar norm control fails')
 return {'marked_root':str(a),'critical_multiplicities':[7,1],
  'critical_points':[[str(z) for z in z1],[str(z) for z in z2]],
  'rouche_l1_bound':str(bound),'coefficient_sha256':digest([[str(z) for z in k] for k in primitive]),
  'origin_and_polar_identities_checked':True}

def closed_origin(u,v,b):
 ratio=gmul(v,grecip(u));endpoint=gadd((F(1),F(0)),gscale(u,-b))
 first=gmul(gadd((F(1),F(0)),gscale(ratio,-1)),
   gadd((F(1),F(0)),gscale(gpower(endpoint,8),-1)))
 second=gmul(ratio,gadd((F(1),F(0)),gscale(gpower(endpoint,9),-1)))
 return gscale(gmul(gadd(gscale(first,F(1,8)),gscale(second,F(1,9))),
   grecip(gscale(u,b))),9)

def obstruction():
 b=F(63,100);r=F(5,8);s=F(29,8);eta=F(-3,8)
 u=(F(35,106),F(225,424));v=(F(6699,2248),F(580,281))
 mu=(7*u[0]+v[0])/8
 require(gnorm(u)==r*r and gnorm(v)==s*s and 7*r+s==8,'Obstruction radii/budget differ')
 require(r==1+eta and s==1-7*eta,'Obstruction imbalance differs')
 require(-b/(1+b)<eta<b/(7*(1+b)) and mu>b,'Obstruction relaxed constraints fail')
 value=direct_integral(u,v,slope=-b)
 require(value==closed_origin(u,v,b),'Obstruction independent integral identity fails')
 ratio=gnorm(value)/(r**14*s**2)
 require(ratio==F(5219893776544959999488590149762052691109849915477,
   27760891127741967700000000000000000000000000000000) and 0<ratio<F(1,5),
   'Exact strict-mean origin obstruction fails')
 Q=(1+F(8,7)*b*(1-b))**2;P0=(1+8*b*(1-b))**2
 L=Q**2*(4*Q+3*P0)/7
 adaptive=F(2,9)*(1-b)/(L*b*(1+b))
 uniform=F(1647086,97253703)*(1-b)/(b*(1+b))
 require(mu-b>adaptive>=uniform,'Obstruction does not survive the proved mean gaps')
 gu=(1-b*b)*r*r+2*b*u[0]-1
 crit=gadd((b,F(0)),gscale(grecip(u),-1))
 require(gu==F(-472677,1356800) and gnorm(crit)==F(1002677,530000)>1,
   'Gauss-Lucas exclusion of the relaxed obstruction fails')
 require(gu==r*r*(1-gnorm(crit)),'Critical disk-gap identity fails')
 # The two existing boundary equality families are identity controls.
 equalities=[]
 for uu,vv,label in [((F(1),F(0)),(F(1),F(0)),'binomial'),
                    ((F(1,2),F(0)),(F(9,2),F(0)),'collapsed')]:
  ii=direct_integral(uu,vv)
  require(ii==closed_origin(uu,vv,F(1)),'Boundary closed primitive control fails')
  require(gnorm(ii)==gnorm(uu)**7*gnorm(vv),'Existing boundary equality control fails')
  equalities.append([label,[str(z) for z in ii]])
 return {'b':str(b),'heavy_radius':str(r),'light_radius':str(s),'eta':str(eta),
   'heavy_reciprocal':[str(z) for z in u],'light_reciprocal':[str(z) for z in v],
   'weighted_real_mean':str(mu),'origin_integral':[str(z) for z in value],
   'squared_origin_ratio':str(ratio),'strict_ratio_bound':'1/5',
   'adaptive_mean_gap':str(adaptive),'uniform_mean_gap':str(uniform),
   'mean_excess':str(mu-b),'heavy_disk_gap':str(gu),
   'heavy_critical_squared_modulus':str(gnorm(crit)),
   'existing_boundary_controls':equalities}

def build(progress=None):
 P0,Q0,E,J,R,D=A.origin_data()
 require((P0,Q0)==A.alternate_coefficients(),'Fresh 7+1 integral coefficients differ')
 require((E,J)==A.alternate_norm(P0,Q0),'Fresh 7+1 norm constructions differ')
 require((len(E),len(J),len(D))==(5115,3642,5129),'Wrong origin-kernel inventory')
 require(tuple(max(e[i] for e in E) for i in range(4))==(16,8,16,32),'Wrong even norm degrees')
 require(tuple(max(e[i] for e in J) for i in range(4))==(15,7,15,30),'Wrong skew norm degrees')
 if progress:progress('both complete origin identity constructions match; no origin sign assertion')
 mean=P.certify(A,B,require,digest,tensor_hash)
 controls=gaussian_controls(E,J)
 poly=polynomial_control()
 # The AM-GM step itself is an exact polynomial identity.
 pair=[]
 for tau in [F(0),F(1,3),F(2,3),F(1)]:
  a=F(3,4);D0=1-a*a
  uu=(F(2,5),F(3,7));vv=(F(5,6),F(-2,9))
  X=gnorm(gadd((a,F(0)),gscale(uu,D0*tau)))
  Y=gnorm(gadd((a,F(0)),gscale(vv,D0*tau)))
  upper=(X**4+X**3*Y)/2
  require(upper>=0 and upper**2-X**7*Y==X**6*(X-Y)**2/4,
    'Paired modulus AM-GM identity fails')
  pair.append([str(z) for z in [tau,X,Y,upper]])
 obs=obstruction()
 return {'agent':'six-sendov-1','role':'researcher',
   'proof_status':'proved polar lemma and exact relaxed-origin obstruction; conditional origin closure open',
   'origin_terms':{'even':len(E),'skew':len(J),'defect':len(D)},
   'origin_norm_sha256':digest([A.canonical(E),A.canonical(J)]),
   'origin_gauss_lucas_sha256':digest([A.canonical(p) for pair0 in A.gauss_lucas() for p in pair0]),
   'origin_sign_assertion':False,'polar_certificate':mean,
   'certified_coefficients':mean['coefficients'],'gaussian_identity_controls':controls,
   'paired_AMGM_controls':{'count':len(pair),'sha256':digest(pair)},
   'polynomial_control':poly,'relaxed_origin_obstruction':obs}

def accept(actual,expected):require(actual==expected,'Compact expected manifest mismatch')

def rejection_controls(actual):
 rejected=0
 for change in range(8):
  bad=copy.deepcopy(actual)
  if change==0:bad['origin_terms']['even']+=1
  elif change==1:bad['origin_sign_assertion']=True
  elif change==2:bad['polar_certificate']['minimum']='-8/9'
  elif change==3:bad['polar_certificate']['coefficients']-=1
  elif change==4:bad['polar_certificate']['uniform_gamma']='1'
  elif change==5:bad['gaussian_identity_controls']['sha256']='0'*64
  elif change==6:bad['relaxed_origin_obstruction']['heavy_disk_gap']='0'
  else:bad['polynomial_control']['origin_and_polar_identities_checked']=False
  try:accept(actual,bad)
  except ArithmeticError:rejected+=1
  else:raise ArithmeticError('Malformed manifest accepted')
 return rejected

def main():
 actual=build();expected=json.loads((ROOT/'expected.json').read_text())
 accept(actual,expected);n=rejection_controls(actual)
 print(json.dumps({'result':'PASS','certified_coefficients':actual['certified_coefficients'],
   'full_polar_tensor_inverse_checked':True,'origin_sign_assertion':False,
   'origin_norm_sha256':actual['origin_norm_sha256'],
   'polar_tensor_sha256':actual['polar_certificate']['sha256'],
   'gaussian_identity_controls':actual['gaussian_identity_controls']['count'],
   'relaxed_origin_obstruction_checked':True,'mean_gaps_checked':True,
   'explicit_disk_root_polynomial_control_checked':True,'rejected_corruptions':n},sort_keys=True))

if __name__=='__main__':main()
