import json
from pathlib import Path
from collections import Counter
from math import comb
from projective import points,lines,hyperplanes,normalize

data=json.loads(Path(__file__).with_name('exceptional128.json').read_text())
rows=data['rows']; assert len(rows)==4 and all(len(r)==128 for r in rows)
counts=Counter(normalize(tuple(map(int,column))) for column in zip(*rows))
pts=points(4); K=[counts[p] for p in pts]
assert len(pts)==156 and Counter(K)=={0:80,1:40,2:20,3:16}
ls=lines(4); hs=hyperplanes(4)
assert len(ls)==806 and all(len(l)==6 for l in ls)
assert len(hs)==156 and all(len(h)==31 for h in hs)
assert all(sum(K[i] for i in l)%5==3 for l in ls)
assert Counter(sum(K[i] for i in h) for h in hs)=={18:20,23:80,28:16,33:40}
assert all(min(K[i] for i in h)==0 for h in hs)  # no full plane in the support
assert sum(K)%25!=18  # lifted strong (3 mod5) arcs have size18 modulo25
profiles=[]
for u in range(21):
 for v in range(40):
  w=18-u-v
  if w<0 or w>80:continue
  a={9:u,10:v,11:w,13:16,14:20-u,15:39-v,16:80-w}
  if sum(comb(m,2)*a[m] for m in a)==15768:profiles.append(a)
assert profiles==[{9:17,10:1,11:0,13:16,14:3,15:38,16:80}]
marked=[]
for i,k in enumerate(K):
 if k!=1:continue
 patterns=Counter(tuple(sorted((K[j] for j in l),reverse=True)) for l in ls if i in l)
 n=patterns[(2,1,0,0,0,0)]
 assert sum(patterns.values())==31 and n==6 and n<17
 marked.append({'point':pts[i],'A2_lines':n,'required_9_planes':17})
result={'exceptional_size':128,'plane_count_profile':profiles[0],'marked_points':marked,
 'all_marked_points_excluded':True,'reason':'17 required distinct A2 lines but exactly6 available at every marked1-point'}
print(json.dumps(result,indent=2))
