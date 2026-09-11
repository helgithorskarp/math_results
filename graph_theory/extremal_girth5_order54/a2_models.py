"""Exact necessary models for z12_A2_reduction.md; standard library only."""
from fractions import Fraction
from itertools import combinations
def compositions(n,bounds):
 if not bounds:
  if n==0:yield ()
  return
 for x in range(min(n,bounds[0])+1):
  for tail in compositions(n-x,bounds[1:]):yield (x,)+tail


def model(kind,p,profile=None):
 # p degree-seven missed endpoints; endpoints total2 except shared total1.
 r=1 if kind=='one' else 2;x=1 if kind=='shared' else 2;a=2 if kind=='one' else 1
 sizes=[16-(x-p),26-p,12-r,r];ds=[6,7,8,8]
 if x-p:sizes.append(x-p);ds.append(6)
 if p:sizes.append(p);ds.append(7)
 nc=len(ds);T=[]
 for cl,d in enumerate(ds):
  for ns in compositions(d,[s-(cl==i) for i,s in enumerate(sizes)]):
   w=sum(x*y for x,y in zip(ds,ns));nx=sum(ns[4:])
   if w>53:continue
   if cl==2 and (w!=53 or nx):continue
   if cl==3 and (w!=53-a or nx!=(kind=='matching')):continue
   if cl>=4 and (ns[2] or ns[3]!=(kind=='matching')):continue
   if kind=='matching' and ((cl==3 and ns[3]) or (cl>=4 and nx) or (cl<2 and ns[3] and nx)):continue
   if profile is not None and d in (6,7) and not any(dd==d and c==ns[2]+ns[3] for dd,c,num in profile):continue
   T.append((cl,ns))
 nt=len(T);E=[(i,j) for i in range(nt) for j in range(i,nt) if T[i][1][T[j][0]] and T[j][1][T[i][0]]]
 eq=[];eb=[];ub=[];bb=[]
 def add(rows,bs,row,b):rows.append({i:v for i,v in row.items() if v});bs.append(b)
 def EQ(row,b):add(eq,eb,row,b)
 def UB(row,b):add(ub,bb,row,b)
 for a in range(nc):EQ({i:1 for i,(cl,ns) in enumerate(T) if cl==a},sizes[a])
 for a,b in combinations(range(nc),2):EQ({i:(cl==a)*ns[b]-(cl==b)*ns[a] for i,(cl,ns) in enumerate(T)},0)
 for a in range(nc):UB({i:ns[a]*(ns[a]-1)+(cl==a)*ns[a] for i,(cl,ns) in enumerate(T)},sizes[a]*(sizes[a]-1))
 for a,b in combinations(range(nc),2):UB({i:ns[a]*ns[b]+(cl==a)*ns[b] for i,(cl,ns) in enumerate(T)},sizes[a]*sizes[b])
 bal={};ball={}
 for i,(cl,ns) in enumerate(T):
  for a in range(nc):
   bal[i,a]=len(eq);EQ({i:-ns[a]},0)
   exact=(a in (2,3) or cl==2 or (cl==3 and a<4))
   f=(r if kind=='shared' else 1) if cl>=4 and a==3 else 0
   if cl==3 and a>=4:
    if kind in ('one','shared'):exact=True;f=sizes[a]
    elif kind=='matching':exact=True;f=sizes[a]-ns[a]
    elif nc==5:exact=True;f=1
   row={i:ns[a]-sizes[a]+f-(ds[cl]-1)*(cl==a)}
   if exact:ball[i,a]=(True,len(eq));EQ(row,0)
   else:ball[i,a]=(False,len(ub));UB(row,0)
 for col,(i,j) in enumerate(E,nt):
  for v,w in ([(i,j)] if i==j else [(i,j),(j,i)]):
   cl,ns=T[w];eq[bal[v,cl]][col]=1
   for a in range(nc):
    ex,k=ball[v,a];(eq if ex else ub)[k][col]=ns[a]
 inventory={};epss={};ceps={};gap={};m={}
 for i,(cl,ns) in enumerate(T):
  d=ds[cl];c=ns[2]+ns[3];s=sum(ns[j]*(dd-6) for j,dd in enumerate(ds));eps=s-(8 if d==6 else 7)
  if d==8:inventory[i]=Fraction(c,2)+int(c==2);ceps[i]=-c-c*(5-s);m[i]=-Fraction(c,2)
  else:inventory[i]=((c-3)*(c-2) if d==6 else (c-1)*(c-2))//2;epss[i]=eps;ceps[i]=c*eps;gap[i]=eps*eps if d==6 else eps*(eps-1)
 p7=p*(2 if kind=='shared' else 1)
 EQ(inventory,6);EQ(epss,6);EQ(ceps,-p7);UB(gap,28-(12 if kind=='one' else 10)-4*p7);UB(m,-2)
 return sizes,ds,T,E,eq,eb,ub,bb

from itertools import product
from fractions import Fraction

