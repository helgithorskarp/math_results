#!/usr/bin/env python3
"""Exact (F) models: a weight-capped four-AP seed, or an uncapped no-four branch."""
import argparse,hashlib,itertools,json,math
from pathlib import Path

def need(ok,message):
 if not ok:raise ValueError(message)

def model(q,case,limit=27):
 need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)),'Prime q>=7 required')
 need(case in ('four','no-four'),'Unknown model kind')
 need(case!='four' or 3<limit<q,'Interior weight cap required')
 labels={p:i+1 for i,p in enumerate(itertools.combinations(range(q),2))}
 edge=lambda x,y:labels[tuple(sorted((x,y)))]
 canonical=lambda row:tuple(sorted(set(row),key=abs))
 clauses=set();base=len(labels);variables=base
 for x in range(1,q):
  for y in range(x+1,q):
   ids=(edge(0,x),edge(0,y),edge(x,y))
   for bits in itertools.product((0,1),repeat=3):
    if sum(bits)%2:clauses.add(canonical(-v if b else v for v,b in zip(ids,bits)))
 for r in range(1,(q+1)//2):
  for a in range(q):
   row=canonical(edge((a+j*r)%q,(a+(j+3)*r)%q) for j in range(4))
   clauses.add(row);clauses.add(tuple(-v for v in row))
 criterion=len(clauses)
 clauses.update(((-1,),(-2,)))
 def add(*literals):
  if any(v is True for v in literals):return
  row={v for v in literals if v is not False}
  if any(-v in row for v in row):return
  need(row,'Unexpected empty initial clause');clauses.add(canonical(row))
 if case=='four':
  # Signed prefix counter, credited to the preceding triplet source.
  cap=limit-1;cells={}
  def neg(v):return not v if isinstance(v,bool) else -v
  for i in range(1,q):
   for k in range(1,min(i,cap+1)+1):
    variables+=1;z=cells[i,k]=variables;a=cells.get((i-1,k),False);b=True if k==1 else cells[i-1,k-1]
    add(neg(a),z);add(i,neg(b),z);add(-z,a,-i);add(-z,a,b)
  add(-cells[q-1,cap+1]);add(-3)
 else:
  half=pow(2,-1,q)
  def word_literal(i,sign):
   i%=q
   return bool(sign<0) if i==0 else sign*i
  for a in range(q):
   for r in range(1,(q+1)//2):
    add(*(word_literal(a+j*r,1) for j in range(4)))
    add(*(word_literal(a+j*r,1) for j in range(3)),
        word_literal(a+half*r,-1),word_literal(a+3*half*r,-1))
 raw=f'p cnf {variables} {len(clauses)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(clauses))
 return raw,{'q':q,'case':case,'weight_cap':limit if case=='four' else None,'variables':variables,
             'clauses':len(clauses),'base_variables':base,'criterion_clauses':criterion,
             'counter_variables':variables-base,'cnf_sha256':hashlib.sha256(raw.encode()).hexdigest()}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--q',type=int,default=103);p.add_argument('--case',choices=('four','no-four'),required=True);p.add_argument('--limit',type=int,default=27);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw,meta=model(a.q,a.case,a.limit);a.output.write_text(raw);print(json.dumps(meta,sort_keys=True))

if __name__=='__main__':main()
