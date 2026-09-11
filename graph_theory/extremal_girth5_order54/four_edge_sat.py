"""Whole four-edge all-sink layer; see z12_A0_four_edge_exclusion.md."""
from a0_inventory import profiles
from four_edge_orbits import forest,independent,reps,components
from itertools import combinations
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType

def near_partitions(R,count,eligible,vertices):
 """Unordered distinct selected slots whose high sets partition R.
 Empty slots are appended after covering all nonempty points."""
 empty=[i for i in eligible if not vertices[i][1]]
 bypoint={t:[i for i in eligible if t in vertices[i][1]] for t in R}
 def visit(left,remaining,chosen):
  if not left:
   for tail in combinations(empty,remaining):yield tuple(sorted(chosen+tail))
   return
  if remaining<=0:return
  t=min(left)
  for i in bypoint[t]:
   B=vertices[i][1]
   if B<=left:
    yield from visit(left-B,remaining-1,chosen+(i,))
 yield from visit(R,count,())

def build(index,fid,orbit,stage="base"):
 m,k,six,seven=list(profiles())[index]
 if m!=4 or sum(six[4:])+sum(seven[4:])<2 or any(six[5:]) or any(seven[5:]):raise ValueError("Outside multi-quad m4 domain")
 if k!=sum(max(0,len(P)-2) for P in components(fid)):raise ValueError("Wrong forest")
 quads=reps(fid,six[4],seven[4])[orbit];H=forest(fid); h=[sum(t in e for e in H) for t in range(12)]
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
 vertices=[(6 if i<six[4] else 7,Q,0) for i,Q in enumerate(quads)]
 qids=list(range(len(quads)))
 for d,counts in [(6,six),(7,seven)]:
  for c,n in enumerate(counts):
   if not n or c==4:continue
   for B in combinations(range(12),c):
    B=frozenset(B)
    if not independent(B,fid) or any(len(B&Q)>1 for Q in quads):continue
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
  if not independent({a,b},fid):continue
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
  for chosen in near_partitions(R,vertices[q][0]-4,eligible,vertices):
   n=pool.id(('near_choice',q,*chosen));choices.append(n)
   for u in chosen:
    cnf.append([-n,X[u]])
    near.setdefault((q,u),[]).append(n)
   near7.extend([n]*sum(vertices[u][0]==7 for u in chosen))
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
  card(terms+n7,9 if vertices[q][0]==6 else 3)
  for t in set(range(12))-Q:
   card([F[tuple(sorted((q,i))) if i in qids else (q,i)] for i,(d,B,j) in enumerate(vertices) if i!=q and not Q&B and t in B],8-vertices[q][0])
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
 card(weighted+[-n for n in near7],4+seven[4]+2*six[1]+6*six[0]+len(near7),'ge')

 data=dict(vertices=vertices,X=X,near=near,F=F,bad=bad,covers=covers,k=k,fid=fid,quads=quads)
 if stage=="base":return cnf,data

 if stage=="packing":
  # Point quotas and linearity give the number of other selected vertices
  # disjoint from each quad. Count distinct six-triple helpers together
  # with six-neighbors that cannot be helpers.
  for q,Q in enumerate(quads):
   sigma=sum(h[t] for t in Q);dq=vertices[q][0]
   outside6=4-sigma+3*(dq==6)
   outside7=6+2*sigma+3*(dq==7)
   for d,bound in ((6,outside6),(7,outside7)):
    card([X[i] for i,(dd,B,j) in enumerate(vertices) if i!=q and dd==d and not Q&B],bound)
   terms=[]
   for c,(v,fs) in covers.items():
    if q in fs and sum(u in qids for u in fs)==1:
     terms.extend([c]*sum(vertices[u][0]==6 for u in fs if u!=q))
   terms.extend(n for (root,u),ns in near.items() if root==q and vertices[u][0]==6 and len(vertices[u][1])!=3 for n in ns)
   card(terms,outside6,'le')
  return cnf,data
 if stage!="near":raise ValueError(stage)
 # Real low adjacency, with exact pointwise near partitions at every
 # selected vertex. This is still a necessary relaxation of full girth.
 E={}
 for u,v in combinations(range(len(vertices)),2):
  U,V=vertices[u][1],vertices[v][1]
  if U&V or any(a in U|V and b in U|V for a,b in H):continue
  E[u,v]=pool.id(('edge',u,v))
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


PACKING_CASES = {(301, 0, 4), (336, 1, 6), (302, 0, 0), (336, 1, 3), (300, 0, 2), (336, 1, 19), (313, 0, 2), (300, 0, 5), (301, 0, 0), (336, 1, 2), (300, 0, 4), (336, 1, 1), (301, 0, 5), (301, 0, 2), (336, 1, 4), (313, 0, 0), (336, 1, 0)}
NEAR_CASES = {(300, 0, 0), (300, 0, 11)}

def cases():
 for index,(m,k,six,seven) in enumerate(profiles()):
  if m!=4 or six[4]+seven[4]<2 or any(six[5:]) or any(seven[5:]):continue
  for fid in range(5):
   if k!=sum(max(0,len(P)-2) for P in components(fid)):continue
   for orbit in range(len(reps(fid,six[4],seven[4]))):
    yield index,fid,orbit

def proof_stage(case):
 case=tuple(case)
 return "near" if case in NEAR_CASES else "packing" if case in PACKING_CASES else "base"

def case_name(case):
 return "four_%s_%s_%s" % tuple(case)