def profiles(p):
 for m in range(2,7):
  for k in range(m):
   B=6-m-k
   if B<2-p:continue
   # Nonzero-charge low c types (6,0):3,(6,1):1,(6,4):1,(6,5):3;
   # (7,0):1,(7,3):1,(7,4):3. Larger types cost >=6, above B<=4.
   costs=[3,1,1,3,1,1,3]
   for a in product(*(range(B//c+1) for c in costs)):
    if sum(x*c for x,c in zip(a,costs))!=B:continue
    n60,n61,n64,n65,n70,n73,n74=a
    if n61<2-p:continue
    l6=16-sum(a[:4]);n63=38+2*m-(n61+4*n64+5*n65)-2*l6;n62=l6-n63
    l7=26-(n70+n73+n74);n72=58-4*m-(3*n73+4*n74)-l7;n71=l7-n72
    if min(n62,n63,n71,n72)<0 or n71<p:continue
    rec=[(6,c,n) for c,n in enumerate((n60,n61,n62,n63,n64,n65)) if n]
    rec +=[(7,c,n) for c,n in enumerate((n70,n71,n72,n73,n74)) if n]
    yield m,k,rec

def build(p,m,k,profile):
 sizes,ds,T,E,eq,eb,ub,bb=model('matching',p,profile)
 for d,c,n in profile:
  eq.append({i:1 for i,(cl,ns) in enumerate(T) if ds[cl]==d and ns[2]+ns[3]==c});eb.append(n)
 for i,(cl,ns) in enumerate(T):
  if ds[cl] in (6,7) and not any(d==ds[cl] and c==ns[2]+ns[3] for d,c,n in profile):ub.append({i:1});bb.append(0)
 eq.append({i:Fraction(ns[2]+ns[3],2) for i,(cl,ns) in enumerate(T) if ds[cl]==8});eb.append(m)
 eq.append({i:1 for i,(cl,ns) in enumerate(T) if ds[cl]==8 and ns[2]+ns[3]==2});eb.append(k)
 # Individual distant-cover consequences, valid for the complete profile.
 counts={(d,c):n for d,c,n in profile}
 b1={};b2={}
 for i,(cl,ns) in enumerate(T):
  if ds[cl]!=7:continue
  c=ns[2]+ns[3];eps=sum(ns[a]*(dd-6) for a,dd in enumerate(ds))-7
  if c==2 and eps==2:ub.append({i:1});bb.append(0)
  if (c,eps)==(1,1):b1[i]=1
  if (c,eps)==(2,1):b2[i]=1
 n5=counts.get((6,5),0);n4=counts.get((6,4),0);n74=counts.get((7,4),0)
 W=dict(b2);W.update({i:2 for i in b1})
 ub.append(W);bb.append(14*n5+9*n4+3*n74)
 if not n5:
  if n4+n74<2 or (n4==2 and not n74):ub.append(b1);bb.append(0)
  elif n4==3 and not n74:ub.append(b1);bb.append(3)
 else:
  ub.append(b1);bb.append(7)
 return sizes,ds,T,E,eq,eb,ub,bb


def bounds(p,m,k,profile):
 ct={(d,c):n for d,c,n in profile};n5=ct.get((6,5),0);n4=ct.get((6,4),0);n74=ct.get((7,4),0);b1=ct.get((7,1),0)
 if not n5 and (n4+n74<2 or (n4==2 and not n74)):b1=0
 elif not n5 and n4==3 and not n74:b1=min(b1,3)
 elif n5:b1=min(b1,7)
 pos=sum(n*((c-3)*(c-2) if c<2 else (c-3)*(2*c-8) if c>=4 else 0) for d,c,n in profile if d==6)+sum(n*(c-3)*(2*c-7) for d,c,n in profile if d==7 and c>=4)
 lower=18-2*m-min(m,2+k)+p+pos
 upper=min(14*n5+9*n4+3*n74,24-4*p+b1,2*b1+ct.get((7,2),0))
 return lower,upper



def m_case():
 from forest_constraints import model as ordinary_model
 T,E,eq,eb,ub,bb=ordinary_model((16,26,12),False)
 eq.append({i:5-b-2*c for i,(d,(a,b,c)) in enumerate(T) if d==8});eb.append(2)
 objective=[Fraction(0)]*(len(T)+len(E))
 for i,(d,ns) in enumerate(T):
  if d==8:objective[i]=Fraction(ns[2],2)
 return (T,E,eq,eb,ub,bb),objective


RESIDUAL_PROFILES={(2,81),(2,92)}

def initial_cases():
 data,obj=m_case()
 yield 'm_at_A2',data,obj,None
 for kind in ('one','shared','zero'):
  for p in range(2 if kind=='shared' else 3):
   sizes,ds,T,E,eq,eb,ub,bb=model(kind,p)
   yield kind+'_'+str(p),(T,E,eq,eb,ub,bb),[Fraction(0)]*(len(T)+len(E)),(kind,p,None,None,None)
 for p in range(3):
  for i,(m,k,pr) in enumerate(profiles(p)):
   lo,hi=bounds(p,m,k,pr)
   if lo>hi or (p,i) in RESIDUAL_PROFILES:continue
   sizes,ds,T,E,eq,eb,ub,bb=build(p,m,k,pr)
   yield 'matching_profile_'+str(p)+'_'+str(i),(T,E,eq,eb,ub,bb),[Fraction(0)]*(len(T)+len(E)),('matching',p,m,k,pr)


def cases():
 yield from initial_cases()
 for m,rho in ((4,0),(5,0),(5,1),(4,2),(5,2)):
  idx=81 if m==4 else 92
  mm,k,pr=list(profiles(2))[idx]
  sizes,ds,T,E,eq,eb,ub,bb=build(2,m,0,pr)
  eq.append({i:ns[2]+ns[3] for i,(cl,ns) in enumerate(T) if cl==3});eb.append(rho)
  obj=[Fraction(0)]*(len(T)+len(E))
  if rho==2:
   for i,(cl,ns) in enumerate(T):
    if cl>=4:obj[i]=2-ns[0]
  name=('endpoint_bound_' if rho==2 else 'rho_')+str(m)+'_'+str(rho)
  yield name,(T,E,eq,eb,ub,bb),obj,('residual',2,m,rho,pr)
 from a2_partner_model import model as partner_model
 sizes,ds,T,E,eq,eb,ub,bb=partner_model(4,1)
 yield 'partner_4_1',(T,E,eq,eb,ub,bb),[Fraction(0)]*(len(T)+len(E)),('partner',2,4,1,None)
