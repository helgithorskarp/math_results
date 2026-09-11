"""Exact necessary local far-cover models; see z12_A0_reduction.md.

Pattern variables sum to42, so the full variable budget is470.
"""
from fractions import Fraction
from itertools import combinations
from math import comb

def model(profile=None, independent_bound=None):
 sizes=(16,26,12);T=[]
 for d in (6,7,8):
  for a in range(d+1):
   for b in range(d-a+1):
    c=d-a-b;s=b+2*c
    if 6*d+s>53 or (d==8 and s!=5):continue
    if profile is not None:
     m,k,six,seven=profile
     if d<8 and (six if d==6 else seven)[c]==0:continue
    T.append((d,(a,b,c)))
 E=[(i,j) for i in range(len(T)) for j in range(i,len(T)) if T[i][1][T[j][0]-6] and T[j][1][T[i][0]-6] and (independent_bound is None or T[i][0]==8 or T[j][0]==8 or T[i][1][2]+T[j][1][2]<=independent_bound)]
 eq=[];eb=[];ub=[];bb=[]
 def EQ(r,b):eq.append({i:v for i,v in r.items() if v});eb.append(b)
 def UB(r,b):ub.append({i:v for i,v in r.items() if v});bb.append(b)
 for d,n in zip((6,7,8),sizes):EQ({i:1 for i,(dd,ns) in enumerate(T) if dd==d},n)
 for a,b in combinations(range(3),2):EQ({i:(d==a+6)*ns[b]-(d==b+6)*ns[a] for i,(d,ns) in enumerate(T)},0)
 for a in range(3):UB({i:2*comb(ns[a],2)+(d==a+6)*ns[a] for i,(d,ns) in enumerate(T)},sizes[a]*(sizes[a]-1))
 for a,b in combinations(range(3),2):UB({i:ns[a]*ns[b]+(d==a+6)*ns[b] for i,(d,ns) in enumerate(T)},sizes[a]*sizes[b])
 bal={};balls={}
 for i,(d,ns) in enumerate(T):
  for a in range(3):
   bal[i,a]=len(eq);EQ({i:-ns[a]},0)
   row={i:ns[a]-sizes[a]-(d-1)*(d==a+6)}
   if d==8 or a==2:balls[i,a]=('eq',len(eq));EQ(row,0)
   else:balls[i,a]=('ub',len(ub));UB(row,0)
 for col,(i,j) in enumerate(E,len(T)):
  for root,other in [(i,j)] if i==j else [(i,j),(j,i)]:
   d,ns=T[other];eq[bal[root,d-6]][col]=1
   for a in range(3):
    kind,row=balls[root,a];(eq if kind=='eq' else ub)[row][col]=ns[a]
 if profile is not None:
  m,k,six,seven=profile
  EQ({i:Fraction(ns[2],2) for i,(d,ns) in enumerate(T) if d==8},m)
  EQ({i:1 for i,(d,ns) in enumerate(T) if d==8 and ns[2]==2},k)
  for d,nums in ((6,six),(7,seven)):
   for c,num in enumerate(nums):
    if num:EQ({i:1 for i,(dd,ns) in enumerate(T) if dd==d and ns[2]==c},num)
 return T,E,eq,eb,ub,bb

from functools import lru_cache
from itertools import combinations


def graphical(degrees):
 ds=sorted(degrees,reverse=True)
 if sum(ds)%2:return False
 return all(sum(ds[:k])<=k*(k-1)+sum(min(k,d) for d in ds[k:]) for k in range(1,len(ds)+1))


def patterns(groups,counts,root,f,total,d):
 caps=[num-(g==root) for g,num in zip(groups,counts)]
 @lru_cache(None)
 def visit(i,n,w):
  if n<0 or w<0:return ()
  if i==len(groups):return ((),) if n==w==0 else ()
  c=groups[i][1];out=[]
  for v in range(min(caps[i],n)+1):
   for rest in visit(i+1,n-v,w-v*c):out.append((v,)+rest)
  return tuple(out)
 for p in visit(0,f,total):
  ds=[c for (_,c),n in zip(groups,p) for _ in range(n)]
  if d==7 or graphical(ds):yield p


def far_model(profile):
 m,k,six,seven=profile
 groups=[(d,c) for d,ns in ((6,six),(7,seven)) for c,n in enumerate(ns) if n]
 counts=[(six if d==6 else seven)[c] for d,c in groups]
 T,E,eq,eb,ub,bb=model(profile,12-m+k)
 n=len(T)+len(E);patcols={};metadata=[]
 for i,(d,(a,b,c)) in enumerate(T):
  if d==8:continue
  eps=b+2*c-(8 if d==6 else 7);f=(9 if d==6 else 4)-eps
  columns=[]
  for pat in patterns(tuple(groups),tuple(counts),(d,c),f,(8-d)*(12-c),d):
   col=n+len(metadata);metadata.append((i,pat));columns.append((col,pat))
  patcols[i]=columns
  eq.append({i:-1,**{col:1 for col,pat in columns}});eb.append(0)
  for target in (6,7):
   row={i:(a if target==6 else b)-(16 if target==6 else 26)-(d-1)*(d==target)}
   for col,(u,v) in enumerate(E,len(T)):
    if u==i:row[col]=T[v][1][target-6]
    elif v==i:row[col]=T[u][1][target-6]
   for col,pat in columns:row[col]=sum(v for (dd,cc),v in zip(groups,pat) if dd==target)
   eq.append(row);eb.append(0)
 for g,h in combinations(range(len(groups)),2):
  row={}
  for col,(i,pat) in enumerate(metadata,n):
   d,ns=T[i];root=(d,ns[2])
   if root==groups[g]:row[col]=pat[h]
   elif root==groups[h]:row[col]=-pat[g]
  eq.append(row);eb.append(0)
 return T,E,eq,eb,ub,bb,metadata


def cases():
 from a0_inventory import profiles
 rows=list(profiles())
 indices=[i for i,row in enumerate(rows) if row[0]==6]
 for i in indices:
  if i==395:continue
  for epsq in ((0,1,2) if i==401 else (None,)):
   T,E,eq,eb,ub,bb,meta=far_model(rows[i])
   if epsq is not None:
    eq.append({j:b for j,(d,(a,b,c)) in enumerate(T) if d==6 and c==4});eb.append(epsq)
   name='m6_profile_'+str(i)+('' if epsq is None else '_quad_epsilon_'+str(epsq))
   yield name,rows[i],epsq,(T,E,eq,eb,ub,bb,meta)
