"""Exact actual fourth repair and optimal-cap shrinking-skew construction.

SAME-AUTHOR finite evidence. Analytic all-root collars, uniform Taylor
remainders and the limiting maximal-motion lower bound are the ordinary
unformalized proof. This does not compute a universal fourth optimum.
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
def zero_components(M=N0,beta3=N0):
 def center(u):return {(1,0):gf(u),(2,0):gf(w2),(3,0):gf(C['m3']),(4,0):gf(M)}
 K={(0,0):(N0,N1),(1,0):(N0,gamma),(2,0):(N0,C['Gamma2']),(3,0):(N0,beta3)}
 return center(uz),center(up),K
def output_roots(rows):
 return [{'label':r['label'],'all_root_coefficients':encoded_vector(r['root']),
          'all_half_normals':encoded_vector(r['normals'])} for r in rows]
def symbolic_repairs(r):
 f=lambda a,b=0,d=0:const(fcf(a,b,d))
 m=na(C['m3'],nm(f(F(35,81),F(-2086,81),F(616,27)),np(r,2)))
 beta=na(C['Gamma2'],nm(f(F(14537,1512),F(-3889,756),F(-1661,756)),np(r,2)),
         nm(f(F(-2,49),F(-4,49),F(-2,49)),np(r,4)))
 nu=na(nm(f(F(-17983,972),F(-25711,486),F(4564,81)),r),
       nm(f(F(28,81),F(56,81)),np(r,3)))
 sigma=na(nm(f(F(-1967,81),F(5479,432),F(-5375,162)),r),
          nm(f(F(-55,189),F(11,63),F(88,189)),np(r,3)))
 return m,beta,nu,sigma
def shrinking_components(M,beta3,nu4=N0,sigma4=N0,inward=N0,damage=None):
 r={1:ar.N1};order=9;rinv=ni(ns(H,2 if damage=='wrong_skew_scaling' else 3))
 m,beta,nu,sigma=symbolic_repairs(r)
 def substitute(z,e):
  out={}
  for component,p in enumerate(z):
   for power,a in p.items():
    if e+power>order:continue
    coeff={power:ar.nm(a,np(rinv,power)[0])};g=[N0,N0];g[component]=coeff
    out=pa(out,{(e+power,0):tuple(g)})
  return out
 q1=na(gamma,ns(nm(np(r,2),ni(H)),F(-4,3)))
 v2=ns(nm(nm(k,H),r),F(3,7))
 A=pa(substitute((uz,ns(r,F(-1,3))),2),substitute((w2,v2),4),
      substitute((m,nu),6),substitute((M,nm(nu4,r)),8),{(9,0):gf(inward)})
 B=pa(substitute((up,r),2),substitute((w2,v2),4),
      substitute((m,nu),6),substitute((M,nm(nu4,r)),8),{(9,0):gf(inward)})
 K=pa({(0,0):(N0,N1)},substitute((nm(d,r),q1),2),substitute((sigma,beta),4),
      substitute((nm(sigma4,r),beta3),6))
 return A,B,K
def fourth_scalar_identity():
 u,h=[ar.variable(j) for j in (0,1)];a=ar.add(ar.constant(1),u)
 q1=ar.add(ar.power(h,2),ar.scale(a,-2));q2=ar.power(a,2)
 lhs=ar.add(ar.scale(ar.power(q2,2),F(3,8)),
   ar.scale(ar.multiply(ar.power(q1,2),q2),F(-15,16)),ar.scale(ar.power(q1,4),F(35,128)))
 rhs=ar.add(ar.power(a,4),ar.scale(ar.multiply(ar.power(a,3),ar.power(h,2)),-5),
   ar.scale(ar.multiply(ar.power(a,2),ar.power(h,4)),F(45,8)),
   ar.scale(ar.multiply(a,ar.power(h,6)),F(-35,16)),ar.scale(ar.power(h,8),F(35,128)))
 ids=[];ar.identity(ids,'ENTIRE generic reciprocal FIRST-power fourth scalar',lhs,rhs)
 return ids
def build(damage=None):
 ids=[];signs=[]
 candidate=ar.ns(fc,-1) if damage=='wrong_embedding' else fc
 need(candidate==ar.ns(ar.na(ar.np(ar.NW,4),ar.np(ar.NW,5)),F(-1,2)),
      'physical cosine embedding')
 eq(ids,'physical cosine cubic',[gf(na(ns(np(c,3),8),ns(c,-6),ns(N1,-1)))],[G0])
 f=lambda a,b=0,d=0:const(fcf(a,b,d))
 p0=actual_polynomial(*zero_components(),4,1,damage)
 pM=actual_polynomial(*zero_components(N1),4,1)
 pB=actual_polynomial(*zero_components(N0,N1),4,1)
 base=roots_and_normals(p0,4,ids,damage)
 F0=direct_first_power(*zero_components(),4,1,damage)
 rows=[]
 for label in range(9):
  omega=np(WW,label)
  Aj=na(N1,ns(ns(na(omega,nc(omega)),F(1,2)),-1))
  Bj=na(N1,ns(ns(na(np(omega,2),nc(np(omega,2))),F(1,2)),-1))
  matrix=[]
  for p in (pM,pB):
   delta=[ga(a,gs(b,-1)) for a,b in zip(p[4],p0[4])]
   value=G0
   for l,z in enumerate(delta):value=ga(value,gm(z,gf(np(omega,l))))
   matrix.append(gs(real(value),F(-1,9)))
  eq(ids,'actual ALL9 fourth normal column '+str(label),matrix,
     [gf(ns(Aj,-1)),gf(ns(nm(Bj,H),F(1,7)))])
  rows.append(matrix)
 fixed_delta_M=[G0]*10;fixed_delta_M[8]=gf(ns(N1,-9));fixed_delta_M[0]=gf(ns(N1,9))
 fixed_delta_B=[G0]*10;fixed_delta_B[7]=gf(ns(H,F(9,7)));fixed_delta_B[0]=gf(ns(H,F(-9,7)))
 eq(ids,'WHOLE fourth primitive real shift column',[ga(a,gs(b,-1)) for a,b in zip(pM[4],p0[4])],fixed_delta_M)
 eq(ids,'WHOLE fourth primitive pair scale column',[ga(a,gs(b,-1)) for a,b in zip(pB[4],p0[4])],fixed_delta_B)
 q3,q4=base[3]['normals'][4][0],base[4]['normals'][4][0]
 det=na(nm(rows[3][0][0],rows[4][1][0]),ns(nm(rows[4][0][0],rows[3][1][0]),-1))
 M=nm(na(ns(nm(q3,rows[4][1][0]),-1),nm(q4,rows[3][1][0])),ni(det))
 beta3=nm(na(ns(nm(rows[3][0][0],q4),-1),nm(rows[4][0][0],q3)),ni(det))
 eq(ids,'closed real fourth repair',[gf(M)],[gf(f(F(8148040331,629856),F(78878749667,1259712),F(-51194418673,629856)))])
 eq(ids,'closed imaginary third pair repair',[gf(beta3)],[gf(f(F(27821775167,17915904),F(80418819893,8957952),F(-12650091319,1119744)))])
 if damage=='wrong_even_repair':beta3=na(beta3,N1)
 pz=actual_polynomial(*zero_components(M,beta3),4,1)
 zero=roots_and_normals(pz,4,ids)
 Fzero=direct_first_power(*zero_components(M,beta3),4,1,damage)
 G4=f(F(183619658945,2519424),F(444829186913,1259712),F(-288729410449,629856))
 eq(ids,'ENTIRE new zero-skew FIRST power through eta4',Fzero,
    [gf(ns(N1,8)),gf(C['C']),gf(C['Bstar']),gf(Tstar),gf(G4)])
 for label in (3,4,5,6):eq(ids,'ALL4 fourth individual zero normals '+str(label),zero[label]['normals'],[G0]*5)
 w4=ni(na(c,ns(np(c,2),2),ns(N1,-1)))
 w3=ns(na(ns(N1,7),ns(nm(na(ns(N1,2),ns(np(c,2),-2)),w4),-1)),F(2,3))
 eq(ids,'ENTIRE first positive dual row',[gf(na(nm(ns(N1,F(3,2)),w3),nm(na(N1,c),w4)))],[gf(ns(N1,8))])
 eq(ids,'ENTIRE second positive dual row',[gf(na(nm(ns(N1,F(3,2)),w3),nm(na(ns(N1,2),ns(np(c,2),-2)),w4)))],[gf(ns(N1,7))])
 eq(ids,'fourth cost and full active dual payments',[gf(na(F0[4][0],nm(w3,q3),nm(w4,q4)))],[gf(G4)])
 eq(ids,'fourth objective common real slope',[ga(direct_first_power(*zero_components(N1),4,1)[4],gs(F0[4],-1))],[gf(ns(N1,8))])
 eq(ids,'fourth objective pair scale slope',[ga(direct_first_power(*zero_components(N0,N1),4,1)[4],gs(F0[4],-1))],[gf(ns(H,-1))])
 # Reviewed ordinary MD formulas are reconstructed from our defining factor.
 p100=actual_polynomial(*zero_components(ns(N1,100)),4,1)
 r100=roots_and_normals(p100,4,ids)
 F100=direct_first_power(*zero_components(ns(N1,100)),4,1,damage)
 eq(ids,'reviewer10182 fourth normals at100',[r100[3]['normals'][4],r100[4]['normals'][4]],
  [gf(f(F(77000544293,6718464),F(371513219527,6718464),F(-483693373045,6718464))),
   gf(f(F(-17159240005,13436928),F(-90073161839,13436928),F(112464832314,13436928)))])
 theta=f(F(-232825395763,40310784),F(-572817768121,20155392),F(46344688537,1259712))
 Gtheta=f(F(-407598998293,10077696),F(-1964260111205,10077696),F(2551353809267,10077696))
 Mdagger=f(F(-174567528253,53747712),F(-872760677921,53747712),F(1126922107823,53747712))
 eq(ids,'reviewer10182 full fourth Gtheta',[direct_first_power(*zero_components(theta),4,1)[4]],[gf(Gtheta)])
 eq(ids,'reviewer10182 exact Mdagger',[gf(Mdagger)],[gf(na(theta,ns(Gtheta,F(-1,16))))])
 pd=actual_polynomial(*zero_components(Mdagger),4,1)
 rd=roots_and_normals(pd,4,ids);Fd=direct_first_power(*zero_components(Mdagger),4,1)
 eq(ids,'reviewer10182 actual Mdagger objective',Fd,
    [gf(ns(N1,8)),gf(C['C']),gf(C['Bstar']),gf(Tstar),gf(ns(Gtheta,F(1,2)))])
 r={1:ar.N1}
 components=shrinking_components(M,beta3,damage=damage)
 pe0=actual_polynomial(*components,9,2)
 pre=roots_and_normals(pe0,9,ids)
 forcing=[];rinv=ni(ns(H,3))
 for label in (3,4,5,6):eq(ids,'unrepaired individual normal through epsilon8 '+str(label),pre[label]['normals'][:9],[G0]*9)
 for label in (3,4):
  odd=pre[label]['normals'][9]
  need(odd[0]==N0 and set(odd[1])=={1},'ENTIRE ninth odd forcing only linear formal parameter')
  sin=ns(na(np(WW,label),ns(np(WW,9-label),-1)),F(-1,2))
  forcing.append(nm({0:odd[1][1]},ni(nm(sin,rinv))))
 sigma4=ns(nm(na(forcing[1],ns(forcing[0],-1)),ni(nm(H,na(ns(c,2),ns(N1,-1))))),7)
 nu4=na(ns(nm(H,sigma4),F(1,7)),ns(forcing[0],-1))
 eq(ids,'closed common odd fourth repair',[gf(nu4)],[gf(f(F(-2424695,13122),F(-136157,4374),F(144046,6561)))])
 eq(ids,'closed real third pair repair',[gf(sigma4)],[gf(f(F(-536333191,1119744),F(-805399537,559872),F(891296017,559872)))])
 if damage=='wrong_odd_repair':nu4=na(nu4,N1)
 inward=ns(N1,-1) if damage=='wrong_inward_shift' else N1
 components=shrinking_components(M,beta3,nu4,sigma4,inward,damage)
 pe=actual_polynomial(*components,9,2)
 pn,powers=newton_polynomial(*components,9,2)
 for i in range(10):eq(ids,'ALL10 factor versus ALL8 Newton primitive epsilon'+str(i),pe[i],pn[i])
 actual=roots_and_normals(pe,9,ids)
 for label in (3,4,5,6):
  Aj=na(N1,ns(ns(na(np(WW,label),np(WW,9-label)),F(1,2)),-1))
  eq(ids,'ALL4 individual active normal through epsilon8 '+str(label),actual[label]['normals'][:9],[G0]*9)
  eq(ids,'ALL4 actual strictly inward ninth normal '+str(label),[actual[label]['normals'][9]],[gf(ns(Aj,-1))])
 for label in range(9):
  omega=np(WW,label)
  L=na(ns(omega,F(-1,3)),ns(C['x'],-1),ns(nm(C['y'],np(WW,(-label)%9)),-1))
  W=ns(na(nm(na(ns(N1,3),ns(c,4)),omega),
      ns(nm(na(N1,ns(c,2)),na(N1,np(WW,(-label)%9))),-1),ns(np(WW,(-2*label)%9),-1)),F(1,18))
  eq(ids,'ALL9 first and quadratic drift plus true fifth-order skew '+str(label),
     [actual[label]['root'][2],actual[label]['root'][4],actual[label]['root'][5]],
     [gf(L),zero[label]['root'][2],(N0,nm(r,W))])
  for i in range(5):
   at_zero=tuple({0:p[0]} if 0 in p else {} for p in actual[label]['root'][2*i])
   eq(ids,'ALL9 zero-parameter complete fourth baseline '+str(label)+'/'+str(i),[at_zero],[zero[label]['root'][i]])
 ideal_norms=[]
 for label in range(9):
  v=ga(zero[label]['root'][2],actual[label]['root'][5])
  ideal_norms.append(gm(v,gc(v)))
 sin=(N0,ns(na(np(WW,4),ns(np(WW,5),-1)),F(-1,2)))
 ideal_target=ga(gf(C['motion_A']),gm(sin,gf(nm(C['motion_B_over_sin'],r))),gf(nm(C['motion_q2'],np(r,2))))
 eq(ids,'ENTIRE ideal positive winning quadratic norm',[ideal_norms[7]],[ideal_target])
 ideal_negative=ga(gf(C['motion_A']),gs(gm(sin,gf(nm(C['motion_B_over_sin'],r))),-1),gf(nm(C['motion_q2'],np(r,2))))
 eq(ids,'ENTIRE ideal negative winning quadratic norm',[ideal_norms[2]],[ideal_negative])
 direct=direct_first_power(*components,9,2,damage)
 target=[G0]*10
 for i,z in [(0,ns(N1,8)),(2,C['C']),(4,C['Bstar']),(6,Tstar),
             (8,na(G4,nm(nm(kappa,ni(H)),np(r,2)))),(9,ns(N1,8))]:target[i]=gf(z)
 eq(ids,'ENTIRE actual first power epsilon0to9 with shrinking-skew cost',direct,target)
 A,B,K=components
 imaginary=lambda p:{key:real((z[1],ns(z[0],-1))) for key,z in p.items()}
 ya,yb,ki=imaginary(A),imaginary(B),imaginary(K)
 variance={(i+2,j):gm(gf(ns(H,F(1,2))),z) for (i,j),z in pp(ki,2,9).items() if i+2<=9}
 cubes=pa(ps(pp(ya,3,9),6),ps(pp(yb,3,9),2),ps(pm(yb,variance,9),6))
 cube_vector=[cubes.get((i,0),G0) for i in range(10)]
 eq(ids,'ALL8 actual imaginary cubes and complete leading skew',cube_vector[:7],[G0]*5+[gf(r),G0])
 # Unique positive cosine root; exact rational isolating interval and signs.
 lo,hi=F(15,16),F(47,50);cubic=lambda t:8*t**3-6*t-1
 need(cubic(lo)<0<cubic(hi) and 24*lo**2-6>0,'unique physical cosine interval')
 for _ in range(48):
  mid=(lo+hi)/2
  if cubic(mid)>0:hi=mid
  else:lo=mid
 def positive(name,z):
  v=field_value(gf(z));coeff=list(map(F,field_real_form(fc,v)));lb=ub=F(0)
  for a in reversed(coeff):
   values=[lb*lo,lb*hi,ub*lo,ub*hi];lb,ub=min(values)+a,max(values)+a
  need(lb>0,'physical exact positive '+name)
  signs.append({'name':name,'whole_real_polynomial':[str(a) for a in coeff],
                'rational_lower':str(lb),'rational_upper':str(ub)})
 for name,z in [('H',H),('kappa',kappa),('even determinant',det),
   ('dual w3',w3),('dual w4',w4),('minus fourth coefficient',ns(G4,-1)),
   ('reviewer dagger minus new fourth',na(ns(Gtheta,F(1,2)),ns(G4,-1))),
   ('motion A',C['motion_A']),('motion B over positive sin',C['motion_B_over_sin']),
   ('motion Q',C['motion_q2'])]:positive(name,z)
 for label in range(9):
  if label in (2,7):continue
  value=tuple({0:p[0]} if 0 in p else {} for p in ideal_norms[label])
  positive('ALL7 strict nonwinning zero-skew gap '+str(label),na(C['motion_A'],ns(value[0],-1)))
 for row in rd:positive('reviewer Mdagger ALL9 inward '+str(row['label']),
                       ns(row['normals'][4 if row['label'] in (3,4,5,6) else 1][0],-1))
 for row in actual:
  i=9 if row['label'] in (3,4,5,6) else 2
  need(row['normals'][i][1]==N0 and set(row['normals'][i][0])=={0},'individual leading radial coefficient independent of parameter')
  positive('new actual ALL9 inward '+str(row['label']),ns(row['normals'][i][0],-1))
 return {'agent':'six-sendov-3','role':'researcher','schema':1,
  'ordinary_analytic_bridges_unformalized':True,'independent_review':False,
  'critical_multiplicities':[6,1,1],
  'constants':{name:ep(z) for name,z in {**C,'w2':w2,'d':d,'M4':M,'beta3':beta3,
    'G4':G4,'nu4':nu4,'sigma4':sigma4,'w3':w3,'w4':w4,'even_determinant':det,
    'theta':theta,'Gtheta':Gtheta,'Mdagger':Mdagger}.items()},
  'inherited_all_r_repairs':{name:rpoly(z) for name,z in zip(('m','beta','nu','sigma'),symbolic_repairs(r))},
  'all_nine_fourth_normal_columns':[encoded_vector(row) for row in rows],
  'all_fourth_base_normals':encoded_vector([row['normals'][4] for row in base]),
  'zero_repaired_all_primitive_columns_through_eta4':[encoded_vector(row) for row in pz],
  'zero_repaired_all_nine_roots':output_roots(zero),
  'zero_repaired_first_power_through_eta4':encoded_vector(Fzero),
  'reviewer_baseline_100':{'all_primitive_columns_through_eta4':[encoded_vector(row) for row in p100],
    'all_nine_roots':output_roots(r100),'first_power_through_eta4':encoded_vector(F100)},
  'reviewer_baseline_Mdagger':{'all_primitive_columns_through_eta4':[encoded_vector(row) for row in pd],
    'all_nine_roots':output_roots(rd),'first_power_through_eta4':encoded_vector(Fd)},
  'normalized_ninth_odd_forcing':[rpoly(z) for z in forcing],
  'all_eight_Newton_powers_epsilon0to9':[[encoded_g(power.get((i,0),G0)) for i in range(10)] for power in powers[1:]],
  'all_shrinking_primitive_columns_epsilon0to9':[encoded_vector(row) for row in pe],
  'all_nine_shrinking_roots_epsilon0to9':output_roots(actual),
  'all_nine_ideal_motion_quadratic_norms':encoded_vector(ideal_norms),
  'direct_first_power_epsilon0to9':encoded_vector(direct),
  'all_eight_imaginary_cubes_epsilon0to9':encoded_vector(cube_vector),
  'field_polynomial_identities':ids,'rational_polynomial_identities':fourth_scalar_identity(),
  'physical_cosine_interval':[str(lo),str(hi)],'rational_sign_bounds':signs,
  'finite_scope':'ALL9 complete fourth zero jets and ninth shrinking-parameter jets; ALL8 critical moments; FIRST-power distances, individual normals and actual imaginary cubes. No universal fourth lower theorem.'}
def compare_baselines(repo,record):
 metadata=json.loads((HERE/'dependencies.json').read_text());reports=[]
 for height in (10152,10197):
  row=next(r for r in metadata['files'] if r['height']==height and r['path'].endswith('/EXPECTED.json'))
  raw=(Path(repo)/row['path']).read_bytes()
  need(len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256'],'WHOLE pinned parent baseline '+str(height))
  old=json.loads(raw)
  if height==10152:
   baseline=record['reviewer_baseline_100']
   for lhs,rhs in zip(baseline['all_primitive_columns_through_eta4'],old['new_witness_all_primitive_columns_through_eta4']):
    need([field_encoded(field_value(decode_g(z))) for z in lhs]==rhs,'ENTIRE10152 factor primitive eta4')
   need(len(baseline['all_primitive_columns_through_eta4'])==len(old['new_witness_all_primitive_columns_through_eta4'])==5,'whole10152 primitive census')
   for lhs,rhs in zip(baseline['all_nine_roots'],old['all_nine_roots']):
    need(lhs['label']==rhs['label'],'whole10152 root labels')
    need([field_encoded(field_value(decode_g(z))) for z in lhs['all_root_coefficients']]==rhs['all_root_coefficients'],'ALL45 full10152 root coefficients')
    need([field_real_form(fc,field_value(decode_g(z))) for z in lhs['all_half_normals']]==rhs['all_half_normals'],'ALL45 full10152 normal coefficients')
   need(len(baseline['all_nine_roots'])==len(old['all_nine_roots'])==9,'ALL9 prior root census')
   need([field_real_form(fc,field_value(decode_g(z))) for z in baseline['first_power_through_eta4'][:4]]==old['new_witness_objective_through_eta3'],'ENTIRE10152 FIRST-power baseline eta3')
   scope='ALL50 full primitive columns, ALL45 full roots/half-normals through eta4, all four FIRST-power coefficients through eta3'
  else:
   for new,prior in [('m','m'),('beta','q2'),('nu','n'),('sigma','s')]:
    need(record['inherited_all_r_repairs'][new]==old[prior],'WHOLE all-r actual parent repair '+prior)
   for lhs,rhs in zip(record['zero_repaired_all_nine_roots'],old['all_nine_roots']):
    need(lhs['label']==rhs['label'],'ALL9 prior10197 labels')
    for i in range(3):
     old_g=decode_g(rhs['root'][i]);old_zero=tuple({0:p[0]} if 0 in p else {} for p in old_g)
     need(decode_g(lhs['all_root_coefficients'][i])==old_zero,'ALL27 full prior10197 zero motion coefficients')
   need(len(old['all_nine_roots'])==9,'ALL9 prior10197 census')
   scope='ALL four complete symbolic real/Gaussian repairs; ALL27 full zero-parameter original coefficients through eta2'
  reports.append({'height':height,'path':row['path'],'source_commit':row['source_commit'],
    'whole_file_sha256':row['sha256'],'comparison':scope,
    'same_author_only':True,'whole_prior_analytic_replay':False})
 return reports
