"""Independent exact geometry and direct Hall-certificate checker.

Imports no producer, matching routine, geometry.py or SAT package.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import gcd
from pathlib import Path
from collections import Counter
import argparse,json
HERE=Path(__file__).resolve().parent;REPO=HERE.parent
BASIS=(1,3,5,15,11,33,55,165)
NAMES=(
 'hadwiger_nelson_parts509_edge_criticality/reduced_edges.json',
 'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json',
 'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json',
 'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json')
def require(ok,why):
 if not ok:raise ValueError(why)
def decode(row):
 require(len(row)==2 and all(len(a)==8 for a in row),'coordinate shape')
 result=[]
 for a in row:
  out={}
  for r,c in zip(BASIS,a):
   q=96*Fraction(c);require(q.denominator==1,'coordinate scale')
   if q:out[r]=int(q)
  result.append(out)
 return result
def norm(p,q):
 terms={}
 for a,b in zip(p,q):
  diff={r:a.get(r,0)-b.get(r,0) for r in a.keys()|b.keys()};items=[(r,c) for r,c in diff.items() if c]
  for r,c in items:terms[1]=terms.get(1,0)+r*c*c
  for (r,c),(s,d) in combinations(items,2):
   g=gcd(r,s);t=r*s//(g*g);terms[t]=terms.get(t,0)+2*c*d*g
 return {r:c for r,c in terms.items() if c}
def adjacency(n,edges):
 a=[set() for _ in range(n)]
 for u,v in edges:a[u].add(v);a[v].add(u)
 return a
def inputs():
 hashes=json.loads((HERE/'inputs.json').read_text());require(set(hashes)==set(NAMES),'input manifest keys')
 for name in NAMES:require(sha256((REPO/name).read_bytes()).hexdigest()==hashes[name],('input hash',name))
 data=[json.loads((REPO/name).read_text()) for name in NAMES]
 se=[tuple(x) for x in data[0]['edges']]
 require(se==sorted(set(se)) and len(se)==2259 and all(0<=u<v<509 for u,v in se),'source edges')
 sp=[decode(data[1]['coordinates'][str(v)]) for v in range(509)]
 ids=[v for v in sorted(map(int,data[2]['coordinates'])) if '510' in data[2]['provenance'][v]]
 rows=data[3];require([r['centre_index'] for r in rows]==sorted({r['centre_index'] for r in rows}),'fresh ordering')
 hp=[decode(data[2]['coordinates'][str(v)]) for v in ids]+[decode(r['coordinates']) for r in rows]
 canonical=lambda p:tuple(tuple(sorted(a.items())) for a in p)
 require(len({canonical(p) for p in sp})==509 and len(hp)==len({canonical(p) for p in hp})==632,'distinct source and host')
 for u,v in se:require(norm(sp[u],sp[v])=={1:9216},'source unit edge')
 he=[]
 for u in range(632):
  for v in range(u+1,632):
   if norm(hp[u],hp[v])=={1:9216}:he.append((u,v))
 require(len(he)==3112,'complete host unit edges')
 return se,he

def check_proof(sa,ha,cert):
 n=len(sa);m=len(ha)
 require(set(cert)=={'format','source_vertices','host_vertices','maximum_identifications','empty_source_vertex','removals'},'certificate keys')
 require(cert['format']=='one-collision-hall-v1' and cert['source_vertices']==n and cert['host_vertices']==m and type(cert['maximum_identifications']) is int and cert['maximum_identifications']==1,'certificate header')
 root=cert['empty_source_vertex'];require(type(root) is int and 0<=root<n,'root label')
 D=[{h for h in range(m) if len(ha[h])+1>=len(sa[v])} for v in range(n)];initial=sum(map(len,D));kinds=Counter();incidences=0
 require(type(cert['removals']) is list,'removal list')
 for rec in cert['removals']:
  require(type(rec) is list and len(rec)==4,'removal row')
  v,h,kind,A=rec
  require(type(v) is int and type(h) is int and 0<=v<n and 0<=h<m and h in D[v],'live candidate')
  require(type(A) is list and all(type(u) is int for u in A) and A==sorted(set(A)) and set(A)<=sa[v],'witness source neighbours')
  if kind=='A':
   require(len(A)==1 and not (D[A[0]]&ha[h]),'unsupported source edge')
  elif kind=='H':
   require(len(A)>=2,'Hall source set')
   B=set()
   for u in A:B.update(D[u]&ha[h]);incidences+=len(D[u]&ha[h])
   require(len(B)<=len(A)-2,'Hall deficiency at least two')
  else:raise ValueError('witness kind')
  D[v].remove(h);kinds[kind]+=1
 require(not D[root],'empty terminal domain')
 return {'verified':True,'initial_domain_values':initial,'checked_removals':sum(kinds.values()),'arc_removals':kinds['A'],'Hall_removals':kinds['H'],'empty_source_vertex':root,'Hall_union_incidences_checked':incidences,'no_homomorphism_with_at_least_source_order_minus_one_images':True}

def main(path):
 se,he=inputs();cert=json.loads(path.read_text());report=check_proof(adjacency(509,se),adjacency(632,he),cert)
 report.update({'source_vertices':509,'source_unit_edges':len(se),'host_vertices':632,'host_pairs_checked':199396,'host_unit_edges':len(he),'source_edge_sha256':sha256(''.join(f'{u} {v}\n' for u,v in se).encode()).hexdigest(),'host_edge_sha256':sha256(''.join(f'{u},{v}\n' for u,v in he).encode()).hexdigest(),'certificate_sha256':sha256(path.read_bytes()).hexdigest(),'certificate_bytes':path.stat().st_size,'excluded_image_orders':[508,509],'all_smaller_images_excluded':False,'record_improvement':False,'solver_required':False})
 print(json.dumps(report,sort_keys=True))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',required=True,type=Path);a=ap.parse_args();main(a.certificate)
