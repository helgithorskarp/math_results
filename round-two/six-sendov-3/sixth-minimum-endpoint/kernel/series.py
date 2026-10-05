"""Public same-author exact series/root engine, trimmed from10212 cap.py.
Source ac5e5ea1bfd10e45fb5acccb775a5061201c842d; whole original cap.py
SHA2560afecff91bd0d868f72b5deda9c348bd193e45d15c6a7530745035d0bacd47f6.
No reviewer code is imported. New mean variation is separate ordinary
unformalized author mathematics, not independent verification.
"""
from pathlib import Path
from math import comb
import json,time,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import arithmetic as ar
from arithmetic import F,need,canonical,sha256
def field_encoded(a):return [str(t) for t in a]
def field_real_form(c,a):
 d=4*a[1];b=-2*a[4];aa=a[0]-d/2
 need(a==ar.na(ar.ns(ar.N1,aa),ar.ns(c,b),ar.ns(ar.np(c,2),d)),'whole real cubic normal form')
 return [str(aa),str(b),str(d)]
HERE=Path(__file__).resolve().parent
def const(a):return {} if a==ar.N0 else {0:a}
N0={};N1=const(ar.N1);WW=const(ar.NW)
fc=ar.ns(ar.na(ar.np(ar.NW,4),ar.np(ar.NW,5)),F(-1,2))
def fcf(a,b=0,d=0):return ar.na(ar.ns(ar.N1,F(a)),ar.ns(fc,F(b)),ar.ns(ar.np(fc,2),F(d)))
fH=ar.ns(ar.ni(ar.na(ar.N1,fc)),F(14,3));fx=ar.na(ar.ns(ar.N1,F(2,3)),ar.ns(fH,F(-1,14)))
fk=fcf(F(-7,18),F(-7,9));frho=fcf(F(-5,3),F(1,3));fU0=ar.ns(fx,-8)
fuz=ar.ns(ar.na(fU0,ar.nm(frho,fH)),F(1,8));fup=ar.na(fuz,ar.ns(ar.nm(frho,fH),F(-1,2)))
falpha=fcf(F(-527,360),F(41,90),F(13,90))
ftau=ar.ns(ar.np(ar.na(fk,frho),2),F(1,2));fkappa=ar.na(ftau,ar.ns(falpha,F(10,27)))
C={k:const(v) for k,v in {'c':fc,'H':fH,'x':fx,'y':ar.ns(fH,F(1,14)),
 'U0':fU0,'u_zero':fuz,'u_pair':fup,'k':fk,'rho':frho,'alpha':falpha,'tau':ftau,'kappa':fkappa,
 'Wstar':fcf(F(2512,27),F(5840,9),F(-21392,27)),
 'Dstar':fcf(F(-4270,27),F(-29492,27),F(4012,3)),
 'gamma':fcf(F(13,36),F(1253,72),F(-50,3)),
 'C':fcf(F(26,9),F(-8,9),F(8,9)),
 'Bstar':fcf(F(2311,108),F(4934,27),F(-1976,9)),
 'Tstar':fcf(F(-60800959,17496),F(-307083769,17496),F(10980067,486)),
 'm3':fcf(F(-17403419,34992),F(-45702565,17496),F(180635,54)),
 'Gamma2':fcf(F(-1162307,23328),F(-5484833,11664),F(52426519,93312)),
 'motion_A':fcf(F(-13638695,972),F(-16011613,243),F(20901119,243)),
 'motion_B_over_sin':fcf(F(1448,243),F(6982,243),F(-8224,243)),
 'motion_q2':fcf(F(8,162),F(25,162),F(20,162))}.items()}
physical_c=C['c'][0]
c,H,k,rho,uz,up,gamma,Tstar,kappa=[C[n] for n in ('c','H','k','rho','u_zero','u_pair','gamma','Tstar','kappa')]
def na(*ps):
 out={}
 for p in ps:
  for key,a in p.items():out[key]=ar.na(out.get(key,ar.N0),a)
 return {key:a for key,a in out.items() if a!=ar.N0}
