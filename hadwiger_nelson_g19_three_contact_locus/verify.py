"""Independent Gram-determinant census and complete external-locus checker.

Imports no producer or sibling module. The old G19 support is checked geometrically; every possible triple centre
is exhausted using a Gram identity and tested against an explicit finite set.
The prior terminal census is not needed or reverified for this proof.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent

def need(ok, message):
    if not ok: raise ValueError(message)

def plus(a,b): return tuple(x+y for x,y in zip(a,b))
def minus(a,b): return tuple(x-y for x,y in zip(a,b))
def times(a,q): return tuple(x*q for x in a)
def m2(a,b): return (a[0]*b[0]+3*a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def m4(a,b):
    return plus(m2(a[:2],b[:2]),times(m2(a[2:],b[2:]),11))+plus(m2(a[:2],b[2:]),m2(a[2:],b[:2]))
H=(Q(2),Q(-1,2),Q(0),Q(0))
def m8(a,b):
    return plus(m4(a[:4],b[:4]),m4(H,m4(a[4:],b[4:])))+plus(m4(a[:4],b[4:]),m4(a[4:],b[:4]))
def number(x):return (Q(x),)+(Q(0),)*7
ZERO=number(0);ONE=number(1)
S=(Q(0),Q(1))+(Q(0),)*6
T=(Q(0),)*2+(Q(1),)+(Q(0),)*5
Y=(Q(0),)*4+(Q(1),)+(Q(0),)*3
def pplus(a,b):return plus(a[0],b[0]),plus(a[1],b[1])
def pminus(a,b):return minus(a[0],b[0]),minus(a[1],b[1])
def pmul(a,b):return minus(m8(a[0],b[0]),m8(a[1],b[1])),plus(m8(a[0],b[1]),m8(a[1],b[0]))
def norm(v):return plus(m8(v[0],v[0]),m8(v[1],v[1]))

def check_g19_geometry(cert):
    need(len(cert['coordinates'])==19,'coordinate count')
    pts=[]
    for row in cert['coordinates']:
        need(len(row)==2 and all(len(v)==8 for v in row),'coordinate shape')
        pts.append(tuple(tuple(Q(x) for x in v) for v in row))
    need(len(set(pts))==19,'collision merging')
    # Verify the Moser frame from two unit diamonds and the stated cap rows.
    source=((0,0,0,0),(12,0,0,0),(6,0,6,0),(18,0,6,0),(10,0,0,2),(5,-1,5,1),(15,-1,5,3),(6,0,-6,0),(12,0,12,0),(20,0,0,4),(-5,-1,5,-1))
    for p,(a,b,c,d) in zip(pts,source):
        want=(times(plus(number(a),times(m8(S,T),b)),Q(1,12)),times(plus(times(S,c),times(T,d)),Q(1,12)))
        need(p==want,'Moser coordinate')
    # Invert the frozen isometry, then check the two retained caps and six
    # common neighbours directly. Deleted caps are construction centres only.
    inverse=(times(S,Q(-1,2)),number(Q(1,2)))
    caps=[(ZERO,ZERO),(times(plus(ONE,S),Q(1,2)),Y),(times(minus(ONE,S),Q(1,2)),Y),(ONE,ZERO)]
    back=[pplus(caps[1],pmul(inverse,pminus(p,(ZERO,ONE)))) for p in pts[11:]]
    need(back[:2]==caps[1:3],'retained palette caps')
    forward=(times(S,Q(-1,2)),number(Q(-1,2)))
    need(all(pplus((ZERO,ONE),pmul(forward,pminus(c,caps[1]))) not in pts for c in (caps[0],caps[3])),'deleted caps absent from union')
    for i in range(3):
        x,y=back[2+2*i:4+2*i];a,b=caps[i:i+2]
        need(pplus(x,y)==pplus(a,b),'diamond midpoint')
        delta=pminus(b,a)
        want=(times(m8(S,delta[1]),Q(-1,3)),times(m8(S,delta[0]),Q(1,3)))
        need(pminus(x,y)==want,'ordered common neighbours')
        need(norm(pminus(x,a))==norm(pminus(x,b))==norm(pminus(y,a))==norm(pminus(y,b))==ONE,'diamond incidence')
    distances=[];edges=[]
    for a,b in combinations(range(19),2):
        v=norm(pminus(pts[a],pts[b]));distances.append([a,b,[str(x) for x in v]])
        if v==ONE:edges.append((a,b))
    inherited=[e for e in edges if (e[0]<11)==(e[1]<11)]
    cross=[e for e in edges if e not in inherited]
    need(edges==[tuple(e) for e in cert['edges']],'complete unit edges')
    need(inherited==[tuple(e) for e in cert['inherited_edges']],'inherited edges')
    need(cross==[tuple(e) for e in cert['new_edges']]==[(0,11),(1,16),(2,15),(3,12)],'new contacts')
    need(len(edges)==34 and len(inherited)==30,'edge counts')
    need({e for e in edges if e[0]>=11}=={(11,13),(11,14),(11,15),(11,16),(12,15),(12,16),(12,17),(12,18),(13,14),(15,16),(17,18)},'palette elimination structure')
    return pts,edges,inherited,distances

def digest(x):return sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def proper(word,k,edges):
 need(len(word)==21 and all(type(c) is int and 0<=c<k for c in word),'colour domain')
 need(all(word[a]!=word[b] for a,b in edges),'proper colour inequalities')

def verify(cert=None):
 if cert is None:cert=json.loads((HERE/'certificate.json').read_text())
 need(cert['schema']=='g19-three-contact-locus-v1','schema')
 g,ge,_,_=check_g19_geometry(json.loads((HERE/'source_g19.json').read_text()))
 # Both new points have simple literal coordinates, independently of any
 # circumcentre search or field inversion in the producer.
 new=[(number(Q(1,2)),minus(ONE,times(S,Q(1,2)))),(ONE,plus(ONE,S))]
 need(cert['new_points']==[[[str(v) for v in co] for co in p] for p in new],'literal new coordinates')
 points=g+new;need(len(set(points))==21,'distinct support')
 norms={};edges=[]
 for a,b in combinations(range(21),2):
  n=norm(pminus(points[a],points[b]));norms[a,b]=n
  if n==ONE:edges.append((a,b))
 need(edges==[tuple(e) for e in cert['edges']] and len(edges)==40,'complete graph')
 need([e for e in edges if e[1]<19]==ge,'old induced graph')
 adjacency=[set() for _ in points]
 for a,b in edges:adjacency[a].add(b);adjacency[b].add(a)
 need(adjacency[19]=={7,11,16} and adjacency[20]=={8,12,15},'external neighbourhoods')
 need(20 not in adjacency[19],'new points independent')
 # For u,v from one triple vertex, 4*Gram(u,v)=4AB-(A+B-C)^2.
 # Unit circumradius requires ABC=4*Gram. This checker computes Gram only
 # from squared side lengths and never inverts a determinant or finds roots.
 count=coll=on=0;counts={};stream=sha256()
 for a,b,c in combinations(range(19),3):
  A=norms[a,b];B=norms[a,c];C=norms[b,c];z=minus(plus(A,B),C)
  fourgram=minus(times(m8(A,B),4),m8(z,z));collinear=fourgram==ZERO
  radius_one=not collinear and m8(m8(A,B),C)==fourgram
  possible=[i for i in range(21) if {a,b,c}<=adjacency[i]]
  need((len(possible)==1)==radius_one and len(possible)<=1,'complete unit-centre list')
  if collinear:coll+=1
  if radius_one:
   on+=1;k=str(possible[0]);counts[k]=counts.get(k,0)+1
  stream.update((f'{a},{b},{c}:{int(collinear)}{int(radius_one)}\n').encode());count+=1
 need((count,coll,on)==(969,6,107),'complete triple census')
 need(cert['collinear_triples']==coll and cert['unit_radius_triples']==on,'certificate triple counts')
 need(cert['triple_truth_sha256']==stream.hexdigest() and cert['centre_multiplicities']==counts,'complete centre census')
 # Any real point with >=3 old unit neighbours gives a noncollinear triple,
 # whose unique circumcentre has just been identified. Only 19 and 20 are new.
 proper(cert['four_colouring'],4,edges);proper(cert['five_colouring'],5,edges)
 need(set(cert['five_colouring'])==set(range(5)),'five labels used')
 need(cert['four_colouring'][:19]==list(map(int,'0120123210111020202')),'known source word retained')
 # Each new point has three old neighbours, so every old four-colouring
 # leaves it a colour; no new-to-new edge couples these choices.
 need(all(len(adjacency[i])==3 and adjacency[i]<=set(range(19)) for i in [19,20]),'universal extension structure')
 return {'status':'COMPLETE_THREE_CONTACT_DRIVER_UNIVERSALLY_NEUTRAL','points':21,'unit_edges':40,
  'all_pairs':210,'old_points':19,'old_edges':34,'external_three_contact_points':2,'external_four_contact_points':0,
  'all_triples':count,'collinear_triples':coll,'unit_radius_triples':on,'unit_circumcentres_including_old':len(counts),
  'new_neighbourhoods':[[7,11,16],[8,12,15]],'all_old_four_colourings_extend':True,
  'any_single_new_point_all_old_four_colourings_extend':True,'full_terminal_relation_unchanged':True,
  'proper_four_colouring_checked':True,'proper_five_colouring_checked':True,'record_candidate':False,'ordinary_nonfour_signal':False,
  'triple_truth_sha256':stream.hexdigest(),'coordinate_sha256':digest([[[str(v) for v in co] for co in p] for p in points]),'edge_sha256':digest(edges)}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check-expected',action='store_true');a=p.parse_args();out=verify()
 if a.check_expected:need(out==json.loads((HERE/'expected.json').read_text()),'expected result')
 print(json.dumps(out,indent=2,sort_keys=True))
