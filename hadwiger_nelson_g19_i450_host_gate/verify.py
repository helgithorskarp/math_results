"""Independent quadratic-tower geometry and host-intersection witness checker.

Imports no producer or sibling module. The old G19 support is checked geometrically, and a proper whole-graph word proves that the selected host and replacement
relations have a nonempty intersection.
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

def read_host():
 rows=[]
 for line in (HERE/'host_points.tsv').read_text().splitlines():
  if not line or line.startswith('#'):continue
  lab,*p=map(int,line.split());need(lab==len(rows) and len(p)==4,'host label or shape');rows.append(p)
 need(len(rows)==450 and len({tuple(p) for p in rows})==450,'host distinctness')
 need(rows[:2]==[[0,0,0,0],[0,0,0,12]],'host marked points')
 return rows

def im2(a,b):return (a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def ip(a,b):return tuple(x+y for x,y in zip(a,b))
def it(a,q):return tuple(x*q for x in a)
def im4(a,b):return ip(im2(a[:2],b[:2]),it(im2(a[2:],b[2:]),11))+ip(im2(a[:2],b[2:]),im2(a[2:],b[:2]))
def twice_product(a,b):
 # 2*(a0+a1*y)*(b0+b1*y), y^2=2-sqrt3/2.
 low=ip(it(im4(a[:4],b[:4]),2),im4((4,-1,0,0),im4(a[4:],b[4:])))
 high=it(ip(im4(a[:4],b[4:]),im4(a[4:],b[:4])),2)
 return low+high

def twice_norm(a,b):
 dx=tuple(x-y for x,y in zip(a[0],b[0]));dy=tuple(x-y for x,y in zip(a[1],b[1]))
 return ip(twice_product(dx,dx),twice_product(dy,dy))

def geometry():
 source=json.loads((HERE/'source_g19.json').read_text());g,ge,_,_=check_g19_geometry(source)
 D=432;gi=[tuple(tuple(int(v*D) for v in c) for c in p) for p in g]
 need(all(all(Q(v,D)==q for v,q in zip(c,z)) for p,h in zip(gi,g) for c,z in zip(p,h)),'integral bridge coordinates')
 rows=read_host();h=[]
 for a,b,c,d in rows:
  # u=(3 sqrt11-sqrt3)/12 + i*(3+sqrt33)/12; translation G7.
  x=216-3*a+33*b-3*c-33*d;z=3*a-b-c-3*d
  y=-216+3*a+11*b-c+33*d;v=3*a+3*b+3*c-3*d
  h.append(((x,0,0,z,0,0,0,0),(0,y,v,0,0,0,0,0)))
 need(h[0]==gi[7] and h[1]==gi[10],'host exact anchor mapping')
 # Verify the displayed rotation has norm one in the independent tower.
 u=(times(minus(times(T,3),S),Q(1,12)),times(plus(number(3),m8(S,T)),Q(1,12)))
 need(norm(u)==ONE,'rotation isometry')
 for row,p in zip(rows,h):
  a,b,c,d=row
  native=(times(plus(times(S,a),times(T,b)),Q(1,36)),times(plus(number(c),times(m8(S,T),d)),Q(1,36)))
  want=pplus(g[7],pmul(u,native))
  need(tuple(tuple(Q(v,D) for v in co) for co in p)==want,'host affine identity')
 points=[];mapping=[]
 for p in gi+h:
  if p not in points:points.append(p)
  mapping.append(points.index(p))
 need(len(points)==461 and mapping[:19]==list(range(19)),'collision gate')
 hm=mapping[19:];shared=[(j,k) for j,k in enumerate(hm) if k<19]
 need(shared==[(0,7),(1,10),(3,0),(7,5),(9,4),(11,1),(391,2),(425,6)],'complete shared-vertex set')
 target=(2*D*D,)+(0,)*7;edges=[];stream=sha256()
 for a,b in combinations(range(461),2):
  n=twice_norm(points[a],points[b]);need(any(n),'noncollision distance')
  stream.update((str(a)+','+str(b)+':'+','.join(map(str,n))+'\n').encode())
  if n==target:edges.append((a,b))
 he=[]
 for a,b in combinations(range(450),2):
  x,y,c,d=[rows[a][i]-rows[b][i] for i in range(4)]
  if 3*x*x+11*y*y+c*c+33*d*d==1296 and x*y+c*d==0:he.append((a,b))
 base=sorted(set(ge)|{tuple(sorted((hm[a],hm[b]))) for a,b in he})
 need(set(base)<=set(edges),'inherited edges preserved')
 extra=sorted(set(edges)-set(base));hi=set(hm);added=[i for i in range(461) if i not in hi]
 boundary=sorted({i for a,b in edges for i,j in [(a,b),(b,a)] if i in hi and j in added})
 return points,D,edges,he,hm,shared,base,extra,added,boundary,stream.hexdigest()

def proper(w,k,n,edges):
 need(len(w)==n and all(type(c) is int and 0<=c<k for c in w),'colour word domain')
 need(all(w[a]!=w[b] for a,b in edges),'proper colour inequalities')

def verify(cert=None):
 if cert is None:cert=json.loads((HERE/'certificate.json').read_text())
 need(cert['schema']=='g19-i450-host-stop-v1','certificate schema')
 points,D,edges,he,hm,shared,base,extra,added,boundary,dist=geometry()
 need((len(edges),len(he),len(base),len(extra),len(added),len(boundary))==(2324,2290,2312,12,11,16),'graph/boundary counts')
 need(cert['edge_sha256']==digest(edges),'complete edge checksum')
 need(cert['shared_vertices']==[list(x) for x in shared],'shared map certificate')
 need(cert['extra_edges']==[list(x) for x in extra],'extra contact certificate')
 need(cert['addition']==added and cert['boundary']==boundary,'actual host interface')
 word=[int(c) for c in cert['four_colouring']];five=[int(c) for c in cert['five_colouring']]
 proper(word,4,461,edges);proper(five,5,461,edges);need(set(five)==set(range(5)),'five colours used')
 host=[word[v] for v in hm];proper(host,4,450,he);need(host[0]!=host[1],'marked host inequality')
 need(cert['boundary_word']==''.join(str(word[v]) for v in boundary),'host boundary word')
 need(cert['addition_word']==''.join(str(word[v]) for v in added),'replacement extension word')
 need(cert['G19_word']==''.join(map(str,word[:19])),'source restriction word')
 return {'status':'EXACT_HOST_INTERSECTION_NONEMPTY','points':461,'unit_edges':2324,'all_pairs':106030,
  'host_points':450,'host_edges':2290,'source_points':19,'source_edges':34,'shared_points':8,'added_points':11,
  'inherited_edges':2312,'extra_edges':12,'host_boundary_points':16,'boundary_word':cert['boundary_word'],
  'addition_word':cert['addition_word'],'G19_word':cert['G19_word'],'marked_host_colours':[host[0],host[1]],
  'proper_four_colouring_checked':True,'proper_five_colouring_checked':True,'full_relation_census_performed':False,
  'host_intersection_empty':False,'ordinary_nonfour_signal':False,'record_candidate':False,
  'coordinate_denominator':D,'coordinate_sha256':digest(points),'distance_sha256':dist,'edge_sha256':digest(edges)}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check-expected',action='store_true');a=p.parse_args();out=verify()
 if a.check_expected:need(out==json.loads((HERE/'expected.json').read_text()),'expected output')
 print(json.dumps(out,indent=2,sort_keys=True))
