"""Exact108 local14 incidence generator. six-books-3, researcher.
Python3.11 standard library; no earlier theorem/checker import.
"""
import itertools,json,time
from collections import Counter,defaultdict
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

spec=json.loads((HERE/'certificate.json').read_text())
if spec['schema']!=1 or spec['core_mask']!=51317328:
    raise RuntimeError('Certificate core/schema differs')
cut=spec['cut']
if cut['F_mask']!=spec['core_mask']:
    raise RuntimeError('Cut and core disagree')
if len(cut['alpha'])!=10 or any(type(q) is not int for q in cut['alpha']):
    raise RuntimeError('Column coefficients must be ten integers')
if any(type(cut[q]) is not int for q in ('gamma','rhs')):
    raise RuntimeError('Cut constants must be integers')
if any(type(i) is not int or type(j) is not int or type(q) is not int
       or not 0<=i<j<10 or q<=0 for i,j,q in cut['beta']):
    raise RuntimeError('Pair coefficients must be positive integers')
if len({(i,j) for i,j,q in cut['beta']})!=len(cut['beta']):
    raise RuntimeError('Repeated pair coefficient')
PAIRS=list(itertools.combinations(range(10),2))
a=[set() for _ in range(10)]
for i,j in ((0,2),(0,3),(1,4),(1,5)):
    a[i].add(j); a[j].add(i)
for bit,(i,j) in enumerate(itertools.combinations(range(8),2)):
    if spec['core_mask']>>bit&1:
        a[i+2].add(j+2); a[j+2].add(i+2)
h=list(map(len,a))
if h!=[2,2]+[3]*8 or any(a[i]&a[j] for i,j in PAIRS if j in a[i]):
    raise RuntimeError('Core is not the specified triangle-free degree graph')
cap=[[h[i]+2 if i==j else h[i]+h[j]-(5 if j in a[i] else 2)-len(a[i]&a[j])
      for j in range(10)] for i in range(10)]
rhs=11*cut['gamma']+sum(cut['alpha'][i]*cap[i][i] for i in range(10))+sum(q*cap[i][j] for i,j,q in cut['beta'])
if rhs!=cut['rhs'] or rhs!=0:
    raise RuntimeError('Integer cut upper bound is not zero')
def cut_score(cut,row):
    return cut['gamma']+sum(q*(row>>i&1) for i,q in enumerate(cut['alpha']))+sum(q for i,j,q in cut['beta'] if row>>i&1 and row>>j&1)
start=time.monotonic()
rows_by_delta=[]
for delta in range(5):
 rows=[]
 for z in range(1024):
  k=z.bit_count()
  if not 4+delta<=k<=8: continue
  if any(tuple(z>>i&1 for i in t) not in ((1,0,0),(0,1,1),(0,1,0),(0,0,1)) for t in ((0,2,3),(1,4,5))): continue
  if any(cap[i][j]<1 for i,j in PAIRS if z>>i&1 and z>>j&1): continue
  if any(k>sum(z>>j&1 for j in a[i])+5+delta for i in range(10) if not(z>>i&1)): continue
  if any(sum(z>>j&1 for j in a[i])<k-7 for i in range(10) if z>>i&1): continue
  if cut_score(cut,z)<0: raise RuntimeError('cut transfer failed')
  if cut_score(cut,z)==0: rows.append(z)
 rows_by_delta.append(rows)
zero=sorted(set().union(*map(set,rows_by_delta)))
fours=[z for z in zero if z.bit_count()==4]
high=[z for z in zero if z.bit_count()>4]
target=[cap[i][i] for i in range(10)]
paircaps=[cap[i][j] for i,j in PAIRS]
info={z:([i for i in range(10) if z>>i&1],[p for p,(i,j) in enumerate(PAIRS) if z>>i&1 and z>>j&1]) for z in zero}
col=[0]*10; pairs=[0]*45; chosen=[]; lookups={}; lowcounts={}
def fits(z):
 cs,ps=info[z]
 return all(col[i]<target[i] for i in cs) and all(pairs[p]<paircaps[p] for p in ps)
def add(z,sign):
 cs,ps=info[z]
 for i in cs: col[i]+=sign
 for p in ps: pairs[p]+=sign
