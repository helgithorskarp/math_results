"""Three-edge layer with high edges chosen inside the incidence model."""
from a0_inventory import profiles
from three_quad_orbits import reps
from itertools import combinations
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType

def build(index,orbit,stage='base',expected_m=3):
 m,k,six,seven=list(profiles())[index]
 if expected_m not in (3,4) or m!=expected_m or six[4]+seven[4]<2 or any(six[5:]) or any(seven[5:]):raise ValueError('Outside supported multi-quad domain')
 quads=reps(six[4],seven[4])[orbit]
 pool=IDPool();cnf=CNF()
 def card(lits,bound,mode='eq',guard=None):
  if bound<0 and mode=='ge':return
  if bound<0 or (mode!='le' and bound>len(lits)):clauses=[[]]
  elif mode=='le' and bound>=len(lits):return
  elif not lits:clauses=[[]] if bound else []
  else:
   fn={'eq':CardEnc.equals,'le':CardEnc.atmost,'ge':CardEnc.atleast}[mode]
   clauses=fn(lits,bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses
  cnf.extend(([ -guard]+c if guard is not None else c) for c in clauses)
 H={(a,b):pool.id(('high_edge',a,b)) for a,b in combinations(range(12),2)}
 def high(a,b):return H[tuple(sorted((a,b)))]
 card(list(H.values()),m)
 for t in range(12):card([high(t,u) for u in range(12) if u!=t],2,'le')
 vertices=[(6 if i<six[4] else 7,Q,0) for i,Q in enumerate(quads)]
 qids=list(range(len(quads)))
 for d,counts in [(6,six),(7,seven)]:
  for c,n in enumerate(counts):
   if not n or c==4:continue
   for B in combinations(range(12),c):
    B=frozenset(B)
    if any(len(B&Q)>1 for Q in quads):continue
    copies=min(n,5) if c==1 else n if c==0 else 1
    for j in range(copies):vertices.append((d,B,j))
 X=[pool.id(('x',i)) for i in range(len(vertices))]
 for q in qids:cnf.append([X[q]])
 for d,counts in [(6,six),(7,seven)]:
  for c,n in enumerate(counts):card([X[i] for i,(dd,B,j) in enumerate(vertices) if dd==d and len(B)==c],n)
 for t in range(12):
  hs=[high(t,u) for u in range(12) if u!=t]
  card([X[i] for i,(d,B,j) in enumerate(vertices) if d==6 and t in B]+[-h for h in hs],3+len(hs))
  card([X[i] for i,(d,B,j) in enumerate(vertices) if d==7 and t in B]+[h for h in hs for _ in range(2)],5)
 paths=[]
 for a,b in combinations(range(12),2):
  ps=[]
  for w in range(12):
   if w in (a,b):continue
   z=pool.id(('high_path',a,b,w));ps.append(z);paths.append(z);u,v=high(a,w),high(b,w)
   cnf.extend([[-z,u],[-z,v],[z,-u,-v]])
  card([high(a,b)]+ps+[X[i] for i,(d,B,j) in enumerate(vertices) if a in B and b in B],1)
 card(paths,k)
 slots={}
 for i,(d,B,j) in enumerate(vertices):slots.setdefault((d,B),[]).append(i)
 for ids in slots.values():
  for a,b in zip(ids,ids[1:]):cnf.append([-X[b],X[a]])
 N={}
 def tag(q,i):return tuple(sorted((q,i)))
 for q,Q in enumerate(quads):
  for i,(d,B,j) in enumerate(vertices):
   if i==q or B&Q:continue
   uv=tag(q,i)
   if uv not in N:N[uv]=pool.id(('near',*uv))
   cnf.append([-N[uv],X[i]])
 for q,Q in enumerate(quads):
  ns=[N[tag(q,i)] for i,(d,B,j) in enumerate(vertices) if i!=q and not B&Q]
  card(ns,vertices[q][0]-4)
  for t in set(range(12))-Q:
   card([N[tag(q,i)] for i,(d,B,j) in enumerate(vertices) if i!=q and not B&Q and t in B]+[high(a,t) for a in Q],1)
 F={}
 for q,Q in enumerate(quads):
  for i,(d,B,j) in enumerate(vertices):
   if i==q or B&Q:continue
   uv=tag(q,i)
   if uv not in F:F[uv]=pool.id(('far',*uv))
   cnf.extend([[-F[uv],X[i]],[-F[uv],-N[uv]]])
 for q,Q in enumerate(quads):
  ids=[i for i,(d,B,j) in enumerate(vertices) if i!=q and not B&Q]
  card([F[tag(q,i)] for i in ids]+[N[tag(q,i)] for i in ids if vertices[i][0]==7],9 if vertices[q][0]==6 else 3)
  for t in set(range(12))-Q:card([F[tag(q,i)] for i in ids if t in vertices[i][1]],8-vertices[q][0])
 bad={};covers={};helpers={};weighted=[]
 for v,(d,B,j) in enumerate(vertices):
  if d!=7 or len(B) not in (1,2):continue
  choices=[]
  for qs in combinations(qids,2):
   if quads[qs[0]]&quads[qs[1]] or any(B&quads[q] for q in qs):continue
   remainder=frozenset(range(12))-B-quads[qs[0]]-quads[qs[1]]
   for u,(dd,A,jj) in enumerate(vertices):
    if u!=v and u not in qs and A==remainder:choices.append(tuple(sorted((*qs,u))))
  if len(B)==2:
   for q,Q in enumerate(quads):
    if B&Q:continue
    remainder=frozenset(range(12))-B-Q
    ts=[u for u,(dd,A,jj) in enumerate(vertices) if len(A)==3 and A<=remainder]
    for a,b in combinations(ts,2):
     if not vertices[a][1]&vertices[b][1] and vertices[a][1]|vertices[b][1]==remainder:choices.append(tuple(sorted((q,a,b))))
  good=[]
  for fs in sorted(set(choices)):
   blocks=[B]+[vertices[u][1] for u in fs]
   if any(q not in fs and any(len(Q&A)!=1 for A in blocks) for q,Q in enumerate(quads)):continue
   c=pool.id(('cover',v,*fs));good.append(c);covers[c]=(v,fs)
   for u in (v,*fs):cnf.append([-c,X[u]])
   for q,Q in enumerate(quads):
    uv=tag(q,v)
    if uv in F:cnf.append([-c,F[uv] if q in fs else -F[uv]])
   if sum(u in qids for u in fs)==1:
    for u in fs:
     if u not in qids:helpers.setdefault(u,[]).append(c)
  if good:
   b=pool.id(('bad',v));bad[v]=b;cnf.append([-b]+good)
   for c in good:cnf.append([-c,b])
   card(good,1,'le');weighted.extend([b]*(3-len(B)))
 for cs in helpers.values():card(cs,1,'le')
 near7=[N[tag(q,i)] for q,Q in enumerate(quads) for i,(d,B,j) in enumerate(vertices) if i!=q and not B&Q and d==7]
 card(weighted+[-n for n in near7],12-2*m+seven[4]+6*six[0]+2*six[1]+len(near7),'ge')
 data=dict(vertices=vertices,X=X,H=H,N=N,F=F,bad=bad,covers=covers,quads=quads,k=k)
 if stage=='base':return cnf,data
 if stage=='packing':
  for q,Q in enumerate(quads):
   sigma=[high(t,u) for t in Q for u in range(12) if u!=t]
   terms=[]
   for c,(v,fs) in covers.items():
    if q in fs and sum(u in qids for u in fs)==1:terms.extend([c]*sum(vertices[u][0]==6 for u in fs if u!=q))
   terms.extend(N[tag(q,i)] for i,(d,B,j) in enumerate(vertices) if i!=q and not B&Q and d==6 and len(B)!=3)
   card(terms+sigma,4+3*(vertices[q][0]==6),'le')
  return cnf,data
 raise ValueError('Unknown model stage')


def raw_cases():
 for i,(m,k,s,t) in enumerate(profiles()):
  if m==3 and s[4]+t[4]>=2 and not any(s[5:]) and not any(t[5:]):
   for j in range(len(reps(s[4],t[4]))):yield i,j


def isolated_pairs(quads):
 D=[(a,b) for a,b in combinations(range(len(quads)),2) if not quads[a]&quads[b]]
 return [(a,b) for a,b in D if sum(a in e for e in D)==1 and sum(b in e for e in D)==1]

def cases():
 for i,j in raw_cases():
  m,k,s,t=list(profiles())[i]
  if isolated_pairs(reps(s[4],t[4])[j]):yield i,j

PACKING_CASES={(179,2),(243,2)}
def proof_stage(case):return 'packing' if tuple(case) in PACKING_CASES else 'base'
def case_name(case):return 'three_%s_%s'%tuple(case)
