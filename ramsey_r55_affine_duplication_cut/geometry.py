#!/usr/bin/env python3
import itertools,json

def rank(rows):
 b={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k not in b:b[k]=x;break
   x^=b[k]
 return len(b)

def apply(basis,x):
 y=0
 for i in range(4):
  if x>>i&1:y^=basis[i]
 return y

def group():
 return [(1,a,b,c) for a,b,c in itertools.product(range(1,16),repeat=3) if rank((1,a,b,c))==4]

def orbits():
 gs=group();allsets=set(itertools.combinations(range(1,16),5));answer=[];transports={}
 while allsets:
  representative=min(allsets);orb=set()
  for basis in gs:
   target=tuple(sorted(apply(basis,x) for x in representative));orb.add(target)
   if target not in transports:transports[target]=(representative,basis)
  allsets-=orb;answer.append({'representative':list(representative),'orbit_size':len(orb)})
 return answer,transports

if __name__=='__main__':
 o,t=orbits();print(json.dumps({'group_order':len(group()),'labeled_doubled_sets':len(t),'orbits':o},sort_keys=True))
