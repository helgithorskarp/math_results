#!/usr/bin/env python3
"""Generate the exact zero-class weight cap with a three-AP at0,1,2."""
import argparse,hashlib,itertools,json,math
from pathlib import Path

def need(ok,message):
 if not ok:raise ValueError(message)

def model(q,limit):
 need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)),'q must be prime>=7')
 need(2<limit<q,'Cap must be between3 andq-1')
 cap=limit-1
 labels={p:i+1 for i,p in enumerate(itertools.combinations(range(q),2))}
 edge=lambda x,y:labels[tuple(sorted((x,y)))]
 def canonical(row):return tuple(sorted(set(row),key=abs))
 clauses=set()
 for x in range(1,q):
  for y in range(x+1,q):
   ids=(edge(0,x),edge(0,y),edge(x,y))
   for bits in itertools.product((0,1),repeat=3):
    if sum(bits)%2:clauses.add(canonical(-v if b else v for v,b in zip(ids,bits)))
 for r in range(1,(q+1)//2):
  for a in range(q):
   row=canonical(edge((a+j*r)%q,(a+(j+3)*r)%q) for j in range(4))
   clauses.add(row);clauses.add(tuple(-v for v in row))
 base=len(labels);criterion_clauses=len(clauses)
 variables=base;cells={}
 def neg(literal):return not literal if isinstance(literal,bool) else -literal
 def add(*literals):
  if any(v is True for v in literals):return
  row={v for v in literals if v is not False}
  if any(-v in row for v in row):return
  need(row,'Unexpected empty clause');clauses.add(canonical(row))
 for i in range(1,q):
  for k in range(1,min(i,cap+1)+1):
   variables+=1;z=cells[i,k]=variables;a=cells.get((i-1,k),False);b=True if k==1 else cells[i-1,k-1]
   add(neg(a),z);add(i,neg(b),z);add(-z,a,-i);add(-z,a,b)
 add(-cells[q-1,cap+1]);add(-edge(0,1));add(-edge(0,2))
 raw=f'p cnf {variables} {len(clauses)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(clauses))
 return raw,{'q':q,'minority_weight_cap':limit,'counted_color':0,'count_target_cap':cap,'criterion_clauses':criterion_clauses,'variables':variables,'clauses':len(clauses),
             'base_variables':base,'counter_variables':variables-base,'model_sha256':hashlib.sha256(raw.encode()).hexdigest()}

def mixed_model(n):
 need(n>=7,'Mixed control length must be at least7')
 clauses=set()
 for length,sign in ((3,-1),(7,1)):
  for d in range(1,(n-1)//(length-1)+1):
   for a in range(1,n-(length-1)*d+1):clauses.add(tuple(sign*(a+j*d) for j in range(length)))
 raw=f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(clauses))
 return raw,{'n':n,'variables':n,'clauses':len(clauses),'model_sha256':hashlib.sha256(raw.encode()).hexdigest()}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--q',type=int,default=103);p.add_argument('--limit',type=int);p.add_argument('--mixed-n',type=int);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need((a.limit is None)!=(a.mixed_n is None),'Choose exactly one model kind')
 raw,meta=mixed_model(a.mixed_n) if a.mixed_n is not None else model(a.q,a.limit)
 a.output.write_text(raw);print(json.dumps(meta,sort_keys=True))

if __name__=='__main__':main()
