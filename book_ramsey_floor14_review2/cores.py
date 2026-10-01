"""six-reviewer-2: literal local adjacency and generator orbit carrier."""
from itertools import combinations, permutations
from collections import Counter, deque
from math import factorial
import hashlib,json
P6=tuple(combinations(range(6),2));POS={e:i for i,e in enumerate(P6)}
P10=tuple(combinations(range(10),2))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def graph(mask):
 a=[set() for _ in range(6)]
 for k,(i,j) in enumerate(P6):
  if mask>>k&1:a[i].add(j);a[j].add(i)
 return a
def moved(mask,p):
 return sum(1<<POS[tuple(sorted((p[i],p[j])))] for k,(i,j) in enumerate(P6) if mask>>k&1)
def local(mask,stars):
 f=graph(mask);a=[set() for _ in range(10)]
 for i,j in P6:
  if j in f[i]:a[4+i].add(4+j);a[4+j].add(4+i)
 for l,edge in enumerate(stars):
  for v in edge:a[l].add(4+v);a[4+v].add(l)
 h=list(map(len,a));need(h==[2]*4+[3]*6,'wrong local degrees')
 s=[[h[i]+2 if i==j else h[i]+h[j]-(5 if j in a[i] else 2)-len(a[i]&a[j]) for j in range(10)] for i in range(10)]
 return s

def build(expected):
 domain=set()
 for mask in range(1<<15):
  if mask.bit_count()!=5:continue
  a=graph(mask)
  if max(map(len,a))<=3 and all(len(a[i]&a[j])<=1 for i,j in P6 if j in a[i]):domain.add(mask)
 gens=[]
 for i in range(5):
  p=list(range(6));p[i],p[i+1]=p[i+1],p[i];gens.append(p)
 unseen=set(domain);orbits=[];profiles=[];labeled=0;prefixes=0
 while unseen:
  rep=min(unseen);orbit={rep};queue=deque([rep])
  while queue:
   m=queue.popleft()
   for p in gens:
    n=moved(m,p)
    if n not in orbit:orbit.add(n);queue.append(n)
  need(orbit<=unseen,'invalid graph orbit');unseen-=orbit
  a=graph(rep);rem=[3-len(x) for x in a];choices=[e for e in P6 if e[1] not in a[e[0]]]
  seen=Counter();chosen=[]
  def visit():
   nonlocal prefixes
   prefixes+=1
   if len(chosen)==4:
    if not any(rem):
     stars=tuple(sorted(chosen));s=local(rep,stars)
     if min(map(min,s))>=0:seen[stars]+=1
    return
   for i,j in choices:
    if rem[i]>0 and rem[j]>0:
     rem[i]-=1;rem[j]-=1;chosen.append((i,j));visit();chosen.pop();rem[i]+=1;rem[j]+=1
  visit()
  orbits.append(dict(mask=rep,size=len(orbit),profiles=len(seen)))
  for stars,multiplicity in sorted(seen.items()):
   expected_mult=factorial(4)
   for amount in Counter(stars).values():expected_mult//=factorial(amount)
   need(multiplicity==expected_mult,'ordered low row coverage differs')
   labeled+=len(orbit)*multiplicity
   profiles.append(dict(F_mask=rep,stars=[list(x) for x in stars],matrix=local(rep,stars),orbit_size=len(orbit),low_multiplicity=multiplicity))
 declared=expected['profiles']
 need([(p['F_mask'],p['stars']) for p in profiles]==[(p['F_mask'],p['stars']) for p in declared],'literal complete core domain differs from source')
 need(len(domain)==2607 and len(orbits)==11 and len(profiles)==56 and labeled==256500,'core totals differ')
 digest=hashlib.sha256(''.join(str(x)+'\n' for x in sorted(domain)).encode()).hexdigest()
 need(digest==expected['F_domain_sha256'],'complete six-graph domain hash differs')
 return profiles,dict(eligible_F=len(domain),F_orbits=orbits,profiles=len(profiles),labeled_local_cores=labeled,ordered_low_prefixes=prefixes,F_domain_sha256=digest)

def row_pairs(profile):
 s=profile['matrix'];words=list(combinations(range(10),5))
 # Every five-subset is examined; repeated rows remain in the domain.
 for pos,a in enumerate(words):
  for b in words[pos:]:
   x=[int(i in a) for i in range(10)];y=[int(i in b) for i in range(10)]
   base=[[s[i][j]-x[i]*x[j]-y[i]*y[j] for j in range(10)] for i in range(10)]
   if min(map(min,base))<0:continue
   d=[sum(row)-4*row[i] for i,row in enumerate(base)]
   need(min(d)>=0 and sum(d)==18,'slack row sum bridge')
   yield list(a),list(b),base,d