for wanted in (7,8,9,10):
 lookup=defaultdict(list)
 def lowvisit(first,left):
  if left==0:
   lookup[tuple(col)].append((tuple(chosen),bytes(pairs)))
   return
  for ix in range(first,len(fours)):
   z=fours[ix]
   if fits(z):
    add(z,1); chosen.append(z); lowvisit(ix,left-1); chosen.pop(); add(z,-1)
 lowvisit(0,wanted)
 lookups[wanted]=lookup; lowcounts[str(wanted)]=sum(map(len,lookup.values()))
matrices=[]; highcounts=Counter()
def highvisit(first,surplus):
 if surplus==0:
  highcounts[tuple(sorted((z.bit_count() for z in chosen),reverse=True))]+=1
  key=tuple(t-c for t,c in zip(target,col)); wanted=11-len(chosen)
  for low,ps in lookups[wanted].get(key,[]):
   if all(x+y<=u for x,y,u in zip(ps,pairs,paircaps)):
    matrices.append(sorted(list(low)+chosen))
  return
 for ix in range(first,len(high)):
  z=high[ix]; extra=z.bit_count()-4
  if extra<=surplus and fits(z):
   add(z,1); chosen.append(z); highvisit(ix,surplus-extra); chosen.pop(); add(z,-1)
highvisit(0,4)
matrices.sort()
if len(matrices)!=len({tuple(z) for z in matrices}): raise RuntimeError('duplicates')
def stars(rows,b,delta):
 z=rows[b]; k=z.bit_count(); deg=k-delta
 if z not in rows_by_delta[delta]: return 0
 candidates=[c for c in range(11) if c!=b]
 cols=[sum(1<<c for c in candidates if rows[c]>>i&1) for i in range(10)]
 t=[sum(z>>j&1 for j in a[i]) for i in range(10)]
 universe=((1<<11)-1)^(1<<b)
 checks_red=[(universe^cols[i],3-len(a[i])+t[i]) for i in range(10) if not(z>>i&1)]
 checks_blue=[(cols[i],len(a[i])+k-6-t[i]) for i in range(10) if z>>i&1]
 count=0
 for chosenstar in itertools.combinations(candidates,deg):
  st=sum(1<<c for c in chosenstar)
  if any((st&mask).bit_count()>bound for mask,bound in checks_red): continue
  if any((st&mask).bit_count()<bound for mask,bound in checks_blue): continue
  count+=1
 return count
records=[]; patterns=Counter(); defect_candidates=[]
for rows in matrices:
 counts=[[stars(rows,b,d) for d in range(5)] for b in range(11)]
 patterns[tuple(sorted((z.bit_count() for z in rows),reverse=True))]+=1
 # At108 local14, sum k=48 and sum delta=4 force delta=k-4 at each b.
 ds=[z.bit_count()-4 for z in rows]
 if sum(ds)!=4 or any(d<0 for d in ds): raise RuntimeError('Summed equality bookkeeping')
 assignments=[ds] if max(ds)<=4 and all(counts[b][d] for b,d in enumerate(ds)) else []
 record={'rows':rows,'star_counts':counts,'deficit_assignments':assignments}
 records.append(record)
 if assignments: defect_candidates.append(record)
result={'agent':'six-books-3','role':'researcher','complete':True,'F_mask':cut['F_mask'],'zero_rows_by_delta':[len(r) for r in rows_by_delta],'low_multisets':lowcounts,'high_multisets':[[list(p),c] for p,c in sorted(highcounts.items())],'incidence_matrices':len(matrices),'patterns':[[list(p),c] for p,c in sorted(patterns.items())],'extendible_deficit_assignments':sum(len(r['deficit_assignments']) for r in records),'deficit_candidate_matrices':len(defect_candidates),'degree8_10_row_size_matrices':sum(max(z.bit_count() for z in r['rows'])<=6 for r in records),'assignment_types':[[list(k),v] for k,v in sorted(Counter(tuple(sorted(d for d in r['deficit_assignments'][0] if d)) for r in records if r['deficit_assignments']).items())],'elapsed_seconds':time.monotonic()-start}
(OUT/'transfer14_result.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'transfer14_records.json').write_text(json.dumps(records,separators=(',',':'))+'\n')
check_expected('transfer14',result)
print(json.dumps(result,indent=2))
