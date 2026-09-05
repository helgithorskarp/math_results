#!/usr/bin/env python3
"""Independent rational monic-polynomial census and direct colour-permutation audit."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from itertools import permutations
from collections import defaultdict,Counter
import importlib.util,json,struct,time,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
P=ROOT/'hadwiger_nelson_nonmono159_moser_triple/verify.py'
if sha256(P.read_bytes()).hexdigest()!='34d251f7e7c2a7d6c4542e260cbab6c9a390373f0eb7073800d70cdba6b271cb':raise ValueError('rational dependency mismatch')
s=importlib.util.spec_from_file_location('rational_reduction',P);T=importlib.util.module_from_spec(s);s.loader.exec_module(T);K=T.K

def construction():
 A=T.C.points();t=K.element(F(5,12),F(1,12),F(5,12),F(-1,12))
 B=list(dict.fromkeys(A+[K.add(K.conjugate(a),t) for a in A]));EB=T.C.internal_edges(B)
 raw=(ROOT/'hadwiger_nelson_nonmono159_214_lowden2/points214.tsv').read_bytes()
 T.require(sha256(raw).hexdigest()=='97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f','wrong V bytes')
 V=[]
 for line in raw.decode().splitlines():
  if not line or line.startswith('#'):continue
  a=tuple(map(int,line.split()));T.require(len(a)==16 and not any(a[i] for i in range(16) if i not in (0,5,9,12)),'wrong source basis')
  V.append(K.element(*(F(a[i],12) for i in (0,5,9,12))))
 EV=T.C.internal_edges(V)
 T.require((len(B),len(EB),len(V),len(EV))==(293,1389,214,977),'wrong geometry')
 T.require(len(set(V))==214 and set(map(K.conjugate,V))==set(V),'bad reflection reduction')
 dd=defaultdict(list)
 for q,a in enumerate(V):
  for v,b in enumerate(V):
   if q!=v:dd[K.add(b,K.negate(a))].append((q,v))
 D=[K.ZERO]+sorted(dd);inc=[[]]+[dd[d] for d in D[1:]]
 T.require(len(D)==4419,'wrong difference census')
 return B,V,D,inc,EB,EV

class Classification:
 def __init__(self):self.h=sha256()
 def update(self,data):
  T.require(data.startswith(b'0:'),'unexpected orientation prefix');self.h.update(data[2:])

def finish(B,V,D,inc,EB,EV,counts,groups,ch):
 lb,_=T.read_library(HERE/'colors_B.txt',B,EB);lv,_=T.read_library(HERE/'colors_V.txt',V,EV)
 partition,coverage=sha256(),sha256();perms=[(0,)+p for p in permutations((1,2,3))]
 choices=[(i,j,k) for i in range(len(lb)) for j in range(len(lv)) for k in range(6)]
 hist=[Counter() for _ in V];total=0
 for gi,ee in enumerate(sorted(groups.values())):
  partition.update((';'.join(f'{b},{d}' for b,d in ee)+'\n').encode())
  projected=defaultdict(list)
  for b,d in ee:
   for q,v in inc[d]:projected[q].append((b,v))
  for q,qe in sorted(projected.items()):
   w=next((r for r,(i,j,k) in enumerate(choices) if all(lb[i][b]!=perms[k][lv[j][v]^lv[j][q]] for b,v in qe)),None)
   T.require(w is not None,'uncovered rational class')
   hist[q][len(qe)]+=1;total+=1;coverage.update(struct.pack('<IIi',gi,q,w))
  if gi and gi%100000==0:print('audited classes',gi,file=sys.stderr,flush=True)
 table=['anchor\tclasses\tunit_multipliers\tmax_cross_edges\tuncovered\thistogram\n']
 for q,h in enumerate(hist):
  table.append(f'{q}\t{sum(h.values())}\t{2*sum(h.values())}\t{max(h)}\t0\t'+json.dumps(dict(sorted(h.items())),separators=(',',':'))+'\n')
 result={'B_vertices':293,'B_edges':1389,'V_vertices':214,'V_edges':977,'inner_overlap':25,'origin_degree':30,'B_library_size':len(lb),'V_library_size':len(lv),'difference_vectors':len(D)-1,'nonzero_pairs':counts.pop('nonzero_pairs'),'pairs':counts,'ambient_classes':len(groups),'classification_sha256':ch,'ambient_edge_partition_sha256':partition.hexdigest(),'coverage_sha256':coverage.hexdigest(),'anchor_classes_total':total,'maximum_cross_edges':max(max(h) for h in hist),'uncovered_total':0,'anchor_table_sha256':sha256(''.join(table).encode()).hexdigest()}
 degrees=Counter(v for e in EB for v in e)
 T.require(degrees[0]==30 and max(degrees[v] for v in range(1,293))==29,'degree claim failed')
 T.require(json.loads(json.dumps(result))==json.loads((HERE/'expected.json').read_text()),'full rational result differs')
 return {'full_result_match':True,'classification_sha256':ch,'ambient_edge_partition_sha256':partition.hexdigest(),'coverage_sha256':coverage.hexdigest(),'ambient_classes':len(groups),'anchor_classes_total':total,'uncovered_total':0}

def main():
 B,V,D,inc,EB,EV=construction();ch=Classification();start=time.monotonic()
 counts,groups=T.enumerate_classes(B,D,False,ch)
 print('rational census seconds',time.monotonic()-start,file=sys.stderr,flush=True)
 print(json.dumps(finish(B,V,D,inc,EB,EV,counts,groups,ch.h.hexdigest()),indent=2))
if __name__=='__main__':main()
