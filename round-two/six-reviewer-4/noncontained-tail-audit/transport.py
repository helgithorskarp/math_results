#!/usr/bin/env python3
"""Independent GF16 subline realization and positive original-point maps.
No author point map/field encoding, automorphism order or cover is imported.
"""
from pathlib import Path
from itertools import combinations
from collections import deque
import argparse,json,hashlib
from core import parent,pts,mask,need,canon
def mul(a,b):
 out=0
 while b:
  if b&1:out^=a
  b>>=1;a<<=1
  if a&16:a^=19
 return out
def power(a,n):
 out=1
 for _ in range(n):out=mul(out,a)
 return out
def image(w,p):return mask(p[i]for i in pts(w))
def main():
 a=argparse.ArgumentParser();a.add_argument('--work',type=Path,required=True);args=a.parse_args();D=parent();ds=set(D)
 need(all(mul(u,power(u,14))==1 for u in range(1,16)),'literal GF16 nonzero inverses')
 sub=[u for u in range(16)if power(u,4)==u];need(len(sub)==4,'literal GF4 subfield')
 gens=[tuple(i^b if i<16 else 16 for i in range(17))for b in (1,2,4,8)]
 gens+=[tuple(mul(2,i)if i<16 else 16 for i in range(17)),tuple(16 if i==0 else 0 if i==16 else power(i,14)for i in range(17)),tuple(mul(i,i)if i<16 else 16 for i in range(17))]
 initial=mask([16]+sub);blocks={initial};queue=deque([initial])
 while queue:
  B=queue.popleft()
  for g in gens:
   t=image(B,g)
   if t not in blocks:blocks.add(t);queue.append(t)
 need(len(blocks)==68,'canonical subline design size')
 cb=sorted(blocks);lookup={mask(t):B for B in D for t in combinations(pts(B),3)}
 visits=0
 # Find a literal hypergraph isomorphism, rather than using author's basis.
 def extend(m):
  nonlocal visits
  visits+=1;need(visits<=2_000_000,'INCOMPLETE fixed2M map-search guard')
  if len(m)==17:
   perm=tuple(m[i]for i in range(17))
   return perm if {image(B,perm)for B in cb}==ds else None
  used=set(m.values());constraints=[]
  for B in cb:
   known=[i for i in pts(B)if i in m]
   if len(known)<3:continue
   target=lookup[mask(m[i]for i in known[:3])]
   if any(bool(B>>i&1)!=bool(target>>j&1)for i,j in m.items()):return None
   constraints.append((B,target))
  choices={}
  for u in range(17):
   if u in m:continue
   allowed=set(range(17))-used
   for B,target in constraints:allowed={v for v in allowed if bool(B>>u&1)==bool(target>>v&1)}
   if not allowed:return None
   choices[u]=allowed
  u=min(choices,key=lambda x:(len(choices[x]),x))
  for v in sorted(choices[u]):
   got=extend(m|{u:v})
   if got is not None:return got
  return None
 fixed={16:0,0:1,1:2};targetline=lookup[7];perm=None
 for v in range(17):
  if targetline>>v&1:continue
  perm=extend(fixed|{2:v})
  if perm is not None:break
 need(perm is not None and sorted(perm)==list(range(17)),'actual canonical-to-literal point bijection')
 inv={j:i for i,j in enumerate(perm)};pgens=[tuple(perm[g[inv[j]]]for j in range(17))for g in gens]
 for g in pgens:need(sorted(g)==list(range(17))and{image(B,g)for B in D}==ds,'actual wholeD generator preservation')
 group={tuple(range(17))};queue=deque(group);steps=0
 while queue:
  h=queue.popleft()
  for g in pgens:
   steps+=1;need(steps<=2_000_000,'INCOMPLETE fixed2M generated-group guard')
   new=tuple(g[h[i]]for i in range(17))
   if new not in group:group.add(new);queue.append(new)
 Q=15;maps={}
 for g in sorted(group):maps.setdefault(image(Q,g),g)
 full={mask(q)for q in combinations(range(17),4)};contained={mask(q)for B in D for q in combinations(pts(B),4)};domain=full-contained
 need(set(maps)==domain,'entire2040 original noncontainedQ cover')
 for q,g in maps.items():need({image(B,g)for B in D}==ds and image(Q,g)==q,'every selected fullD transport')
 forms=json.loads((args.work/'NORMAL_FORMS.json').read_text())['words'];formset={tuple(c)for c in forms};stabilizer=[g for g in group if image(Q,g)==Q];remaining=set(formset);orbits=[]
 while remaining:
  code=min(remaining);orb={tuple(sorted(image(w,g+(17,))for w in code))for g in stabilizer}
  need(orb<=formset,'normal-form image outside complete census');orbits.append(sorted(orb));remaining-=orb
 coverraw=canon([[q,list(g)]for q,g in sorted(maps.items())]);(args.work/'point-maps.json').write_bytes(coverraw)
 print(json.dumps({'complete':True,'field_polynomial':19,'literal_subfield':sub,'canonical_parent_blocks':len(cb),'canonical_to_literal_points':perm,'isomorphism_search_nodes':visits,'generated_group_size':len(group),'group_generation_steps':steps,'noncontainedQ_domain':len(domain),'selected_wholeD_maps':len(maps),'wholeD_images_checked':68*len(maps),'entire_selected_maps_sha256':hashlib.sha256(coverraw).hexdigest(),'Q_stabilizer_size':len(stabilizer),'generated_Q_stabilizer_normal_form_orbit_sizes':sorted(map(len,orbits)),'all_automorphisms_claimed':False,'author_maps_imported':False},sort_keys=True))
if __name__=='__main__':main()
