#!/usr/bin/env python3
"""Complete field-valued host-pair circle intersections and list-triangle census."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter,defaultdict
from itertools import combinations
from math import isqrt
import argparse,sys,json,time,resource
sys.dont_write_bytecode=True
import common as C
import field as F
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
w=a.work;w.mkdir(parents=True,exist_ok=False);G=C.producer();started=time.perf_counter()
h=G.host();colors=C.colors()
t=time.perf_counter();ds={}
for i in range(506):
 for j in range(i+1,506):
  if colors[i]==colors[j]:continue
  d=G.norm(G.sub(h[i][0],h[j][0]),G.sub(h[i][1],h[j][1]))
  ds.setdefault(d,[]).append((i,j))

T=G.scale(G.ONE,4*G.D**2);rows=[];counts={}
t=time.perf_counter()
for d in sorted(ds):
 q=F.mul(F.sub(T,d),F.inv(F.scale(d,3)))
 r=F.sqrt4(q)
 kind='field' if r is not None else ('negative' if F.sign4(q)<0 else 'nonfield')
 counts[kind]=counts.get(kind,0)+len(ds[d])
 rows.append({'distance':d,'pairs':ds[d],'q':list(map(str,q)),'root':None if r is None else list(map(str,r)),'kind':kind})
(w/'lengths.json').write_text(json.dumps(rows,separators=(',',':'))+'\n')
# Producer-independent decision certificate: finite-field images for every nonsquare.
left={i:row for i,row in enumerate(rows) if row['root'] is None};cert={};maps=[]
for p in range(5,10000):
 if any(p%d==0 for d in range(2,1+isqrt(p))):continue
 squares={j*j%p:j for j in range(p)}
 if 33%p not in squares:continue
 z=squares[33%p]
 for z in sorted({z,p-z}):
  a=(-408+72*z)%p
  if a not in squares:continue
  r=squares[a]
  for r in sorted({r,p-r}):
   if not 0<z<p or not 0<r<p:continue
   mid=len(maps);maps.append((p,z,r));solved=[]
   for i,row in left.items():
    q=tuple(map(Q,row['q']))
    if any(a.denominator%p==0 for a in q):continue
    v=[a.numerator*pow(a.denominator,-1,p)%p for a in q]
    b=(v[0]+z*v[1]+r*v[2]+z*r*v[3])%p
    if pow(b,(p-1)//2,p)==p-1:cert[i]=mid;solved.append(i)
   for i in solved:del left[i]
 if not left:break

if left:raise AssertionError(list(left)[:20])
# Save only maps that were needed, canonically remap.
used=sorted(set(cert.values()));rename={old:new for new,old in enumerate(used)}
certificate={'maps':[maps[i] for i in used],'rows':[[i,rename[v]] for i,v in sorted(cert.items())]}
(w/'nonsquare_certificate.json').write_text(json.dumps(certificate,separators=(',',':'))+'\n')
points=defaultdict(set);t=time.perf_counter();endpoint_checks=0;tangent_pairs=0
for row in rows:
 if row['root'] is None:continue
 rt=tuple(map(Q,row['root']))
 for a,b in row['pairs']:
  x,y=h[a];X,Y=h[b];dx,dy=F.sub(X,x),F.sub(Y,y)
  ox=F.scale(F.mul(dy,rt),-3);oy=F.mul(dx,rt)
  if rt==F.Z:tangent_pairs+=1
  for e in [-1,1] if rt!=F.Z else [1]:
   key=G.canonical(F.add(F.add(x,X),F.scale(ox,e)),F.add(F.add(y,Y),F.scale(oy,e)),2*G.D)
   if not G.unit(key,G.canonical(x,y,G.D)) or not G.unit(key,G.canonical(X,Y,G.D)):raise AssertionError('endpoint')
   endpoint_checks+=2;points[key].add((a,b))
actual={G.canonical(x,y,G.D):i for i,(x,y) in enumerate(h)}
result=[];counts=Counter();palette=Counter()
for point,pairs in sorted(points.items()):
 neigh=sorted(set(x for pair in pairs for x in pair))
 kind='host' if point in actual else 'C3' if len(neigh)>=3 else 'new'
 if kind=='new' and len(neigh)!=2:raise AssertionError(('new has >=3 neighbours',point))
 mask=sum(1<<c for c in set(colors[i] for i in neigh))
 if kind=='new':palette[mask]+=1
 counts[kind]+=1
 result.append({'point':point,'pairs':sorted(pairs),'kind':kind,'neighbors_from_pairs':neigh,'host_color_mask':mask})
(w/'points.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
rows=json.loads((w/'points.json').read_text());groups=defaultdict(list)
for i,row in enumerate(rows):
 if row['kind']=='new':groups[row['host_color_mask']].append(i)
t=time.perf_counter();result=[]
for mask,inds in sorted(groups.items()):
 pts=[tuple(rows[i]['point']) for i in inds];mods=list(map(G.modpoint,pts));adj=[set() for _ in pts];edges=[];tests=0
 for i,j in combinations(range(len(pts)),2):
  if G.maybe(mods[i],mods[j]):
   tests+=1
   if G.unit(pts[i],pts[j]):adj[i].add(j);adj[j].add(i);edges.append((i,j))
 tris=[(inds[i],inds[j],inds[k]) for i,j in edges for k in sorted(adj[i]&adj[j]) if k>j]
 cc=[];seen=set()
 for i in range(len(pts)):
  if i in seen:continue
  todo=[i];seen.add(i);component=[]
  while todo:
   v=todo.pop();component.append(v)
   for u in adj[v]-seen:seen.add(u);todo.append(u)
  cc.append((len(component),sum(len(adj[v]) for v in component)//2))
 result.append({'mask':mask,'points':len(pts),'pairs':len(pts)*(len(pts)-1)//2,'modular_survivors':tests,'edges':[(inds[i],inds[j]) for i,j in edges],'triangles':tris,'component_sizes_edges':[[list(k),v] for k,v in sorted(Counter(cc).items())]})
C.write(w/'triangles.json',result)
summary={
 'status':'COMPLETE FIELD CENSUS; NO SAME-LIST UNIT TRIANGLE',
 'host_pairs':sum(len(x['pairs']) for x in json.loads((w/'lengths.json').read_text())),
 'distance_rows':len(json.loads((w/'lengths.json').read_text())),
 'square_distances':184,
 'field_points':len(rows),
 'point_kinds':dict(sorted(Counter(x['kind'] for x in rows).items())),
 'nonsquare_maps':certificate['maps'],
 'nonsquare_witnesses':len(certificate['rows']),
 'tangent_pairs':tangent_pairs,'endpoint_checks':endpoint_checks,
 'palette_graphs':[{'mask':x['mask'],'points':x['points'],'pairs':x['pairs'],'modular_survivors':x['modular_survivors'],'edges':len(x['edges']),'triangles':len(x['triangles'])} for x in result],
 'files':{n:{'bytes':(w/n).stat().st_size,'sha256':C.file_hash(w/n)} for n in ['lengths.json','nonsquare_certificate.json','points.json','triangles.json']}}
summary['square_distances']=sum(x['root'] is not None for x in json.loads((w/'lengths.json').read_text()))
if any(x['triangles'] for x in result):raise AssertionError('List triangle found; this is not a closure.')
C.write(w/'summary.json',summary)
C.write(w/'measurements_generate.json',{'seconds':time.perf_counter()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
print(json.dumps(summary,indent=2))
