"""Solver-free independent checker for one exact H630 block replacement.
Radicand/gcd arithmetic and closed Cartesian coordinates; no producer import.
"""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
from math import gcd,isqrt
import json,copy
HERE=Path(__file__).resolve().parent
OLD=(1,3,5,15,11,33,55,165)
NEW=(1,2,3,6,11,22,33,66)
SOURCE_SHA='5bc6df88afed13c6ccff2154c749fc1f5e74a9892b6b13f79ab08bbc49cd2e17'
def need(b,s):
 if not b:raise ValueError(s)
def parse(raw):
 rows=[tuple(map(int,line.split(','))) for line in raw.decode('ascii').splitlines()]
 need(all(len(r)==16 for r in rows),'point dimensions');return rows
def sparse(row,basis):return [{r:c for r,c in zip(basis,row[k:k+8]) if c} for k in (0,8)]
def norm(p,q):
 out={}
 for a,b in zip(p,q):
  delta=[(r,a.get(r,0)-b.get(r,0)) for r in sorted(a.keys()|b.keys()) if a.get(r,0)!=b.get(r,0)]
  for r,c in delta:out[1]=out.get(1,0)+r*c*c
  for (r,c),(s,d) in combinations(delta,2):
   g=gcd(r,s);t=r*s//(g*g);out[t]=out.get(t,0)+2*g*c*d
 return {r:c for r,c in out.items() if c}
def graph(points):return [(u,v) for u,v in combinations(range(len(points)),2) if norm(points[u],points[v])=={1:9216}]
def edges_raw(E):return ''.join(f'{u},{v}\n' for u,v in E).encode()
def rows_raw(P):return ''.join(','.join(map(str,p))+'\n' for p in P).encode()
def disk(m,n):
 # Direct Cartesian formula, independent of the producer's complex rotation.
 a=m+2*n
 return (48*m,0,0,-16*a,0,0,0,0,0,48*m,16*a,0,0,0,0,0)
def convert(p):
 r=[0]*16
 for k in (0,8):
  for old,new in ((0,0),(1,2),(4,4),(5,6)):r[k+new]=p[k+old]
 return tuple(r)
def source_box(rows):
 S=10**6;bound=[(isqrt(r*S*S),isqrt(r*S*S)+1) for r in OLD]
 # Each radical enclosure follows from exact integer square inequalities.
 for r,(lo,hi) in zip(OLD,bound):need(lo*lo<=r*S*S<hi*hi,'rational radical enclosure')
 for row in rows:
  for axis in (row[:8],row[8:]):
   lo=sum(c*bound[i][0 if c>=0 else 1] for i,c in enumerate(axis));hi=sum(c*bound[i][1 if c>=0 else 0] for i,c in enumerate(axis))
   need(-3*96*S<lo<=hi<3*96*S,'original source bounding box')
 # Every congruent copy of H632, H560 or H516 has squared diameter <72.
def check_certificate(c,retained,removed,oldmap,patchmap,Q,E,split,oldnew,ph,eh):
 need(c['vertices']==len(Q)==508 and c['unit_edges']==len(E)==2341,'complete graph size')
 need(c['source_vertices']==630 and c['source_edges']==3098,'source counts')
 need(c['retained_vertices']==418 and c['removed_vertices']==212 and c['replacement_formal_points']==91 and c['added_points']==90 and c['net_reduction']==122,'physical budget')
 need(c['retained_labels']==retained and c['removed_labels']==removed,'fixed whole block')
 need(c['old_to_final']==oldmap and c['disk_to_final']==patchmap,'physical role maps')
 need(c['two_anchor_old_labels']==[0,193],'fixed anchors')
 need(c['outside_original_field_points']==90,'outside-field count')
 need(c['edge_split']==split and c['old_new_edges']==oldnew,'complete contact partition')
 need(c['point_sha256']==ph and c['edge_sha256']==eh,'canonical graph bytes')
 need(c['status']=='SAT_FOUR' and c['record_certified'] is False,'claim status')
 word=c['four_word'];need(isinstance(word,str) and len(word)==508 and set(word)<=set('0123'),'colour domain');need(all(word[u]!=word[v] for u,v in E),'proper four-word')
 M=c['moser_witness'];need(len(M)==len(set(M))==7 and all(type(v)is int and 0<=v<508 for v in M),'Moser roles')
 o,t,a,b,s,d,e=M;required=[(o,a),(o,b),(t,a),(t,b),(a,b),(o,d),(o,e),(s,d),(s,e),(d,e),(t,s)]
 ES=set(E);need(all(tuple(sorted(x)) in ES for x in required),'Moser unit edges')
 # In three colours the two diamonds force o=t=s; checked edge t-s forbids it.
 need(c['chromatic_number']==4,'ordinary chromatic number')
