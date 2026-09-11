"""Full-incidence one-quad cases; see z12_A0_one_quad_exclusion.md.

All high-high edges remain variables. No high forest is fixed or sampled.
"""
from itertools import combinations
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType
from a0_inventory import profiles
from seven_edge_sat import lex_chain

REPS={2:[(),(0,),(0,1),(0,2)],3:[(),(0,),(0,1),(0,2),(0,3)]}
BAD=[{4,5},{6,7},{8,11}]
HELP=[{6,8,9},{7,10,11},{4,8,10},{5,9,11},{4,7,9},{5,6,10}]

def build(index,branch,seven_helpers,stage='final'):
 if stage not in ('base','helpers','all','final'):raise ValueError('Unknown model stage')
 m,k,six,seven=list(profiles())[index];r=2 if branch=='A' else 3; qe=int(branch=='B')
 ds=[8]*12;cs=[None]*12;eps=[None]*12;fixedC={};q=12
 ds.append(6);cs.append(4);eps.append(qe);fixedC[q]={0,1,2,3}
 bad=list(range(13,13+r))
 for i in range(r):ds.append(7);cs.append(2);eps.append(1);fixedC[13+i]=BAD[i]
 helpers=list(range(13+r,13+3*r))
 for i in range(2*r):ds.append(7 if i in seven_helpers else 6);cs.append(3);eps.append(None);fixedC[13+r+i]=HELP[i]
 for d,counts in ((6,six),(7,seven)):
  for c,n in enumerate(counts):
   used=sum(dd==d and cc==c for dd,cc in zip(ds,cs))
   for j in range(n-used):
    e=None if c==3 else 0
    if (branch=='C' and d==6 and c==2 and j==0) or (branch=='D' and d==7 and c==2 and j==0):e=-1
    ds.append(d);cs.append(c);eps.append(e)
 if len(ds)!=54:raise ValueError('profile assignment')
 fixedfar={tuple(sorted((b,h))) for b,hs in zip(bad,[helpers[2*j:2*j+2] for j in range(r)]) for h in [q]+hs}
 pool=IDPool();cnf=CNF()
 def allowed(u,v):
  if (u,v) in fixedfar:return False
  if v<12:return all(not({u,v}<=C) for C in fixedC.values())
  if u<12 and v in fixedC:return u in fixedC[v]
  if u in fixedC and v in fixedC and fixedC[u]&fixedC[v]:return False
  return True
 E={uv:pool.id(('e',*uv)) for uv in combinations(range(54),2) if allowed(*uv)}
 def edge(u,v):return E.get(tuple(sorted((u,v))))
 def card(lits,bound,mode='eq'):
  if bound<0 or (mode=='eq' and bound>len(lits)):cnf.append([])
  elif mode=='le' and bound>=len(lits):pass
  elif lits:cnf.extend((CardEnc.equals if mode=='eq' else CardEnc.atmost)(lits,bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses)
  elif bound:cnf.append([])
 for v,C in fixedC.items():
  for t in C:cnf.append([edge(v,t)])
 card([e for (u,v),e in E.items() if v<12],5)
 for v in range(54):
  card([edge(u,v) for u in range(54) if u!=v and edge(u,v)],ds[v])
  if v<12:
   he=[edge(v,t) for t in range(12) if t!=v and edge(v,t)]
   card(he,2,'le')
   card([edge(v,u) for u in range(12,54) if ds[u]==6 and edge(v,u)]+[-x for x in he],3+len(he))
   card([edge(v,u) for u in range(12,54) if ds[u]==7 and edge(v,u)]+he*2,5)
  else:
   card([edge(v,t) for t in range(12) if edge(v,t)],cs[v])
   se=[edge(v,u) for u in range(12,54) if u!=v and ds[u]==7 and edge(v,u)]
   if eps[v] is not None:card(se,(8 if ds[v]==6 else 7)-2*cs[v]+eps[v])
   elif ds[v]==6:card(se,3,'le')
 shorts={}
 for u,v in combinations(range(54),2):
  short=[edge(u,v)] if edge(u,v) else []
  for w in range(54):
   if w in (u,v):continue
   a,b=edge(u,w),edge(v,w)
   if a and b:
    p=pool.id();short.append(p);cnf.extend([[-p,a],[-p,b],[-a,-b,p]])
  shorts[u,v]=short
  card(short,1,'le')
  if (u,v) in fixedfar:
   for p in short:cnf.append([-p])
  elif u<12 or v<12 or u in bad or v in bad:cnf.append(short)
 free=[v for v in range(12,54) if v not in fixedC]
 for key in sorted(set((ds[v],cs[v],eps[v] if eps[v] is not None else 99) for v in free)):
  vs=[v for v in free if (ds[v],cs[v],eps[v] if eps[v] is not None else 99)==key]
  lex_chain(cnf,pool,[[edge(v,t) for t in range(12)] for v in vs])
 if stage=='base':return cnf,E,ds,cs
 # Redundant exact far partitions/double covers at the quad and helpers.
 # These append clauses after the base model, preserving its variable IDs.
 cover_roots=[q]+helpers
 F={uv:pool.id(('far',*uv)) for uv in combinations(range(12,54),2) if any(v in cover_roots for v in uv)}
 for uv,f in F.items():
  cnf.append(shorts[uv]+[f])
  for p in shorts[uv]:cnf.append([-f,-p])
 for v in cover_roots:
  for t in range(12):
   terms=[]
   for u in range(12,54):
    if u==v or not edge(u,t):continue
    f=F[tuple(sorted((u,v)))];e=edge(u,t);z=pool.id()
    cnf.extend([[-z,f],[-z,e],[-f,-e,z]]);terms.append(z)
   card(terms,(8-ds[v])*int(t not in fixedC[v]))
 if stage=='helpers':return cnf,E,ds,cs
 # Complete the same pointwise identities at every remaining low root.
 for uv in combinations(range(12,54),2):
  if uv not in F:
   f=pool.id(('far',*uv));F[uv]=f;cnf.append(shorts[uv]+[f])
   for p in shorts[uv]:cnf.append([-f,-p])
 for v in range(12,54):
  if v in cover_roots:continue
  for t in range(12):
   terms=[]
   for u in range(12,54):
    if u==v or not edge(u,t):continue
    f=F[tuple(sorted((u,v)))];e=edge(u,t);z=pool.id()
    cnf.extend([[-z,f],[-z,e],[-f,-e,z]]);terms.append(z)
   if edge(v,t):terms += [edge(v,t)]*(8-ds[v])
   card(terms,8-ds[v])
 # A seven-triple cannot partition nine outside points with only two
 # far sets (whose total size is at most four plus three).
 for v in range(12,54):
  if ds[v]==7 and cs[v]==3:
   card([edge(v,u) for u in range(12,54) if u!=v and ds[u]==7 and edge(v,u)],2,'le')
 if stage=='all':return cnf,E,ds,cs
 # In382/A/role1 the unique seven-triple is a helper and hence cannot
 # neighbor either bad vertex. The weighted local identity forces the bad
 # edge, epsilon0 at the first bad's six-neighbor and epsilon1 at the second's.
 if index==382 and branch=='A' and tuple(seven_helpers)==(0,):
  cnf.append([edge(*bad)])
  for j,b in enumerate(bad):
   for u in range(12,54):
    guard=edge(b,u)
    if ds[u]!=6 or not guard:continue
    if j==1 and cs[u]!=3:
     cnf.append([-guard]);continue
    lits=[edge(u,v) for v in range(12,54) if v!=u and ds[v]==7 and edge(u,v)]
    bound=2 if j==0 else 3
    if bound>len(lits):cnf.append([-guard]);continue
    clauses=CardEnc.equals(lits,bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses
    for clause in clauses:cnf.append([-guard]+clause)
 return cnf,E,ds,cs


def cases():
    """Complete profile / charge / helper-degree orbit cover."""
    for index, n73 in ((366,2),(367,1),(368,0),(382,1),(383,0),(390,0)):
        for branch in ('A','B','C','D'):
            if n73 == 0 and branch != 'A':
                continue
            r = 2 if branch == 'A' else 3
            for role, seven_helpers in enumerate(REPS[r]):
                if len(seven_helpers) <= n73:
                    yield index, branch, role


def case_name(case):
    return 'onequad_%s_%s_%s' % tuple(case)


def proof_stage(case):
    """The measured discovery route, followed by checking the final formula."""
    special={(366,'A',1):'helpers',(366,'A',2):'all',
             (367,'A',1):'all',(382,'A',1):'final'}
    return special.get(tuple(case),'base')
