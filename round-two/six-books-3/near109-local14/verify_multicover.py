"""Independent multicover enumeration of near109 zero-face rows.
Author six-books-3, researcher. No import of the generator or old certificate code.
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
# Public local14 core51317328, reconstructed from the 28-edge encoding.
pairs8=list(combinations(range(8),2)); a=[set() for _ in range(10)]
for i,j in ((0,2),(0,3),(1,4),(1,5)):
 a[i].add(j); a[j].add(i)
for bit,(i,j) in enumerate(pairs8):
 if 51317328>>bit&1: a[i+2].add(j+2); a[j+2].add(i+2)
h=list(map(len,a)); pairs=list(combinations(range(10),2))
upper=[h[i]+h[j]-(5 if j in a[i] else 2)-len(a[i]&a[j]) for i,j in pairs]
beta=[(0,6),(0,7),(0,8),(0,9),(1,6),(1,7),(1,8),(1,9),(2,7),(2,9),(3,6),(3,8),(4,8),(4,9),(5,6),(5,7)]
alpha=[-4,-4]+[-2]*8
bydelta=[]
for delta in range(3):
 zero=[]
 for elements in (set(c) for k in range(4+delta,11) for c in combinations(range(10),k)):
  k=len(elements)
  if any((low in elements and elements&other) or (low not in elements and not elements&other) for low,other in ((0,{2,3}),(1,{4,5}))): continue
  if any(cap<1 and i in elements and j in elements for (i,j),cap in zip(pairs,upper)): continue
  if any(k>len(a[i]&elements)+5+delta for i in set(range(10))-elements): continue
  if any(len(a[i]&elements)<k-7 for i in elements): continue
  score=8+sum(alpha[i] for i in elements)+sum(i in elements and j in elements for i,j in beta)
  if score<0: raise RuntimeError('negative integer score')
  if score==0: zero.append(sum(1<<i for i in elements))
 bydelta.append(sorted(zero))
words=sorted(set().union(*map(set,bydelta)))
cs=[[i for i in range(10) if z>>i&1] for z in words]
ps=[[p for p,(i,j) in enumerate(pairs) if z>>i&1 and z>>j&1] for z in words]
column=[x+2 for x in h]; pairleft=upper.copy(); selected=[]; answers=[]
nodes=0; start=time.monotonic(); deadline=start+20.0
# A phase chooses every row containing a selected column, in sorted order.
# The next phase starts only when that column is completely covered.
def fits(q,left,surplus):
 return (len(cs[q])-4<=surplus and all(column[i]>0 for i in cs[q]) and all(pairleft[p]>0 for p in ps[q]))
def visit(left,surplus,pivot=None,first=0):
 global nodes
 nodes+=1
 if nodes%10000==0 and time.monotonic()>deadline: raise TimeoutError('INCOMPLETE ENUMERATION')
 if left==0:
  if not any(column) and surplus==0: answers.append(sorted(words[q] for q in selected))
  return
 if sum(column)!=4*left+surplus: raise RuntimeError('column bookkeeping')
 if any(c>left for c in column): return
 if pivot is None:
  options=[]
  for i,need in enumerate(column):
   if need:
    candidates=[q for q in range(len(words)) if i in cs[q] and fits(q,left,surplus)]
    if not candidates: return
    options.append((len(candidates),i))
  if not options: return
  pivot=min(options)[1]; first=0
 for q in range(first,len(words)):
  if pivot not in cs[q] or not fits(q,left,surplus): continue
  for i in cs[q]: column[i]-=1
  for p in ps[q]: pairleft[p]-=1
  selected.append(q)
  if column[pivot]: visit(left-1,surplus-len(cs[q])+4,pivot,q)
  else: visit(left-1,surplus-len(cs[q])+4)
  selected.pop()
  for p in ps[q]: pairleft[p]+=1
  for i in cs[q]: column[i]+=1
visit(11,4)
answers.sort()
reference=json.loads((OUT/'transfer14_records.json').read_text())
expected=sorted(r['rows'] for r in reference)
if answers!=expected: raise RuntimeError(('enumeration mismatch',len(answers),len(expected)))
if len(answers)!=len({tuple(x) for x in answers}): raise RuntimeError('duplicate matrices')
result={'agent':'six-books-3','role':'researcher','complete':True,'method':'column-driven exact multicover; no generator import','zero_rows_by_deficit':list(map(len,bydelta)),'matrices':len(answers),'all_matrices_match_entrywise':True,'nodes':nodes,'elapsed_seconds':time.monotonic()-start,'matrix_sha256':hashlib.sha256(json.dumps(answers,separators=(',',':')).encode()).hexdigest()}
(OUT/'verify14_multicover_result.json').write_text(json.dumps(result,indent=2)+'\n')
check_expected('verify14_multicover',result)
print(json.dumps(result,indent=2))
