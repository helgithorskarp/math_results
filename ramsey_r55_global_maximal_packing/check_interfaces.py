"""Adversarial interface controls and supplied-isomorphism certificate checks."""
from pathlib import Path
import json,tempfile,random
from itertools import combinations
import family,reproduce,catalog

def run(cache):
 transport_count=0;rejected=0;rng=random.Random(20260908)
 for q in range(7,11):
  n=43-4*q;count=next(x['count'] for x in catalog.specs() if x['n']==n)
  task=family.Task(family.task_id(q,q,count-1),cache);g=task.unrank(task.size//2);a=family.matrix(g)
  permutation=list(range(43));rng.shuffle(permutation);shuffled=family.graph([[a[u][v] for v in permutation] for u in permutation]);inverse=[permutation.index(v) for v in range(43)]
  got=family.transport(shuffled,inverse,task)
  if got['graph']!=g or got['code']!=task.size//2:raise ValueError('transport')
  transport_count+=1
  for bad in [inverse[:-1],inverse+[0],[0]*43,[True]+inverse[1:]]:
   try:family.transport(shuffled,bad,task)
   except ValueError:rejected+=1
   else:raise ValueError('bad transport accepted')
 # Full carrier model deliberately contains monochromatic fives; it must never
 # be accepted as a target merely for satisfying the pair and star carrier.
 task=family.Task('mp1-q10-r10-c000003',cache);g=task.unrank(0);a=family.matrix(g)
 model=[1]+[v if a[u][w] else -v for (u,w),v in task.variables.items()]
 bodies=['s UNKNOWN\n','s UNSATISFIABLE\n','s SATISFIABLE\nv 1 0\n','s SATISFIABLE\nv '+' '.join(map(str,model))+' 0\n','s SATISFIABLE\nv '+' '.join(map(str,model+[9999]))+' 0\n','s SATISFIABLE\nv 1 -1 0\n']
 with tempfile.TemporaryDirectory() as tmp:
  for body in bodies:
   path=Path(tmp)/'answer';path.write_text(body)
   try:family.accept_sat(task,path)
   except ValueError:rejected+=1
   else:raise ValueError('non-target solver response accepted')
 for name in ['mp1-q6-r5-c000000','mp1-q7-r4-c000000','mp1-q7-r8-c000000','mp1-q7-r5-c000640','mp1-q8-r5-c546356','mp1-q7-r5-c0']:
  try:family.parameters(name)
  except ValueError:rejected+=1
  else:raise ValueError('invalid task accepted')
 for line,n in [(b'B?\r\n',3),(b'B@\n',3),(b'C~\n',3),(b'B?',3)]:
  try:catalog.parse(line,n)
  except ValueError:rejected+=1
  else:raise ValueError('malformed graph6 accepted')
 return dict(status='INTERFACE_CONTROLS_PASSED',non_target_transport_certificates=transport_count,negative_inputs_rejected=rejected)

if __name__=='__main__':
 import sys
 print(json.dumps(run(sys.argv[1]),sort_keys=True))
