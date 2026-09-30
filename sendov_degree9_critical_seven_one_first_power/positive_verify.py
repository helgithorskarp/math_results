"""Exact critical7+1 positive-sector origin proof and light-arc reduction.

Author six-sendov-1, researcher. Python3.10+ standard library.
Origin identities, Gaussian helpers and generic tensor arithmetic reuse
0bebc1748ea52c1c770c660fcb9eb04b76fb888f with attribution.
Fresh sector margins, complete sign cells and stability are checked here.
The opposite heavy/light ordering remains an unproved scalar inequality.
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
ARC=module('critical71_arc','arc.py')
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
  for K in [F(3,4),F(4,5),F(5,6),F(7,8)]:
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
      require(original>=F(3,4)*max((1-c)**9,(1-x)**19),
       'Exact phase stability control fails')
      require((original==0)==(t==c==x==1 and K==F(3,4)),
       'Positive-sector equality control fails')
      if c==x==1:
       require(original>=F(1,4)*((1-t)+(8*K-6)**2),
        'Exact corner radial stability control fails')
      r=F(4,7)*(1+K);s=4*(1-K)
      gu=(1-t*t*q*x*x)*r*r+2*t*x*gmul(w,u)[0]-1
      gv=(1-t*t*q*x*x)*s*s+2*t*x*gmul(w,v)[0]-1
      require(gu==gu0(values)+lam*gu1(values) and gv==gv0(values)+lam*gv1(values),'Normalized Gauss-Lucas identities fail')
      rows.append([str(z) for z in [t,c,x,K,delta,y,original]])
 require(len(rows)==288 and references==8,'Wrong Gaussian/reference control count')
 # A nonreal original-coordinate bridge in the claimed sector.
 K=F(3,4);rho=K;c=F(0);delta=F(0)
 t=F(3,4);x=F(3,5);y=F(4,5);b=t*rho*x
 u=(x,y);v=(-x,-y)
 raw=gnorm(direct_integral(u,v,slope=-b))
 modeled=ev([t,c,x,K])
 require(raw==modeled and b==F(27,80),'Original reciprocal-coordinate bridge fails')
 return {'count':len(rows),'fraction_reference_checks':references,'sha256':digest(rows),
  'original_coordinate_bridge_b':'27/80','original_coordinate_bridge_norm':str(raw)}

def polynomial_control():
 a=F(3,4);z1=(F(1,40),F(1,40));z2=(F(0),F(1,20))
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
 require(gnorm(u)>=gnorm(v)>1,'Actual polynomial misses the marked positive sector')
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
  'origin_and_polar_identities_checked':True,'marked_positive_sector_checked':True}

def closed_origin(u,v,b):
 ratio=gmul(v,grecip(u));endpoint=gadd((F(1),F(0)),gscale(u,-b))
 first=gmul(gadd((F(1),F(0)),gscale(ratio,-1)),
   gadd((F(1),F(0)),gscale(gpower(endpoint,8),-1)))
 second=gmul(ratio,gadd((F(1),F(0)),gscale(gpower(endpoint,9),-1)))
 return gscale(gmul(gadd(gscale(first,F(1,8)),gscale(second,F(1,9))),
   grecip(gscale(u,b))),9)

def certify_envelope(p,sign):
 require(sign in [-1,1],'Invalid sector margin sign')
 whole_poly=B.affine_cell_integer(p,3,F(3,4),F(7,8))
 whole,den,deg=B.bernstein(whole_poly)
 require(deg==(16,9,19,32) and len(whole)==112200,'Wrong sector degree/count')
 require(B.invert(whole,den,deg)==whole_poly,'Complete global sector inversion fails')
 shape=[d+1 for d in deg];stride=[prod(shape[j+1:]) for j in range(4)]
 records=[]
 for cell,((xl,xh),(vals,d)) in enumerate(zip(
   [(F(0),F(1,2)),(F(1,2),F(1))],B.split(whole,den,deg,2))):
  direct=B.affine_cell_integer(whole_poly,2,xl,xh)
  if sign==1 and cell==0:
   slow=B.affine_cell(B.affine_cell(p,3,F(3,4),F(7,8)),2,xl,xh)
   require(slow==direct,'Complete Fraction/integer affine reference mismatch')
  require(B.invert(vals,d,deg)==direct,'Complete sector cell inversion fails')
  other,od,odeg=B.bernstein(direct,deg)
  require(odeg==deg and len(other)==len(vals)==112200,'Incomplete sector cell tensor')
  require(all(v*od==w*d for v,w in zip(vals,other)),
    'Every-entry affine/de Casteljau comparison fails')
  require(min(vals)>=0,'Negative sector coefficient')
  zeros=[tuple((i//stride[j])%shape[j] for j in range(4)) for i,v in enumerate(vals) if not v]
  require(len(zeros)==(0 if cell==0 else 565),'Wrong sector zero support')
  zc=[v for i,v in enumerate(vals) if (i//stride[1])%shape[1]==0]
  zx=[v for i,v in enumerate(vals) if (i//stride[2])%shape[2]==0]
  require(F(min(zc),d)>=3 and F(min(zx),d)>=3,'Sector phase support constant below 3')
  if cell==0:require(F(min(vals),d)>=3,'Low-x whole tensor phase support below 3')
  records.append({'sign':sign,'K':['3/4','7/8'],'c':['0','1'],'x':[str(xl),str(xh)],
   'degrees':list(deg),'coefficients':len(vals),'minimum':str(F(min(vals),d)),
   'minimum_positive':str(F(min(v for v in vals if v>0),d)),
   'zeros':len(zeros),'zero_indices_sha256':digest(zeros),
   'zeroth_c_minimum':str(F(min(zc),d)),'zeroth_x_minimum':str(F(min(zx),d)),
   'sha256':tensor_hash(vals,d)})
 require([row['x'] for row in records]==[['0','1/2'],['1/2','1']],
  'Two-cell exact coverage fails')
 return records

def certify_corner(D):
 p={}
 for e,v in D.items():
  f=(e[0],0,0,e[3]);p[f]=p.get(f,F(0))+v
 p={e:v for e,v in p.items() if v}
 z=A.add(A.scale(A.variable(3),8),A.scale(A.ONE,-6))
 radial=A.add(A.ONE,A.scale(A.variable(0),-1),A.power(z,2))
 difference=A.add(p,A.scale(radial,F(-1,4)))
 whole_poly=B.affine_cell_integer(difference,3,F(3,4),F(7,8))
 require(whole_poly==B.affine_cell(difference,3,F(3,4),F(7,8)),
  'Corner full Fraction affine reference fails')
 vals,d,deg=B.bernstein(whole_poly)
 require(deg==(16,0,0,16) and len(vals)==289,'Wrong stability corner degree/count')
 require(B.invert(vals,d,deg)==whole_poly,'Complete stability corner inversion fails')
 require(min(vals)>=0,'Negative radial corner coefficient')
 zeros={(i//17,0,0,i%17) for i,v in enumerate(vals) if not v}
 require(zeros=={(16,0,0,0),(16,0,0,1)},'Wrong radial corner equality support')
 require(A.evaluate(p,[F(1),F(0),F(0),F(3,4)])==0,'Binomial corner equality fails')
 return {'K':['3/4','7/8'],'degrees':list(deg),'coefficients':len(vals),
   'subtracted_bound':'((1-t)+(8K-6)^2)/4','minimum':str(F(min(vals),d)),
   'minimum_positive':str(F(min(v for v in vals if v>0),d)),
   'zero_indices':[list(e) for e in sorted(zeros)],'sha256':tensor_hash(vals,d)}

def arc_checks():
 data=ARC.data(A);alternate=ARC.alternate(A)
 require(data['factors']==alternate,'Light-arc coefficient constructions differ')
 Ar,Ai,Br,Bi=data['factors'];PA,PB,ZR,ZI=data['gram']
 Y=A.add(A.ONE,A.scale(A.power(A.variable(2),2),-1))
 require(A.mul(PA,PB)==A.add(A.power(ZR,2),A.mul(Y,A.power(ZI,2))),
  'Full light-arc Gram identity fails')
 evs=list(map(exact_evaluator,[Ar,Ai,Br,Bi,PA,PB,ZR,ZI]))
 rows=[]
 for b in [F(0),F(1,5),F(1,2),F(1)]:
  for r in [F(1,2),F(1),F(15,14)]:
   s=8-7*r
   for x,y0 in [(F(1),F(0)),(F(3,5),F(4,5)),
    (F(5,13),F(12,13)),(F(0),F(1))]:
    for sy in [-1,1]:
     y=sy*y0;u=(x,y);values=[b,r,x,F(0)]
     aa=(evs[0](values),y*evs[1](values))
     bb=(evs[2](values),y*evs[3](values))
     z=gmul((aa[0],-aa[1]),bb)
     require(gnorm(aa)==evs[4](values) and gnorm(bb)==evs[5](values)
       and z==(evs[6](values),y*evs[7](values)),'Light-arc Gram evaluation fails')
     for v in [(F(1),F(0)),(F(3,5),F(4,5)),(F(3,5),F(-4,5)),(F(-1),F(0))]:
      modeled=gadd(aa,gscale(gmul(v,bb),-s))
      raw=direct_integral(gscale(u,r),gscale(v,s),slope=-b)
      require(raw==modeled,'Light-linear integral evaluation fails')
      require(gnorm(raw)==gnorm(aa)+s*s*gnorm(bb)-2*s*gmul(z,v)[0],
        'Light-arc norm objective identity fails')
      rows.append([str(z0) for z0 in [b,r,x,y,*v,*raw]])
 require(len(rows)==384,'Wrong light-arc exact control count')
 support=ARC.support_controls(require,gmul,gnorm)
 return {'polynomial_sha256':digest([A.canonical(p) for p in data['factors']+data['gram']]),
  'full_coefficient_and_gram_identities_checked':True,'Gaussian_count':len(rows),
  'Gaussian_sha256':digest(rows),'support_controls':support,
  'negative_imbalance_sign_assertion':False}

def build(progress=None):
 P0,Q0,E,J,R,D=A.origin_data()
 require((P0,Q0)==A.alternate_coefficients(),'Fresh 7+1 integral coefficients differ')
 require((E,J)==A.alternate_norm(P0,Q0),'Fresh 7+1 norm constructions differ')
 require((len(E),len(J),len(D))==(5115,3642,5129),'Wrong origin-kernel inventory')
 if progress:progress('both complete 7+1 origin constructions agree')
 s,h,n,d,H=A.sector_margins(D,J)
 require([len(p) for p in H]==[15610,15610],'Wrong first-Newton margin inventory')
 cells=[]
 for sign,p in zip([-1,1],H):
  cells.extend(certify_envelope(p,sign))
  if progress:progress('all sign '+str(sign)+' sector entries, inverses and affine controls pass')
 radial=certify_corner(D)
 mean=P.certify(A,B,require,digest,tensor_hash)
 controls=gaussian_controls(E,J);poly=polynomial_control();arc=arc_checks()
 if progress:progress('corner, baseline polar, phase, actual polynomial and light-arc checks pass')
 origin_count=sum(row['coefficients'] for row in cells)+radial['coefficients']
 require(origin_count==449089,'Incomplete origin sign inventory')
 return {'agent':'six-sendov-1','role':'researcher',
  'proof_status':'ordinary author sector proof with exact finite evidence; unformalized; independent review pending',
  'origin_terms':{'even':len(E),'skew':len(J),'defect':len(D)},
  'origin_norm_sha256':digest([A.canonical(E),A.canonical(J)]),
  'margin_sha256':[digest(A.canonical(p)) for p in H],'Newton_iterations':1,
  'K_domain':['3/4','7/8'],'new_origin_sign_coefficients':origin_count,
  'phase_stability_constant':'3/4','corner_radial_stability_constant':'1/4',
  'envelope_cells':cells,'radial_corner':radial,
  'polar_certificate':mean,'polar_status':'credited reproduced logical premise from 0bebc1748ea52c1c770c660fcb9eb04b76fb888f',
  'certified_coefficients':origin_count+mean['coefficients'],
  'gaussian_sector_controls':controls,'polynomial_control':poly,
  'light_arc_reduction':arc,'full_seven_one_case_claimed':False}

def accept(actual,expected):require(actual==expected,'Compact expected manifest mismatch')

def rejection_controls(actual):
 rejected=0
 for change in range(10):
  bad=copy.deepcopy(actual)
  if change==0:bad['origin_terms']['even']+=1
  elif change==1:bad['K_domain'][0]='-1/8'
  elif change==2:bad['polar_certificate']['minimum']='-8/9'
  elif change==3:bad['envelope_cells'].pop()
  elif change==4:bad['envelope_cells'][0]['zeroth_c_minimum']='0'
  elif change==5:bad['gaussian_sector_controls']['sha256']='0'*64
  elif change==6:bad['radial_corner']['zero_indices'].append([0,0,0,0])
  elif change==7:bad['polynomial_control']['marked_positive_sector_checked']=False
  elif change==8:bad['light_arc_reduction']['negative_imbalance_sign_assertion']=True
  else:bad['full_seven_one_case_claimed']=True
  try:accept(actual,bad)
  except ArithmeticError:rejected+=1
  else:raise ArithmeticError('Malformed manifest accepted')
 return rejected

def main():
 actual=build();expected=json.loads((ROOT/'expected.json').read_text())
 accept(actual,expected);n=rejection_controls(actual)
 print(json.dumps({'result':'PASS','certified_coefficients':actual['certified_coefficients'],
  'new_origin_sign_coefficients':actual['new_origin_sign_coefficients'],
  'all_sector_tensors_inverted_and_rebuilt':True,'sector_equality_and_stability_checked':True,
  'origin_norm_sha256':actual['origin_norm_sha256'],
  'sector_tensor_sha256':[row['sha256'] for row in actual['envelope_cells']],
  'polar_tensor_sha256':actual['polar_certificate']['sha256'],
  'gaussian_sector_controls':actual['gaussian_sector_controls']['count'],
  'light_arc_Gaussian_controls':actual['light_arc_reduction']['Gaussian_count'],
  'explicit_disk_root_polynomial_control_checked':True,
  'full_seven_one_case_claimed':False,'rejected_corruptions':n},sort_keys=True))

if __name__=='__main__':main()
