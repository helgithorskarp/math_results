"""Exact outside-star CSP for109 local14. six-books-3, researcher.
Reciprocity and literal B-spine caps; complete arc-consistency branching.
"""
import hashlib,itertools,json,time
from collections import Counter,deque
from pathlib import Path

import argparse
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--output-dir',type=Path,default=HERE/'_work')
parser.add_argument('--expected',type=Path,default=HERE/'expected.json')
args=parser.parse_args()
OUT=args.output_dir
OUT.mkdir(parents=True,exist_ok=True)
EXPECTED=json.loads(args.expected.read_text())
def check_expected(name,result):
    canonical=json.loads(json.dumps(result))
    for key,value in EXPECTED[name].items():
        if canonical.get(key)!=value:
            raise RuntimeError('Expected result differs: '+name+'.'+key)

start=time.monotonic()
records=json.loads((OUT/'transfer14_records.json').read_text())
a=[set() for _ in range(10)]
for i,j in ((0,2),(0,3),(1,4),(1,5)):
    a[i].add(j); a[j].add(i)
for bit,(i,j) in enumerate(itertools.combinations(range(8),2)):
    if 51317328>>bit&1:
        a[i+2].add(j+2); a[j+2].add(i+2)
U=(1<<11)-1
stats=Counter(); cases=[]
def domains_for(rows,deficits):
 domains=[]
 for b,(z,delta) in enumerate(zip(rows,deficits)):
  k=z.bit_count(); candidates=[c for c in range(11) if c!=b]
  cols=[sum(1<<c for c in candidates if rows[c]>>i&1) for i in range(10)]
  t=[sum(z>>j&1 for j in a[i]) for i in range(10)]
  universe=U^(1<<b)
  red=[(universe^cols[i],3-len(a[i])+t[i]) for i in range(10) if not(z>>i&1)]
  blue=[(cols[i],len(a[i])+k-6-t[i]) for i in range(10) if z>>i&1]
  stars=[]
  for c in itertools.combinations(candidates,k-delta):
   st=sum(1<<q for q in c)
   if any((st&mask).bit_count()>bound for mask,bound in red): continue
   if any((st&mask).bit_count()<bound for mask,bound in blue): continue
   stars.append(st)
  domains.append(stars)
 return domains

def solve(rows,deficits):
 stars=domains_for(rows,deficits)
 sizes=[len(s) for s in stars]
 allowed={(b,c):[0]*sizes[b] for b in range(11) for c in range(11) if b!=c}
 for b,c in itertools.combinations(range(11),2):
  miss=(rows[b]&rows[c]).bit_count()
  redA=10-rows[b].bit_count()-rows[c].bit_count()+miss
  for i,x in enumerate(stars[b]):
   for j,y in enumerate(stars[c]):
    edge=x>>c&1
    if edge!=(y>>b&1): continue
    if edge:
     if redA+(x&y).bit_count()>3: continue
    else:
     xb=(U^(1<<b))^x; yb=(U^(1<<c))^y
     if 1+miss+(xb&yb).bit_count()>6: continue
    allowed[(b,c)][i]|=1<<j
    allowed[(c,b)][j]|=1<<i
 counter=Counter(); trace=[]
 def visit(ds,depth):
  counter['nodes']+=1
  queue=deque((b,c) for b in range(11) for c in range(11) if b!=c)
  while queue:
   b,c=queue.popleft(); old=ds[b]; revised=0
   for i in range(sizes[b]):
    if old>>i&1 and allowed[(b,c)][i]&ds[c]: revised|=1<<i
   if revised==old: continue
   counter['removed_values']+=(old^revised).bit_count()
   trace.append([depth,b,c,old,revised,ds[c]])
   ds[b]=revised
   if revised==0:
    counter['empty_domains']+=1
    return None
   for q in range(11):
    if q!=b and q!=c: queue.append((q,b))
  if all(d.bit_count()==1 for d in ds):
   return [stars[b][d.bit_length()-1] for b,d in enumerate(ds)]
  _,b=min((d.bit_count(),b) for b,d in enumerate(ds) if d.bit_count()>1)
  for i in range(sizes[b]):
   if ds[b]>>i&1:
    nd=ds.copy(); nd[b]=1<<i
    answer=visit(nd,depth+1)
    if answer is not None: return answer
  return None
 solution=visit([(1<<n)-1 for n in sizes],0)
 return {'rows':rows,'deficits':deficits,'domain_sizes':sizes,'csp':dict(counter),'trace_sha256':hashlib.sha256(json.dumps(trace,separators=(',',':')).encode()).hexdigest(),'solution_stars':solution}
for ri,r in enumerate(records):
 for deficits in r['deficit_assignments']:
  case=solve(r['rows'],deficits); case['incidence_index']=ri
  cases.append(case); stats.update(case['csp'])
result={'agent':'six-books-3','role':'researcher','complete':True,'incidence_matrices':len(records),'candidate_deficit_cases':len(cases),'solutions':sum(c['solution_stars'] is not None for c in cases),'csp_totals':dict(stats),'elapsed_seconds':time.monotonic()-start}
(OUT/'coupled14_cases.json').write_text(json.dumps(cases,indent=2)+'\n')
(OUT/'coupled14_result.json').write_text(json.dumps(result,indent=2)+'\n')
check_expected('coupled14',result)
print(json.dumps(result,indent=2))
