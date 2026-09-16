"""Standalone incidence-count verifier; interval nonedges, exact algebraic edges."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent;BITS=192;DEN=1<<BITS
Z=(Q(0),Q(0));ONE=(Q(1),Q(0))
def need(p,m):
 if not p:raise ValueError(m)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def sub(a,b):return add(a,neg(b))
def mul(a,b):return a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def k(a=0,b=0):return Q(a),Q(b)
def sg(a):
 x,y=a
 if y==0:return (x>0)-(x<0)
 if x==0:return (y>0)-(y<0)
 if x*y>0:return 1 if x>0 else -1
 t=x*x-3*y*y;return ((t>0)-(t<0))*(1 if x>0 else -1)
def ca(a,b):return add(a[0],b[0]),add(a[1],b[1])
def cs(a,b):return sub(a[0],b[0]),sub(a[1],b[1])
def cm(a,b):return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
def norm(a):return add(mul(a[0],a[0]),mul(a[1],a[1]))
def raw(a):return (json.dumps(a,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(a):return hashlib.sha256(raw(a)).hexdigest()
def parse_k(a):
 need(type(a) is list and len(a)==2,'quadratic coefficient')
 out=[]
 for v in a:
  need(type(v) is list and len(v)==2 and all(type(x) is int for x in v) and v[1]>0,'rational format');q=Q(*v);need([q.numerator,q.denominator]==v,'reduced rational');out.append(q)
 return tuple(out)
def parse_c(a):need(type(a) is list and len(a)==2,'complex coefficient');return tuple(parse_k(x) for x in a)
def ia(a,b):return a[0]+b[0],a[1]+b[1]
def im(a,b):
 z=[x*y for x in a for y in b];return min(z),max(z)
def ine(a):return -a[1],-a[0]
def square(a):return (0 if a[0]<=0<=a[1] else min(a[0]*a[0],a[1]*a[1])),max(a[0]*a[0],a[1]*a[1])
def sqrt_interval(a):
 need(0<=a[0]<=a[1],'positive interval for sqrt')
 lo=isqrt((a[0].numerator*DEN*DEN)//a[0].denominator)
 hi=isqrt((a[1].numerator*DEN*DEN)//a[1].denominator)+1
 return Q(lo,DEN),Q(hi,DEN)
SQ3=sqrt_interval((Q(3),Q(3)))
def ki(a):return ia((a[0],a[0]),im((a[1],a[1]),SQ3))
def polynomial_axis(p,axis):
 a,b,j=p;z={0:a[axis]}
 if j>=0:z[1<<j]=b[axis]
 return {m:c for m,c in z.items() if c!=Z}
def padd(a,b):
 z=dict(a)
 for m,c in b.items():z[m]=add(z.get(m,Z),c)
 return {m:c for m,c in z.items() if c!=Z}
def pneg(a):return {m:neg(c) for m,c in a.items()}
def psquare(a,roots):
 z={}
 for i,c in a.items():
  for j,d in a.items():
   v=mul(c,d);common=i&j
   for h,r in enumerate(roots):
    if common&(1<<h):v=mul(v,r)
   m=i^j;z[m]=add(z.get(m,Z),v)
 return {m:c for m,c in z.items() if c!=Z}
def exact_unit(p,q,roots):
 z={}
 for axis in (0,1):z=padd(z,psquare(padd(polynomial_axis(p,axis),pneg(polynomial_axis(q,axis))),roots))
 return z=={0:ONE}

def verify(geometry,cert):
 need(type(geometry) is dict and set(geometry)=={'roots','points'},'geometry schema')
 roots=[parse_k(r) for r in geometry['roots']];need(all(sg(x)>0 for x in roots),'positive physical roots');ris=[sqrt_interval(ki(x)) for x in roots]
 points=[];boxes=[]
 for row in geometry['points']:
  need(type(row) is list and len(row)==3 and type(row[2]) is int and -1<=row[2]<len(roots),'point format')
  a,b,j=parse_c(row[0]),parse_c(row[1]),row[2]
  need(j>=0 or b==(Z,Z),'base point format');points.append((a,b,j))
  boxes.append(tuple(ki(a[h]) if j<0 else ia(ki(a[h]),im(ki(b[h]),ris[j])) for h in (0,1)))
 n=len(points);need(n<=400,'support cap');edges=[];adj=[set() for _ in points];separation=[];nonedge_gaps=[]
 for i,j in combinations(range(n),2):
  d=[ia(boxes[i][h],ine(boxes[j][h])) for h in (0,1)]
  gaps=[max(Q(0),v[0],-v[1]) for v in d];need(max(gaps)>0,'distinct physical point boxes');separation.append(max(gaps))
  q=ia(square(d[0]),square(d[1]))
  if q[0]<=1<=q[1]:
   need(exact_unit(points[i],points[j],roots),'interval ambiguity at possible edge')
   edges.append((i,j));adj[i].add(j);adj[j].add(i)
  else:nonedge_gaps.append(max(q[0]-1,1-q[1]))
 # Independently construct the base kernel; completeness of boundary follows
 # from intersection counts, without trusting the producer's square-root formula.
 zero=(Z,Z);one=(ONE,Z);omega=(k(Q(1,2)),k(0,Q(1,2)));r=(k(Q(3,5)),k(Q(4,5)));t=cm(cs(one,r),omega);D=[zero,one,t,ca(t,r)]
 need(len(set(D))==4 and norm(r)==ONE,'unit paired centres')
 need(all(norm(cs(omega,d))==ONE for d in D),'common unit neighbour')
 U=[one]
 for _ in range(5):U.append(cm(U[-1],omega))
 directions=set(U+[cm(r,u) for u in U]);need(len(directions)==12,'two direction orbits')
 P=set(ca(d,u) for d in D for u in directions);need(len(P)<=48 and set(D)<=P,'kernel budget')
 lookup={a:i for i,(a,b,j) in enumerate(points) if j<0}
 need(all(x in lookup for x in P),'every kernel point present');pi={lookup[x] for x in P};di=[lookup[d] for d in D]
 used=set(pi);counts={0:0,1:0,2:0};incidences=0
 for x in P-set(D):
  i=lookup[x]
  for h,d in enumerate(D):
   q=norm(cs(x,d));need(sg(q)>0,'distinct circle centres')
   expected=0 if sg(sub(q,k(4)))>0 else (1 if q==k(4) else 2)
   actual=adj[i]&adj[di[h]];need(len(actual)==expected,'complete boundary intersection count')
   used|=actual;counts[expected]+=1;incidences+=expected
 need(used==set(range(n)),'every listed point belongs to declared support')
 # The signed self-incidence makes F_{00,11,1} vanish with d=v, q=w.
 e=cs(D[3],one);v=cm((omega[0],neg(omega[1])),e)
 need(v==t and cs(omega,one)==cm(omega,omega),'exact exceptional incidence')
 need(ca(D[0],D[1])!=ca(D[2],D[3]),'not shared midpoint')
 cross=[norm(cs(D[j],D[i])) for i in (0,1) for j in (2,3)]
 need(cross==[k(Q(4,5)),k(Q(7,5),Q(4,5)),k(Q(7,5),-Q(4,5)),k(Q(4,5))],'exact cross distances')
 need(all(sg(q)>0 and sg(sub(q,k(4)))<0 and q not in (ONE,k(3)) for q in cross),'regular, no dropped clause')
 need(set(cert)=={'four_word','five_word','vertices','edges','coordinate_sha256','edge_sha256'},'colour certificate schema')
 need(cert['vertices']==n and cert['edges']==len(edges),'physical counts')
 need(cert['coordinate_sha256']==digest(geometry) and cert['edge_sha256']==digest(edges),'canonical hashes')
 for key,alphabet in [('four_word','0123'),('five_word','01234')]:
  w=cert[key];need(type(w) is str and len(w)==n and set(w)==set(alphabet),'word alphabet/length')
  need(all(w[i]!=w[j] for i,j in edges),'proper '+key)
 return {'verified':True,'vertices':n,'edges':len(edges),'kernel_vertices':len(P),'kernel_edges':sum(i in pi and j in pi for i,j in edges),'boundary_added_vertices':n-len(P),'all_pairs_checked':n*(n-1)//2,'interval_bits':BITS,'minimum_coordinate_box_separation':str(min(separation)),'minimum_nonedge_squared_distance_gap':str(min(nonedge_gaps)),'boundary_circle_pairs':sum(counts.values()),'circle_pair_counts':counts,'boundary_root_incidences':incidences,'exact_exceptional_incidence':True,'not_shared_midpoint':True,'cross_distances_regular':True,'complete_support_verified_by_intersection_counts':True,'ordinary_four_colourable':True,'proper_five_word':True,'record_certified':False,'coordinate_sha256':digest(geometry),'edge_sha256':digest(edges)}

def main():
 p=argparse.ArgumentParser();p.add_argument('--check-expected',action='store_true');a=p.parse_args()
 out=verify(json.loads((HERE/'geometry_certificate.json').read_text()),json.loads((HERE/'certificate.json').read_text()))
 if a.check_expected:need(json.loads(json.dumps(out))==json.loads((HERE/'EXPECTED.json').read_text()),'expected result')
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
