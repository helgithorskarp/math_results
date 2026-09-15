#!/usr/bin/env python3
"""Exact cyclic-amalgam geometry and universal extension; no solver required."""
import argparse,hashlib,json
from fractions import Fraction as F
from itertools import combinations,product,permutations
from math import gcd,lcm
from pathlib import Path
HERE=Path(__file__).resolve().parent
RAD=(1,3,7,21,11,33,77,231)
F_PATH=HERE.parent/'hadwiger_nelson_frozen_centre_transfer/points.tsv'
B_PATH=HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2/points214.tsv'
HASHES={F_PATH:'3631210e31697804a86437cc7b6f734870097e22de50e5c4721ecea6ab633924',B_PATH:'97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def rmul(a,b):
 out=[0]*8
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:
     g=gcd(RAD[i],RAD[j]);out[RAD.index(RAD[i]*RAD[j]//(g*g))]+=x*y*g
 return tuple(out)
def ra(a,b):return tuple(x+y for x,y in zip(a,b))
def rn(a):return tuple(-x for x in a)
def pt(x=None,y=None):return tuple(F((x or {}).get(d,0)) for d in RAD),tuple(F((y or {}).get(d,0)) for d in RAD)
def add(p,q):return ra(p[0],q[0]),ra(p[1],q[1])
def neg(p):return rn(p[0]),rn(p[1])
def conj(p):return p[0],rn(p[1])
def mul(p,q):return ra(rmul(p[0],q[0]),rn(rmul(p[1],q[1]))),ra(rmul(p[0],q[1]),rmul(p[1],q[0]))
def ecoord(a,b,c,d):return pt({1:F(a,12),33:F(b,12)},{3:F(c,12),11:F(d,12)})
def squared(p,q):
 dx=tuple(a-b for a,b in zip(p[:8],q[:8]));dy=tuple(a-b for a,b in zip(p[8:],q[8:]));return ra(rmul(dx,dx),rmul(dy,dy))
def digest(rows):return hashlib.sha256(('\n'.join(rows)+'\n').encode()).hexdigest()
def geometry():
 for path,h in HASHES.items():need(hashlib.sha256(path.read_bytes()).hexdigest()==h,'fixture hash')
 f=[]
 for line in F_PATH.read_text().splitlines():
  if line and not line.startswith('#'):
   row=list(map(int,line.split()));need(row[0]==len(f),'F29 source labels');f.append(ecoord(*row[1:]))
 b=[]
 for line in B_PATH.read_text().splitlines():
  if line and not line.startswith('#'):
   z=list(map(int,line.split()));need(len(z)==16 and all(z[i]==0 for i in range(16) if i not in (0,5,9,12)),'B214 basis');b.append(ecoord(z[0],z[5],z[9],z[12]))
 g=[ecoord(*z) for z in [(0,0,0,0),(12,0,0,0),(6,0,6,0),(-6,0,6,0),(-12,0,0,0),(-6,0,-6,0),(6,0,-6,0),(2,0,0,2),(-1,-1,1,-1),(-1,1,-1,-1)]]
 one=pt({1:1});zero=pt();eta=pt({33:F(1,6)},{3:F(1,6)});u=pt({1:F(-1,8)},{7:F(3,8)});v=pt({1:F(-3,4)},{7:F(1,4)})
 for z in (eta,u,v):need(mul(z,conj(z))==one,'unit isometry')
 blocks=[[add(one,neg(z)) for z in g],[mul(u,add(one,mul(conj(eta),z))) for z in f],[add(add(one,u),mul(v,z)) for z in b]]
 points=[];index={};maps=[]
 for block in blocks:
  image=[]
  for z in block:
   if z not in index:index[z]=len(points);points.append(z)
   image.append(index[z])
  maps.append(image)
 need(list(map(len,maps))==[10,29,214] and len(points)==250,'exact collisions')
 need(points[maps[0][1]]==zero and points[maps[0][4]]==pt({1:2}),'O and P')
 need(maps[0][1]==maps[1][9] and maps[0][4]==maps[2][187] and maps[1][12]==maps[2][186],'marked overlaps')
 sets=list(map(set,maps));need([sorted(sets[i]&sets[j]) for i,j in ((0,1),(0,2),(1,2))]==[[1],[4],[21]],'complete pairwise overlap sets')
 den=lcm(*(x.denominator for p in points for xy in p for x in xy));need(den==96,'coordinate denominator')
 rows=[tuple(int(x*den) for xy in p for x in xy) for p in points];edges=[];norms=[]
 for a,b in combinations(range(250),2):
  d=squared(rows[a],rows[b]);norms.append((a,b,*d))
  if d==(den*den,0,0,0,0,0,0,0):edges.append((a,b))
 need(len(edges)==1070,'complete unit graph')
 own=[]
 for image in maps:
  inv={v:i for i,v in enumerate(image)};own.append([(inv[a],inv[b]) for a,b in edges if a in inv and b in inv])
 need(list(map(len,own))==[18,75,977],'complete component edges')
 extra=[(a,b) for a,b in edges if not any({a,b}<=s for s in sets)];need(not extra,'new contact beyond amalgam')
 O,P,Q=1,4,21
 need(squared(rows[O],rows[P])==(4*den*den,0,0,0,0,0,0,0),'distance OP')
 need(squared(rows[O],rows[Q])==(4*den*den,0,0,0,0,0,0,0),'distance OQ')
 need(squared(rows[P],rows[Q])==(9*den*den,0,0,0,0,0,0,0),'distance PQ')
 return rows,edges,maps,own,norms

def proper(word,n,edges,colours='0123'):
 need(isinstance(word,str) and len(word)==n and set(word)<=set(colours),'word format');need(all(word[a]!=word[b] for a,b in edges),'improper word')
def recolour(word,requirements):
 # Complete permutation search is just a deterministic way to extend a
 # one- or two-colour injective assignment to a permutation of four colours.
 for perm in permutations('0123'):
  if all(perm[int(word[i])]==c for i,c in requirements.items()):return ''.join(perm[int(c)] for c in word)
 raise ValueError('incompatible colour permutation')
def extend(cert,a,b):
 # B187 (P) has colour a, B186 (Q) has colour b. Put O=b.
 fw=recolour(cert['f29_equal_template'],{9:b,12:b})
 gw=cert['golomb_equal_template'] if a==b else cert['golomb_different_template']
 gw=recolour(gw,{1:b,4:a})
 return gw,fw

def run(cert):
 need(cert['schema']=='golomb-f29-b214-cycle-stop-v1','schema');rows,edges,maps,own,norms=geometry()
 proper(cert['proper4'],250,edges);proper(cert['proper5'],250,edges,'01234');need(set(cert['proper5'])==set('01234'),'five colours used')
 need(cert['proper4'][1]!=cert['proper4'][4],'selected equal-pair gate survives inequality')
 for key in ['golomb_equal_template','golomb_different_template']:proper(cert[key],10,own[0])
 need(cert['golomb_equal_template'][1]==cert['golomb_equal_template'][4],'equal G template');need(cert['golomb_different_template'][1]!=cert['golomb_different_template'][4],'different G template')
 proper(cert['f29_equal_template'],29,own[1]);need(cert['f29_equal_template'][9]==cert['f29_equal_template'][12],'equal F template')
 proper(cert['b214_template'],214,own[2])
 inp=sorted(set(maps[0])|set(maps[1]));inv={v:i for i,v in enumerate(inp)};ie=[(inv[a],inv[b]) for a,b in edges if a in inv and b in inv];iw=cert['connected_input_equal_tips_word'];proper(iw,len(inp),ie);need(iw[inv[4]]==iw[inv[21]] and iw[inv[1]]!=iw[inv[4]],'initial input compatibility')
 for a,b in product('0123',repeat=2):
  gw,fw=extend(cert,a,b);proper(gw,10,own[0]);proper(fw,29,own[1]);need(gw[1]==fw[9]==b and gw[4]==a and fw[12]==b,'gluing all terminal assignments')
 bw=cert['b214_template'];gw,fw=extend(cert,bw[187],bw[186]);whole=['?']*250
 for image,word in zip(maps,(gw,fw,bw)):
  for i,c in zip(image,word):need(whole[i] in ('?',c),'collision agreement');whole[i]=c
 proper(''.join(whole),250,edges)
 need(not any(all(w[a]!=w[b] for a,b in own[0]) for tail in product(range(3),repeat=7) for w in [(0,1,2)+tail]),'Golomb not three-colourable')
 adj=[set() for _ in range(250)]
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 def cc(skip=None):
  remain=set(range(250))-{skip};count=0
  while remain:
   todo=[remain.pop()];count+=1
   while todo:
    z=adj[todo.pop()]&remain;remain-=z;todo.extend(z)
  return count
 need(cc()==1 and all(cc(v)==1 for v in range(250)),'connected without articulation')
 return {'status':'VERIFIED_FIXED_CYCLIC_AMALGAM_EXTENSION','points':250,'complete_unit_edges':1070,'all_pairs':31125,'component_orders':[10,29,214],'component_edges':[18,75,977],'pairwise_overlaps':[[1],[4],[21]],'extra_private_contacts':0,'minimum_degree':min(map(len,adj)),'articulations':[],'chromatic_number':4,'all_full_B214_colourings_extend':True,'terminal_assignment_templates_checked':16,'root_P_equal_forced':False,'conditional_spindle_cap':499,'spindle_constructed':False,'record_candidate':False,'receiver_tested':False,'point_hash':digest(' '.join(map(str,r)) for r in rows),'edge_hash':digest(f'{a} {b}' for a,b in edges),'norm_stream_hash':digest(' '.join(map(str,r)) for r in norms)}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check-expected',action='store_true');args=ap.parse_args();result=run(json.loads((HERE/'certificate.json').read_text()))
 if args.check_expected:need(result==json.loads((HERE/'EXPECTED.json').read_text()),'expected output')
 print(json.dumps(result,indent=2,sort_keys=True))
