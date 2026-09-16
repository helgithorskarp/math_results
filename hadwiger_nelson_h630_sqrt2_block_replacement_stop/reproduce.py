"""One frozen H630 block replacement, exact geometry before colouring."""
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import isqrt
import json,time
import argparse
PACKAGE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--repo',default=str(PACKAGE.parent));args=parser.parse_args()
W=Path(args.output).resolve();W.mkdir(parents=True,exist_ok=True)
R=Path(args.repo).resolve()
(W/'ARCHITECTURE.json').write_bytes((PACKAGE/'ARCHITECTURE.json').read_bytes())
OLD='hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json'
FRESH='hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json'
CERT='hadwiger_nelson_heule632_pair_pilot/certificate.json'
PINS={OLD:'bc8e0f5f5ec7fa5f2376cc77ba0e65f6023b340cf48990370d5eda575d30ae79',FRESH:'89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317',CERT:'fffa224298854425f7c40726a9dd96196b1c5e82b75ffa4d8c6c19fefbc8274f'}
RADOLD=(1,3,5,15,11,33,55,165);RAD=(1,2,3,6,11,22,33,66)
def need(b,s):
 if not b:raise ValueError(s)
def save(f,o):(W/f).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def point_bytes(P):return ''.join(','.join(map(str,p))+'\n' for p in P).encode()
def edge_bytes(E):return ''.join(f'{u},{v}\n' for u,v in E).encode()
def norm(p,q,rad=RAD):
 a=[0]*8
 for k in (0,8):
  d=[(i,p[k+i]-q[k+i]) for i in range(8) if p[k+i]!=q[k+i]]
  for i,x in d:
   for j,y in d:a[i^j]+=x*y*rad[i&j]
 return tuple(a)
def edges(P,rad=RAD):return [(u,v) for u,v in combinations(range(len(P)),2) if norm(P[u],P[v],rad)==(9216,0,0,0,0,0,0,0)]
def root3(a):
 out=[0]*8
 for i,c in enumerate(a):out[i^2]+=c*RAD[i&2]
 return out
