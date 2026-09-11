"""Independent multisets, Havel-Hakimi patterns, and incident-edge row replay."""
from collections import Counter
from fractions import Fraction
from itertools import combinations,combinations_with_replacement


def hh(ds):
 ds=sorted(ds,reverse=True)
 while ds and ds[0]:
  d=ds.pop(0)
  if d>len(ds):return False
  for i in range(d):ds[i]-=1
  if any(x<0 for x in ds):return False
  ds.sort(reverse=True)
 return True


def inventory():
 costs=(3,1,1,3,6,1,1,3,6)
 def charged(i,b):
  if i==len(costs):
   if b==0:yield ()
   return
  for n in range(b//costs[i]+1):
   for rest in charged(i+1,b-n*costs[i]):yield (n,)+rest
 out=[]
 for m in range(9):
  for k in range(max(1,m)):
   if m+k>8:continue
   for ns in charged(0,8-m-k):
    a,b,e,f,g,u,x,y,z=ns
    r6=16-sum(ns[:5]);d=36+2*m-b-4*e-5*f-6*g-2*r6;c=r6-d
    r7=26-sum(ns[5:]);w=60-4*m-3*x-4*y-5*z-r7;v=r7-w
    if min(c,d,v,w)<0:continue
    out.append((m,k,(a,b,c,d,e,f,g),(u,v,w,x,y,z,0,0)))
 return sorted(out)


def reconstruct(profile,epsq=None):
 m,k,six,seven=profile;counts_by_degree=(16,26,12)
 types=[]
 for d in(6,7,8):
  for neighbors in combinations_with_replacement((6,7,8),d):
   if sum(neighbors)>53 or (d==8 and sum(neighbors)!=53):continue
   ns=tuple(neighbors.count(a) for a in(6,7,8))
   if d<8 and (six if d==6 else seven)[ns[2]]==0:continue
   types.append((d,ns))
 types.sort()
 nt=len(types);edges=[]
 for i in range(nt):
  for j in range(i,nt):
   di,ni=types[i];dj,nj=types[j]
   if not ni[dj-6] or not nj[di-6]:continue
   if di<8 and dj<8 and ni[2]+nj[2]>12-m+k:continue
   edges.append((i,j))
 groups=[(d,c) for d,ns in((6,six),(7,seven)) for c,num in enumerate(ns) if num]
 nums=[(six if d==6 else seven)[c] for d,c in groups]
 metadata=[]
 for i,(d,(a,b,c)) in enumerate(types):
  if d==8:continue
  eps=b+2*c-(8 if d==6 else 7);f=(9 if d==6 else 4)-eps
  patterns=[]
  # Definition-level multisets, with no DP recurrence or Erdos-Gallai test.
  for word in combinations_with_replacement(range(len(groups)),f):
   if sum(groups[g][1] for g in word)!=(8-d)*(12-c):continue
   cnt=Counter(word);pat=tuple(cnt[g] for g in range(len(groups)))
   if any(pat[g]>nums[g]-(groups[g]==(d,c)) for g in range(len(groups))):continue
   if d==6 and not hh([groups[g][1] for g in word]):continue
   patterns.append(pat)
  metadata.extend((i,p) for p in sorted(patterns))
 # Generator DP chooses multiplicities in increasing lexicographic order.
 metadata.sort()
 n=nt+len(edges)+len(metadata)
 incident={i:[] for i in range(nt)}
 for col,(i,j) in enumerate(edges,nt):
  incident[i].append((col,j))
  if i!=j:incident[j].append((col,i))
 eq=[];eb=[];ub=[];bb=[]
 def eqrow(row,rhs):eq.append({i:v for i,v in row.items() if v});eb.append(rhs)
 def ubrow(row,rhs):ub.append({i:v for i,v in row.items() if v});bb.append(rhs)
 for d,num in zip((6,7,8),counts_by_degree):eqrow({i:1 for i,(dd,ns) in enumerate(types) if dd==d},num)
 for a,b in combinations(range(3),2):
  eqrow({i:(d==a+6)*ns[b]-(d==b+6)*ns[a] for i,(d,ns) in enumerate(types)},0)
 for a in range(3):
  ubrow({i:ns[a]*(ns[a]-1)+(d==a+6)*ns[a] for i,(d,ns) in enumerate(types)},counts_by_degree[a]*(counts_by_degree[a]-1))
 for a,b in combinations(range(3),2):
  ubrow({i:ns[a]*ns[b]+(d==a+6)*ns[b] for i,(d,ns) in enumerate(types)},counts_by_degree[a]*counts_by_degree[b])
 for i,(d,ns) in enumerate(types):
  for a in range(3):
   row={i:-ns[a]}
   row.update({col:1 for col,j in incident[i] if types[j][0]==a+6})
   eqrow(row,0)
   row={i:ns[a]-counts_by_degree[a]-(d-1)*(d==a+6)}
   row.update({col:types[j][1][a] for col,j in incident[i]})
   (eqrow if d==8 or a==2 else ubrow)(row,0)
 eqrow({i:Fraction(ns[2],2) for i,(d,ns) in enumerate(types) if d==8},m)
 eqrow({i:1 for i,(d,ns) in enumerate(types) if d==8 and ns[2]==2},k)
 for d,nums0 in((6,six),(7,seven)):
  for c,num in enumerate(nums0):
   if num:eqrow({i:1 for i,(dd,ns) in enumerate(types) if dd==d and ns[2]==c},num)
 for i,(d,ns) in enumerate(types):
  if d==8:continue
  cols=[(col,pat) for col,(j,pat) in enumerate(metadata,nt+len(edges)) if j==i]
  eqrow({i:-1,**{col:1 for col,pat in cols}},0)
  for a in(0,1):
   row={i:ns[a]-counts_by_degree[a]-(d-1)*(d==a+6)}
   row.update({col:types[j][1][a] for col,j in incident[i]})
   row.update({col:sum(v for (dd,cc),v in zip(groups,pat) if dd==a+6) for col,pat in cols})
   eqrow(row,0)
 for g,h in combinations(range(len(groups)),2):
  eqrow({col:(pat[h] if (types[i][0],types[i][1][2])==groups[g] else
              -pat[g] if (types[i][0],types[i][1][2])==groups[h] else 0)
         for col,(i,pat) in enumerate(metadata,nt+len(edges))},0)
 if epsq is not None:eqrow({i:ns[1] for i,(d,ns) in enumerate(types) if d==6 and ns[2]==4},epsq)
 return types,edges,eq,eb,ub,bb,metadata
