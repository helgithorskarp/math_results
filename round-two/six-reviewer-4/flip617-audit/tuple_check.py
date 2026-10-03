"""Enumerate increasing tuples, never an author closed-state family."""
import argparse,json
from model import endpoint,neighbors,need,digest
def enumerate_tuples(sq,ns,A,threshold=10,depth_limit=5):
 visits=[0]*6;trials=[0]*6;sizes=[{} for _ in range(6)];tuples=[]
 def visit(chosen,B,next_index):
  depth=len(chosen);visits[depth]+=1;k=str(B.bit_count());sizes[depth][k]=sizes[depth].get(k,0)+1
  tuples.append([list(chosen),[x for i,x in enumerate(ns) if B>>i&1]])
  if depth==depth_limit:return
  for i in range(next_index,len(sq)):
   trials[depth+1]+=1;C=B&A[sq[i]]
   if C.bit_count()>=threshold:visit(chosen+(sq[i],),C,i+1)
 visit((1,),A[1],1)
 return visits,trials,sizes,tuples
def run():
 units,V,D=endpoint();sq,ns,A=neighbors(D)
 visits,trials,sizes,tuples=enumerate_tuples(sq,ns,A)
 need(visits[5]==0,'forbidden five-tuple')
 # Separate literal replay checks each retained tuple's exact common neighborhood.
 for chosen,B in tuples:
  common=[x for x in ns if all(x*pow(q,-1,617)%617 in D for q in chosen)]
  need(common==B,'tuple exact common neighbors')
 # The native 867-state count is independently recoverable but not used for coverage.
 distinct=sorted(set(tuple(B) for _,B in tuples))
 closures={str(k):0 for k in range(1,5)}
 for B in distinct:
  T=[q for q in sq if all(x*pow(q,-1,617)%617 in D for x in B)]
  need(1<=len(T)<=4,'closure maximum');closures[str(len(T))]+=1
 transitions=0
 family={frozenset(B) for B in distinct}
 for B in family:
  for q in sq:
   C=frozenset(x for x in B if x*pow(q,-1,617)%617 in D)
   if len(C)>=10:need(C in family,'closure transition');transitions+=1
 return dict(schema=1,method='anchored increasing tuples with complete monotone pruning',endpoint_supports=units,
  V=sorted(V),D=sorted(D),visits=visits,trials=trials,common_sizes=sizes,
  tuple_sha256=digest(tuples),distinct_intersections=len(distinct),closure_histogram=closures,
  retained_transitions=transitions,all_state_transitions=len(distinct)*len(sq),no_K5_10=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args()
 result=run();open(args.output,'w').write(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
