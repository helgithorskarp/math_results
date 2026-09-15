#!/usr/bin/env python3
"""Independent exact geometry and literal colouring checker; standard library only."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import gcd
import hashlib,json,argparse
HERE=Path(__file__).resolve().parent
B=(1,3,5,15,11,33,55,165)
def require(ok,msg):
 if not ok:raise ValueError(msg)
def digest(x):return hashlib.sha256((json.dumps(x,separators=(',',':'))+'\n').encode()).hexdigest()

def norm_twice(p,q):
 # Flat radical monomials: sqrt(d)*Y^e. Expand ordered products and then
 # reduce Y^2=2-sqrt3/2. Twice the norm has integral coefficients.
 out={}
 def put(key,c):out[key]=out.get(key,0)+c
 for start in (0,16):
  v=[(B[i%8],i//8,p[start+i]-q[start+i]) for i in range(16) if p[start+i]!=q[start+i]]
  for d,e,c in v:
   for f,h,k in v:
    a=gcd(d,f);rad=d*f//(a*a);coef=c*k*a;power=e+h
    if power==2:
     put((rad,0),4*coef);b=gcd(rad,3);put((rad*3//(b*b),0),-b*coef)
    else:put((rad,power),2*coef)
 return {key:c for key,c in out.items() if c}
def unit(p,q):return norm_twice(p,q)=={(1,0):2*96**2}

def load_points():
 pts=json.loads((HERE/'points.json').read_text())
 require(len(pts)==508 and all(len(p)==32 and all(type(x) is int for x in p) for p in pts),'point shape')
 require(len({tuple(p) for p in pts})==508,'distinct points')
 return pts

def provenance(pts):
 manifest=json.loads((HERE/'inputs.json').read_text());r=HERE.parent
 for name,pin in manifest['input_sha256'].items():require(hashlib.sha256((r/name).read_bytes()).hexdigest()==pin,'input pin '+name)
 raw=(r/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text()
 parent=[]
 for line in raw.splitlines():
  if line.startswith('#'):continue
  p=list(map(int,line.split()));parent.append(tuple(p[:8]+[0]*8+p[8:]+[0]*8))
 cert=json.loads((r/'hadwiger_nelson_moser_palette_private_bridge/certificate.json').read_text())
 # Named radical map from the source basis to this compositum. No source code imports.
 source_radicals=[(1,0),(3,0),(11,0),(33,0),(1,1),(3,1),(11,1),(33,1)]
 bridge=[]
 for point in cert['coordinates']:
  q=[]
  for coord in point:
   d={key:F(x)*96 for key,x in zip(source_radicals,coord)}
   values=[d.get((rad,e),0) for e in (0,1) for rad in B]
   require(all(F(x).denominator==1 for x in values),'source scale')
   q.extend(map(int,values))
  bridge.append(tuple(q))
 new=sorted(set(bridge)-set(parent));delete=set(manifest['deleted_parent_labels'])
 require(len(delete)==len(manifest['deleted_parent_labels'])==len(new)+1,'cut budget')
 require(all(type(v) is int and 0<=v<509 for v in delete),'cut labels')
 source=[p for i,p in enumerate(parent) if i not in delete]+new
 require(source==[tuple(p) for p in pts],'all source-to-support points')
 require([pts.index(list(p)) for p in bridge]==manifest['bridge_to_support'],'whole bridge support mapping')
 return parent,bridge,new

def check_word(path,pts,edges,k):
 word=path.read_text().strip();require(len(word)==len(pts) and all(c in '01234'[:k] for c in word),'colour domain')
 require(all(word[i]!=word[j] for i,j in edges),'physical edge colouring')
 return len(set(word))

def verify():
 pts=load_points();parent,bridge,new=provenance(pts)
 edges=[(i,j) for i,j in combinations(range(508),2) if unit(pts[i],pts[j])]
 four=check_word(HERE/'colour4.txt',pts,edges,4);five=check_word(HERE/'colour5.txt',pts,edges,5)
 require(five==5,'five colours actually used')
 bridge_edges=[(i,j) for i,j in combinations(range(19),2) if unit(bridge[i],bridge[j])]
 old={tuple(p) for p in parent}
 report={'all_checks':True,'points':508,'complete_edges':len(edges),'all_pairs_checked':128778,'source_points_compared_entrywise':True,'bridge_retained':19,'bridge_edges':len(bridge_edges),'bridge_parent_overlap':sum(p in old for p in bridge),'added_points':len(new),'removed_parent_points':len(new)+1,'added_outside_parent_field':sum(any(p[8:16]+p[24:32]) for p in new),'four_colouring_checked':True,'five_colouring_checked':True,'colours_used':[four,five],'edge_inequalities_checked':2*len(edges),'point_sha256':digest(pts),'edge_sha256':digest(edges),'ordinary_non_four_signal':False,'record_candidate':False}
 return report,edges

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--edges-out',type=Path);args=a.parse_args();result,edges=verify()
 expected=HERE/'expected.json'
 if expected.exists():require(result==json.loads(expected.read_text()),'expected result')
 if args.edges_out:args.edges_out.write_text(json.dumps(edges,separators=(',',':'))+'\n')
 print(json.dumps(result,sort_keys=True))
