#!/usr/bin/env python3
"""Generate the exact at-most-weight fiber of ternary-period-avoiding words."""
import argparse,hashlib,itertools,json,math
from pathlib import Path

def need(ok,message):
 if not ok:raise ValueError(message)

def model(q,limit,encoding="cut"):
 need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)),'q must be prime>=7')
 need(0<limit<q-1,'Weight cap must be between1 andq-2')
 labels={p:i+1 for i,p in enumerate(itertools.combinations(range(q),2))}
 edge=lambda x,y:labels[tuple(sorted((x,y)))]
 def canonical(row):return tuple(sorted(set(row),key=abs))
 clauses=set()
 need(encoding in ('cut','word'),'Unsupported encoding')
 if encoding=='cut':
  for x in range(1,q):
   for y in range(x+1,q):
    ids=(edge(0,x),edge(0,y),edge(x,y))
    for bits in itertools.product((0,1),repeat=3):
     if sum(bits)%2:clauses.add(canonical(-v if b else v for v,b in zip(ids,bits)))
  for r in range(1,(q+1)//2):
   for a in range(q):clauses.add(canonical(edge((a+j*r)%q,(a+(j+3)*r)%q) for j in range(4)))
 else:
  for r in range(1,(q+1)//2):
   for a in range(q):
    positions=[(a+j*r)%q for j in range(7)]
    for prefix in itertools.product((0,1),repeat=3):
     row=[];trivial=False
     for j,v in enumerate(positions):
      bit=prefix[j%3]
      if v==0:
       if bit:trivial=True;break
      else:row.append(-v if bit else v)
     if not trivial:clauses.add(canonical(row))
 base=len(labels) if encoding=='cut' else q-1;criterion_clauses=len(clauses)
 variables=base;cells={}
 def neg(literal):return not literal if isinstance(literal,bool) else -literal
 def add(*literals):
  if any(v is True for v in literals):return
  row={v for v in literals if v is not False}
  if any(-v in row for v in row):return
  need(row,'Unexpected empty clause');clauses.add(canonical(row))
 for i in range(1,q):
  for k in range(1,min(i,limit+1)+1):
   variables+=1;z=cells[i,k]=variables;a=cells.get((i-1,k),False);b=True if k==1 else cells[i-1,k-1]
   add(neg(a),z);add(-i,neg(b),z);add(-z,a,i);add(-z,a,b)
 add(-cells[q-1,limit+1]);add(edge(0,1))
 raw=f'p cnf {variables} {len(clauses)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(clauses))
 return raw,{'encoding':encoding,'q':q,'weight_limit':limit,'criterion_clauses':criterion_clauses,'variables':variables,'clauses':len(clauses),
             'base_variables':base,'counter_variables':variables-base,'model_sha256':hashlib.sha256(raw.encode()).hexdigest()}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--q',type=int,default=103);p.add_argument('--encoding',choices=['cut','word'],default='cut');p.add_argument('--limit',type=int,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw,meta=model(a.q,a.limit,a.encoding);a.output.write_text(raw);print(json.dumps(meta,sort_keys=True))

if __name__=='__main__':main()
