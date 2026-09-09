#!/usr/bin/env python3
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product
import json
import verify as V

def polynomial_product(i,j):
 powers=[((i>>k)&1)+((j>>k)&1) for k in range(4)]
 def reduce(e):
  for k,d in enumerate((-3,-11,5)):
   if e[k]>=2:
    f=e.copy();f[k]-=2;return V.scale(reduce(f),d)
  if e[3]>=2:
   f=e.copy();f[3]-=2;g=f.copy();g[0]+=1;g[1]+=1
   return V.add(V.scale(reduce(f),-3320),V.scale(reduce(g),632))
  return V.basis(sum(a<<k for k,a in enumerate(e)))
 return reduce(powers)

def main():
 for i,j in product(range(16),repeat=2):
  V.need(V.mul(V.basis(i),V.basis(j))==polynomial_product(i,j),'independent monomial product')
  V.need(V.bar(V.mul(V.basis(i),V.basis(j)))==V.mul(V.bar(V.basis(i)),V.bar(V.basis(j))),'conjugate product')
 cert=json.loads((V.HERE/'certificate.json').read_text());rows=json.loads((V.HERE/'seed.json').read_text())['moser_rows']
 mutations=[]
 x=deepcopy(cert);x['generator_anchors'][0][1]=x['generator_anchors'][0][0];mutations.append(('collapsed anchor',x))
 x=deepcopy(cert);x['generator_anchors'][0][4]=2;mutations.append(('invalid orientation',x))
 x=deepcopy(cert);x['generator_anchors'][0][2]=29;mutations.append(('outside seed index',x))
 x=deepcopy(cert);x['copy_tape'][0][0]=1;mutations.append(('future parent',x))
 x=deepcopy(cert);x['address_colours']=x['address_colours'][:-1];mutations.append(('truncated word',x))
 x=deepcopy(cert);x['address_colours']='0'*len(x['address_colours']);mutations.append(('all monochromatic',x))
 x=deepcopy(cert);x['physical_vertices']-=1;mutations.append(('incorrect physical order',x))
 rejected=[]
 for name,x in mutations:
  try:V.verify(x,rows)
  except ValueError:rejected.append(name)
  else:raise RuntimeError('accepted mutation: '+name)
 # A real unit triangle and a nonunit radical norm guard the metric predicate.
 A=V.basis(1);w=V.scale(V.add(V.ONE,A),Q(1,2))
 es,false=V.graph([V.ZERO,V.ONE,w]);V.need(es==[(0,1),(0,2),(1,2)] and false==0,'unit triangle')
 z=V.add(V.scale(V.basis(2),Q(1,2)),V.scale(V.basis(1),Q(-1,2)))
 # norm(z)=7/2 - sqrt(33)/2, not one: all radical terms matter.
 V.need(V.norm(z)!=V.ONE,'nonunit radical norm')
 V.need(V.evaluate(V.norm(z))!=1,'new modular nonunit test')
 print(json.dumps({'basis_product_cases':256,'conjugation_cases':256,'unit_triangle_edges':3,'rejected_mutations':rejected},indent=2,sort_keys=True))
if __name__=='__main__':main()
