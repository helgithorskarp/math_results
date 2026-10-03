"""Whole parameter-polynomial algebra for actual nonzero-skew attainment.

SAME-AUTHOR exact finite evidence. The common analytic original-root collar,
uniform Taylor remainders and all-competitor maximal-envelope transfer remain
the written ordinary proof, unformalized and independently unreviewed.
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
def family(r,m=N0,q2=N0,n=N0,s=N0,damage=None):
 order=3;q1=na(gamma,ns(nm(np(r,2),ni(H)),F(-4,3)));v2=ns(nm(nm(k,H),r),F(3,7))
 if damage=='wrong_norm_payment':q1=gamma
 if damage=='wrong_imaginary_mean':v2=N0
 local_d=rho if damage=='wrong_real_split' else d
 a={(0,1):G1,(1,0):gs((uz,ns(r,F(-1,3))),-1),(2,0):gs((w2,v2),-1),(3,0):gs((m,n),-1)}
 b={(0,1):G1,(1,0):gs((up,r),-1),(2,0):gs((w2,v2),-1),(3,0):gs((m,n),-1)}
 K={(0,0):(N0,N1),(1,0):(nm(local_d,r),q1),(2,0):(s,q2)}
 shift={(i+1,j):gm(gf(ns(H,F(-1,2))),z) for (i,j),z in pp(K,2,order).items() if i+1<=order}
 pair=pa(pp(b,2,order),shift)
 derivative=ps(pm(pp(a,6,order),pair,order),9)
 prim={(i,j+1):gs(z,F(1,j+1)) for (i,j),z in derivative.items()};p=dict(prim)
 for (i,j),z in prim.items():
  for t in range(min(order-i,j)+1):p=pa(p,{(i+t,0):gs(z,-comb(j,t)*(-2 if damage=='wrong_anchor' else -1)**t)})
 return [[p.get((i,j),G0) for j in range(10)] for i in range(order+1)]
def sm(a,b,n):
 out=[G0]*(n+1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<=n:out[i+j]=ga(out[i+j],gm(x,y))
 return out
def equation(p,root,n):
 out=[G0]*(n+1);powers=[[G1]+[G0]*n]
 for j in range(1,10):powers.append(sm(powers[-1],root,n))
 for i,poly in enumerate(p):
  if i>n:continue
  for j,a in enumerate(poly):
   for t in range(n-i+1):out[i+t]=ga(out[i+t],gm(a,powers[j][t]))
 return out
def roots(p,damage=None):
 rows=[]
 for j in range(8 if damage=='missing_ninth_root' else 9):
  omega=np(WW,j);root=[gf(omega)]+[G0]*3
  for i in range(1,4):
   root[i]=gs(gm(equation(p,root,i)[i],gf(omega)),F(-1,9))
   need(equation(p,root,i)==[G0]*(i+1),'ALL9 whole root recursion')
  norm=sm(root,[gc(a) for a in root],3);norm[0]=ga(norm[0],gs(G1,-1));norm=[gs(a,F(1,2)) for a in norm]
  rows.append({'label':j,'root':root,'normals':norm})
 need(len(rows)==9,'ALL9 original root census')
 return rows
def objective(r,m,q2,damage=None):
 q1=na(gamma,ns(nm(np(r,2),ni(H)),F(-4,3)));v2=ns(nm(nm(k,H),r),F(3,7));ap=na(N1,up);az=na(N1,uz)
 z=[N1,ns(az,-2),na(np(az,2),ns(w2,-2),ns(np(r,2),F(1,9))),na(ns(nm(az,w2),2),ns(m,-2),ns(nm(r,v2),F(-2,3)))]
 p=[N1,na(ns(ap,-2),ns(H,F(1,2))),na(np(ap,2),ns(w2,-2),np(r,2),nm(H,q1)),
    na(ns(nm(ap,w2),2),ns(m,-2),ns(nm(r,v2),2),ns(nm(H,na(np(q1,2),ns(q2,2),nm(np(d,2),np(r,2)))),F(1,2)))]
 def f(q):return [N1,ns(q[1],F(-1,2)),na(ns(q[2],F(-1,2)),ns(np(q[1],2),F(3,8))),na(ns(q[3],F(-1,2)),ns(nm(q[1],q[2]),F(3,4)),ns(np(q[1],3),F(-5,16)))]
 out=[na(ns(a,6),ns(b,2)) for a,b in zip(f(z),f(p))]
 out[3]=na(out[3],ns(nm(nm(H,np(r,2)),np(na(d,ns(N1,-1)),2)),F(-3,2) if damage=='wrong_pair_distance_sign' else F(3,2)))
 return out
def run(r,damage=None):
 base=roots(family(r,damage=damage),damage);A3=ns(N1,F(3,2));B3=A3;A4=na(N1,c);B4=na(ns(N1,2),ns(np(c,2),-2))
 av=[gs(ga(base[j]['normals'][3],base[9-j]['normals'][3]),F(1,2)) for j in (3,4)]
 need(all(z[1]==N0 for z in av),'even averages have no Gaussian-i component')
 matrix=[(ns(A3,-1),ns(nm(B3,H),F(1,7))),(ns(A4,-1),ns(nm(B4,H),F(1,7)))]
 det=na(nm(matrix[0][0],matrix[1][1]),ns(nm(matrix[1][0],matrix[0][1]),-1))
 m=nm(na(ns(nm(av[0][0],matrix[1][1]),-1),nm(av[1][0],matrix[0][1])),ni(det))
 q2=nm(na(ns(nm(matrix[0][0],av[1][0]),-1),nm(matrix[1][0],av[0][0])),ni(det))
 odd=[]
 for j in (3,4):
  v=gs(ga(base[j]['normals'][3],gs(base[9-j]['normals'][3],-1)),F(1,2))
  need(v[0]==N0,'odd differences have no non-i component')
  sin=ns(na(np(WW,j),ns(np(WW,9-j),-1)),F(-1,2))
  odd.append(nm(v[1],ni(sin)))
 s=ns(nm(na(odd[1],ns(odd[0],-1)),ni(nm(H,na(ns(c,2),ns(N1,-1))))),7)
 n=na(ns(nm(H,s),F(1,7)),ns(odd[0],-1))
 if damage=='wrong_even_repair':m=na(m,N1)
 if damage=='wrong_odd_repair':n=na(n,N1)
 actual=roots(family(r,m,q2,n,s));lam=ns(nm(H,r),3)
 for j in (3,4,5,6):need(actual[j]['normals']==[G0]*4,'ALL4 individual active normals through eta3 zero')
 for j in range(9):
  w=np(WW,j)
  L=na(ns(w,F(-1,3)),ns(C['x'],-1),ns(nm(C['y'],np(WW,(-j)%9)),-1))
  Wfield=ns(na(nm(na(ns(N1,3),ns(c,4)),w),ns(nm(na(N1,ns(c,2)),na(N1,np(WW,(-j)%9))),-1),ns(np(WW,(-2*j)%9),-1)),F(1,18))
  need(actual[j]['root'][1]==gf(L),'whole existing first motion')
  zero_base=actual[j]['root'][2][0]
  need(set(zero_base)<={0},'entire real second motion has no r dependence')
  need(actual[j]['root'][2][1]==nm(lam,Wfield),'whole all-nine skew harmonic')
 obj=objective(r,m,q2,damage);target=[ns(N1,8),C['C'],C['Bstar'],na(Tstar,ns(nm(nm(kappa,H),np(r,2)),9))]
 need(obj==target,'exact nonzero-skew minimum cost attained')
 return {'r':rpoly(r),'lambda':rpoly(lam),'m':rpoly(m),'q2':rpoly(q2),'n':rpoly(n),'s':rpoly(s),'objective':[rpoly(a) for a in obj],
         'base_even_forcing':[rpoly(a[0]) for a in av],'base_odd_forcing':[rpoly(a) for a in odd],
         'all_primitive_columns_through_eta3':[[[ep(a) for a in z] for z in row] for row in family(r,m,q2,n,s)],
         'all_nine_roots':[{key:([[ep(a) for a in g] for g in v] if key!='label' else v) for key,v in row.items()} for row in actual]}

def primitive(derivative,order,anchor_power=1):
 prim={(i,j+1):gs(z,F(1,j+1)) for (i,j),z in derivative.items()};out=dict(prim)
 for (i,j),z in prim.items():
  for t in range(min((order-i)//anchor_power,j)+1):
   out=pa(out,{(i+anchor_power*t,0):gs(z,-comb(j,t)*(-1)**t)})
 return [[out.get((i,j),G0) for j in range(10)] for i in range(order+1)]

def newton_primitive(r,m,q2,n,s):
 q1=na(gamma,ns(nm(np(r,2),ni(H)),F(-4,3)));v2=ns(nm(nm(k,H),r),F(3,7))
 A={(1,0):(uz,ns(r,F(-1,3))),(2,0):(w2,v2),(3,0):(m,n)}
 B={(1,0):(up,r),(2,0):(w2,v2),(3,0):(m,n)}
 K={(0,0):(N0,N1),(1,0):(nm(d,r),q1),(2,0):(s,q2)}
 split={(i+1,j):gm(gf(ns(H,F(1,2))),a) for (i,j),a in pp(K,2,3).items() if i+1<=3}
 P=[{}]
 for l in range(1,9):
  P.append(pa(ps(pp(A,l,3),6),*(ps(pm(pp(B,l-j,3),pp(split,j//2,3),3),2*comb(l,j)) for j in range(0,l+1,2))))
 elementary=[{(0,0):G1}]
 for l in range(1,9):
  elementary.append(ps(pa(*(ps(pm(elementary[l-j],P[j],3),(-1)**(j-1)) for j in range(1,l+1))),F(1,l)))
 derivative={}
 for l,e in enumerate(elementary):
  derivative=pa(derivative,{(i,8-l):gs(a,9*(-1)**l) for (i,z),a in e.items()})
 return primitive(derivative,3),P

def epsilon_primitive(r,m,q2,n,s,inward):
 q1=na(gamma,ns(nm(np(r,2),ni(H)),F(-4,3)));v2=ns(nm(nm(k,H),r),F(3,7))
 A={(0,1):G1,(2,0):gs((uz,ns(r,F(-1,3))),-1),(4,0):gs((w2,v2),-1),
    (6,0):gs((m,n),-1),(7,0):gs(gf(inward),-1)}
 B={(0,1):G1,(2,0):gs((up,r),-1),(4,0):gs((w2,v2),-1),
    (6,0):gs((m,n),-1),(7,0):gs(gf(inward),-1)}
 K={(0,0):(N0,N1),(2,0):(nm(d,r),q1),(4,0):(s,q2)}
 split={(i+2,j):gm(gf(ns(H,F(-1,2))),a) for (i,j),a in pp(K,2,7).items() if i+2<=7}
 derivative=ps(pm(pp(A,6,7),pa(pp(B,2,7),split),7),9)
 return primitive(derivative,7,2)

def direct_distance_objective(r,m,q2,n,s,inward):
 q1=na(gamma,ns(nm(np(r,2),ni(H)),F(-4,3)));v2=ns(nm(nm(k,H),r),F(3,7))
 A={(2,0):(uz,ns(r,F(-1,3))),(4,0):(w2,v2),(6,0):(m,n),(7,0):gf(inward)}
 B={(2,0):(up,r),(4,0):(w2,v2),(6,0):(m,n),(7,0):gf(inward)}
 K={(0,0):(N0,N1),(2,0):(nm(d,r),q1),(4,0):(s,q2)}
 anchor={(0,0):G1,(2,0):gs(G1,-1)}
 da=pa(anchor,ps(A,-1));db=pa(anchor,ps(B,-1))
 conjugate=lambda p:{key:gc(a) for key,a in p.items()}
 va=pm(da,conjugate(da),7)
 vk=pm(K,conjugate(K),7)
 vb=pa(pm(db,conjugate(db),7),{(i+2,j):gm(gf(ns(H,F(1,2))),a) for (i,j),a in vk.items() if i+2<=7})
 def invsqrt(v):
  t=pa(v,{(0,0):gs(G1,-1)})
  return pa({(0,0):G1},ps(t,F(-1,2)),ps(pp(t,2,7),F(3,8)),ps(pp(t,3,7),F(-5,16)))
 cross={key:real(a) for key,a in pm(db,conjugate(K),7).items()}
 cross2={(i+2,j):gm(gf(ns(H,2)),a) for (i,j),a in pp(cross,2,7).items() if i+2<=7}
 out=pa(ps(invsqrt(va),6),ps(invsqrt(vb),2),ps(cross2,F(3,4)))
 return [out.get((i,0),G0) for i in range(8)]

def decode(p):return {i:tuple(F(t) for t in a) for i,a in p}
def decode_real(p):return {i:fcf(*(F(t) for t in a)) for i,a in p}
def decode_g(g):return tuple(decode(p) for p in g)
def encoded_g(g):return [ep(p) for p in g]
def encoded_vector(xs):return [encoded_g(g) for g in xs]
def eq(rows,name,lhs,rhs):
 need(lhs==rhs,'WHOLE polynomial identity '+name)
 rows.append({'name':name,'complete_lhs_sha256':sha256(canonical(encoded_vector(lhs))).hexdigest(),
              'complete_rhs_sha256':sha256(canonical(encoded_vector(rhs))).hexdigest(),
              'whole_maps_compared_before_hash':True,'nonzero_residual_coefficients':0})
def polynomial_interval(coefficients,lo,hi):
 lb=ub=F(0)
 for a in reversed(coefficients):
  v=(lb*lo,lb*hi,ub*lo,ub*hi);lb,ub=min(v)+a,max(v)+a
 return lb,ub

def build(damage=None):
 r={1:ar.N1};ids=[];signs=[];result=run(r,damage)
 need(fc==ar.ns(ar.na(ar.np(ar.NW,4),ar.np(ar.NW,5)),F(-1,2)),'physical cosine embedding')
 m,q2,n,s=(decode_real(result[key]) for key in ('m','q2','n','s'))
 closed={
 'm':na(C['m3'],nm(fpoly(F(35,81),F(-2086,81),F(616,27)),np(r,2))),
 'q2':na(C['Gamma2'],nm(fpoly(F(14537,1512),F(-3889,756),F(-1661,756)),np(r,2)),
         nm(fpoly(F(-2,49),F(-4,49),F(-2,49)),np(r,4))),
 'n':na(nm(fpoly(F(-17983,972),F(-25711,486),F(4564,81)),r),nm(fpoly(F(28,81),F(56,81)),np(r,3))),
 's':na(nm(fpoly(F(-1967,81),F(5479,432),F(-5375,162)),r),nm(fpoly(F(-55,189),F(11,63),F(88,189)),np(r,3)))}
 for key,value in zip(('m','q2','n','s'),(m,q2,n,s)):eq(ids,'closed actual repair '+key,[gf(value)],[gf(closed[key])])
 p=family(r,m,q2,n,s);newton,powers=newton_primitive(r,m,q2,n,s)
 for i in range(4):eq(ids,'ALL TEN complex primitive columns factor versus ALL EIGHT Newton moments eta'+str(i),p[i],newton[i])
 zero=family(N0,C['m3'],C['Gamma2'])
 lam=ns(nm(H,r),3)
 Q=[G0]*10
 Q[8]=(N0,ns(na(N1,ns(c,2)),F(1,2)));Q[7]=Q[8];Q[6]=(N0,ns(N1,F(1,2)))
 Q[0]=gs(ga(Q[8],Q[7],Q[6]),-1)
 eq(ids,'whole first primitive agrees with zero skew',p[1],zero[1])
 eq(ids,'whole second primitive equals credited real jet plus lambda Q',p[2],
    [ga(a,gm(gf(lam),q)) for a,q in zip(zero[2],Q)])
 # Reconstruct actual changes in the four individual normal rows, not guessed rows.
 A3=ns(N1,F(3,2));B3=A3;A4=na(N1,c);B4=na(ns(N1,2),ns(np(c,2),-2))
 matrices=[]
 for j,A,B,ratio in ((3,A3,B3,N1),(4,A4,B4,ns(c,2))):
  sin=(N0,ns(na(np(WW,j),ns(np(WW,9-j),-1)),F(-1,2)))
  row=[gf(ns(A,-1)),gf(ns(nm(B,H),F(1,7))),sin,gm(sin,gf(ns(nm(ratio,H),F(-1,7))))]
  matrices.append({'label':j,'all_four_columns':encoded_vector(row)})
  for col in range(4):
   args=[N0]*4;args[col]=N1
   pp1=family(r,*args)
   diff=[ga(a,gs(b,-1)) for a,b in zip(pp1[3],family(r)[3])]
   val=G0
   for l,a in enumerate(diff):val=ga(val,gm(a,gf(np(WW,(j*l)%9))))
   normal=gs(real(val),F(-1,9))
   eq(ids,'actual defining-factor individual normal column '+str(j)+'/'+str(col),[normal],[row[col]])
 even_det=na(nm(ns(A3,-1),ns(nm(B4,H),F(1,7))),ns(nm(ns(A4,-1),ns(nm(B3,H),F(1,7))),-1))
 eq(ids,'even repair determinant 2c-1',[gf(even_det)],[gf(na(ns(c,2),ns(N1,-1)))])
 odd_det=ns(nm(H,na(N1,ns(c,-2))),F(1,7))
 eq(ids,'sine-normalized odd determinant',[gf(odd_det)],[gf(ns(nm(H,na(ns(c,2),ns(N1,-1))),F(-1,7)))])
 inward=ns(N1,-1) if damage=='wrong_inward_shift' else N1
 pe=epsilon_primitive(r,m,q2,n,s,inward)
 expected_eps=[[G0]*10 for _ in range(8)]
 for i in range(4):expected_eps[2*i]=p[i]
 expected_eps[7][8]=gf(ns(inward,-9));expected_eps[7][0]=gf(ns(inward,9))
 for i in range(8):eq(ids,'actual anchored factor epsilon primitive ALL10 order'+str(i),pe[i],expected_eps[i])
 epsrows=[]
 for row in result['all_nine_roots']:
  j=row['label'];eta_roots=[decode_g(g) for g in row['root']]
  root=[G0]*8
  for i,z in enumerate(eta_roots):root[2*i]=z
  root[7]=gf(nm(inward,na(N1,ns(np(WW,j),-1))))
  eq(ids,'ALL9 full epsilon7 original root equation '+str(j),equation(pe,root,7),[G0]*8)
  half=sm(root,[gc(a) for a in root],7);half[0]=ga(half[0],gs(G1,-1));half=[gs(a,F(1,2)) for a in half]
  for i,a in enumerate(half):eq(ids,'ALL9 actual conjugation of normal '+str(j)+'/'+str(i),[a],[gc(a)])
  if j in (3,4,5,6):
   eq(ids,'individual active normal through epsilon6 '+str(j),half[:7],[G0]*7)
   Aj=A3 if j in (3,6) else A4
   eq(ids,'individual active inward epsilon7 '+str(j),[half[7]],[gf(ns(Aj,-1))])
  epsrows.append({'label':j,'all_original_root_coefficients_epsilon0to7':encoded_vector(root),
      'all_half_normals_epsilon0to7':encoded_vector(half),
      'strict_inward_order':7 if j in (3,4,5,6) else 2})
 # The new common shift changes the FIRST-power objective by exactly8*epsilon7.
 eq(ids,'common shift FIRST-power coefficient epsilon7',[gf(ns(inward,8))],[gf(ns(N1,8))])
 direct_F=direct_distance_objective(r,m,q2,n,s,inward)
 expected_F=[G0]*8
 for i,a in enumerate(objective(r,m,q2)):expected_F[2*i]=gf(a)
 expected_F[7]=gf(ns(N1,8))
 eq(ids,'ENTIRE actual squared-distance FIRST-power epsilon0to7',direct_F,expected_F)
 lo,hi=map(F,('21159996684071109/22517998136852480','52899991710177773/56294995342131200'))
 need(F(9,10)<lo<hi<1,'physical branch interval')
 f=lambda t:8*t**3-6*t-1
 need(f(lo)<0<f(hi) and 24*lo**2-6>0,'unique physical cubic root enclosed')
 targets={'H':H,'kappa':kappa,'2c-1':na(ns(c,2),ns(N1,-1)),
          'motion_A':C['motion_A'],'motion_B_over_positive_sin':C['motion_B_over_sin'],'motion_q2':C['motion_q2']}
 for row in epsrows:
  j=row['label'];order=row['strict_inward_order'];z=decode_g(row['all_half_normals_epsilon0to7'][order])
  need(z[1]==N0 and set(z[0])<={0},'leading strict inward normal independent of r')
  targets['strict original inward '+str(j)]=ns(z[0],-1)
 for name,value in targets.items():
  coefficients=[F(t) for t in field_real_form(fc,value[0])]
  lb,ub=polynomial_interval(coefficients,lo,hi);need(lb>0,'strict physical sign '+name)
  signs.append({'name':name,'whole_real_cubic_coefficients':[str(a) for a in coefficients],
                'rational_interval_lower':str(lb),'rational_interval_upper':str(ub)})
 result.update({'agent':'six-sendov-3','role':'researcher','schema':'actual-nonzero-skew-parameter-polynomial-v1',
   'ordinary_analytic_bridges_unformalized':True,'independent_review':False,
   'constants':{key:field_encoded(value[0]) for key,value in C.items()},
   'all_eight_Newton_powers_eta0to3':[[[list(key),encoded_g(value)] for key,value in sorted(P.items())] for P in powers[1:]],
   'individual_active_repair_matrix':matrices,'even_determinant':rpoly(even_det),'normalized_odd_determinant':rpoly(odd_det),
   'all_epsilon_primitive_columns_through7':[encoded_vector(row) for row in pe],
   'all_nine_epsilon_roots':epsrows,'field_polynomial_identities':ids,
   'physical_cosine_interval':[str(lo),str(hi)],'rational_sign_bounds':signs,
   'first_power_epsilon7_coefficient':rpoly(ns(inward,8)),
   'direct_actual_first_power_epsilon0to7':encoded_vector(direct_F),
   'actual_skew_limit':rpoly(lam),'uniform_compact_parameter_remainder':'ordinary analytic proof, not a finite certificate'})
 return result

def fpoly(a,b=0,d=0):return const(fcf(a,b,d))

def evaluate_constant(p):
 p=decode(p);return p.get(0,ar.N0)
def compare_baselines(root,record):
 deps=json.loads((HERE/'dependencies.json').read_text())
 row=next(v for v in deps['files'] if v['height']==10152 and v['path'].endswith('/EXPECTED.json'))
 raw=(Path(root)/row['path']).read_bytes()
 need(len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256'],'ENTIRE pinned useful prior finite record')
 old=json.loads(raw);matched=0
 for key,value in record['constants'].items():
  if key in old['constants']:need(value==old['constants'][key],'whole prior shared constant '+key);matched+=1
 for i in range(4):
  for j in range(10):
   z=record['all_primitive_columns_through_eta3'][i][j]
   need([str(t) for t in evaluate_constant(z[0])]==old['new_witness_all_primitive_columns_through_eta4'][i][j] and evaluate_constant(z[1])==ar.N0,
        'ALL40 prior zero-skew primitive columns')
 for j in range(9):
  need(record['all_nine_roots'][j]['label']==old['all_nine_roots'][j]['label'],'prior all9 label census')
  for i in range(4):
   z=record['all_nine_roots'][j]['root'][i]
   need([str(t) for t in evaluate_constant(z[0])]==old['all_nine_roots'][j]['all_root_coefficients'][i] and evaluate_constant(z[1])==ar.N0,'ALL36 prior full root coefficients')
   z=record['all_nine_roots'][j]['normals'][i]
   rhs=fcf(*(F(t) for t in old['all_nine_roots'][j]['all_half_normals'][i]))
   need(evaluate_constant(z[0])==rhs and evaluate_constant(z[1])==ar.N0,'ALL36 prior full half normals')
 for i in range(4):
  need(field_real_form(fc,fcf(*(F(t) for t in record['objective'][i][0][1])))==old['new_witness_objective_through_eta3'][i],
       'ALL4 prior FIRST-power objective coefficients')
 return {'height':10152,'whole_record_source_sha256':row['sha256'],'shared_constants':matched,
    'whole_primitive_columns_through_eta3':40,'all9_full_root_coefficients_through_eta3':36,
    'all9_full_half_normals_through_eta3':36,'first_power_objective_coefficients':4,
    'same_author_validation_only':True,'whole_prior_analytic_replay':False,'independent_review':False}
