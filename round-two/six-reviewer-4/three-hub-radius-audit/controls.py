"""Physical covariance, negative scope, and final-incidence controls."""
from itertools import combinations
from collections import Counter
from copy import deepcopy
from pathlib import Path
import argparse,json
from rows import census,need,encoded
from populations import project,types_of,endpoints
from radius import closed_unit_bridge

def rejects(f):
 try:f()
 except ValueError:return
 raise ValueError('damaged control accepted')

def inverse(r,permutation):
 inv={v:i for i,v in enumerate(permutation)};z=deepcopy(r)
 for f in ('hubs','high','isolated_hubs'):z[f]=sorted(inv[v]for v in z[f])
 z['hh_edges']=sorted(sorted(inv[v]for v in edge)for edge in z['hh_edges'])
 z['replication']=[r['replication'][permutation[v]]for v in range(17)]
 return z

def run(stars,record):
 rows=project(census(stars));need(encoded(rows)==encoded(record['physical']),'undamaged complete positive control')
 types=types_of(rows);need(encoded([list(t[:4])+[list(t[4]),*t[5:]]for t in types])==encoded(record['types']),'full types positive control')
 checks=[]
 for damage in ('missing-quad','repeat-quad','repeat-pair','point-domain'):
  bad=deepcopy(stars)
  if damage=='missing-quad':bad[0].pop()
  elif damage=='repeat-quad':bad[0][1]=bad[0][0][:]
  elif damage=='point-domain':bad[0][0][0]=17
  else:
   pair=bad[0][0][:2];bad[0][1]=pair+[v for v in range(17)if v not in pair][:2]
  rejects(lambda:census(bad));checks.append(damage)
 transported=0
 for perm in ([16-i for i in range(17)],[(3*i+7)%17 for i in range(17)],[(5*i+2)%17 for i in range(17)]):
  moved=[[[perm[v]for v in reversed(word)]for word in reversed(star)]for star in stars]
  new=project(census(moved))
  restored=sorted((inverse(r,perm)for r in new),key=lambda r:(r['fixture'],len(r['hubs']),r['hubs']))
  need(encoded(restored)==encoded(rows),'every transported physical/color field')
  need(types_of(new)==types,'entire type catalogue covariant');transported+=len(new)
 checks.append('three-complete-physical-point-bijections')
 failures=[r for r in rows if r['margin3']<0]
 need(len(failures)==8 and all(r['k']==5 for r in failures),'eight actual off-scope marks')
 need(any(r['e']==4 and 0 in r['replication']for r in rows),'actual missing-link-point row')
 need(all(r['margin3']>=0 for r in rows if r['k']<=4),'exact imported coefficient3 scope')
 checks+=['retain-eight-k5-failures','retain-replication-zero']
 # Every final-type realization has the stated three actual SS leave pairs.
 relevant=[r for r in rows if r['e']==0 and r['k']==1 and r['q']==1 and not r['eligible']]
 for r in relevant:
  sat=set(r['high'])-set(r['hubs']);ss=[p for p in r['hh_edges']if set(p)<=sat]
  need(len(ss)==3 and len(sat)==4,'every final unit-row physical wedge count')
 checks.append('all-final-unit-row-physical-leave-incidences')
 bridge=closed_unit_bridge(record['final_support'],5,0,0,0)
 for damage in ('unit-count','nonunit-eligibility','nonunit-colors','q','tau'):
  support=deepcopy(record['final_support']);Q,tau=5,0
  if damage=='q':Q=4
  elif damage=='tau':tau=1
  elif damage=='unit-count':support[0]['count']=4
  elif damage=='nonunit-eligibility':support[1]['type'][3]=False
  else:support[1]['type'][4]=[2,1,0,0,0]
  rejects(lambda:closed_unit_bridge(support,Q,0,0,tau));checks.append('final-'+damage)
 a=next(i for i,t in enumerate(types)if t[:4]==(0,1,0,True))
 b=next(i for i,t in enumerate(types)if t[:4]==(1,1,1,False)and t[4]==(3,0,0,0,0))
 c=next(i for i,t in enumerate(types)if t[:4]==(1,1,0,True)and t[4]==(3,0,0,0,0))
 counts=[0]*len(types);counts[a]=counts[b]=counts[c]=1
 fail=endpoints(types,counts,False);need(fail and fail['reason']=='distinct-endpoints','one endpoint cannot be used four times')
 checks.append('distinct-endpoints')
 old=[(b,r)for b in record['branches']for r in b['records']if b['Q']==0 and r['old_failure']is None]
 need(len(old)==1 and old[0][0]['X']==2 and old[0][1]['failure']['reason']=='radius-two'and old[0][1]['failure']['upper_sum_degrees']==12,'complete Q0 old-survivor radius necessity')
 checks.append('radius-coverage-essential')
 return {'checks':checks,'checks_count':len(checks),'transported_full_rows':transported,'final_unit_physical_marks':len(relevant),'final_bridge':bridge,'all_eight_off_scope_marks_retained':True,'e4_replication_zero_retained':True}

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--record',type=Path,required=True);a=p.parse_args()
 print(json.dumps(run(json.loads(a.input.read_bytes())['stars'],json.loads(a.record.read_bytes())),sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
