#!/usr/bin/env python3
"""Independent elementary-generator orbits, contact cells and color coverage."""
import itertools,json
from collections import Counter
import geometry

def transform(x,i,j):return x^((1<<i) if x>>j&1 else 0)
def run():
 unseen=set(itertools.combinations(range(1,16),5));orbits=[]
 while unseen:
  rep=min(unseen);seen={rep};stack=[rep]
  while stack:
   D=stack.pop()
   for j in range(1,4):
    for i in range(4):
     if i==j:continue
     E=tuple(sorted(transform(x,i,j) for x in D))
     if E not in seen:seen.add(E);stack.append(E)
  unseen-=seen;orbits.append({'representative':list(rep),'orbit_size':len(seen)})
 direct,transports=geometry.orbits()
 if direct!=orbits or len(transports)!=3003:raise ValueError('orbit coverage')
 bits={x:[(x>>k)&1 for k in range(4)] for x in range(16)}
 def dot(x,y):return sum(a*b for a,b in zip(bits[x],bits[y]))%2
 gs=geometry.group();contact_checks=0
 for basis in gs:
  perm={x:geometry.apply(basis,x) for x in range(16)}
  # Find the dual images by solving four scalar product equations literally.
  dual={y:next(z for z in range(16) if all(dot(basis[k],z)==bits[y][k] for k in range(4))) for y in range(16)}
  if sorted(perm.values())!=list(range(16)) or sorted(dual.values())!=list(range(16)):raise ValueError('invertibility')
  if perm[1]!=1 or {dual[y] for y in range(1,16,2)}!=set(range(1,16,2)):raise ValueError('affine set preservation')
  for x in range(1,16):
   for y in range(1,16):
    if dot(perm[x],dual[y])!=dot(x,y):raise ValueError('physical cross contact')
    contact_checks+=1
 B=list(range(1,16))+list(range(1,16,2));cells=Counter()
 for x in range(1,16):
  for z in range(1,16):
   if x==z:continue
   size=sum(dot(x,y)==1 and dot(z,y)==0 for y in B);cells[size]+=1
   if (size<=5)!=(z==1):raise ValueError('contact-cell condition')
 accepted=0
 for D in itertools.combinations(range(1,16),5):
  survivors=[]
  for colors in itertools.product((0,1),repeat=5):
   c=dict(zip(D,colors))
   if 1 in c and c[1]:continue
   if any(c[x]==1 and c[z]==0 and sum(dot(x,y)==1 and dot(z,y)==0 for y in B)>5 for x in D for z in D if x!=z):continue
   survivors.append(colors)
  expected=[tuple(0 for x in D),tuple(0 if x==1 else 1 for x in D)]
  if survivors!=expected:raise ValueError('color branch completeness')
  accepted+=len(survivors)
 return {'status':'COMPLETE_GEOMETRY_AND_COLOR_COVERAGE','group_order':len(gs),'orbits':orbits,'labeled_five_sets':len(transports),'physical_type_contacts_checked':contact_checks,'ordered_cell_sizes':dict(sorted(cells.items())),'physical_pair_color_assignments_considered':3003*32,'surviving_pair_color_assignments':accepted,'canonical_global_branches':32}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
