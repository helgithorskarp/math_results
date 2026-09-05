#!/usr/bin/env python3
"""Exact radius-one circle-center census for the two mixed506 components."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter,defaultdict
from functools import cache
from hashlib import sha256
from math import isqrt,comb
import importlib.util,json,time,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
def module(name,path,pin):
 if sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('dependency hash mismatch')
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
F=module('inputs',ROOT/'hadwiger_nelson_mixed505_all_gadget_anchors/verify.py','526b12cbd9d28217e59feb7191c93ace4e5a572ebeadd66cdf384393126aee38')
K=module('field',ROOT/'hadwiger_nelson_nonmono_field_obstruction/coloring.py','a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e')

def ratroot(x):
 if x<0:return None
 a,b=isqrt(x.numerator),isqrt(x.denominator)
 return Q(a,b) if a*a==x.numerator and b*b==x.denominator else None

def sqrtR(x):
 a,b=x
 if b==0:
  r=ratroot(a)
  if r is not None:return (r,Q(0))
  r=ratroot(a/33)
  return None if r is None else (Q(0),r)
 n=ratroot(a*a-33*b*b)
 if n is None:return None
 for e in (-1,1):
  r=ratroot((a+e*n)/2)
  if r:
   z=(r,b/(2*r))
   assert K.multiply(K.element(*z),K.element(*z))==K.element(*x)
   return z
 return None

def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def norm(x):return K.multiply(x,K.conjugate(x))
def encode(p):return [str(x) for x in p]
def census(P,lib):
 assert len(P)==len(set(P)),'repeated input point'
 @cache
 def offsets(d):
  n=norm(d); n4=K.add(K.element(4),K.negate(n))
  if F.sign_real(*n4[:2])<0:return 'too_far',()
  w=K.multiply(n4,K.inverse(tuple(3*x for x in n)))
  r=sqrtR(w[:2])
  if r is None:return 'outside_E',()
  off=tuple(x/2 for x in K.multiply(K.multiply(d,K.element(0,0,1)),K.element(*r)))
  return 'in_E',((K.ZERO,) if off==K.ZERO else (off,K.negate(off)))
 hits=defaultdict(set);freq=Counter();counts=Counter()
 for i,a in enumerate(P):
  for j in range(i+1,len(P)):
   d=sub(P[j],a);case,oo=offsets(d);counts[case]+=1
   mid=tuple((x+y)/2 for x,y in zip(a,P[j]))
   for off in oo:
    p=K.add(mid,off);hits[p].update((i,j));freq[p]+=1
 result=[];degrees=Counter();outside=Counter(); saturation=0
 Pset=set(P)
 for p,ns in sorted(hits.items()):
  assert freq[p]==comb(len(ns),2)
  if len(ns)<3:continue
  assert all(norm(sub(p,P[i]))==K.ONE for i in ns)
  cc=K.color(p);assert all(K.color(P[i])!=cc for i in ns)
  masks=[15^sum(1<<c for c in set(row[i] for i in ns)) for row in lib]
  internal=p in Pset;degrees[len(ns)]+=1
  if not internal:
   outside[len(ns)]+=1;saturation+=not any(masks)
  result.append({'point':encode(p),'neighbors':sorted(ns),'internal':internal,'field_color':cc,'library_free_masks':masks})
 encoded=json.dumps(result,separators=(',',':'))+'\n'
 return {'vertices':len(P),'pairs':comb(len(P),2),'pair_classes':dict(counts),'distinct_pair_centers_in_E':len(hits),'centers_ge3':len(result),'degree_histogram':dict(sorted(degrees.items())),'external_centers_ge3':sum(outside.values()),'external_degree_histogram':dict(sorted(outside.items())),'external_centers_saturating_library':saturation,'center_incidence_sha256':sha256(encoded.encode()).hexdigest()},result

def controls():
 # Known circumradius-one triangle, a non-unit circumradius, and pair boundaries.
 P=[K.ONE,K.element(Q(-1,2),0,Q(1,2)),K.element(Q(-1,2),0,Q(-1,2))]
 stats,rows=census(P,[(0,1,2)])
 assert len(rows)==1 and rows[0]['point']==['0']*4 and rows[0]['neighbors']==[0,1,2]
 for d,case in [(Q(1,2),'outside_E'),(Q(2),'in_E'),(Q(3),'too_far')]:
  stats,rows=census([K.ZERO,K.element(d)],[(0,1)])
  assert stats['pair_classes']=={case:1} and rows==[]
 stats,rows=census([K.ZERO,K.ONE,K.element(Q(1,2),0,Q(1,2))],[(0,1,2)])
 assert rows==[]


def main():
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--catalog-dir',type=Path,help='write regenerable center/incidence catalogs outside the source tree')
 args=parser.parse_args()
 controls()
 if args.catalog_dir:args.catalog_dir.mkdir(parents=True,exist_ok=True)
 B,V,D,inc,EB,EV=F.construction();lb,lv=F.libraries(B,V,EB,EV)
 for side,lib,points,edges in [('B',lb,B,EB),('V',lv,V,EV)]:
  path=ROOT/f'hadwiger_nelson_mixed505_high_degree_attachments/new_{side}.txt'
  raw=path.read_bytes()
  pins={'B': '6951cfb9a8e7c1fc60857e4534aacff41bb2ecf73ac057a294fc288400567f99', 'V': 'f0653c47a7ea801145fb28b7fc11d045d09c5f1cad61cf4d4ffa7ee354258a9c'}
  assert sha256(raw).hexdigest()==pins[side]
  rows=[tuple(map(int,line)) for line in raw.decode().splitlines()]
  assert len(rows)==5
  assert all(len(c)==len(points) and all(x in range(4) for x in c) and all(c[i]!=c[j] for i,j in edges) for c in rows)
  lib.extend(rows)
 summaries={}
 for side,P,scale,lib in [('B',B,72,lb),('V',V,12,lv)]:
  PP=[tuple(Q(x,scale) for x in p) for p in P]
  summary,rows=census(PP,lib)
  summary['original_first_row_extends_at_every_external_center']=all(r['library_free_masks'][0] for r in rows if not r['internal'])
  summaries[side]=summary
  if args.catalog_dir:(args.catalog_dir/f'centers_{side}.json').write_text(json.dumps(rows,separators=(',',':'))+'\n')
 assert [summaries[k]['external_centers_ge3'] for k in ('B','V')]==[881,534]
 assert all(max(summaries[k]['external_degree_histogram'])==10 for k in ('B','V'))
 out={'components':summaries,'external_centers_total':1415,'labelled_hub_anchor_families':881*214+534*292,'max_hub_degree':10,'analytic_single_hub_lemma_required':True,'angular_families_not_enumerated':True,'controls_passed':True}
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
