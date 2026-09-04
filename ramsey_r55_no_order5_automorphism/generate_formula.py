#!/usr/bin/env python3
"""Exact 148-variable Ramsey encodings for the two residual incidence patterns.

No extra normalization is used for h=0. For h=1, choose the first internal
orientation and independently minimize seven anchor cross words by rotation.
Generated CNFs and proofs belong in an external work directory.
"""
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json,time

TRUE=149
PAIRS=tuple(combinations(range(8),2))
def cross(i,j,d):
 assert i<j
 return 9+5*PAIRS.index((i,j))+d

def incidence(h):return (0,1,2,3,5,5,6,6) if h==0 else tuple(range(8))

def literal(h,u,v):
 if u>v:u,v=v,u
 if v<3:return TRUE if (u,v)==(0,1) else 0
 j,b=divmod(v-3,5)
 if u<3:return TRUE if incidence(h)[j]&(1<<u) else 0
 i,a=divmod(u-3,5)
 if i==j:return i+1 if (b-a)%5 in (1,4) else -(i+1)
 return cross(i,j,(b-a)%5)

def base(h):
 matrix=[[0]*43 for _ in range(43)]
 for u,v in combinations(range(43),2):matrix[u][v]=literal(h,u,v)
 clauses=set()
 for vertices in combinations(range(43),5):
  lits={matrix[u][v] for u,v in combinations(vertices,2)}
  variables=lits-{0,TRUE}
  if any(-v in variables for v in variables):continue
  if 0 not in lits:clauses.add(tuple(sorted(-v for v in variables)))
  if TRUE not in lits:clauses.add(tuple(sorted(variables)))
 return sorted(clauses,key=lambda c:(len(c),c))

def symmetry(h):
 if h==0:return []
 clauses=[(1,)] # simultaneous coordinate multiplication by 2 flips all internal bits
 # Each other cycle can be independently shifted relative to cycle zero.
 for j in range(1,8):
  for word in range(32):
   bits=tuple((word>>d)&1 for d in range(5))
   if bits==min(bits[s:]+bits[:s] for s in range(5)):continue
   clauses.append(tuple(-cross(0,j,d) if bits[d] else cross(0,j,d) for d in range(5)))
 return clauses

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--h',type=int,choices=(0,1),required=True);parser.add_argument('--out',type=Path,required=True)
 args=parser.parse_args();start=time.monotonic()
 clauses=base(args.h);nbase=len(clauses);clauses+=symmetry(args.h)
 data=f'p cnf 148 {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
 args.out.write_text(data)
 rec={'h':args.h,'variables':148,'base_clauses':nbase,'symmetry_clauses':len(clauses)-nbase,'sha256':hashlib.sha256(data.encode()).hexdigest(),'generation_seconds':time.monotonic()-start}
 args.out.with_suffix('.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec),flush=True)
if __name__=='__main__':main()
