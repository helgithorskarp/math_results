"""Exact necessary models for z12_A3_exclusion.md; no solver dependency."""
from fractions import Fraction
from forest_constraints import model as degree_model
from itertools import combinations
from math import comb

def compositions(total,n):
 if n==1:
  yield (total,);return
 for a in range(total+1):
  for t in compositions(total-a,n-1):yield (a,)+t

def model(p=0,profile=None,m=None,k=None):
 # bulk6,bulk7,S,R,X6[,X7]
 sizes=[13+p,26-p,9,3,3-p]+([p] if p else [])
 degrees=[6,7,8,8,6]+([7] if p else [])
 nc=len(sizes);types=[]
 for cls,d in enumerate(degrees):
  for ns in compositions(d,nc):
   if any(ns[i]>sizes[i]-(i==cls) for i in range(nc)):continue
   weighted=sum(a*b for a,b in zip(ns,degrees))
   if weighted>53:continue
   h=ns[2]+ns[3];nx=sum(ns[4:])
   if d==8 and h>2:continue
   if cls==2 and (weighted!=53 or nx or ns[3]>1):continue
   if cls==3 and (weighted!=52 or nx!=2 or ns[3]):continue
   if cls>=4 and (ns[3]!=2 or ns[2] or nx):continue
   if cls<2 and (ns[3]>1 or nx>1):continue
   if profile is not None and cls!=2 and cls!=3:
    if not any(dd==d and c==h for dd,c,num in profile):continue
    eps=weighted-6*d-(8 if d==6 else 7)
    if d==7 and h==2 and eps==2:continue
   types.append((cls,ns))
 nt=len(types);edges=[(i,j) for i in range(nt) for j in range(i,nt) if types[i][1][types[j][0]] and types[j][1][types[i][0]]]
 eq=[];eb=[];ub=[];bb=[]
 def E(row,rhs):eq.append({i:v for i,v in row.items() if v});eb.append(rhs)
 def U(row,rhs):ub.append({i:v for i,v in row.items() if v});bb.append(rhs)
 for cls in range(nc):E({i:1 for i,(cl,ns) in enumerate(types) if cls==cl},sizes[cls])
 for a,b in combinations(range(nc),2):E({i:(cl==a)*ns[b]-(cl==b)*ns[a] for i,(cl,ns) in enumerate(types)},0)
 for a in range(nc):U({i:2*comb(ns[a],2)+(cl==a)*ns[a] for i,(cl,ns) in enumerate(types)},2*comb(sizes[a],2))
 for a,b in combinations(range(nc),2):U({i:ns[a]*ns[b]+(cl==a)*ns[b] for i,(cl,ns) in enumerate(types)},sizes[a]*sizes[b])
 balances={};balls={}
 for i,(cl,ns) in enumerate(types):
  for a in range(nc):
   balances[i,a]=len(eq);E({i:-ns[a]},0)
   # All S are sinks. All R miss only their matched X. Every low bulk
   # vertex reaches all R; an X reaches exactly the other two R.
   far=1 if cl>=4 and a==3 else 0
   exact=(a==2 or a==3 or (cl in(2,3) and a<4) or cl==2)
   row={i:ns[a]-sizes[a]+far-(degrees[cl]-1)*(cl==a)}
   if exact:balls[i,a]=('eq',len(eq));E(row,0)
   else:balls[i,a]=('ub',len(ub));U(row,0)
 for col,(i,j) in enumerate(edges,nt):
  for root,neighbor in ([(i,j)] if i==j else [(i,j),(j,i)]):
   cl,ns=types[neighbor];eq[balances[root,cl]][col]=1
   for a in range(nc):
    key,row=balls[root,a]
    (eq if key=='eq' else ub)[row][col]=ns[a]
 if profile is not None:
  for d,c,num in profile:E({i:1 for i,(cl,ns) in enumerate(types) if degrees[cl]==d and ns[2]+ns[3]==c},num)
  # b1=0 with two fours; <=3 with three.
  count4=next(num for d,c,num in profile if d==6 and c==4)
  U({i:1 for i,(cl,ns) in enumerate(types) if degrees[cl]==7 and ns[2]+ns[3]==1 and sum(ns[j]*(degrees[j]-6) for j in range(nc))==8},0 if count4==2 else 3)
 if m is not None:E({i:Fraction(ns[2]+ns[3],2) for i,(cl,ns) in enumerate(types) if cl in(2,3)},m)
 if k is not None:E({i:1 for i,(cl,ns) in enumerate(types) if cl in(2,3) and ns[2]+ns[3]==2},k)
 return sizes,degrees,types,edges,eq,eb,ub,bb


PROFILES = [
    (2,0,'six1',[(6,1,1),(6,2,5),(6,3,8),(6,4,2),(7,1,3),(7,2,23)]),
    (2,0,'threefour',[(6,2,8),(6,3,5),(6,4,3),(7,1,3),(7,2,23)]),
    (2,0,'sev0',[(6,2,7),(6,3,7),(6,4,2),(7,0,1),(7,1,1),(7,2,24)]),
    (2,0,'sev3',[(6,2,7),(6,3,7),(6,4,2),(7,1,4),(7,2,21),(7,3,1)]),
    (2,1,'P3',[(6,2,7),(6,3,7),(6,4,2),(7,1,3),(7,2,23)]),
    (3,0,'3P2',[(6,2,5),(6,3,9),(6,4,2),(7,1,7),(7,2,19)])]


def base_case(shared=False):
    T,E,eq,eb,ub,bb=degree_model((16,26,12),False)
    if shared:
        for d,c,num in PROFILES[0][3]:
            eq.append({i:1 for i,(dd,ns) in enumerate(T) if dd==d and ns[2]==c});eb.append(num)
        for c,num in enumerate((8,4,0)):
            eq.append({i:1 for i,(d,ns) in enumerate(T) if d==8 and ns[2]==c});eb.append(num)
    eq.append({i:5-b-2*c for i,(d,(a,b,c)) in enumerate(T) if d==8});eb.append(3)
    if shared:
        ub.append({i:c*(5-b-2*c) for i,(d,(a,b,c)) in enumerate(T) if d==8});bb.append(2)
        for i,(d,(a,b,c)) in enumerate(T):
            if (d==8 and b+2*c not in (4,5)) or (d==7 and ((c==1 and b+2*c==8) or (c==2 and b+2*c==9))):
                ub.append({i:1});bb.append(0)
    return T,E,eq,eb,ub,bb


def cases():
    for shared in (False,True):
        T,E,eq,eb,ub,bb=base_case(shared)
        objective=[Fraction(0)]*(len(T)+len(E))
        if not shared:
            for i,(d,ns) in enumerate(T):
                if d==8:objective[i]=Fraction(ns[2],2)
        yield ('shared_six_endpoint' if shared else 'm_at_A3'),(T,E,eq,eb,ub,bb),objective
    for p in (0,1):
        for m,k,name,profile in PROFILES:
            _,_,T,E,eq,eb,ub,bb=model(p,profile,m,k)
            yield 'cycle_p'+str(p)+'_'+name,(T,E,eq,eb,ub,bb),[Fraction(0)]*(len(T)+len(E))
