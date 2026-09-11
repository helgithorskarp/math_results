"""Exact necessary incidence models; see z12_A0_multi_quad_exclusion.md."""
from a0_inventory import profiles
from a0_quad_orbits import forest,independent,reps
from itertools import combinations
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType

def build(index,orbit,stage="base"):
 if index not in (372,373,377,378,386):raise ValueError("Unknown profile")
 m,k,six,seven=list(profiles())[index]
 quads=reps(k,six[4])[orbit];H=forest(k); h=[sum(t in e for e in H) for t in range(12)]
 pool=IDPool();cnf=CNF()
 def card(lits,bound,mode='eq'):
  if bound<0 and mode=='ge':return
  if bound<0 or (mode!='le' and bound>len(lits)):cnf.append([]);return
  if mode=='le' and bound>=len(lits):return
  if not lits:
   if bound:cnf.append([])
   return
  f={'eq':CardEnc.equals,'le':CardEnc.atmost,'ge':CardEnc.atleast}[mode]
  cnf.extend(f(lits,bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses)
 # Vertex slots of each actual high set. Sets of size>=2 cannot repeat;
 # singleton multiplicity bounded by its high point's corresponding quota.
 vertices=[(6,Q,0) for Q in quads]
 qids=list(range(len(quads)))
 for d,counts in [(6,six),(7,seven)]:
  for c,n in enumerate(counts):
   if not n or c==4:continue
   for B in combinations(range(12),c):
    B=frozenset(B)
    if not independent(B,k) or any(len(B&Q)>1 for Q in quads):continue
    copies=min(n,(3+h[next(iter(B))] if d==6 else 5-2*h[next(iter(B))])) if c==1 else (n if c==0 else 1)
    for j in range(copies):vertices.append((d,B,j))
 X=[pool.id(('x',i)) for i in range(len(vertices))]
 for q in qids:cnf.append([X[q]])
 for d,counts in [(6,six),(7,seven)]:
  for c,n in enumerate(counts):
   card([X[i] for i,(dd,B,j) in enumerate(vertices) if dd==d and len(B)==c],n)
 for t in range(12):
  for d,bound in [(6,3+h[t]),(7,5-2*h[t])]:
   card([X[i] for i,(dd,B,j) in enumerate(vertices) if dd==d and t in B],bound)
 for a,b in combinations(range(12),2):
  if not independent({a,b},k):continue
  card([X[i] for i,(d,B,j) in enumerate(vertices) if a in B and b in B],1)
 # Slot-prefix symmetry only for repeated singleton or empty sets.
 slots={}
 for i,(d,B,j) in enumerate(vertices):slots.setdefault((d,B),[]).append(i)
 for ids in slots.values():
  for a,b in zip(ids,ids[1:]):cnf.append([-X[b],X[a]])
 near={}; near7=[]
 for q,Q in enumerate(quads):
  forbidden=Q|{v for e in H if set(e)&Q for v in e}
  R=frozenset(range(12))-forbidden
  choices=[]
  eligible=[i for i,(d,B,j) in enumerate(vertices) if i!=q and B<=R]
  for a,b in combinations(eligible,2):
   A=vertices[a][1];B=vertices[b][1]
   if A&B or A|B!=R:continue
   n=pool.id(('near_pair',q,a,b));choices.append(n)
   cnf.extend([[-n,X[a]],[-n,X[b]]])
   near.setdefault((q,a),[]).append(n);near.setdefault((q,b),[]).append(n)
   near7.extend([n]*(int(vertices[a][0]==7)+int(vertices[b][0]==7)))
  card(choices,1)
 # Quad adjacency is symmetric.
 for q,r in combinations(qids,2):
  a=near.get((q,r),[]);b=near.get((r,q),[])
  for v in a:cnf.append([-v]+b)
  for v in b:cnf.append([-v]+a)
 # Exact far sets at every quad; symmetric on quad pairs.
 F={}
 for q,Q in enumerate(quads):
  for i,(d,B,j) in enumerate(vertices):
   if i==q or Q&B:continue
   tag=tuple(sorted((q,i))) if i in qids else (q,i)
   f=F.get(tag)
   if f is None:f=pool.id(('far',*tag));F[tag]=f
   cnf.append([-f,X[i]])
   for n in near.get((q,i),[]):cnf.append([-f,-n])
 for q,Q in enumerate(quads):
  terms=[]
  for i,(d,B,j) in enumerate(vertices):
   tag=tuple(sorted((q,i))) if i in qids else (q,i)
   if i!=q and not Q&B:terms.append(F[tag])
  n7=[n for (root,i),ns in near.items() if root==q and vertices[i][0]==7 for n in ns]
  card(terms+n7,9)
  for t in set(range(12))-Q:
   card([F[tuple(sorted((q,i))) if i in qids else (q,i)] for i,(d,B,j) in enumerate(vertices) if i!=q and not Q&B and t in B],2)
 # Choose the necessary negative-charge seven vertices, each with its
 # complete far partition. Unchosen vertices may also be negative.
 bad={}; covers={}; helpers={}; weighted=[]
 for v,(d,B,j) in enumerate(vertices):
  if d!=7 or len(B) not in (1,2):continue
  choices=[]
  for qs in combinations(qids,2):
   if quads[qs[0]]&quads[qs[1]] or any(B&quads[q] for q in qs):continue
   remainder=frozenset(range(12))-B-quads[qs[0]]-quads[qs[1]]
   for u,(dd,A,jj) in enumerate(vertices):
    if u!=v and u not in qs and A==remainder:
     choices.append(tuple(sorted((*qs,u))))
  if len(B)==2:
   for q,Q in enumerate(quads):
    if B&Q:continue
    remainder=frozenset(range(12))-B-Q
    ts=[u for u,(dd,A,jj) in enumerate(vertices) if len(A)==3 and A<=remainder]
    for a,b in combinations(ts,2):
     if not vertices[a][1]&vertices[b][1] and vertices[a][1]|vertices[b][1]==remainder:
      choices.append(tuple(sorted((q,a,b))))
  good=[]
  for fs in sorted(set(choices)):
   # Any unused quad must be met by the own set, by linearity of
   # the four-block partition; otherwise four points fit in three blocks.
   if any(q not in fs and not B&Q for q,Q in enumerate(quads)):continue
   c=pool.id(('cover',v,*fs));good.append(c);covers[c]=(v,fs)
   for u in (v,*fs):cnf.append([-c,X[u]])
   for q,Q in enumerate(quads):
    tag=(q,v)
    if tag in F:cnf.append([-c,F[tag] if q in fs else -F[tag]])
   if sum(u in qids for u in fs)==1:
    for u in fs:
     if u not in qids:helpers.setdefault(u,[]).append(c)
  if good:
   b=pool.id(('bad',v));bad[v]=b;cnf.append([-b]+good)
   for c in good:cnf.append([-c,b])
   card(good,1,'le')
   weighted.extend([b]*(3-len(B)))
 for cs in helpers.values():card(cs,1,'le')
 # The complete charge identity implies this inequality even when
 # additional negative epsilon values occur at ordinary vertices.
 card(weighted+[-n for n in near7],2+2*six[1]+len(near7),'ge')

 data=dict(vertices=vertices,X=X,near=near,F=F,bad=bad,covers=covers,k=k,quads=quads)
 if stage=="base":return cnf,data
 if stage!="near":raise ValueError(stage)
 # Real low adjacency, with exact pointwise near partitions at every
 # selected vertex. This is still a necessary relaxation of full girth.
 E={}
 for u,v in combinations(range(len(vertices)),2):
  U,V=vertices[u][1],vertices[v][1]
  if U&V or not independent(U|V,k):continue
  # Allocate H-square-independent unions first, then append the additional
  # allowed cross-leaf pairs below. This order fixes reproducible IDs.
  E[u,v]=pool.id(('edge',u,v))
 # A low edge only requires union independence in H. The two P3 leaves
 # may lie in different blocks; their resulting five-cycle is allowed.
 if k:
  for u,v in combinations(range(len(vertices)),2):
   U,V=vertices[u][1],vertices[v][1]
   if U&V or any(a in U|V and b in U|V for a,b in H):continue
   if (u,v) not in E:E[u,v]=pool.id(('edge',u,v))
 def edge(u,v):return E.get(tuple(sorted((u,v))))
 for (u,v),e in E.items():cnf.extend([[-e,X[u]],[-e,X[v]]])
 for v,(d,B,j) in enumerate(vertices):
  neighbors=[u for u in range(len(vertices)) if u!=v and edge(u,v)]
  card([edge(u,v) for u in neighbors]+[-X[v]]*(d-len(B)),d-len(B))
  R=frozenset(range(12))-B-{w for a,b in H if a in B or b in B for w in (a,b)}
  for t in R:
   card([edge(u,v) for u in neighbors if t in vertices[u][1]]+[-X[v]],1)
  if v in bad:
   lits=[edge(u,v) for u in neighbors if vertices[u][0]==7]
   bound=8-2*len(B)
   if bound>len(lits):cnf.append([-bad[v]])
   else:
    for c in CardEnc.equals(lits,bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses:cnf.append([-bad[v]]+c)
 for q in qids:
  for i in range(len(vertices)):
   if i==q:continue
   e=edge(q,i);ns=near.get((q,i),[])
   if e:
    cnf.append([-e]+ns)
    for n in ns:cnf.append([-n,e])
   else:
    for n in ns:cnf.append([-n])
 # Every prescribed far pair has no edge and no common low neighbor.
 prescribed=dict(F)
 for c,(v,fs) in covers.items():
  for u in fs:
   uv=tuple(sorted((u,v)))
   if uv not in prescribed:prescribed[uv]=pool.id(('prescribed_far',*uv))
   cnf.append([-c,prescribed[uv]])
 for (u,v),f in prescribed.items():
  if edge(u,v):cnf.append([-f,-edge(u,v)])
  for w in range(len(vertices)):
   if w in (u,v):continue
   a,b=edge(u,w),edge(v,w)
   if a and b:cnf.append([-f,-a,-b])
 data["E"]=E
 return cnf,data

NEAR_CASES={(372,j) for j in (2,7,9,10,12,13,18,22,23)} | {(373,7),(373,9),(386,32),(386,39),(386,59)}

def cases():
    for index,k,r in ((372,0,2),(373,0,2),(377,0,3),(378,0,2),(386,1,2)):
        for orbit in range(len(reps(k,r))):
            yield index,orbit

def proof_stage(case):
    return "near" if tuple(case) in NEAR_CASES else "base"

def case_name(case):
    return "multiquad_%s_%s" % tuple(case)
