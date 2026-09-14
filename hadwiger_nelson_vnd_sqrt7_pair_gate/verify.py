"""Complete physical geometry and unrestricted individual-pair certificate."""
from pathlib import Path
from itertools import combinations,product
from hashlib import sha256
import json
from model import atom,build,r,mul,add,sub,sign

HERE=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(obj):return sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def verify(certificate=None):
 P,E,N=build();pairs=list(combinations(range(100),2));edges=set(E)
 need(len(P)==len(set(P))==100 and len(E)==344 and len(N)==4950,'geometry counts')
 need(all(sign(n)>0 for n in N),'exact positive squared separations')
 A=atom();AE=[]
 for i,j in combinations(range(10),2):
  x,y=(sub(A[i][k],A[j][k]) for k in range(2))
  if add(mul(x,x),mul(y,y))==r(36):AE.append((i,j))
 need(len(AE)==17,'exact atom graph')
 cart=set()
 for i,j in AE:
  for k in range(10):
   cart.add((10*i+k,10*j+k));cart.add((10*k+i,10*k+j))
 need(len(cart)==340 and cart<=edges,'inherited product contacts')
 extra=sorted(edges-cart)
 need(extra==[(0,22),(1,23),(10,32),(11,33)],'all nonfactor physical contacts')
 # Pin a genuine triangle; every three-colouring can be renamed this way.
 need({(0,7),(0,8),(7,8)}<=set(AE),'atom triangle')
 free=[i for i in range(10) if i not in (0,7,8)]
 three=0
 for colours in product(range(3),repeat=7):
  w=[0]*10;w[0]=0;w[7]=1;w[8]=2
  for v,c in zip(free,colours):w[v]=c
  three+=all(w[a]!=w[b] for a,b in AE)
 need(three==0,'atom has no three-colouring')
 if certificate is None:certificate=json.loads((HERE/'certificate.json').read_text())
 need(certificate['schema']=='vnd-sqrt7-pair-v1','certificate schema')
 words=certificate['words'];need(type(words) is list and words,'nonempty word list')
 same=set();different=set()
 for w in words:
  need(type(w) is str and len(w)==100 and set(w)<=set('0123'),'word encoding')
  need(all(w[a]!=w[b] for a,b in E),'all physical edges properly coloured')
  for a,b in pairs:(same if w[a]==w[b] else different).add((a,b))
 need(same==set(pairs)-edges and different==set(pairs),'full neutral pair relation')
 bridge=[p for p,n in zip(pairs,N) if sign(sub(n,r(144)))>=0]
 boundary=[p for p,n in zip(pairs,N) if n==r(144)]
 nonunit_bridge=[p for p in bridge if p not in edges]
 return {'status':'FIXED VND SQRT7 SOURCE HAS NEUTRAL PAIR RELATIONS',
         'points':100,'strict_unit_edges':344,'atom_unit_edges':17,'chromatic_number':4,
         'all_pairs':4950,'same_colour_nonunit_pairs':len(same),
         'different_colour_pairs':len(different),'canonical_pair_requests':len(same)+len(different),
         'words':len(words),'word_edge_checks':len(words)*len(E),
         'nonfactor_edges':extra,'distance_at_least_half_pairs':len(bridge),
         'nonunit_distance_at_least_half_pairs':len(nonunit_bridge),
         'distance_exactly_half_pairs':len(boundary),'conditional_two_copy_bound':199,
         'forced_equal_pair_found':False,'physical_milestone_achieved':False,
         'point_sha256':digest(P),'edge_sha256':digest(E),'norm_sha256':digest(N),
         'relation_sha256':digest([sorted(same),sorted(different)]),
         'record_improvement':False}

if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
