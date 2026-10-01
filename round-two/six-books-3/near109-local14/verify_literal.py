"""Independent literal22-point replay. six-books-3, researcher.
No generator/certificate/CSP import. Enumerates each outside red neighborhood;
uses ordinary set intersections for every tested spine and forward filtering.
"""
from collections import Counter
from itertools import combinations
import hashlib,json,time
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
start=time.monotonic(); allvertices=set(range(22)); a=[set() for _ in range(10)]
for i,j in ((0,2),(0,3),(1,4),(1,5)):
 a[i].add(j); a[j].add(i)
for bit,(i,j) in enumerate(combinations(range(8),2)):
 if 51317328>>bit&1: a[i+2].add(j+2); a[j+2].add(i+2)
records=json.loads((OUT/'transfer14_records.json').read_text())
if len(records)!=135 or hashlib.sha256(json.dumps(sorted(r['rows'] for r in records),separators=(',',':')).encode()).hexdigest()!=EXPECTED['matrix_sha256']:
 raise RuntimeError('Incomplete/altered incidence input')
expected=json.loads((OUT/'coupled14_cases.json').read_text())
if len(expected)!=35 or any(len(r['deficits'])!=11 or any(type(d) is not int or d<0 or d>2 for d in r['deficits']) or sum(r['deficits'])!=2 for r in expected):
 raise RuntimeError('Incomplete/altered deficit-case input')
cases=[]; stats=Counter(); assignment_hist=Counter()
def compatible(u,nu,v,nv):
 if (v in nu)!=(u in nv): return False
 if v in nu: return len(nu&nv)<=3
 return len((allvertices-{u}-nu)&(allvertices-{v}-nv))<=6
for index,r in enumerate(records):
 rows=r['rows']; fixed={0:set(range(1,11))}
 for i in range(10):
  fixed[i+1]={0}|{j+1 for j in a[i]}|{b+11 for b,z in enumerate(rows) if not(z>>i&1)}
 if any(len(n)!=10 for n in fixed.values()): raise RuntimeError('Fixed full degrees differ')
 for u,v in combinations(range(11),2):
  if not compatible(u,fixed[u],v,fixed[v]): raise RuntimeError('fixed spine invalid')
 possible=[]
 for b,z in enumerate(rows):
  pb=[]
  for delta in range(3):
   candidates=[]; lowadj={i+1 for i in range(10) if not(z>>i&1)}
   for star in combinations([c+11 for c in range(11) if c!=b],z.bit_count()-delta):
    adj=lowadj|set(star)
    if len(adj)!=10-delta: raise RuntimeError('degree reconstruction')
    if all(compatible(b+11,adj,i,fixed[i]) for i in range(11)):
     candidates.append(adj)
   pb.append(candidates)
  possible.append(pb)
 # Full global deficit alternatives, independently regenerating the35 cases.
 assignments=[]
 for low in range(11):
  deficit=[0]*11; deficit[low]=2
  if all(possible[b][d] for b,d in enumerate(deficit)): assignments.append(deficit)
 for p,q in combinations(range(11),2):
  deficit=[0]*11; deficit[p]=deficit[q]=1
  if all(possible[b][d] for b,d in enumerate(deficit)): assignments.append(deficit)
 if assignments!=r['deficit_assignments']: raise RuntimeError('deficit-case mismatch')
 for deficit in assignments:
  if sum(deficit)!=2: raise RuntimeError('Total degree deficiency differs')
  initial={b:possible[b][d] for b,d in enumerate(deficit)}
  counter=Counter()
  def visit(pending,assigned):
   counter['nodes']+=1
   if not pending:
    full=fixed|{b+11:n for b,n in assigned.items()}
    if not all(compatible(u,full[u],v,full[v]) for u,v in combinations(range(22),2)):
     raise RuntimeError('completed graph fails literal verification')
    return full
   b=min(pending,key=lambda q:(len(pending[q]),q))
   for adj in pending[b]:
    nextpending={}; good=True
    for c,choices in pending.items():
     if c==b: continue
     kept=[n for n in choices if compatible(b+11,adj,c+11,n)]
     counter['filtered_values']+=len(choices)-len(kept)
     if not kept:
      counter['empty_domains']+=1; good=False; break
     nextpending[c]=kept
    if good:
     answer=visit(nextpending,assigned|{b:adj})
     if answer is not None: return answer
   return None
  answer=visit(initial,{})
  cases.append({'incidence_index':index,'deficits':deficit,'domain_sizes':[len(initial[b]) for b in range(11)],'nodes':counter['nodes'],'solution':answer is not None})
  stats.update(counter); assignment_hist[tuple(sorted(d for d in deficit if d))]+=1
if [(r['incidence_index'],r['deficits'],r['domain_sizes']) for r in cases]!=[(r['incidence_index'],r['deficits'],r['domain_sizes']) for r in expected]: raise RuntimeError('all case/domain sizes do not match')
result={'agent':'six-books-3','role':'researcher','complete':True,'method':'literal22-vertex adjacency sets; forward-filtering search without arc consistency','incidences':len(records),'cases':len(cases),'assignment_types':[[list(k),v] for k,v in sorted(assignment_hist.items())],'solutions':sum(r['solution'] for r in cases),'all_cases_and_domains_match':True,'search':dict(stats),'elapsed_seconds':time.monotonic()-start,'case_sha256':hashlib.sha256(json.dumps(cases,separators=(',',':')).encode()).hexdigest()}
(OUT/'verify14_literal_cases.json').write_text(json.dumps(cases,indent=2)+'\n')
(OUT/'verify14_literal_result.json').write_text(json.dumps(result,indent=2)+'\n')
check_expected('verify14_literal',result)
print(json.dumps(result,indent=2))
