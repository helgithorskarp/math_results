"""Exact complete comparator-function closures on at most four free ports.

Packed-mask BFS production, then scalar-vector reachability/closure replay.
All function outputs are on the entire Boolean cube; no heuristic cutoff.
"""
from collections import deque
from itertools import combinations
import hashlib,json,resource,time
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)

def need(test,message):
 if not test:raise ValueError(message)

def packed(rows,n):return sum(row<<(n*x) for x,row in enumerate(rows))
def decode(f,n):return [(f>>(n*x))&((1<<n)-1) for x in range(1<<n)]
def rank(rows,n):return sum(sum(p*((row>>p)&1) for p in range(n)) for row in rows)
def main():
 start=time.monotonic();summary=[];all_data=[]
 for n in range(1,5):
  gates=list(combinations(range(n),2));initial=packed(range(1<<n),n)
  ids={initial:0};rows=[{'function':initial,'parent':None,'gate':None,'length':0}];todo=deque([initial]);transitions=0
  while todo:
   f=todo.popleft();values=decode(f,n);fid=ids[f];old_rank=rank(values,n)
   for a,b in gates:
    bit_a,bit_b=1<<a,1<<b
    out=[v^(bit_a|bit_b) if v&bit_a and not v&bit_b else v for v in values]
    nf=packed(out,n);transitions+=1
    if nf!=f:need(rank(out,n)>old_rank,'function changed without rank growth')
    if nf not in ids:
     ids[nf]=len(rows);rows.append({'function':nf,'parent':fid,'gate':[a,b],'length':rows[fid]['length']+1});todo.append(nf)
  # Scalar full-vector checker: no producer transition or bit-exchange rule reused.
  cube=[[x>>p&1 for p in range(n)] for x in range(1<<n)]
  reconstructed=[];checks=0
  for i,row in enumerate(rows):
   if row['parent'] is None:
    need(i==0 and row['length']==0,'root metadata differs');actual=cube
   else:
    need(row['parent']<i,'parent not previously reachable')
    a,b=row['gate'];actual=[]
    for previous in reconstructed[row['parent']]:
     v=list(previous);v[a],v[b]=min(v[a],v[b]),max(v[a],v[b]);actual.append(v)
    need(row['length']==rows[row['parent']]['length']+1,'representative length differs')
   need(actual==[[v>>p&1 for p in range(n)] for v in decode(row['function'],n)],'full representative function differs')
   reconstructed.append(actual)
  for i,actual in enumerate(reconstructed):
   for a,b in gates:
    actual_after=[]
    for previous in actual:
     values=list(previous);values[a],values[b]=min(values[a],values[b]),max(values[a],values[b]);actual_after.append(sum(v*2**p for p,v in enumerate(values)))
    nf=packed(actual_after,n)
    need(nf in ids,'certificate function set not closed under every comparator')
    need(rows[ids[nf]]['length']<=rows[i]['length']+1,'assigned word not shortest')
    checks+=1
  ordered=sorted(row['function'] for row in rows)
  sha=hashlib.sha256(json.dumps(ordered,separators=(',',':')).encode()).hexdigest()
  summary.append({'n':n,'functions':len(rows),'producer_transitions':transitions,'scalar_complete_closure_transitions':checks,'scalar_representative_input_controls':len(rows)*(1<<n),'maximum_shortest_word_length':max(row['length'] for row in rows),'function_set_sha256':sha})
  all_data.append({'n':n,'functions':rows})
  print(json.dumps(summary[-1],sort_keys=True),flush=True)
 result={'status':'COMPLETE_EXACT_PREPARATION_FUNCTION_CLOSURES_PACKED_AND_SCALAR_AGREE','agent':'six-sorting-2','role':'researcher','orders':[1,2,3,4],'summary':summary,'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'warning':'This covers the arbitrary preparation subword only after the pre6 event normalization. Full sorting-network root cover and exclusion are not inferred.'}
 (ROOT/'preparation-functions.json').write_text(json.dumps(all_data,separators=(',',':'))+'\n')
 (ROOT/'preparation-functions-summary.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':main()