def ns(p,q):return {key:ar.ns(a,q) for key,a in p.items() if ar.ns(a,q)!=ar.N0}
def nm(p,q):
 out={}
 for i,a in p.items():
  for j,b in q.items():out[i+j]=ar.na(out.get(i+j,ar.N0),ar.nm(a,b))
 return {key:a for key,a in out.items() if a!=ar.N0}
def np(p,n):
 out=N1
 for _ in range(n):out=nm(out,p)
 return out
def ni(p):
 need(set(p)=={0},'inverse only of whole nonzero constant-r coefficient')
 return const(ar.ni(p[0]))
def nc(p):return {key:ar.nc(a) for key,a in p.items()}
def rpoly(p):return [[i,field_real_form(physical_c,a)] for i,a in sorted(p.items())]
def ep(p):return [[i,field_encoded(a)] for i,a in sorted(p.items())]
w2=ns(C['Wstar'],F(1,8));d=na(ns(k,3),rho)
G0=(N0,N0);G1=(N1,N0)
def gf(a):return (a,N0)
def ga(*zs):return na(*(z[0] for z in zs)),na(*(z[1] for z in zs))
def gs(z,q):return ns(z[0],q),ns(z[1],q)
def gm(z,w):return na(nm(z[0],w[0]),ns(nm(z[1],w[1]),-1)),na(nm(z[0],w[1]),nm(z[1],w[0]))
def gc(z):return nc(z[0]),ns(nc(z[1]),-1)
def gp(z,n):
 a=G1
 for _ in range(n):a=gm(a,z)
 return a
def real(z):return gs(ga(z,gc(z)),F(1,2))
def pa(*ps):
 out={}
 for p in ps:
  for key,a in p.items():out[key]=ga(out.get(key,G0),a)
 return {key:a for key,a in out.items() if a!=G0}
def pm(p,q,order):
 out={}
 for (r,j),a in p.items():
  for (s,l),b in q.items():
   if r+s<=order:out[r+s,j+l]=ga(out.get((r+s,j+l),G0),gm(a,b))
 return {key:a for key,a in out.items() if a!=G0}
def pp(p,n,order):
 out={(0,0):G1}
 for _ in range(n):out=pm(out,p,order)
 return out
def ps(p,q):return {key:gs(a,q) for key,a in p.items() if gs(a,q)!=G0}
def decode(p):return {i:tuple(F(t) for t in a) for i,a in p}
def decode_g(g):return tuple(decode(p) for p in g)
def encoded_g(g):return [ep(p) for p in g]
def encoded_vector(v):return [encoded_g(g) for g in v]
def eq(ids,name,lhs,rhs):
 need(lhs==rhs,'WHOLE coefficient identity '+name)
 ids.append({'name':name,'equal_whole_vector_sha256':sha256(canonical(encoded_vector(lhs))).hexdigest(),
  'whole_maps_compared_before_hash':True,'nonzero_residual_coefficients':0})
def field_value(z):
 need(z[1]==N0 and set(z[0])<={0},'whole constant field coefficient')
 return z[0].get(0,ar.N0)
