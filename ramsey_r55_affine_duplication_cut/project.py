#!/usr/bin/env python3
"""Necessary 23-side CNF for complete global43 affine-duplication branches."""
import hashlib,itertools,json,sys
from pathlib import Path
import geometry

def neg(x):return not x if type(x) is bool else -x
class CNF:
 def __init__(self,n):self.n=n;self.cs=[]
 def add(self,*lits):
  if any(type(x) is bool and x for x in lits):return
  s=set(x for x in lits if type(x) is not bool)
  if any(-x in s for x in s):return
  self.cs.append(tuple(sorted(s,key=lambda x:(abs(x),x))))
 def bounds(self,lits,lo,hi):
  if lo<0:lo=0
  if hi>=len(lits):hi=len(lits)
  if lo>hi:self.add();return
  old={0:True}
  for i,x in enumerate(lits,1):
   new={0:True}
   for j in range(1,min(i,hi+1)+1):
    a=old.get(j,False);b=old.get(j-1,False);self.n+=1;s=self.n;new[j]=s
    self.add(neg(a),s);self.add(neg(x),neg(b),s)
    self.add(-s,a,x);self.add(-s,a,b)
   old=new
  if lo:self.add(old.get(lo,False))
  if hi<len(lits):self.add(neg(old.get(hi+1,False)))

def build(D,mode):
 if type(D) is not list or len(D)!=5 or any(type(x) is not int or not 1<=x<=15 for x in D) or sorted(set(D))!=D:raise ValueError('five distinct doubled row labels')
 if type(mode) is not int or mode not in (0,1):raise ValueError('pair color mode')
 B=list(range(1,16))+[x for x in range(1,16) if x&1]
 A=list(range(1,16))+list(D)
 pairs=list(itertools.combinations(range(23),2));var={p:i+1 for i,p in enumerate(pairs)}
 cnf=CNF(253)
 for q in itertools.combinations(range(23),5):
  for c in (0,1):cnf.add(*(var[p]*(1-2*c) for p in itertools.combinations(q,2)))
 for q in itertools.combinations(range(23),4):
  colors=set()
  for x in range(1,16):
   contact={(x&B[y]).bit_count()%2 for y in q}
   if len(contact)==1:colors|=contact
  for c in colors:cnf.add(*(var[p]*(1-2*c) for p in itertools.combinations(q,2)))
 for x in D:
  c=0 if x==1 else mode
  contacts=[y for y in range(23) if (x&B[y]).bit_count()%2==c]
  for q in itertools.combinations(contacts,3):cnf.add(*(var[p]*(1-2*c) for p in itertools.combinations(q,2)))
 raw=len(cnf.cs);cnf.cs=sorted(set(cnf.cs));base=len(cnf.cs)
 degrees=[]
 for v,y in enumerate(B):
  cross=sum((x&y).bit_count()%2 for x in A);lo=18-cross;hi=24-cross
  degrees.append([lo,hi]);cnf.bounds([var[tuple(sorted((u,v)))] for u in range(23) if u!=v],lo,hi)
 body=f'p cnf {cnf.n} {len(cnf.cs)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cnf.cs)
 report={'D':list(D),'mode':mode,'physical_variables':253,'variables':cnf.n,'clauses':len(cnf.cs),'physical_raw_clauses':raw,'physical_unique_clauses':base,'B_red_degree_bounds':degrees,'cnf_bytes':len(body),'cnf_sha256':hashlib.sha256(body.encode()).hexdigest()}
 return body,report
if __name__=='__main__':
 orbit=int(sys.argv[1]);mode=int(sys.argv[2]);dest=Path(sys.argv[3]);D=geometry.orbits()[0][orbit]['representative']
 body,report=build(D,mode);dest.write_text(body);dest.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
