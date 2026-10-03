"""Full field AP scan, affine supports, independent cover DFS and shift distance."""
import argparse,json
from model import P,need,endpoint,squares,digest
def run():
 units,V,D=endpoint();sq=squares();L={x:int(x not in sq) for x in range(1,P)}
 partial={'root_free':0,'root_hit':0};trace=[]
 for a in range(P):
  for d in range(1,P):
   points=[(a+j*d)%P for j in range(7)];bits={L[x] for x in points if x}
   need(bits=={0,1},'partial field AP both colors');partial['root_hit' if 0 in points else 'root_free']+=1
   trace.append([a,d,points])
 affine=0;columns=0
 for r in range(P):
  for alpha in range(1,P):
   q=(r+alpha)%P;seen=set()
   for d,S in units[:5]:
    C={(r+alpha*x)%P for x in S};need(len(C)==6 and not(C&seen) and r not in C and q not in C,'affine disjointness')
    need(all(L[(x-r)%P]!=L[alpha] for x in C),'affine opposite character');seen|=C;columns+=6
   affine+=1
 # Count minimum hitting sets via branching and canonical complete-set de-duplication.
 edges=[set(s) for _,s in units];covers=set();searched=0
 def dfs(chosen):
  nonlocal searched
  searched+=1
  uncovered=[s for s in edges if not(s&chosen)]
  if not uncovered:covers.add(tuple(sorted(chosen)));return
  if len(chosen)==5:return
  for x in sorted(uncovered[0]):dfs(chosen|{x})
 dfs(set());need(covers and {len(c) for c in covers}=={5},'minimum cover size')
 for C in covers:need(all(set(C)&s for s in edges),'positive minimum cover')
 # No two different shifted/paletted baselines coincide on their shared regular columns.
 distances=[]
 for h in range(1,P):
  unequal=sum(L[x]!=L[(x-h)%P] for x in range(1,P) if x!=h)
  need(unequal==308 and P-2-unequal==307,'shift distance');distances.append([h,unequal])
 # Generic arc inequality and the K(5,10) missing-degree contradictions, all small cases.
 balances={}
 for m in (20,21,22):
  allowed=[];excluded=[]
  for a in range(1,m//2+1):
   b=m-a
   if a*b<5*m:continue
   e=a*b-5*m
   guaranteed=b-(5*e//a)
   complete_vertices=max(0,a-e)
   (excluded if guaranteed>=10 or (complete_vertices>=5 and b>=10) else allowed).append([a,b,e,guaranteed,complete_vertices])
  balances[str(m)]={'excluded_by_missing_degree_bounds':excluded,'unresolved':allowed}
 need(not balances['20']['unresolved'] and not balances['21']['unresolved'],'exclude20/21')
 need([x[:2] for x in balances['22']['unresolved']]==[[10,12],[11,11]],'22 balances')
 return dict(schema=1,partial_AP=partial,partial_trace_sha256=digest(trace),affine_cases=affine,affine_support_columns=columns,
  minimum_cover_size=5,minimum_cover_count=len(covers),cover_DFS_visits=searched,minimum_cover_sha256=digest(sorted(covers)),
  shifted_distances=[307,308],shift_cases=len(distances),shift_distance_sha256=digest(distances),balances=balances,
  classification_N3702=617*2*(2**6),classification_N3703=2*(2**7-2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args();result=run()
 open(args.output,'w').write(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