def primitive(derivative,order,anchor_power,damage=None):
 prim={(i,j+1):gs(z,F(1,j+1)) for (i,j),z in derivative.items()};out=dict(prim)
 for (i,j),z in prim.items():
  for t in range(min((order-i)//anchor_power,j)+1):
   out=pa(out,{(i+anchor_power*t,0):gs(z,-comb(j,t)*(-2 if damage=='wrong_anchor' else -1)**t)})
 return [[out.get((i,j),G0) for j in range(10)] for i in range(order+1)]
def actual_polynomial(A,B,K,order,eta_power,damage=None):
 la=pa({(0,1):G1},ps(A,-1));lb=pa({(0,1):G1},ps(B,-1))
 split={(i+eta_power,j):gm(gf(ns(H,F(-1,2))),z)
        for (i,j),z in pp(K,2,order).items() if i+eta_power<=order}
 deriv=ps(pm(pp(la,6,order),pa(pp(lb,2,order),split),order),9)
 return primitive(deriv,order,eta_power,damage)
def newton_polynomial(A,B,K,order,eta_power):
 split={(i+eta_power,j):gm(gf(ns(H,F(1,2))),z)
        for (i,j),z in pp(K,2,order).items() if i+eta_power<=order}
 powers=[{}]
 for l in range(1,9):
  powers.append(pa(ps(pp(A,l,order),6),
   *(ps(pm(pp(B,l-j,order),pp(split,j//2,order),order),2*comb(l,j))
     for j in range(0,l+1,2))))
 elementary=[{(0,0):G1}]
 for l in range(1,9):
  elementary.append(ps(pa(*(ps(pm(elementary[l-j],powers[j],order),(-1)**(j-1))
                           for j in range(1,l+1))),F(1,l)))
 deriv={}
 for l,e in enumerate(elementary):
  deriv=pa(deriv,{(i,8-l):gs(z,9*(-1)**l) for (i,j),z in e.items()})
 return primitive(deriv,order,eta_power),powers
def sm(a,b,order):
 out=[G0]*(order+1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<=order:out[i+j]=ga(out[i+j],gm(x,y))
 return out
def equation(p,root,order):
 out=[G0]*(order+1);powers=[[G1]+[G0]*order]
 for j in range(1,10):powers.append(sm(powers[-1],root,order))
 for i,row in enumerate(p):
  if i>order:continue
  for j,a in enumerate(row):
   for t in range(order-i+1):out[i+t]=ga(out[i+t],gm(a,powers[j][t]))
 return out
def roots_and_normals(p,order,ids,damage=None):
 rows=[]
 for label in range(8 if damage=='missing_ninth_root' else 9):
  omega=np(WW,label);root=[gf(omega)]+[G0]*order
  for e in range(1,order+1):
   root[e]=gs(gm(equation(p,root,e)[e],gf(omega)),F(-1,9))
   eq(ids,'ALL9 full original equation '+str(order)+'/'+str(label)+'/'+str(e),
      equation(p,root,e),[G0]*(e+1))
  half=sm(root,[gc(a) for a in root],order)
  half[0]=ga(half[0],gs(G1,-1));half=[gs(a,F(1,2)) for a in half]
  rows.append({'label':label,'root':root,'normals':half})
 need(len(rows)==9,'ALL9 original root census')
 return rows
def direct_first_power(A,B,K,order,eta_power,damage=None):
 anchor={(0,0):G1,(eta_power,0):gs(G1,-1)}
 da=pa(anchor,ps(A,-1));db=pa(anchor,ps(B,-1))
 conjugate=lambda p:{key:gc(z) for key,z in p.items()}
 va=pm(da,conjugate(da),order)
 vb=pa(pm(db,conjugate(db),order),
   {(i+eta_power,j):gm(gf(ns(H,F(1,2))),z)
    for (i,j),z in pm(K,conjugate(K),order).items() if i+eta_power<=order})
 # Both variances have constant coefficient one. Only four binomial
 # powers can contribute to eta4 or epsilon9, respectively.
 def invsqrt(v):
  t=pa(v,{(0,0):gs(G1,-1)})
  coeff=F(36,128) if damage=='wrong_fourth_binomial' else F(35,128)
  return pa({(0,0):G1},ps(t,F(-1,2)),ps(pp(t,2,order),F(3,8)),
            ps(pp(t,3,order),F(-5,16)),ps(pp(t,4,order),coeff))
 cross={key:real(z) for key,z in pm(db,conjugate(K),order).items()}
 x2={(i+eta_power,j):gm(gf(ns(H,2)),z)
     for (i,j),z in pp(cross,2,order).items() if i+eta_power<=order}
 # For the zero-skew family X=0. For shrinking skew X^2 begins at
 # epsilon8, so replacing V^(-5/2) by 1 costs only epsilon10.
 need(not x2 or (eta_power==2 and min(i for i,j in x2)>=8),
      'complete physical pair cross-term truncation boundary')
 total=pa(ps(invsqrt(va),6),ps(invsqrt(vb),2),
          ps(x2,F(-3,4) if damage=='wrong_pair_distance_sign' else F(3,4)))
 return [total.get((i,0),G0) for i in range(order+1)]
def output_roots(rows):
 return [{'label':r['label'],'all_root_coefficients':encoded_vector(r['root']),
          'all_half_normals':encoded_vector(r['normals'])} for r in rows]
