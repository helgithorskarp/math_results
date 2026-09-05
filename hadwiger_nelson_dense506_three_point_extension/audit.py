"""No imports from the producer or its square-root implementation."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict,Counter
from itertools import combinations
from math import lcm,isqrt
import importlib.util,sys,json,time,resource
sys.dont_write_bytecode=True
import argparse
import common as C
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
w=a.work;repo=C.ROOT;R=C.reviewer()
source=repo/'hadwiger_nelson_nonmono159_214_lowden2'
H=R.build_host(R.read_source(source/'points159.tsv',159),R.read_source(source/'points214.tsv',214),-1)
colors=C.colors()
rows=json.loads((w/'lengths.json').read_text());pts=json.loads((w/'points.json').read_text());certificate=json.loads((w/'nonsquare_certificate.json').read_text());tri=json.loads((w/'triangles.json').read_text())
def real(a):
 a=tuple(map(Q,a));return a[0],a[1],0,0,-a[2],-a[3],0,0

def normal(a,den):
 dd=lcm(*(Q(x,den).denominator for x in a));n=tuple(int(Q(x,den)*dd) for x in a);b=R.normalize(n,dd)
 # conjugate back to plus for canonical comparison to producer rows.
 b=(b[0],)+R.sigma(b[1:]);return b[0],b[1],b[2],b[5],b[6],b[3],b[4],b[7],b[8]

def prime(p):return p>=2 and not any(p%d==0 for d in range(2,isqrt(p)+1))
for p,z,r in certificate['maps']:
 assert prime(p) and p%2 and p%3 and p%11
 assert z*z%p==33%p and r*r%p==(-408+72*z)%p
exclusions=dict(certificate['rows']);assert len(exclusions)==len(certificate['rows'])
assert set(exclusions)=={i for i,row in enumerate(rows) if row['root'] is None}
pairdict={};raw_norms={};edge_count=0;t=time.perf_counter()
for a,b in combinations(range(506),2):
 n=R.norm(R.sub(H[b],H[a]))
 if n==R.scale(R.ONE,R.D**2):assert colors[a]!=colors[b];edge_count+=1
 if colors[a]!=colors[b]:raw_norms[a,b]=n
assert edge_count==2389 and len(raw_norms)==96003
rebuilt=defaultdict(set);alpha=(0,0,1,0,0,0,0,0);square_count=0
for i,row in enumerate(rows):
 d=real(row['distance']);q=real(row['q'])
 assert R.multiply(R.scale(d,3),q)==R.sub(R.scale(R.ONE,4*R.D**2),d)
 for pair in row['pairs']:
  pair=tuple(pair);assert pair not in pairdict and pair in raw_norms
  assert d==raw_norms[pair];pairdict[pair]=i
 if row['root'] is None:
  p,z,r=certificate['maps'][exclusions[i]]
  # q is from the minus host: evaluate r -> -r to audit its stated plus-image witness.
  r=(-r)%p
  assert all(Q(a).denominator%p for a in q)
  qq=[Q(a).numerator*pow(Q(a).denominator,-1,p)%p for a in q]
  value=(qq[0]+z*qq[1]+r*qq[4]+z*r*qq[5])%p
  assert pow(value,(p-1)//2,p)==p-1
  continue
 b=real(row['root']);assert R.multiply(b,b)==q;square_count+=1
 for a,c in row['pairs']:
  offset=R.multiply(R.multiply(alpha,R.sub(H[c],H[a])),b);mid=R.add(H[a],H[c])
  for e in [-1,1] if b!=R.ZERO else [1]:
   key=normal(R.add(mid,R.scale(offset,e)),2*R.D);rebuilt[key].add((a,c))
assert set(pairdict)==set(raw_norms)
assert len(pts)==len(rebuilt) and [tuple(row['point']) for row in pts]==sorted(rebuilt)
assert all(set(map(tuple,row['pairs']))==rebuilt[tuple(row['point'])] for row in pts)
# Complete independent host-neighbour scan, no reliance on old C3 table.
rr=[(R.sigma(R.decode_candidate(row['point'])[0]),row['point'][0]) for row in pts]
mh=[R.modular_point((h,R.D)) for h in H];mp=[R.modular_point(a) for a in rr]
hdict={R.normalize(h,R.D) for h in H};new_groups=defaultdict(list);kinds=Counter();host_tests=0;incidences=0
for i,row in enumerate(pts):
 nn=[]
 for j in range(506):
  if R.maybe_unit(mp[i],mh[j]):
   host_tests+=1
   if R.unit_pair(rr[i],(H[j],R.D)):nn.append(j)
 assert row['neighbors_from_pairs']==nn
 pair_nn=[(a,b) for a,b in combinations(nn,2) if colors[a]!=colors[b]]
 assert set(pair_nn)==rebuilt[tuple(row['point'])]
 ishost=(rr[i][1],)+rr[i][0] in hdict
 kind='host' if ishost else 'C3' if len(nn)>=3 else 'new';assert kind==row['kind']
 mask=sum(1<<c for c in set(colors[j] for j in nn));assert mask==row['host_color_mask']
 if kind=='new':assert len(nn)==2;new_groups[mask].append(i)
 kinds[kind]+=1;incidences+=len(nn)
# Geometric triangle audit via exact 60-degree rotation of every pair, not graph intersection.
# Test all candidate pairs directly against the hash table of the two possible equilateral thirds.
triangle_counts={};rotated_lookups=0
for mask,ids in sorted(new_groups.items()):
 lookup={normal(rr[i][0],rr[i][1]):i for i in ids};edges=[];hits=[]
 for ii,jj in combinations(ids,2):
  if not R.maybe_unit(mp[ii],mp[jj]):continue
  if not R.unit_pair(rr[ii],rr[jj]):continue
  edges.append((ii,jj));(a,da),(b,db)=rr[ii],rr[jj]
  mid=R.add(R.scale(a,db),R.scale(b,da));offset=R.multiply(alpha,R.sub(R.scale(b,da),R.scale(a,db)))
  for e in [-1,1]:
   rotated_lookups+=1;key=normal(R.add(mid,R.scale(offset,e)),2*da*db)
   if key in lookup:hits.append((ii,jj,lookup[key]))
 source_row=next(row for row in tri if row['mask']==mask)
 assert source_row['edges']==[list(e) for e in edges]
 assert not hits and not source_row['triangles'];triangle_counts[mask]=0
out={'host_root':-1,'host_pairs_checked':len(pairdict),'host_edges':edge_count,'distance_rows':len(rows),'exact_square_roots':square_count,'finite_field_nonsquare_witnesses':len(exclusions),'finite_field_maps':len(certificate['maps']),'points_rebuilt_entrywise':len(rebuilt),'complete_host_point_pairs':len(rr)*506,'exact_host_point_tests':host_tests,'host_point_incidences':incidences,'kinds':dict(kinds),'same_palette_edges':sum(len(row['edges']) for row in tri),'rotated_third_lookups':rotated_lookups,'triangles':triangle_counts,'finite_field_prime_checks':True}
C.write(w/'measurements_audit.json',{'seconds':time.perf_counter()-t,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
(w/'audit_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
