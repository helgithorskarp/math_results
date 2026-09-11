"""Exhaust every trace class and verify the structural closure conditions."""
import json,sys
from collections import Counter
from coloring import *
from forest import star_bound

def main():
 out={};small={}
 assert 26*((26+2)//4)>170
 for v in range(9,17):
  z=F(34*(comb(v//2,5)+comb((v+1)//2,5)),comb(v,5));assert z<1;small[v]=str(z)
 for v in [17,18]:
  z=tail(v,v//2,5,34);assert z<1;small[v]=str(z)
 z=max(star_bound(19,34,d) for d in range(5,9));assert z<1;small[19]=str(z)
 for v in range(20,25):
  bad=[];count=0;skipped=0;four=Counter()
  for x in M.profiles(v,34,3):
   ds=[sum(n for A,n in enumerate(x) if A>>i&1) for i in range(3)]
   if v==24 and ds[0]==7:skipped+=1;continue
   count+=1
   if good(v,x):continue
   if v==24:
    for d in range(ds[-1],(170-sum(ds))//21+1):
     for y in M.extends(x,d):
      four['raw']+=1
      if not admissible(v,y):continue
      four['admissible']+=1
      if not good(v,y):bad.append(y)
   else:bad.append(x)
  out[v]={'initial':count,'deferred_minimum_seven':skipped,'residual':bad,'four':dict(four)}
  print('vertex count',v,'checked',file=sys.stderr,flush=True)
 assert not out[20]['residual'] and not out[21]['residual'] and not out[23]['residual'] and not out[24]['residual']
 assert len(out[22]['residual'])==3
 for x in out[22]['residual']:
  assert [sum(n for A,n in enumerate(x) if A>>i&1) for i in range(3)]==[7]*3
  assert all(sum(n for A,n in enumerate(x) if A>>i&1 and A>>j&1)==2 for i,j in combinations(range(3),2))
 assert 22-(170-7*22)==6
 cases=pair2_four();assert len(cases)==26
 assert all(good(22,x) for x in cases)
 assert 24-(170-7*24)==22 and 22>3*(28-23+1)
 assert 25*7-170==5
 for v,d in [(24,7),(25,6)]:assert all(good(v,x) for x in pbd_four(d))
 assert [out[v]['initial'] for v in range(20,25)]==[2985,2496,497,350,50]
 assert out[24]['four']=={'raw':5594,'admissible':613}
 return {'theorem':'Every finite simple 5-uniform hypergraph with at most 34 edges has Property B.','lower_bound_m5':35,'known_upper_bound_m5':51,'small_cases':small,'trace_cases':out,'four_degree_seven_codegree_two_types':26,'four_pair_partition_types_each':3,'used_link_certificates':len(USED)}

if __name__=='__main__':
 assert __debug__,'Run without -O'
 print(json.dumps(main(),indent=2,sort_keys=True))
