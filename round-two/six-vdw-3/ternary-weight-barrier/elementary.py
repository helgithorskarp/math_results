#!/usr/bin/env python3
"""Finite controls for the pair-extension and product lemmas.

The mathematical proofs are in PROOF.md. These controls enumerate the local
truth relation and small-field identities, rather than proposing a witness.
"""
import itertools,json

def need(ok,message):
 if not ok:raise ValueError(message)

def periodic(bits):return all(bits[j]==bits[j+3] for j in range(4))

def counts(bits):
 q=len(bits);A=B=R=incidences=pairs=0
 for x in range(q):
  for r in range(1,q):
   at=lambda k:bits[(x+k*r)%q]
   A+=at(0)*at(1)*at(3);B+=at(0)*at(1)*at(4)
   R+=at(-2)*at(0)*at(3)*at(5)
   pairs+=at(0)*at(3)
   incidences+=at(0)*at(3)*sum(at(k) for k in (-1,1,2,4))
 return A,B,R,incidences,pairs

def main():
 local=eligible=0
 for bits in itertools.product((0,1),repeat=8):
  # Positions -2,-1,0,1,2,3,4,5; only the two relevant windows.
  local+=1
  if bits[2] and bits[5] and not periodic(bits[:7]) and not periodic(bits[1:]):
   need(any(bits[i] for i in (1,3,4,6)) or (bits[0] and bits[7]),'Pair extension failed')
   eligible+=1
 identities=valid_checks=0
 for q in (11,13):
  for tail in itertools.product((0,1),repeat=q-1):
   bits=(0,)+tail;A,B,R,I,P=counts(bits);n=sum(bits)
   need(I==2*A+2*B and P==n*(n-1),'Double-counting identity failed');identities+=1
   valid=all(not periodic(tuple(bits[(x+j*r)%q] for j in range(7))) for x in range(q) for r in range(1,q))
   if valid:
    need(2*A+2*B+R>=n*(n-1),'Pair-extension moment bound failed');valid_checks+=1
 # Every nonconstant three-bit pattern is a rotation or complement of001.
 patterns=set()
 for shift in range(3):
  for color in (0,1):patterns.add(tuple(int((shift+j)%3==2)^color for j in range(3)))
 need(patterns==set(itertools.product((0,1),repeat=3))-{(0,0,0),(1,1,1)},'Order-three cover failed')
 print(json.dumps({'status':'PAIR_EXTENSION_AND_PRODUCT_CONTROLS_CHECKED','local_truth_cases':local,
                   'eligible_local_pairs':eligible,'small_field_moment_identities':identities,
                   'criterion_valid_moment_checks':valid_checks,'nonconstant_three_cycle_patterns':len(patterns)},sort_keys=True))

if __name__=='__main__':main()
