#!/usr/bin/env python3
"""Verify one exact period-two lattice quotient and its ordinary four-colouring."""
import argparse,hashlib,json
from pathlib import Path
from itertools import combinations
from math import gcd,isqrt
HERE=Path(__file__).resolve().parent
RAD=(1,3,5,15,11,33,55,165)
TERMS=[(i,j,RAD.index(RAD[i]*RAD[j]//gcd(RAD[i],RAD[j])**2),2*gcd(RAD[i],RAD[j])) for i in range(8) for j in range(i+1,8)]
def require(ok,msg):
 if not ok:raise ValueError(msg)
def sign128(a):
 if not any(a):return 0
 scale=1<<128;lo=hi=0
 for c,d in zip(a,RAD):
  t=isqrt(d*scale*scale);u=t+(t*t!=d*scale*scale)
  lo+=c*(t if c>=0 else u);hi+=c*(u if c>=0 else t)
 require(lo>0 or hi<0,'unresolved rigorous field sign')
 return 1 if lo>0 else -1
def norm(p,q):
 x=[a-b for a,b in zip(p[:8],q[:8])];y=[a-b for a,b in zip(p[8:],q[8:])]
 out=[sum(d*(a*a+b*b) for d,a,b in zip(RAD,x,y))]+[0]*7
 for i,j,k,c in TERMS:out[k]+=c*(x[i]*x[j]+y[i]*y[j])
 return out
def edges(rows):return [[i,j] for i,j in combinations(range(len(rows)),2) if norm(rows[i],rows[j])==[96**2]+[0]*7]
def root3(a):
 out=[0]*8
 for i,c in enumerate(a):out[i^1]+=c*(3 if i&1 else 1)
 return out
def inside(a):
 # a/288 lies in [-1,1), with both boundary conventions checked exactly.
 lo=list(a);lo[0]+=288;hi=list(a);hi[0]-=288
 return sign128(lo)>=0 and sign128(hi)<0
def run(emit=None):
 cert=json.loads((HERE/'certificate.json').read_text());raw=(HERE/'seed_points.tsv').read_bytes()
 require(hashlib.sha256(raw).hexdigest()==cert['source_points_sha256'],'source bytes')
 rows=[tuple(map(int,l.split())) for l in raw.decode().splitlines() if l and not l.startswith('#')]
 require(len(rows)==len(set(rows))==509 and all(len(r)==16 for r in rows),'input shape and distinctness')
 require(hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()==cert['canonical_source_rows_sha256']=='db7abc5818aee6729675838cefd92e12589f695bea9970425b62b9ee27afbae8','published positive-parent coordinate identity')
 shifts=cert['shifts'];require(len(shifts)==509,'one translation per source point')
 images=[];classes=[];image_of=[];lookup={}
 for i,(p,shift) in enumerate(zip(rows,shifts)):
  require(len(shift)==2 and all(type(v) is int for v in shift),'integral lattice translation')
  m,n=shift;q=list(p);q[0]-=96*(2*m+n);q[9]-=96*n;q=tuple(q)
  ry=root3(q[8:]);s=[3*x-y for x,y in zip(q[:8],ry)];t=[2*y for y in ry]
  require(inside(s) and inside(t),'translated representative outside frozen fundamental domain')
  if q not in lookup:lookup[q]=len(images);images.append(q);classes.append([])
  j=lookup[q];classes[j].append(i);image_of.append(j)
 # A translation by2m+2n*omega changes the two lattice coordinates by2m,2n.
 # The half-open domain therefore proves uniqueness of each supplied representative.
 old=edges(rows);es=edges(images);unit=set(map(tuple,es));require(len(old)==2447,'complete parent unit graph')
 word=cert['four_word'];require(len(word)==len(images) and set(word)<=set('0123'),'ordinary word domain')
 require(all(word[a]!=word[b] for a,b in es),'proper word on every physical edge')
 require(len(images)<=508,'physical cap')
 plus=(96,)+(0,)*15;minus=(-96,)+(0,)*15
 require(plus in rows and minus in rows and image_of[rows.index(plus)]==image_of[rows.index(minus)],'prescribed +/-1 cap collision')
 mapped={tuple(sorted((image_of[a],image_of[b]))) for a,b in old}
 retained=sum(tuple(sorted((image_of[a],image_of[b]))) in unit for a,b in old)
 adj=[set() for _ in images]
 for a,b in es:adj[a].add(b);adj[b].add(a)
 remain=set(range(len(images)));degen=0
 while remain:
  v=min(remain,key=lambda x:(len(adj[x]&remain),x));degen=max(degen,len(adj[v]&remain));remain.remove(v)
 hist={str(k):sum(len(c)==k for c in classes) for k in sorted({len(c) for c in classes if len(c)>1})}
 out=dict(parent_points=509,parent_edges=2447,points=len(images),unit_edges=len(es),translation_cells=[list(x) for x in sorted({tuple(x) for x in shifts})],moved_points=sum(x!=[0,0] for x in shifts),source_edges_retained=retained,new_unit_pairs_without_source_edge=len(unit-mapped),source_adjacent_collisions=sum(image_of[a]==image_of[b] for a,b in old),minimum_degree=min(map(len,adj)),maximum_degree=max(map(len,adj)),degeneracy=degen,points_outside_parent=sum(q not in set(rows) for q in images),positive_parent_plus_minus_indices=[rows.index(plus),rows.index(minus)],point_reduction=509-len(images),collision_size_histogram=hist,colliding_source_labels=sum(len(c) for c in classes if len(c)>1),original_edges_lost=2447-retained,unique_inherited_unit_pairs=len(unit&mapped),proper_four_word_checked=True,record_candidate=False)
 require(out==json.loads((HERE/'expected.json').read_text()),'expected exact output')
 if emit:
  emit.mkdir(parents=True,exist_ok=True);(emit/'geometry.json').write_text(json.dumps(dict(points=images,denominator=96,edges=es,image_of=image_of,classes=classes),separators=(',',':'))+'\n')
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--emit',type=Path);args=ap.parse_args();print(json.dumps(run(args.emit),indent=2))
