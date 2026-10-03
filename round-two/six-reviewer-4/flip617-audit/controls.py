"""Small exact graphs compare monotone tuple pruning with full combinations."""
import argparse,itertools,json
from tuple_check import enumerate_tuples
from model import need,digest
def run():
 sq=list(range(1,8));ns=list(range(101,113));cases=[];true=false=0
 for seed in range(32):
  if seed==0:A={q:(1<<12)-1 for q in sq}
  elif seed==1:A={q:((1<<12)-1 if q<5 else 0) for q in sq}
  else:A={q:sum(1<<i for i in range(12) if (seed*19+q*7+i*13+q*i)%17<14) for q in sq}
  visits,trials,sizes,tuples=enumerate_tuples(sq,ns,A)
  expected=[]
  for rest in itertools.combinations(sq[1:],4):
   chosen=(1,)+rest;common=[x for i,x in enumerate(ns) if all(A[q]>>i&1 for q in chosen)]
   if len(common)>=10:expected.append([list(chosen),common])
  actual=[t for t in tuples if len(t[0])==5]
  need(actual==expected,'small model full-combination agreement')
  if expected:true+=1
  else:false+=1
  cases.append([seed,A,len(expected),visits,trials])
 need(true and false,'positive and negative coverage controls')
 # Explicit failure boundary under optimization: a forbidden tuple is an error, never an absence.
 try:need(not cases[0][2],'forbidden five-tuple')
 except ValueError as e:need(str(e)=='forbidden five-tuple','intended control rejection')
 else:raise ValueError('missed counterexample')
 return dict(small_graphs=32,full_anchored_five_tuples_per_graph=15,with_K5_10=true,without_K5_10=false,
  whole_cases_sha256=digest(cases),explicit_positive_counterexample_rejected=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run()
 open(a.output,'w').write(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,sort_keys=True))
