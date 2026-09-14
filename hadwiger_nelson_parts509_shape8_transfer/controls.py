#!/usr/bin/env python3
"""Definition-level fault controls and exhaustive small conditional-CNF checks."""
from copy import deepcopy
from itertools import product
import json
import verify as v

def main():
 data=v.inputs();original=json.loads((v.HERE/'certificate.json').read_text());v.validate(original,data)
 changes=[]
 def mutate(fn):
  c=deepcopy(original);fn(c);changes.append(c)
 mutate(lambda c:c['X'].__setitem__(0,c['X'][1]))
 mutate(lambda c:c['X'].__setitem__(-1,999999))
 mutate(lambda c:c.__setitem__('unit_edges',c['unit_edges']+1))
 mutate(lambda c:c['positive_words'][0].__setitem__('word','0'*508))
 mutate(lambda c:c['positive_words'][0].__setitem__('class',c['forbidden_classes'][0]))
 mutate(lambda c:c.__setitem__('five_colouring','0'*508))
 mutate(lambda c:c['forbidden_classes'].pop())
 mutate(lambda c:c['allowed_classes'].append(c['allowed_classes'][0]))
 for i,c in enumerate(changes):
  try:v.validate(c,data)
  except (ValueError,IndexError,KeyError):pass
  else:raise ValueError('accepted corrupted certificate '+str(i))
 # Check the generated conditional CNF against literal graph-colouring
 # semantics on every graph with two source pins and two driver vertices.
 # Enumerate *all* Boolean assignments, including invalid one-hot encodings.
 potential=[(0,374),(0,375),(1,374),(1,375),(374,375)]
 words=['00','01','02'];cert={'X':[374,375],'forbidden_classes':[0,1,2]}
 checks=0
 for edge_bits in product((0,1),repeat=5):
  E=[e for e,on in zip(potential,edge_bits) if on];encoded,nv,nc=v.negative_cnf(cert,E,words)
  cs=[list(map(int,l.split()))[:-1] for l in encoded.decode().splitlines()[1:]]
  actual=False
  for bits in product((0,1),repeat=nv):
   checks+=1
   if all(any(bool(bits[abs(l)-1])==(l>0) for l in c) for c in cs):actual=True
  expected=False
  for p in range(3):
   for a,b in product(range(4),repeat=2):
    col={0:int(words[p][0]),1:int(words[p][1]),374:a,375:b}
    if all(col[u]!=col[w] for u,w in E):expected=True
  v.need(actual==expected,'conditional CNF differs from physical extension semantics')
 # Add one source pin of each colour around a single driver. No extension.
 cert={'X':[374],'forbidden_classes':[0]};encoded,nv,nc=v.negative_cnf(cert,[(i,374) for i in range(4)],['0123'])
 cs=[list(map(int,l.split()))[:-1] for l in encoded.decode().splitlines()[1:]]
 v.need(not any(all(any(bool(bits[abs(l)-1])==(l>0) for l in c) for c in cs) for bits in product((0,1),repeat=nv)),'four forbidden colours should refute one vertex')
 print(json.dumps({'status':'CONTROLS_PASS','corruptions_rejected':len(changes),'exhaustive_small_graphs':32,'boolean_assignments_checked':checks,'no_extension_control':True},sort_keys=True))

if __name__=='__main__':main()
