"""Independent quadratic-tower geometry and universal extension checker.

Imports no producer or sibling module. The old G19 support is checked geometrically, and a two-word witness proves
that every proper four-colouring extends to the complete new support.
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

def digest(value):return sha256(json.dumps(value,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def proper(w,k,edges,n):
 need(len(w)==n and all(type(c) is int and 0<=c<k for c in w),'colour word domain')
 need(all(w[a]!=w[b] for a,b in edges),'proper colour inequalities')

def verify(cert=None):
 if cert is None:cert=json.loads((HERE/'certificate.json').read_text())
 need(cert['schema']=='g19-f29-translation-gate-v1','schema')
 old=json.loads((HERE/'source_g19.json').read_text())
 g,ge,_,_=check_g19_geometry(old)
 rows=[]
 for line in (HERE/'f29_points.tsv').read_text().splitlines():
  if not line or line.startswith('#'):continue
  label,a,b,c,d=map(int,line.split());need(label==len(rows),'F29 source label')
  rows.append((a,b,c,d))
 need(len(rows)==29,'F29 source count')
 f=[(times(plus(number(a),times(m8(S,T),b)),Q(1,12)),plus(ONE,times(plus(times(S,c),times(T,d)),Q(1,12)))) for a,b,c,d in rows]
 points=[];mapping=[]
 for p in g+f:
  if p not in points:points.append(p)
  mapping.append(points.index(p))
 need(len(points)==45 and mapping[:19]==list(range(19)),'merged point gate')
 need(cert['coordinates']==[[[str(c) for c in v] for v in p] for p in points],'exact coordinate rows')
 fm=mapping[19:];need(cert['f29_map']==fm,'F29 map')
 shared=[(i,v) for i,v in enumerate(fm) if v<19]
 need(shared==[(0,11),(25,15),(28,16)],'shared triangle')
 need(cert['shared_vertices']==[list(x) for x in shared],'shared certificate')
 fe=[(a,b) for a,b in combinations(range(29),2) if norm(pminus(f[a],f[b]))==ONE]
 need(len(fe)==75 and cert['f29_edges']==[list(x) for x in fe],'F29 complete edges')
 edges=[];distances=[]
 for a,b in combinations(range(45),2):
  d=norm(pminus(points[a],points[b]));need(any(d),'no coincident points')
  distances.append([a,b,[str(v) for v in d]])
  if d==ONE:edges.append((a,b))
 need(cert['edges']==[list(x) for x in edges] and len(edges)==107,'complete unit graph')
 need(cert['distance_sha256']==digest(distances),'all-pairs distance checksum')
 base=sorted(set(ge)|{tuple(sorted((fm[a],fm[b]))) for a,b in fe})
 need(len(base)==106 and cert['inherited_edges']==[list(x) for x in base],'inherited graph')
 extra=sorted(set(edges)-set(base))
 need(extra==[(7,40)] and cert['new_edges']==[[7,40]] and fm[22]==40,'sole extra contact')
 need({(11,15),(11,16),(15,16)}<=set(ge),'old shared triangle is proper')
 proper(cert['four_colouring'],4,edges,45);proper(cert['five_colouring'],5,edges,45)
 need(set(cert['five_colouring'])==set(range(5)),'five colours used')
 words=cert['f29_extension_words'];need(len(words)==2,'two extension words')
 for w in words:
  proper(w,4,fe,29);need((w[0],w[25],w[28])==(0,1,2),'extension triangle normalization')
 need(words[0][22]!=words[1][22],'contact colour flexibility')
 # Any proper old colouring gives distinct colours to the shared triangle.
 # Enumerate its 24 labelled assignments and all four old M7 colours. This
 # explicit extension check covers the entire old boundary (no extra hypotheses).
 count=0
 for tri in product(range(4),repeat=3):
  if len(set(tri))<3:continue
  perm=tuple(tri)+(next(c for c in range(4) if c not in tri),)
  for outside in range(4):
   transformed=[tuple(perm[c] for c in w) for w in words]
   good=[w for w in transformed if w[22]!=outside]
   need(bool(good),'universal boundary extension')
   for w in good:
    proper(w,4,fe,29);need((w[0],w[25],w[28])==tri,'renamed overlap')
   count+=1
 need(count==96,'complete named boundary domain')
 # A source colouring and one such word merge consistently. The exhaustive
 # all-pairs check proves there is exactly one remaining edge, already handled.
 return {'status':'UNIVERSAL_EXTENSION_DRIVER_RETIRED','points':45,'strict_unit_edges':107,
  'all_pairs':990,'inherited_edges':106,'shared_points':3,'new_edges':[[7,40]],
  'all_original_G19_four_colourings_extend':True,'all_projected_relations_unchanged':True,
  'named_boundary_assignments_checked':count,'proper_four_colouring_checked':True,
  'proper_five_colouring_checked':True,'record_candidate':False,'ordinary_nonfour_signal':False,
  'coordinate_sha256':digest(cert['coordinates']),'edge_sha256':digest(cert['edges']),
  'distance_sha256':digest(distances)}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check-expected',action='store_true');a=p.parse_args()
 result=verify()
 if a.check_expected:need(result==json.loads((HERE/'expected.json').read_text()),'expected output')
 print(json.dumps(result,indent=2,sort_keys=True))
