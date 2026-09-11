#!/usr/bin/env python3
"""Exact controls and finite equality classification; standard library only."""
from pathlib import Path
from itertools import combinations,product,permutations
from collections import Counter
from math import comb
import json,random
from template import bitset,transversal,edges,proper,decide,fano_planes
HERE=Path(__file__).resolve().parent

def small_complete():
 r=3;w=3
 candidates=[(1<<u)|(3<<(w+2*i)) for i in range(r) for u in range(w)]
 candidates += [transversal(r,w,t) for t in range(1<<r)]
 # All colorings modulo global color reversal, represented by a bit vector.
 colorings=1<<(w+2*r-1);full=(1<<(w+2*r))-1;universe=(1<<colorings)-1
 cover=[]
 for E in candidates:cover.append(sum(1<<C for C in range(colorings) if not(E&C) or E&C==E))
 unions=[0]*(1<<len(candidates));noncolorable=Counter();witnesses=0
 outer=[]
 for tm in range(256):
  T={t for t in range(8) if tm>>t&1}
  outer.append(all(t in T or (t^7) in T for t in range(8)) and all(t in T or (t^(1<<i)) in T for t in range(8) for i in range(3)))
 corepass=[]
 for cm in range(512):
  Cs=[tuple(1<<u for u in range(3) if cm>>(3*i+u)&1) for i in range(3)]
  corepass.append(decide(r,w,Cs,range(8))[0])
 for mask in range(1<<len(candidates)):
  if mask:
   low=mask&-mask;unions[mask]=unions[mask^low]|cover[low.bit_length()-1]
  actual=unions[mask]==universe
  assert actual==(corepass[mask&511] and outer[mask>>9])
  if actual:noncolorable[mask.bit_count()]+=1
  elif mask%97==0:
   cm=mask&511;tm=mask>>9;Cs=[tuple(1<<u for u in range(3) if cm>>(3*i+u)&1) for i in range(3)];T=[t for t in range(8) if tm>>t&1]
   verdict,R=decide(r,w,Cs,T);assert not verdict and proper(r,w,edges(r,w,Cs,T),R);witnesses+=1
 assert min(noncolorable)==7 and noncolorable[7]==6
 return {'templates_checked':1<<len(candidates),'noncolorable_by_edges':dict(sorted(noncolorable.items())),'minimum_edges':7,'equality_templates':6,'proper_witness_controls':witnesses}

def equality_and_witness():
 fs=fano_planes();assert len(fs)==len(set(fs))==30
 # All 30 labeled Steiner triple systems are in one orbit, checked entrywise.
 base=fs[0];orbit=set()
 for p in permutations(range(7)):
  orbit.add(tuple(sorted(sum(1<<p[i] for i in range(7) if E>>i&1) for E in base)))
 assert orbit==set(fs)
 for C in fs:
  assert all(E&F for E,F in combinations(C,2))
  assert all((int(S in C)+sum(F&S==0 for F in C))==1 for S in map(bitset,combinations(range(7),3)))
  for parity in [0,1]:assert decide(5,7,[C]*5,[t for t in range(32) if t.bit_count()%2==parity])[0]
 T=[t for t in range(32) if t.bit_count()%2==1];es=edges(5,7,[base]*5,T)
 assert len(es)==51 and all(sum(E>>i&1 for E in es)==15 for i in range(17))
 unique=[0]*51;hist=Counter()
 for R in range(1<<16):
  mono=[i for i,E in enumerate(es) if not(E&R) or E&R==E]
  assert mono;hist[len(mono)]+=1
  if len(mono)==1:unique[mono[0]]+=1
 assert all(unique)
 expected_witness=json.loads((HERE/'witness51.json').read_text())
 assert expected_witness=={'vertices':17,'edges':[[i for i in range(17) if E>>i&1] for E in es]}
 return {'labeled_Fano_planes':30,'Fano_isomorphism_types':1,'equality_templates_fixed_labels':60,'equality_isomorphism_types':1,'witness_vertices':17,'witness_edges':51,'degree':15,'colorings_modulo_reversal':1<<16,'monochromatic_edge_histogram':dict(sorted(hist.items())),'sole_edge_witness_counts':dict(sorted(Counter(unique).items()))}

def symbolic_controls():
 out=[]
 for r in range(3,10):
  k=r-2;w=2*k+1;C=comb(w,k);num=r*(r-1)*C
  # Sum all balanced-cut inequalities: each variable has coefficient r(r-1).
  # Check one layer/edge's occurrence count by direct combinatorial enumeration.
  A=set(range(k));left=1;right=sum(not A&set(S) for S in combinations(range(w),k))
  assert right==k+1 and (r-1)*(left+right)==r*(r-1)
  out.append({'r':r,'core_vertices':w,'balanced_cuts':C,'inequalities':num,'variable_coefficient':r*(r-1),'core_edge_lower_bound':C,'odd_template_lower_bound':2**(r-1)+C if r%2 else None})
 # Pointwise stability inequality, allowing nonminimal slack values.
 stability=0
 for r in range(3,10):
  for bits in range(1<<r):
   b=bits.bit_count();ys=[int(any(not(bits>>i&1) for i in range(r) if i!=j)) for j in range(r)]
   slack=(r-1)*(b+sum(ys)-r)
   assert b*(r-b)<=slack;stability+=1
 # Equality at r=9 would require S(6,7,15); its 4-subset replication number is 55/3.
 assert comb(15-4,6-4)%comb(7-4,6-4)!=0
 return {'counting_identities':out,'stability_patterns':stability,'r9_equality_divisibility_obstruction':'55/3 is not an integer; template edge count is at least 6692'}

def random_controls():
 rng=random.Random(280051);checked=0
 for r,w in [(3,4),(4,5),(5,7)]:
  allcores=list(map(bitset,combinations(range(w),r-2)))
  for trial in range(60):
   Cs=[tuple(E for E in allcores if rng.randrange(4)==0) for _ in range(r)]
   T=[t for t in range(1<<r) if rng.randrange(3)]
   yes,R=decide(r,w,Cs,T);es=edges(r,w,Cs,T)
   if not yes:assert proper(r,w,es,R)
   else:assert all(any(not(E&C) or E&C==E for E in es) for C in range(1<<(w+2*r-1)))
   checked+=1
 return checked

def run():return {'scope':'general theorem proved in proof.md; computations are finite controls and the r=5 equality classification','small_complete':small_complete(),'equality':equality_and_witness(),'symbolic_controls':symbolic_controls(),'additional_template_controls':random_controls(),'global_m5_bounds':[35,51],'new_global_bound_claimed':False}
if __name__=='__main__':
 if not __debug__:raise RuntimeError('Run without -O')
 result=run();text=json.dumps(result,indent=2,sort_keys=True)+'\n'
 expected=HERE/'expected.json'
 if expected.exists():assert json.loads(text)==json.loads(expected.read_text())
 print(text,end='')
