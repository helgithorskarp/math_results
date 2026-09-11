"""Necessary singleton-partner models; see z12_A2_reduction.md."""
from itertools import combinations
from fractions import Fraction
def compositions(n,bounds):
 if not bounds:
  if n==0:yield ()
  return
 for x in range(min(n,bounds[0])+1):
  for tail in compositions(n-x,bounds[1:]):yield (x,)+tail

def model(m,rho,endpoint_unit=False):
 frame={"r":2,"far":[[3],[2]],"degrees":[8,8,7,7]+[8]*rho,"edges":[[0,2],[1,3]]+[[i,4+i] for i in range(rho)]}
 profile=[(6,2,4 if m==4 else 1),(6,3,10 if m==4 else 14),(6,4,2 if m==4 else 1),(7,1,10 if m==4 else 14),(7,2,16 if m==4 else 12)]
 r=frame['r'];core_ds=frame['degrees'];nc0=len(core_ds);far=list(map(set,frame['far']))
 adj=[set() for _ in core_ds]
 for a,b in frame['edges']:adj[a].add(b);adj[b].add(a)
 missed=set().union(*far)
 sizes=[16-core_ds.count(6),26-core_ds.count(7),12-core_ds.count(8)]+[1]*nc0
 ds=[6,7,8]+core_ds;nc=len(ds);types=[]
 q=sum(x<r for f in far for x in f)//2;p7=sum(core_ds[x]==7 for f in far for x in f)
 for cl,d in enumerate(ds):
  for ns in compositions(d,[s-(cl==a) for a,s in enumerate(sizes)]):
   total=sum(a*b for a,b in zip(ds,ns))
   if total>53:continue
   if cl==2 and (total!=53 or any(ns[3+x] for x in range(nc0))):continue
   if cl>=3:
    v=cl-3
    if any(ns[3+x]!=int(x in adj[v]) for x in range(nc0)):continue
    if ns[2]:continue
    if v>=r and core_ds[v]==8 and total!=53:continue
    if v<r and total!=53-len(far[v]):continue
   good=True
   for a,b in combinations(range(nc0),2):
    if not (ns[3+a] and ns[3+b]):continue
    if b in adj[a] or (a<r and b in far[a]) or (b<r and a in far[b]):good=False;break
    common=adj[a]&adj[b]
    if common and (cl<3 or cl-3 not in common):good=False;break
   c=sum(ns[a] for a,dd in enumerate(ds) if dd==8)
   if d==8 and c>1:continue
   if d in (6,7) and not any(dd==d and cc==c for dd,cc,num in profile):continue
   eps=total-6*d-(8 if d==6 else 7)
   if d==7 and ((c==1 and eps==1) or (c==2 and eps==2)):continue
   if endpoint_unit and cl in (5,6) and ns[0]!=1:continue
   if good:types.append((cl,ns))
 nt=len(types);edges=[(i,j) for i in range(nt) for j in range(i,nt) if types[i][1][types[j][0]] and types[j][1][types[i][0]]]
 eq=[];eb=[];ub=[];bb=[]
 def E(row,b):eq.append({i:v for i,v in row.items() if v});eb.append(b)
 def U(row,b):ub.append({i:v for i,v in row.items() if v});bb.append(b)
 for a in range(nc):E({i:1 for i,(cl,ns) in enumerate(types) if cl==a},sizes[a])
 for a,b in combinations(range(nc),2):E({i:(cl==a)*ns[b]-(cl==b)*ns[a] for i,(cl,ns) in enumerate(types)},0)
 for a in range(nc):U({i:ns[a]*(ns[a]-1)+(cl==a)*ns[a] for i,(cl,ns) in enumerate(types)},sizes[a]*(sizes[a]-1))
 for a,b in combinations(range(nc),2):U({i:ns[a]*ns[b]+(cl==a)*ns[b] for i,(cl,ns) in enumerate(types)},sizes[a]*sizes[b])
 balances={};balls={}
 for i,(cl,ns) in enumerate(types):
  for a in range(nc):
   balances[i,a]=len(eq);E({i:-ns[a]},0)
   exact=False;f=0
   if a==2 or cl==2:exact=True
   if cl>=3 and ds[cl]==8:
    exact=True;f=int(cl-3<r and a>=3 and a-3 in far[cl-3])
   elif a>=3 and ds[a]==8:
    exact=True;f=int(a-3<r and cl>=3 and cl-3 in far[a-3])
   row={i:ns[a]-sizes[a]+f-(ds[cl]-1)*(cl==a)}
   if exact:balls[i,a]=(True,len(eq));E(row,0)
   else:balls[i,a]=(False,len(ub));U(row,0)
 for col,(i,j) in enumerate(edges,nt):
  for v,w in ([(i,j)] if i==j else [(i,j),(j,i)]):
   cl,ns=types[w];eq[balances[v,cl]][col]=1
   for a in range(nc):
    exact,k=balls[v,a];(eq if exact else ub)[k][col]=ns[a]
 # Corrected degree identities with A=2, every exceptional incidence retained.
 inventory={};eps_sum={};ceps={};gap={}
 for i,(cl,ns) in enumerate(types):
  d=ds[cl];c=sum(ns[a] for a,dd in enumerate(ds) if dd==8);s=sum(ns[a]*(dd-6) for a,dd in enumerate(ds));eps=s-(8 if d==6 else 7)
  if d==8:
   inventory[i]=Fraction(c,2)+int(c==2)
   ceps[i]=-c-c*(5-s)
  else:
   inventory[i]=((c-3)*(c-2) if d==6 else (c-1)*(c-2))//2
   eps_sum[i]=eps;ceps[i]=c*eps;gap[i]=eps*eps if d==6 else eps*(eps-1)
 E(inventory,6-q);E(eps_sum,6);E(ceps,-p7-4*q)
 U(gap,28-sum(len(f)*(len(f)+4) for f in far)-4*p7-8*q)
 for d,c,num in profile:E({i:1 for i,(cl,ns) in enumerate(types) if ds[cl]==d and sum(ns[j] for j,dd in enumerate(ds) if dd==8)==c},num)
 E({i:Fraction(sum(ns[j] for j,dd in enumerate(ds) if dd==8),2) for i,(cl,ns) in enumerate(types) if ds[cl]==8},m)
 return sizes,ds,types,edges,eq,eb,ub,bb
