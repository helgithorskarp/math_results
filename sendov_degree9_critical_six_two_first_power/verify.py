"""Complete exact checks for the degree-nine complex critical 6+2 case.

Python 3.10+ standard library, one process, no assert-based proof guards.
Tensor arithmetic and shared-denominator evaluation reuse the author's
49de03a4636330c86a240bc97d772720991ae548 source with attribution.
The geometric and polynomial deductions remain ordinary written proofs.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod, lcm, comb, factorial
import hashlib, importlib.util, json, copy

ROOT=Path(__file__).resolve().parent

def module(name,file):
 spec=importlib.util.spec_from_file_location(name,ROOT/file)
 obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
 return obj

A=module('critical62_algebra','algebra.py')
B=module('critical62_bernstein','certificate.py')

def require(condition,message):
 if not condition:raise ArithmeticError(message)

def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def tensor_hash(values,den):
 h=hashlib.sha256()
 for v in values:h.update((str(F(v,den))+'\n').encode())
 return h.hexdigest()

K_BOXES=[(F(-1,4),F(1,2)),(F(1,2),F(3,4))]

# A deterministic rectangular subdivision tree. Every internal cut has
# an exact rational ratio in its parent interval, on the indicated axis.
def layout(sign):
 require(sign in [-1,1],'Invalid margin sign')
 middle=(2,F(1,2),None,None) if sign==-1 else None
 tail=(1,F(1,2),None,None)
 left=(2,F(1,2),None,(2,F(1,2),middle,tail))
 right=(2,F(1,2),None,None)
 return (3,F(3,4),left,right)

INITIAL_BOX=((F(0),F(1)),(F(0),F(1)),(F(0),F(1)),(F(-1,4),F(3,4)))

def children(node,box):
 axis,ratio,left,right=node;low,high=box[axis]
 middle=low+ratio*(high-low)
 bl=list(box);br=list(box);bl[axis]=(low,middle);br[axis]=(middle,high)
 return (left,tuple(bl)),(right,tuple(br))

def boxes(node,box=INITIAL_BOX):
 if node is None:return [box]
 left,right=children(node,box)
 return boxes(*left)+boxes(*right)

def coverage():
 require(K_BOXES==[(F(-1,4),F(1,2)),(F(1,2),F(3,4))],'Wrong corner partition')
 for sign,count in [(-1,7),(1,6)]:
  cells=boxes(layout(sign));require(len(cells)==count,'Incomplete cell tree')
  require(all(b[0]==(0,1) for b in cells),'Unexpected t restriction')
  for i,box in enumerate(cells):
   require(all(lo<=a<b<=hi for (a,b),(lo,hi) in zip(box,INITIAL_BOX)),'Cell outside the domain')
   for other in cells[:i]:
    require(not all(max(a,c)<min(b,d) for (a,b),(c,d) in zip(box,other)),'Cell interiors overlap')
  require(sum(prod(b-a for a,b in cell) for cell in cells)==1,'Wrong complete cell volume')

def tensors(node,data,den,degree,box=INITIAL_BOX):
 if node is None:
  yield box,data,den;return
 axis,ratio,left,right=node
 ldata,rdata=B.split_at(data,den,degree,axis,ratio)
 lchild,rchild=children(node,box)
 yield from tensors(lchild[0],*ldata,degree,lchild[1])
 yield from tensors(rchild[0],*rdata,degree,rchild[1])

def certify_envelope(p,sign):
 whole_poly=B.affine_cell_integer(p,3,F(-1,4),F(3,4))
 whole,den,deg=B.bernstein(whole_poly)
 require(deg==(16,15,31,32) and len(whole)==287232,'Wrong envelope degree/count')
 require(B.invert(whole,den,deg)==whole_poly,'Complete global envelope inversion fails')
 shape=[d+1 for d in deg];stride=[prod(shape[j+1:]) for j in range(4)]
 kpolys={k:B.affine_cell_integer(p,3,*k) for k in K_BOXES}
 records=[];reference=0
 for box,vals,d in tensors(layout(sign),whole,den,deg):
   (tl,th),(cl,ch),(xl,xh),(kl,kh)=box
   direct=B.affine_cell_integer(kpolys[(kl,kh)],2,xl,xh)
   if (cl,ch)!=(0,1):direct=B.affine_cell_integer(direct,1,cl,ch)
   if sign==1 and (kl,kh)==K_BOXES[1] and (xl,xh)==(0,F(1,2)):
    slow=B.affine_cell(B.affine_cell(p,3,kl,kh),2,xl,xh)
    require(slow==direct,'Complete Fraction/integer affine reference mismatch')
    reference+=1
   require(B.invert(vals,d,deg)==direct,'Complete envelope cell inversion fails')
   other,od,odeg=B.bernstein(direct,deg)
   require(odeg==deg and len(other)==len(vals)==287232,'Incomplete cell tensor')
   require(all(v*od==w*d for v,w in zip(vals,other)),'Affine/de Casteljau entry mismatch')
   require(min(vals)>=0,'Negative envelope coefficient')
   zeros={tuple((i//stride[j])%shape[j] for j in range(4)) for i,v in enumerate(vals) if v==0}
   require((not zeros)==(not (ch==xh==1)),'Wrong noncorner zero/positive support')
   zc=[v for i,v in enumerate(vals) if (i//stride[1])%shape[1]==0]
   zx=[v for i,v in enumerate(vals) if (i//stride[2])%shape[2]==0]
   require(min(zc)>0 and min(zx)>0,'Envelope strictness support fails')
   records.append({'sign':sign,'K':[str(kl),str(kh)],'x':[str(xl),str(xh)],'c':[str(cl),str(ch)],
    'degrees':list(deg),'coefficients':len(vals),'minimum':str(F(min(vals),d)),
    'minimum_positive':str(F(min(v for v in vals if v>0),d)),
    'zeros':len(zeros),'zero_indices_sha256':digest(sorted(zeros)),
    'zeroth_c_minimum':str(F(min(zc),d)),'zeroth_x_minimum':str(F(min(zx),d)),
    'sha256':tensor_hash(vals,d)})
 require(reference==(sign==1),'Missing full Fraction affine control')
 require([tuple(tuple(map(F,row[key])) for key in ['c','x','K']) for row in records]
   ==[tuple(box[i] for i in [1,2,3]) for box in boxes(layout(sign))],'Cell tree traversal incomplete')
 return records

def corner(p):
 out={}
 for e,v in p.items():
  f=(e[0],0,0,e[3]);out[f]=out.get(f,F(0))+v
 return {e:v for e,v in out.items() if v}

def certify_corner(p):
 p=corner(p);whole_poly=B.affine_cell(p,3,F(-1,4),F(3,4))
 vals,d,deg=B.bernstein(whole_poly)
 require(deg==(16,0,0,16),'Wrong corner degree')
 require(B.invert(vals,d,deg)==whole_poly,'Complete corner inversion fails')
 cells=B.split_at(vals,d,deg,3,F(3,4));records=[]
 for ki,(kl,kh) in enumerate(K_BOXES):
  vals,d=cells[ki];direct=B.affine_cell(p,3,kl,kh)
  require(B.invert(vals,d,deg)==direct,'Complete corner cell inversion fails')
  other,od,odeg=B.bernstein(direct,deg)
  require(odeg==deg and len(vals)==len(other)==289,'Incomplete corner tensor')
  require(all(v*od==w*d for v,w in zip(vals,other)),'Corner affine/de Casteljau mismatch')
  require(min(vals)>=0,'Negative corner coefficient')
  zeros={(i//17,0,0,i%17) for i,v in enumerate(vals) if not v}
  expected={(16,0,0,j) for j in ([15,16] if ki==0 else [0,1])}
  require(zeros==expected,'Wrong corner equality support')
  records.append({'K':[str(kl),str(kh)],'degrees':list(deg),'coefficients':len(vals),
   'minimum':str(F(min(vals),d)),'minimum_positive':str(F(min(v for v in vals if v>0),d)),
   'zero_indices':[list(e) for e in sorted(zeros)],'sha256':tensor_hash(vals,d)})
 return records

P=module('critical62_polar','polar.py')

def mean_certificate():
 return P.certify(A,B,require,digest,tensor_hash)

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
 for z in [u]*6+[v]*2:
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
 phases=[(F(1,2),F(1,2),F(3,5),F(4,5)),
  (F(1,5),F(2,5),F(5,13),F(12,13)),
  (F(4,5),F(2,5),F(99,101),F(20,101)),
  (F(0),F(0),F(0),F(1)),(F(1),F(0),F(3,5),F(4,5)),
  (F(1),F(0),F(1),F(0))]
 rows=[];references=0
 for c,d0,x,y0 in phases:
  require(d0*d0==c*(1-c) and x*x+y0*y0==1,'Bad rational phase control')
  for K in [F(-1,4),F(0),F(1,2),F(3,4)]:
   q=K*K+(1-K*K)*c;R=F(2,3)**12*F(2)**4*(1+K)**12*(1-K)**4
   for sd in [-1,1]:
    delta=sd*d0
    u=(F(2,3)*(q+K),F(2,3)*(1-K*K)*delta)
    v=(F(2)*(q-K),F(-2)*(1-K*K)*delta)
    require(gadd(gscale(u,6),gscale(v,2))==(8*q,F(0)),'Weighted mean-coordinate identity fails')
    require(gnorm(u)==q*F(2,3)**2*(1+K)**2 and gnorm(v)==q*F(2)**2*(1-K)**2,'Phase norm-coordinate identity fails')
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
      require(original>=0 and ((original==0)==(t==c==x==1 and K==F(1,2))),'Exact minimum/equality control fails')
      rows.append([str(z) for z in [t,c,x,K,delta,y,original]])
 require(len(rows)==288 and references==8,'Wrong Gaussian/reference control count')
 # An exact nondegenerate bridge to original reciprocal phase coordinates.
 K=F(0);rho=F(3,5);q=rho*rho;c=q;delta=F(12,25)
 t=F(3,4);x=F(3,5);y=F(4,5);b=t*rho*x
 require(x*x+y*y==1 and delta*delta==c*(1-c),'Bad bridge phase control')
 u=gscale(gmul((x,y),(F(3,5),F(4,5))),F(2,3))
 v=gscale(gmul((x,y),(F(3,5),F(-4,5))),F(2))
 raw=gnorm(direct_integral(u,v,slope=-b))
 modeled=ev([t,c,x,K])-delta*y*jv([t,c,x,K])
 require(raw==modeled and b==F(27,100),'Original reciprocal-coordinate bridge fails')
 return {'count':len(rows),'fraction_reference_checks':references,'sha256':digest(rows),
  'original_coordinate_bridge_b':'27/100','original_coordinate_bridge_norm':str(raw)}

def polynomial_control():
 a=F(3,4);z1=(F(0),F(1,20));z2=(F(1,40),F(1,40))
 coeff=[(F(1),F(0))]
 for z in [z1]*6+[z2]*2:
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
 qp=gmul(gpower(u,6),gpower(v,2))
 original=direct_integral(u,v,slope=-a)
 require(original==gscale(gmul(primitive[0],qp),-1/a),'Polynomial origin identity control fails')
 polar=direct_integral(u,v,start=a,slope=1-a*a,factor=F(1))
 atfar=(F(0),F(0));atprime=(F(0),F(0))
 for i,k in enumerate(primitive):
  atfar=gadd(atfar,gscale(k,(1/a)**i))
  if i:atprime=gadd(atprime,gscale(k,i*a**(i-1)))
 require(polar==gscale(gmul(atfar,grecip(atprime)),a**9/(1-a*a)),'Polynomial polar identity control fails')
 require(gnorm(polar)>=1,'Disk-root polar norm control fails')
 return {'marked_root':str(a),'critical_multiplicities':[6,2],
  'critical_points':[[str(z) for z in z1],[str(z) for z in z2]],
  'rouche_l1_bound':str(bound),'coefficient_sha256':digest([[str(z) for z in k] for k in primitive]),
  'origin_and_polar_identities_checked':True}

def build(progress=None):
 coverage();E,J,D,H=A.margins();P,Q=A.coefficients()
 require((P,Q)==A.alternate_coefficients(),'Integral coefficient constructions differ')
 require((E,J)==A.alternate_norm(P,Q),'Norm constructions differ')
 require((len(E),len(J),len(D))==(5052,3577,5068),'Wrong origin-kernel inventory')
 require([len(p) for p in H]==[57422,57422],'Wrong margin inventory')
 if progress:progress('origin algebra cross-checks complete')
 cells=[]
 for sign,p in zip([-1,1],H):
  cells.extend(certify_envelope(p,sign))
  if progress:progress('sign '+str(sign)+' envelope cells completely verified')
 corners=certify_corner(D)
 if progress:progress('corner equality completely verified')
 mean=mean_certificate();controls=gaussian_controls(E,J)
 poly=polynomial_control()
 return {'agent':'six-sendov-1','role':'researcher',
  'proof_status':'complete ordinary author proof with exact finite evidence; unformalized; independent review pending',
  'norm_terms':{'even':len(E),'skew':len(J),'defect':len(D)},
  'norm_sha256':digest([A.canonical(E),A.canonical(J)]),
  'margin_sha256':[digest(A.canonical(p)) for p in H],
  'envelope_cells':cells,'corner_cells':corners,'mean_certificate':mean,
  'certified_coefficients':sum(r['coefficients'] for r in cells+corners)+mean['coefficients'],
  'gaussian_controls':controls,'polynomial_control':poly}

def accept(actual,expected):require(actual==expected,'Compact expected manifest mismatch')

def rejection_controls(actual):
 rejected=0
 for change in range(8):
  bad=copy.deepcopy(actual)
  if change==0:bad['norm_terms']['even']+=1
  elif change==1:bad['envelope_cells'][0]['minimum']='-1'
  elif change==2:bad['envelope_cells'][1]['zeroth_c_minimum']='0'
  elif change==3:bad['envelope_cells'][0]['K'][0]='-3/8'
  elif change==4:bad['corner_cells'][0]['zero_indices'].pop()
  elif change==5:bad['mean_certificate']['minimum']='-8/9'
  elif change==6:bad['gaussian_controls']['sha256']='0'*64
  else:bad['polynomial_control']['origin_and_polar_identities_checked']=False
  try:accept(actual,bad)
  except ArithmeticError:rejected+=1
  else:raise ArithmeticError('Malformed manifest accepted')
 return rejected

def main():
 actual=build();expected=json.loads((ROOT/'expected.json').read_text())
 accept(actual,expected);n=rejection_controls(actual)
 print(json.dumps({'result':'PASS','certified_coefficients':actual['certified_coefficients'],
  'envelope_cells':len(actual['envelope_cells']),'corner_cells':len(actual['corner_cells']),
  'gaussian_controls':actual['gaussian_controls']['count'],'norm_sha256':actual['norm_sha256'],
  'margin_sha256':actual['margin_sha256'],'all_entries_compared':True,
  'all_global_and_cell_tensors_inverted':True,'complete_fraction_affine_reference_checked':True,'mean_certificate_checked':True,
  'explicit_polynomial_control_checked':True,'rejected_corruptions':n},sort_keys=True))

if __name__=='__main__':main()
