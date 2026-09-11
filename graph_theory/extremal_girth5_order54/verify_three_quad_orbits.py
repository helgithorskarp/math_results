"""Independent augmentation audit of quad-family point-permutation orbits."""
from itertools import combinations,permutations
from collections import Counter
from functools import lru_cache
import json,hashlib,time
from three_quad_orbits import reps

def iso(A,B,da,db):
 if len(A)!=len(B):return False
 left=Counter(tuple(i for i,Q in enumerate(A) if t in Q) for t in range(12))
 for p in permutations(range(len(A))):
  if any(da[i]!=db[p[i]] for i in range(len(A))):continue
  right=Counter(tuple(i for i in range(len(A)) if t in B[p[i]]) for t in range(12))
  if left==right:return True
 return False
@lru_cache(None)
def independent_reps(n6,n7):
 if n6+n7==0:return ((),)
 previous=independent_reps(n6,n7-1) if n7 else independent_reps(n6-1,0)
 degrees=(6,)*n6+(7,)*n7;out=[]
 for A in previous:
  for Q in combinations(range(12),4):
   Q=frozenset(Q)
   if any(len(Q&B)>1 for B in A):continue
   family=A+(Q,)
   if not any(iso(family,B,degrees,degrees) for B in out):out.append(family)
 return tuple(out)

def audit(n6,n7):
 degrees=(6,)*n6+(7,)*n7;A=independent_reps(n6,n7);B=reps(n6,n7)
 for C in B:
  if len(C)!=n6+n7 or any(len(Q)!=4 or not Q<=set(range(12)) for Q in C) or any(len(Q&R)>1 for Q,R in combinations(C,2)):raise ValueError('Malformed proposed representative')
 for C,D in combinations(B,2):
  if iso(C,D,degrees,degrees):raise ValueError('Duplicate proposed orbit')
 mapping=[]
 for C in A:
  matches=[i for i,D in enumerate(B) if iso(C,D,degrees,degrees)]
  if len(matches)!=1:raise ValueError('Coverage mismatch')
  mapping.extend(matches)
 if sorted(mapping)!=list(range(len(B))):raise ValueError('Extra proposed orbits')
 return dict(n6=n6,n7=n7,orbits=len(B),independent_orbits=len(A),augmentation_to_production=mapping,representatives=[[sorted(Q) for Q in C] for C in B])
