"""Necessary local contact-map constraints; see PROOF.md. Stdlib only."""
from itertools import combinations, permutations
from collections import Counter,defaultdict

F,D,U,V,A,B,C,Z,I,R,S,P=range(12)
ORD=set(range(8,15)); THREE={U,V}; ONET={A,B,C}; ZERO={U,V,Z}
DEG={v:5 if v in (F,D) else 3 if v in THREE else 4 for v in range(15)}
QUOTA={v:4 if v==F else 3 if v==D else 0 if v in ZERO else 1 if v in ONET else 2 for v in range(15)}

def edge(a,b):return tuple(sorted((a,b)))
def face(f):
 return min(tuple(x[k:]+x[:k]) for x in (list(f),list(reversed(f))) for k in range(len(f)))

class Bad(Exception):pass

class Patch:
 def __init__(self,faces=(),extra=(),*,fd_contact=False,missing_capacity=True):
  self.fd_contact=fd_contact
  self.missing_capacity=missing_capacity
  self.faces=set(face(f) for f in faces)
  self.extra=set(edge(*e) for e in extra)
 def plus(self,*fs):return Patch(self.faces|set(face(f) for f in fs),self.extra,fd_contact=self.fd_contact,missing_capacity=self.missing_capacity)
 def evaluate(self,check_edges=True):
  faces=set(self.faces); contacts=set(self.extra); non=set() if self.fd_contact else {edge(F,D)}
  for f in sorted(faces):
   if len(f) not in (3,4) or len(set(f))!=len(f):raise Bad('simple-face')
   contacts.update(edge(f[k],f[(k+1)%len(f)]) for k in range(len(f)))
   if len(f)==4:non.update((edge(f[0],f[2]),edge(f[1],f[3])))
  if contacts&non:raise Bad('contact-diagonal')
  for e in contacts:
   if set(e)&THREE and set(e)&ORD:raise Bad('ordinary-three-contact')
   if e==edge(U,V):raise Bad('three-three-contact')
  n={v:set() for v in range(15)}
  for a,b in contacts:
   if a==b:raise Bad('contact-loop')
   n[a].add(b);n[b].add(a)
  if any(len(n[v])>DEG[v] for v in n):raise Bad('degree')
  # Every contact 3-cycle is an empty minor equilateral triangle, hence a face.
  for q in combinations(range(15),3):
   if all(edge(a,b) in contacts for a,b in combinations(q,2)):faces.add(face(q))
  ts=Counter(v for f in faces if len(f)==3 for v in f)
  if any(ts[v]>QUOTA[v] for v in n):raise Bad('T-quota')
  ec=defaultdict(list); corner={v:{} for v in n}
  for f in sorted(faces):
   for k,v in enumerate(f):
    e=edge(v,f[(k+1)%len(f)]);ec[e].append(f)
    c=edge(f[k-1],f[(k+1)%len(f)])
    if c in corner[v] and corner[v][c]!=f:raise Bad('repeated-corner')
    corner[v][c]=f
   if len(f)==4:
    for k,v in enumerate(f):
     o=f[(k+2)%4]
     if v in (F,D) and o not in ONET|{Z}:raise Bad('five-opposite-corner')
     if v==D and V in n[D] and V not in (f[k-1],f[(k+1)%4]):raise Bad('D-Q-misses-three')
  if any(len(a)>2 for a in ec.values()):raise Bad('edge-face-count')
  for a,b in combinations(range(15),2):
   if len(n[a]&n[b])>2:raise Bad('common-contact')
  qq=set()
  for e in contacts:
   if set(e)&ZERO or len(ec[e])==2 and all(len(f)==4 for f in ec[e]):qq.add(e)
  qqd=Counter(v for e in qq for v in e)
  maxqq={v:DEG[v] if QUOTA[v]==0 else 2 if QUOTA[v]==1 else 1 if QUOTA[v] in (2,3) else 0 for v in n}
  if any(qqd[v]>maxqq[v] for v in n):raise Bad('QQ-quota')
  cycles={}
  for v in n:
   adj=defaultdict(set)
   for a,b in corner[v]:adj[a].add(b);adj[b].add(a)
   if any(len(q)>2 for q in adj.values()):raise Bad('link-degree')
   if adj:
    todo=set(adj)
    while todo:
     seed=next(iter(todo));component={seed};pending=[seed]
     while pending:
      x=pending.pop()
      for y in adj[x]:
       if y not in component:component.add(y);pending.append(y)
     todo-=component
     if all(len(adj[x])==2 for x in component) and len(component)!=DEG[v]:raise Bad('short-closed-link')
   # If exactly one contact is missing and all known corners form one
   # spanning link path, its two ends must meet the missing neighbor.
   # A new T there needs unused T capacity at that end original.
   if self.missing_capacity and len(n[v])==DEG[v]-1 and set(adj)==n[v] and sum(len(a) for a in adj.values())==2*(len(n[v])-1):
    ends=[a for a in adj if len(adj[a])==1]
    if len(ends)==2 and QUOTA[v]-ts[v]>sum(ts[a]<QUOTA[a] for a in ends):
     raise Bad('missing-star-T-capacity')
   if len(n[v])!=DEG[v]:continue
   a=min(n[v]);opts=[]
   for tail in permutations(sorted(n[v]-{a})):
    cyc=(a,)+tail
    if cyc[1]>cyc[-1]:continue
    ces={edge(cyc[k],cyc[(k+1)%len(cyc)]) for k in range(len(cyc))}
    if not set(corner[v])<=ces:continue
    t=sum(e in contacts for e in ces);unknown=sum(e not in contacts|non for e in ces)
    if t<=QUOTA[v]<=t+unknown:opts.append(cyc)
   if not opts:raise Bad('no-full-link-cycle')
   cycles[v]=opts
  if check_edges:
   for (u,v),fs in sorted(ec.items()):
    if len(fs)!=1 or u not in cycles or v not in cycles:continue
    f=fs[0]
    def other(v,w):
     k=f.index(v);known=f[k-1] if f[(k+1)%len(f)]==w else f[(k+1)%len(f)]
     out=set()
     for cyc in cycles[v]:
      j=cyc.index(w);nbr={cyc[j-1],cyc[(j+1)%len(cyc)]}
      if known not in nbr:raise RuntimeError('known corner missing')
      out.update(nbr-{known})
     return out
    found=False
    for w in other(u,v):
     for x in other(v,u):
      ff=(u,v,w) if w==x else (u,v,x,w)
      try:self.plus(ff).evaluate(False)
      except Bad:continue
      found=True
    if not found:raise Bad('no-other-edge-face')
  return {'contacts':n,'cycles':cycles,'faces':faces}