def patch_point(m,n):
 qx=[48,0,0,-16,0,0,0,0];qy=[0,48,16,0,0,0,0,0];tx=root3(qx);ty=root3(qy)
 x=[((2*m+n)*a-n*b)//2 for a,b in zip(qx,ty)]
 y=[((2*m+n)*a+n*b)//2 for a,b in zip(qy,tx)]
 need(all(((2*m+n)*a-n*b)%2==0 for a,b in zip(qx,ty)) and all(((2*m+n)*a+n*b)%2==0 for a,b in zip(qy,tx)),'exact half')
 return tuple(x+y)
def source_box(P):
 S=10**6;bounds=[(isqrt(r*S*S),isqrt(r*S*S)+1) for r in RADOLD]
 lo=10**30;hi=-lo
 for p in P:
  for axis in (p[:8],p[8:]):
   l=sum(c*bounds[i][0 if c>=0 else 1] for i,c in enumerate(axis));h=sum(c*bounds[i][1 if c>=0 else 0] for i,c in enumerate(axis));lo=min(lo,l);hi=max(hi,h)
 need(lo>-3*96*S and hi<3*96*S,'strict source box')
 return {'scale':S,'lower_numerator':lo,'upper_numerator':hi,'coordinate_denominator':96*S,'box':'(-3,3)^2','diameter_squared_upper_bound':72}
def moser(n,E):
 adj=[set() for _ in range(n)]
 for u,v in E:adj[u].add(v);adj[v].add(u)
 for o in range(n):
  diamonds=[]
  for t in range(n):
   if t==o or t in adj[o]:continue
   pair=next(((a,b) for a,b in combinations(sorted(adj[o]&adj[t]),2) if b in adj[a]),None)
   if pair:diamonds.append((t,*pair))
  for x in diamonds:
   for y in diamonds:
    if y[0] in adj[x[0]] and len({o,*x,*y})==7:return [o,*x,*y]
 return None
def main():
 start=time.monotonic();inputs={}
 for f,h in PINS.items():
  b=(R/f).read_bytes();need(sha256(b).hexdigest()==h,'source '+f);inputs[f]=json.loads(b)
 old=inputs[OLD];oldlabels=[i for i,x in enumerate(old['provenance']) if '510' in x]
 rows=[old['coordinates'][str(i)] for i in oldlabels]+[a['coordinates'] for a in inputs[FRESH]]
 P=[]
 for row in rows:
  vals=[96*Fraction(c) for a in row for c in a];need(all(c.denominator==1 for c in vals),'source denominator');P.append(tuple(map(int,vals)))
 need(len(P)==len(set(P))==632,'H632 support');E=edges(P,RADOLD);need(len(E)==3112,'H632 graph')
 source=[v for v in range(632) if v not in (399,462)];ES=[(u,v) for u,v in E if u in source and v in source];need(len(ES)==3098,'H630 graph')
 word=inputs[CERT]['five_colouring'];need(len(word)==632 and [i for i,c in enumerate(word) if c=='.']==[399,462] and all(word[u]!=word[v] for u,v in ES),'source proper five-word')
 sourcebox=source_box(P)
 retained=[v for v in source if all(P[v][axis+i]==0 for axis in (0,8) for i in (2,3,6,7))];removed=sorted(set(source)-set(retained));need(len(retained)==418 and len(removed)==212,'block sizes')
 def convert(p):
  out=[0]*16
  for axis in (0,8):
   for oldi,newi in [(0,0),(1,2),(4,4),(5,6)]:out[axis+newi]=p[axis+oldi]
  return tuple(out)
 A=[convert(P[v]) for v in retained];origin=(0,)*16;a=[0]*16;a[0]=96;a[10]=32;a=tuple(a)
 need(origin in A and a in A,'two retained anchors');q=patch_point(1,0);need(norm(q,origin)==norm(q,a)==(9216,0,0,0,0,0,0,0),'unit-circle anchor geometry')
 addresses=[(m,n) for m in range(-5,6) for n in range(-5,6) if max(abs(m),abs(n),abs(m+n))<=5];T=[patch_point(m,n) for m,n in addresses];need(len(T)==len(set(T))==91,'one triangular disk')
 need(set(A)&set(T)=={origin},'unique exact intersection');need(all(any(p[axis+i] for axis in (0,8) for i in (1,3,5,7)) for p in T if p!=origin),'all 90 nonzero points outside original field')
 Q=sorted(set(A)|set(T));need(len(Q)==508 and 630-len(Q)==122,'physical cap')
 QE=edges(Q);pos={p:i for i,p in enumerate(Q)}
 oldmap={str(v):pos[convert(P[v])] for v in retained};patchmap=[{'m':m,'n':n,'vertex':pos[t]} for (m,n),t in zip(addresses,T)]
 oldindices=set(oldmap.values());newindices=set(range(508))-oldindices
 split={k:[] for k in ('old_old','old_new','new_new')}
 for u,v in QE:
  key='old_old' if u in oldindices and v in oldindices else 'new_new' if u in newindices and v in newindices else 'old_new';split[key].append([u,v])
 pointdata=point_bytes(Q);edgedata=edge_bytes(QE);(W/'points.csv').write_bytes(pointdata);(W/'edges.csv').write_bytes(edgedata);(W/'h632.csv').write_bytes(point_bytes(P))
 support={'denominator':96,'radicands':list(RAD),'coordinates':Q,'edges':QE,'retained_labels':retained,'removed_labels':removed,'old_to_final':oldmap,'disk_to_final':patchmap,'two_anchor_old_labels':[retained[A.index(origin)],retained[A.index(a)]],'edge_split':{k:len(v) for k,v in split.items()},'old_new_edges':split['old_new'],'outside_original_field_points':90,'source_box':sourcebox,'point_sha256':sha256(pointdata).hexdigest(),'edge_sha256':sha256(edgedata).hexdigest(),'architecture_sha256':sha256((W/'ARCHITECTURE.json').read_bytes()).hexdigest(),'input_hashes':PINS,'source_five_word':word}
 save('selected_support.json',support)
 print('FROZEN',len(Q),len(QE),'split',support['edge_split'],'anchors',support['two_anchor_old_labels'],flush=True)
 from pysat.solvers import Cadical195
 C=[]
 for v in range(508):
  names=[4*v+c+1 for c in range(4)];C.append(names);C.extend([[-x,-y] for x,y in combinations(names,2)])
 for u,v in QE:C.extend([[-(4*u+c+1),-(4*v+c+1)] for c in range(4)])
 C.append([1]);cnf=(f'p cnf 2032 {len(C)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in C)).encode();(W/'four.cnf').write_bytes(cnf)
 with Cadical195(bootstrap_with=C) as solver:sat=solver.solve();model=set(solver.get_model() or [])
 result={'vertices':508,'unit_edges':len(QE),'source_vertices':630,'source_edges':3098,'retained_vertices':418,'removed_vertices':212,'replacement_formal_points':91,'added_points':90,'net_reduction':122,'status':'SAT_FOUR' if sat else 'UNSAT_SIGNAL_REQUIRES_CERTIFICATE','record_certified':False,'point_sha256':support['point_sha256'],'edge_sha256':support['edge_sha256'],'edge_split':support['edge_split'],'cnf_sha256':sha256(cnf).hexdigest(),'runtime_seconds':time.monotonic()-start}
 if sat:
  word=''.join(str(next(c for c in range(4) if 4*v+c+1 in model)) for v in range(508));need(all(word[u]!=word[v] for u,v in QE),'ordinary four-word');result['four_word']=word
  witness=moser(508,QE);result['moser_witness']=witness
  if witness:result['chromatic_number']=4
 save('result.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