def main():
 prov=json.loads((HERE/'PROVENANCE.json').read_text());arch=(HERE/'ARCHITECTURE.json').read_bytes();need(sha256(arch).hexdigest()==prov['architecture_sha256'],'architecture bytes')
 raw=(HERE/'h632.csv').read_bytes();need(sha256(raw).hexdigest()==SOURCE_SHA==prov['source_h632_sha256'],'original source identity')
 P=parse(raw);need(len(P)==len(set(P))==632,'source collisions');PS=[sparse(p,OLD) for p in P];PE=graph(PS);need(len(PE)==3112,'H632 complete graph')
 original=set(range(632))-{399,462};SE=[(u,v) for u,v in PE if u in original and v in original];need(len(SE)==3098,'H630 source edges')
 five=prov['source_five_word'];need(len(five)==632 and [i for i,c in enumerate(five) if c=='.']==[399,462] and set(five)<=set('01234.') and all(five[u]!=five[v] for u,v in SE),'source five-word')
 source_box(P)
 retained=sorted(v for v in original if all(P[v][k+i]==0 for k in (0,8) for i in (2,3,6,7)));removed=sorted(original-set(retained));need((len(retained),len(removed))==(418,212),'field block')
 A=[convert(P[v]) for v in retained];addresses=[(m,n) for m in range(-5,6) for n in range(-5,6) if max(abs(m),abs(n),abs(m+n))<=5];T=[disk(m,n) for m,n in addresses];zero=(0,)*16
 need(len(T)==len(set(T))==91 and set(A)&set(T)=={zero},'exact merge')
 need(all(any(p[k+i] for k in (0,8) for i in (1,3,5,7)) for p in T if p!=zero),'nonzero sqrt2 coefficients')
 Q=sorted(set(A)|set(T));need(len(Q)==508,'cap');qraw=rows_raw(Q);need(qraw==(HERE/'points.csv').read_bytes(),'canonical exact points')
 QS=[sparse(p,NEW) for p in Q];E=graph(QS);eraw=edges_raw(E);need(eraw==(HERE/'edges.csv').read_bytes(),'all 128778 unit-pair decisions')
 positions={p:i for i,p in enumerate(Q)};oldmap={str(v):positions[convert(P[v])] for v in retained};patchmap=[{'m':m,'n':n,'vertex':positions[disk(m,n)]} for m,n in addresses]
 oldset=set(oldmap.values());split={'old_old':0,'old_new':0,'new_new':0};oldnew=[]
 for u,v in E:
  key='old_old' if u in oldset and v in oldset else 'new_new' if u not in oldset and v not in oldset else 'old_new';split[key]+=1
  if key=='old_new':oldnew.append([u,v])
 # Independently predict the exact mixed interface from the six first-ring sites.
 predicted=set();anchor_roles=[]
 for m,n in addresses:
  if m*m+m*n+n*n!=1:continue
  anchor=[0]*16;anchor[0]=96*m;anchor[10]=32*(m+2*n);anchor=tuple(anchor);need(anchor in A,'rotated retained anchor')
  new=positions[disk(m,n)];predicted.add(tuple(sorted((positions[zero],new))));predicted.add(tuple(sorted((positions[anchor],new))))
  anchor_roles.append(next(int(k) for k,v in oldmap.items() if v==positions[anchor]))
 need(predicted==set(map(tuple,oldnew)) and len(predicted)==12,'entire mixed interface')
 need(convert(P[193])==tuple([96]+[0]*9+[32]+[0]*5),'named anchor coordinate')
 q=sparse(disk(1,0),NEW);need(norm(q,sparse(zero,NEW))==norm(q,sparse(convert(P[193]),NEW))=={1:9216},'two-circle geometry')
 # Three disjoint opposite pairs are farther apart than the entire old source.
 diameter_pairs=[]
 for m,n in [(5,0),(0,5),(5,-5)]:
  a,b=positions[disk(m,n)],positions[disk(-m,-n)];need(norm(QS[a],QS[b])=={1:100*9216},'ten-unit span');diameter_pairs.append([a,b])
 need(len({v for p in diameter_pairs for v in p})==6,'disjoint diameter witnesses')
 # A congruent H632 cannot contain an opposite pair. H516 plus one arbitrary
 # point cannot accommodate all three disjoint pairs, so neither closure applies.
 c=json.loads((HERE/'certificate.json').read_text());need(c['architecture_sha256']==prov['architecture_sha256'],'certificate architecture')
 def check(x):check_certificate(x,retained,removed,oldmap,patchmap,Q,E,split,oldnew,sha256(qraw).hexdigest(),sha256(eraw).hexdigest())
 check(c)
 bad=[]
 z=copy.deepcopy(c);v=list(z['four_word']);v[E[0][1]]=v[E[0][0]];z['four_word']=''.join(v);bad.append(('monochromatic unit edge',z))
 z=copy.deepcopy(c);z['four_word']=z['four_word'][:-1];bad.append(('truncated word',z))
 z=copy.deepcopy(c);z['retained_labels']=z['retained_labels'][:-1];bad.append(('wrong retained block',z))
 z=copy.deepcopy(c);z['removed_labels'][0]=0;bad.append(('wrong removed block',z))
 z=copy.deepcopy(c);z['disk_to_final'][0]['m']+=1;bad.append(('wrong lattice role',z))
 z=copy.deepcopy(c);z['added_points']=89;bad.append(('false collision saving',z))
 z=copy.deepcopy(c);z['net_reduction']=123;bad.append(('false net reduction',z))
 z=copy.deepcopy(c);z['old_new_edges']=z['old_new_edges'][:-1];bad.append(('missing mixed contact',z))
 z=copy.deepcopy(c);z['unit_edges']-=1;bad.append(('incomplete graph claim',z))
 z=copy.deepcopy(c);z['point_sha256']='0'*64;bad.append(('wrong coordinate bytes',z))
 z=copy.deepcopy(c);z['moser_witness'][0]=z['moser_witness'][1];bad.append(('colliding Moser roles',z))
 for name,z in bad:
  try:check(z)
  except (ValueError,IndexError,KeyError):continue
  raise ValueError('accepted corruption: '+name)
 print(json.dumps({'verified':True,'vertices':508,'unit_edges':2341,'chromatic_number':4,'parent_vertices':630,'parent_edges':3098,'retained_points':418,'removed_points':212,'new_points':90,'net_reduction':122,'complete_final_pairs':128778,'source_pairs':199396,'edge_split':split,'nonzero_contact_anchor_labels':sorted(anchor_roles),'ten_unit_disjoint_pairs':diameter_pairs,'source_squared_diameter_strict_upper_bound':72,'point_sha256':sha256(qraw).hexdigest(),'edge_sha256':sha256(eraw).hexdigest(),'rejected_corruptions':[x for x,z in bad],'scope':'One frozen H630 block replacement; no record improvement.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
