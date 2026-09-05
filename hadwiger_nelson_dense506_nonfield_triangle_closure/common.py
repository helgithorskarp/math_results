"""Pinned plus-host geometry and canonical input generation."""
from pathlib import Path
from hashlib import sha256
from collections import defaultdict
from itertools import combinations
import importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SOURCE=ROOT/'hadwiger_nelson_dense506_two_point_extension/geometry.py'
if sha256(SOURCE.read_bytes()).hexdigest()!='ce68ab6130082828fbd4e709586ae9dd53273c41e0cb4bfe3aad0278d08faddd':raise ValueError('geometry source pin')
spec=importlib.util.spec_from_file_location('prior_geometry',SOURCE)
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
def require(x,message):
 if not x:raise AssertionError(message)
def file_hash(path):
 h=sha256()
 with path.open('rb') as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
def load():
 raw=(SOURCE.parent/'host_colors.txt').read_bytes()
 require(sha256(raw).hexdigest()=='010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4','colour source pin')
 colors=list(map(int,raw.decode().strip()));host=G.host()
 require(len(colors)==len(host)==506,'host size')
 edges=G.distances(host)[2];require(all(colors[i]!=colors[j] for i,j in edges),'fixed host colouring')
 groups=defaultdict(lambda:defaultdict(list))
 for i,j in combinations(range(506),2):
  if colors[i]==colors[j]:continue
  x,y=host[i];X,Y=host[j]
  groups[tuple(sorted((colors[i],colors[j])))][G.add(x,X)+G.add(y,Y)].append((i,j))
 rows=[(pal,sorted(g.items())) for pal,g in sorted(groups.items())]
 return host,rows

def write_inputs(work):
 host,groups=load();p,z,r=10007,283,6718
 require(z*z%p==33 and r*r%p==(-408+72*z)%p,'invalid modular roots')
 (work/'groups.json').write_text(json.dumps(groups,separators=(',',':'))+'\n')
 with (work/'midpoints.txt').open('w') as f:
  f.write(str(len(groups))+'\n')
  for _,rows in groups:
   f.write(str(len(rows))+'\n')
   for m,_ in rows:f.write(' '.join(map(str,m))+'\n')
 mp=lambda a:G.embedding(p,z,r,a)
 mh=[(mp(x),mp(y)) for x,y in host]
 with (work/'screen_input.txt').open('w') as f:
  f.write(f'{p} {(2*G.D)**2%p} {len(groups)}\n')
  for _,rows in groups:
   f.write(str(len(rows))+'\n')
   for m,pairs in rows:
    f.write(f'{mp(m[:4])} {mp(m[4:])} {len(pairs)}\n')
    for a,b in pairs:f.write(f'{a} {b} {2*(mh[b][0]-mh[a][0])%p} {2*(mh[b][1]-mh[a][1])%p}\n')
 return {'host_pairs':sum(len(ps) for _,rs in groups for _,ps in rs),
         'midpoints_per_palette':[len(rs) for _,rs in groups],
         'maximum_midpoint_coefficient':max(abs(a) for _,rs in groups for m,_ in rs for a in m),
         'groups_sha256':G.digest(groups),
         'midpoints_sha256':file_hash(work/'midpoints.txt'),
         'screen_input_sha256':file_hash(work/'screen_input.txt')}
