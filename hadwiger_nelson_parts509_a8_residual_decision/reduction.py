"""Exact a=8 master: capped unary prefix counters and direct degree clauses."""
from itertools import combinations

def require(ok,msg):
 if not ok:raise ValueError(msg)

def negate(x):return not x if type(x) is bool else -x

def clean_clause(items):
 if any(type(x) is bool and x for x in items):return None
 vals=[x for x in items if type(x) is not bool]
 return vals

def counter(literals,k,top):
 """r[i,j] iff at least j of the first i literals hold, capped at k+1."""
 clauses=[];previous={0:True};meaning={}
 def emit(*xs):
  row=clean_clause(xs)
  if row is not None:clauses.append(row)
 for i,x in enumerate(literals,1):
  current={0:True}
  for j in range(1,min(i,k+1)+1):
   top+=1;w=top;current[j]=w;meaning[w]=(i,j)
   u=previous.get(j,False);v=previous.get(j-1,False)
   # w <=> u OR (x AND v)
   emit(negate(u),w);emit(-x,negate(v),w)
   emit(-w,u,x);emit(-w,u,v)
  previous=current
 emit(previous.get(k,False));emit(negate(previous.get(k+1,False)))
 return top,clauses,meaning

def build(U,E,killing):
 idx={v:i+1 for i,v in enumerate(U)};top=len(U)
 clauses=[[idx[v] for v in d] for d in killing]
 top,cs,sm=counter([-idx[v] for v in U[:135]],9,top);clauses+=cs
 top,cs,qm=counter([idx[v] for v in U[135:]],8,top);clauses+=cs
 vs=set(range(374))|set(U);adj={v:set() for v in vs};us=set(U);direct=0
 for a,b in E:adj[a].add(b);adj[b].add(a)
 for q in U[135:]:
  ns=sorted(adj[q]&us);need=4-len(adj[q]&set(range(374)));guard=-idx[q]
  if need<=0:continue
  if need>len(ns):clauses.append([guard]);direct+=1;continue
  # More than |ns|-need omitted neighbours is forbidden when q is selected.
  for subset in combinations(ns,len(ns)-need+1):clauses.append([guard]+[idx[v] for v in subset]);direct+=1
 return top,clauses,idx,adj,{'S_counter':sm,'Q_counter':qm,'degree_clauses':direct}

def structural_assignment(U,X,meanings):
 selected=set(X);model={i+1:v in selected for i,v in enumerate(U)}
 for key,literals in [('S_counter',[-(i+1) for i in range(135)]),('Q_counter',[i+1 for i in range(135,303)])]:
  for var,(i,j) in meanings[key].items():model[var]=sum(model[abs(v)]==(v>0) for v in literals[:i])>=j
 return model

def satisfies(clauses,model):return all(any(model[abs(v)]==(v>0) for v in c) for c in clauses)

def controls():
 from itertools import product
 tests=0
 for n in range(1,9):
  for k in range(n+1):
   for sign in [-1,1]:
    lits=[sign*(i+1) for i in range(n)];top,clauses,meaning=counter(lits,k,n)
    for bits in product([False,True],repeat=n):
     model={i+1:b for i,b in enumerate(bits)}
     for var,(i,j) in meaning.items():model[var]=sum(model[abs(v)]==(v>0) for v in lits[:i])>=j
     require(satisfies(clauses,model)==(sum(model[abs(v)]==(v>0) for v in lits)==k),'counter semantics')
     # From fixed inputs, unit propagation must force these exact thresholds
     # or detect a violated requested count. No SAT oracle is used.
     assigned={i+1:b for i,b in enumerate(bits)};conflict=False
     while True:
      changed=False
      for clause in clauses:
       if any(abs(v) in assigned and assigned[abs(v)]==(v>0) for v in clause):continue
       missing=[v for v in clause if abs(v) not in assigned]
       if not missing:conflict=True;break
       if len(missing)==1:assigned[abs(missing[0])]=missing[0]>0;changed=True
      if conflict or not changed:break
     good=sum(model[abs(v)]==(v>0) for v in lits)==k
     require((not conflict)==good and (not good or assigned==model),'counter propagation')
     tests+=1
 return tests
