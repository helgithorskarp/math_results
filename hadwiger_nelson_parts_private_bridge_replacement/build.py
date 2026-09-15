from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,importlib.util,math,hashlib,datetime
import argparse
REPO=Path(__file__).resolve().parent.parent
HERE=None
D=(1,3,5,15,11,33,55,165)
def require(ok,msg):
 if not ok:raise ValueError(msg)
def mul(a,b):
 out=[0]*8
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:out[i^j]+=x*y*D[i&j]
 return out
def square(a):return mul(a,a)
def norm_twice(p,q):
 out=[0]*16
 for start in (0,16):
  a=[p[start+i]-q[start+i] for i in range(8)];b=[p[start+8+i]-q[start+8+i] for i in range(8)]
  aa=square(a);bb=square(b);ab=mul(a,b)
  for i in range(8):out[i]+=2*aa[i]+4*bb[i];out[8+i]+=4*ab[i];out[i^1]-=bb[i]*(3 if i&1 else 1)
 return tuple(out)
def unit(p,q,scale):return norm_twice(p,q)==(2*scale*scale,)+(0,)*15
def digest(x):return hashlib.sha256((json.dumps(x,separators=(',',':'))+'\n').encode()).hexdigest()

def build():
 path=REPO/'hadwiger_nelson_moser_palette_private_bridge/produce.py'
 spec=importlib.util.spec_from_file_location('bridge',path);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
 bridge,mp,bedges,be=b.geometry()
 # Embed s^a*t^b*y^c into sqrt3^a*sqrt5^d*sqrt11^b*y^c.
 def embed(v):
  out=[F(0)]*16
  for i,x in enumerate(v):out[(i&1)+((i&2)<<1)+((i&4)<<1)]=x
  return tuple(out)
 Q=[embed(x)+embed(y) for x,y in bridge]
 table=REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv'
 rows=[tuple(map(int,l.split())) for l in table.read_text().splitlines() if not l.startswith('#')]
 P=[tuple(F(x,96) for x in v[:8])+(F(0),)*8+tuple(F(x,96) for x in v[8:])+(F(0),)*8 for v in rows]
 sc=math.lcm(*(x.denominator for p in P+Q for x in p))
 P=[tuple(int(sc*x) for x in p) for p in P];Q=[tuple(int(sc*x) for x in p) for p in Q]
 new=sorted(set(Q)-set(P));union=P+new;protected={P.index(p) for p in Q if p in P}
 edges=[(i,j) for i,j in combinations(range(len(union)),2) if unit(union[i],union[j],sc)]
 adj=[set() for p in union]
 for i,j in edges:adj[i].add(j);adj[j].add(i)
 C=set.union(*(adj[i]&set(range(509)) for i in range(509,len(union)))) if new else set()
 # One deterministic cut. Contact coverage is a selector, not a chromatic claim.
 alive=set(range(509));delete=[];history=[]
 for step in range(len(new)+1):
  def key(v):
   a=adj[v]&alive;return (-F(len(a&C),max(1,len(a))),len(a),v)
  v=min(alive-protected,key=key);a=adj[v]&alive
  history.append({'vertex':v,'covered_neighbors':len(a&C),'remaining_original_degree':len(a)})
  delete.append(v);alive.remove(v)
 kept=sorted(alive)+list(range(509,len(union)));index={v:i for i,v in enumerate(kept)}
 points=[union[i] for i in kept];target_edges=[(index[i],index[j]) for i,j in edges if i in index and j in index]
 require(len(points)==508,'cap');require(len(set(points))==508,'collision merge')
 require(all(p in points for p in Q),'whole bridge retained')
 require(len([(i,j) for i,j in combinations(range(19),2) if unit(Q[i],Q[j],sc)])==34,'bridge geometry')
 summary={'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scale':sc,'parent_points':509,'bridge_points':19,'shared_points':len(protected),'shared_parent_labels':sorted(protected),'new_points':len(new),'new_points_outside_parent_field':sum(any(p[8:16]+p[24:32]) for p in new),'union_points':len(union),'union_edges':len(edges),'new_point_degrees':[len(adj[509+i]) for i in range(len(new))],'old_vertices_receiving_new_contacts':sorted(C),'deleted_parent_labels':delete,'selection_history':history,'support_points':len(points),'support_edges':len(target_edges),'support_point_sha256':digest(points),'support_edge_sha256':digest(target_edges),'record_candidate':False,'new_non_four_signal':False,'ordinary_colour_queries_before_freeze':0}
 data={'scale':sc,'points':points,'edges':target_edges,'parent_to_support':{str(v):index[v] for v in alive},'bridge_to_support':[points.index(p) for p in Q],'deleted':delete,'union_points':union,'union_edges':edges}
 (HERE/'frozen_support.json').write_text(json.dumps(data,separators=(',',':'))+'\n');(HERE/'frozen_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 require(not a.out.exists(),'output directory exists');a.out.mkdir(parents=True);HERE=a.out
 manifest=json.loads((Path(__file__).resolve().parent/'inputs.json').read_text())
 for name,pin in manifest['input_sha256'].items():require(hashlib.sha256((REPO/name).read_bytes()).hexdigest()==pin,'input pin')
 build()
