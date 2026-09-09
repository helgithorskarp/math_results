#!/usr/bin/env python3
"""Boundary, arithmetic, physical, and malformed-certificate controls."""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import verify as V
G,E=V.G,V.E

def physical_real(z):
 points=sorted({tuple(sum((Q(G.T[a[j]][k])*z**j for j in range(5)),Q(0)) for k in range(2)) for a in G.LABELS})
 edges=[]
 for i,p in enumerate(points):
  for j,q in enumerate(points[:i]):
   a,b=p[0]-q[0],p[1]-q[1]
   if a*a+a*b+b*b==1:edges.append((j,i))
 return points,edges

def run():
 V.need(G.primitive({(0,0):0})==(),'zero polynomial normalization')
 V.need(G.primitive({(0,0):0,(1,0):-2})==((1,0,1),),'sparse sign/content normalization')
 V.need(E.simple_root_factor([(1,0),(2,0),(1,0)])==[E.ONE],'square has no simple root')
 V.need(E.simple_root_factor([(0,0),(0,0),(1,0),(1,0)])==[E.ONE,E.ONE],'one simple root beside a repeated root')
 rejected=[]
 try:E.inv(E.ZERO)
 except ValueError:rejected.append('zero field inverse')
 else:raise RuntimeError('accepted zero inverse')
 # Verify physical witnesses directly with rational Eisenstein coordinates.
 physical=[]
 for z,n in [(Q(0),3),(Q(1),21),(Q(1,2),243),(Q(2),243),(Q(3),243)]:
  points,edges=physical_real(z);V.need(len(points)==n,'physical order')
  if z in (0,1,2,3):
   word=[int(a-b)%3 for a,b in points]
  else:
   # At |z|<=1/2 a physical point has a unique first digit.
   fibres={}
   for label in G.LABELS:
    point=tuple(sum(Q(G.T[label[j]][k])*z**j for j in range(5)) for k in range(2))
    if point in fibres:V.need(fibres[point]==label[0],'first-digit fibre consistency')
    fibres[point]=label[0]
   word=[fibres[p] for p in points]
  V.need(all(word[a]!=word[b] for a,b in edges),'direct physical three-colouring')
  physical.append({'z':str(z),'vertices':len(points),'unit_edges':len(edges)})
 # Exact digit identities behind the proposed D3 parameter interface.
 for j in range(5):
  u=G.U[(2*j)%6];shift=((0,0),(-1,0),(0,-1))[j%3]
  V.need({G.emul(u,t) for t in G.T}=={(t[0]+shift[0],t[1]+shift[1]) for t in G.T},'C3 digit translation')
 V.need({(a+b,-b) for a,b in G.T}=={(1-a,-b) for a,b in G.T},'conjugate digit identity')
 original=json.loads((V.HERE/'certificate.json').read_text());variants=[]
 c=deepcopy(original);c['factor_inventory_sha256']='0'*64;variants.append(('wrong factor hash',c))
 c=deepcopy(original);c['colour_specs'][0]['weights'][0]=0;variants.append(('monochromatic universal triangle',c))
 c=deepcopy(original);c['protectors'].pop();variants.append(('missing curve protector',c))
 c=deepcopy(original);c['protectors'][0][1]=0;variants.append(('wrong curve protector',c))
 with TemporaryDirectory(prefix='hn-radix-controls-') as folder:
  for i,(name,c) in enumerate(variants):
   f=Path(folder)/f'{i}.json';f.write_text(json.dumps(c))
   try:V.run(f)
   except ValueError:rejected.append(name)
   else:raise RuntimeError('accepted corruption: '+name)
 return {'status':'CONTROLS_PASSED','rejected_corruptions':rejected,'physical_checks':physical,'simple_root_boundary_checks':2,'parameter_symmetry_digit_checks':6,'CAS_calls':0,'solver_calls':0}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
