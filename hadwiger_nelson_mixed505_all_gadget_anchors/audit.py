from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
from hashlib import sha256
from itertools import permutations
import importlib.util,json,struct,time,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
P=ROOT/'hadwiger_nelson_nonmono159_moser_triple/verify.py'
if sha256(P.read_bytes()).hexdigest()!='34d251f7e7c2a7d6c4542e260cbab6c9a390373f0eb7073800d70cdba6b271cb':raise ValueError('reference implementation pin mismatch')
spec=importlib.util.spec_from_file_location('reference',P);T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T)
K=T.K

def construction():
 _,B,_,EB=T.construction()
 raw=(ROOT/'hadwiger_nelson_nonmono159_214_lowden2/points214.tsv').read_bytes()
 T.require(sha256(raw).hexdigest()=='97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f','wrong V bytes')
 V=[]
 for s in raw.decode().splitlines():
  if not s or s.startswith('#'):continue
  a=tuple(map(int,s.split()));T.require(len(a)==16 and not any(a[i] for i in range(16) if i not in (0,5,9,12)),'unsupported coordinates')
  V.append(K.element(*(F(a[i],12) for i in (0,5,9,12))))
 T.require(len(V)==len(set(V))==214,'wrong V size')
 EV=T.C.internal_edges(V);T.require(len(EV)==977,'wrong V edges')
 dd=defaultdict(list)
 for q,a in enumerate(V):
  for v,b in enumerate(V):
   if q!=v:dd[K.add(b,K.negate(a))].append((q,v))
 D=[K.ZERO]+sorted(dd);inc=[[]]+[dd[d] for d in D[1:]]
 T.require(len(D)==4419,'wrong difference set')
 T.require(set(map(K.conjugate,V))==set(V),'V is not conjugation-invariant')
 return B,V,D,inc,EB,EV

class Classification:
 def __init__(self):self.h=sha256()
 def update(self,data):
  T.require(data.startswith(b'0:'),'unexpected orientation prefix')
  self.h.update(data[2:])

def main():
 B,V,D,inc,EB,EV=construction()
 libB,_=T.read_library('colors_B.txt',B,EB)
 libV,_=T.read_library(ROOT/'hadwiger_nelson_mixed505_anchor0/colors_H.txt',V,EV)
 print('rational construction ready',file=sys.stderr,flush=True)
 ch=Classification();start=time.monotonic();counts,groups=T.enumerate_classes(B,D,False,ch)
 print('rational census complete',time.monotonic()-start,'seconds',file=sys.stderr,flush=True)
 partition,coverage=sha256(),sha256();perms=[(0,)+p for p in permutations((1,2,3))]
 choices=[(i,j,k) for i in range(len(libB)) for j in range(len(libV)) for k in range(6)]
 hist=[Counter() for _ in V];total=0
 for gi,ee in enumerate(sorted(groups.values())):
  partition.update((';'.join(f'{b},{d}' for b,d in ee)+'\n').encode())
  projected=defaultdict(list)
  for b,d in ee:
   for q,v in inc[d]:projected[q].append((b,v))
  for q,qe in sorted(projected.items()):
   hist[q][len(qe)]+=1;total+=1
   w=next((r for r,(i,j,k) in enumerate(choices) if all(libB[i][b]!=perms[k][libV[j][v]^libV[j][q]] for b,v in qe)),None)
   T.require(w is not None,'uncovered rational class')
   coverage.update(struct.pack('<IIi',gi,q,w))
  if gi and gi%50000==0:print('rational projections',gi,file=sys.stderr,flush=True)
 result={'B_vertices':len(B),'V_vertices':len(V),'difference_vectors':len(D)-1,'nonzero_pairs':counts.pop('nonzero_pairs'),'pairs':counts,'ambient_classes':len(groups),'classification_sha256':ch.h.hexdigest(),'ambient_edge_partition_sha256':partition.hexdigest(),'coverage_sha256':coverage.hexdigest(),'anchor_classes_total':total,'maximum_cross_edges':max(max(h) for h in hist),'uncovered_total':0,'anchors':[{'anchor':q,'classes':sum(h.values()),'unit_multipliers':2*sum(h.values()),'histogram':dict(sorted(h.items())),'uncovered':0} for q,h in enumerate(hist)]}
 expected=json.loads((HERE/'screen.json').read_text())
 T.require(json.loads(json.dumps(result))==expected,'full audit differs from integer census')
 print(json.dumps({'full_result_match':True,'classification_sha256':ch.h.hexdigest(),'ambient_edge_partition_sha256':partition.hexdigest(),'coverage_sha256':coverage.hexdigest(),'ambient_classes':len(groups),'anchor_classes_total':total,'uncovered_total':0},indent=2))

if __name__=='__main__':main()
