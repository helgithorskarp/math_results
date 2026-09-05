#!/usr/bin/env python3
"""Known circles, exact field inverses, and the complete two-list criterion."""
from itertools import product,combinations
from fractions import Fraction as Q
import json
import geometry as G
import verify as V

def centre(points):
 p,q,r=points;dx,dy=G.sub(q[0],p[0]),G.sub(q[1],p[1]);ex,ey=G.sub(r[0],p[0]),G.sub(r[1],p[1])
 a,b,c=G.norm(dx,dy),G.norm(ex,ey),G.norm(G.sub(dx,ex),G.sub(dy,ey))
 h=G.sub(G.scale(G.add(G.add(G.mul(a,b),G.mul(a,c)),G.mul(b,c)),2),G.add(G.add(G.mul(a,a),G.mul(b,b)),G.mul(c,c)))
 if G.mul(G.mul(a,b),c)!=h:return None
 det=G.sub(G.mul(dx,ey),G.mul(ex,dy))
 if det==G.ZERO:return None
 inv=G.inv(G.scale(det,6))
 x=G.mul(G.scale(G.sub(G.mul(a,ey),G.mul(b,dy)),3),inv);y=G.mul(G.sub(G.mul(dx,b),G.mul(ex,a)),inv)
 return G.add(p[0],x),G.add(p[1],y)

def main():
 inverses=0
 for a in product((-1,0,1),repeat=4):
  if a==G.ZERO:continue
  assert G.mul(a,G.inv(a))==G.ONE;inverses+=1
 try:G.inv(G.ZERO)
 except ZeroDivisionError:pass
 else:raise AssertionError('zero inverse accepted')
 O=G.ZERO;one=G.ONE;half=(Q(1,2),0,0,0)
 circle=[(one,O),(G.neg(one),O),(half,half)]
 assert centre(circle)==(O,O)
 assert centre([(O,O),(one,O),(half,half)]) is None # Equilateral unit sides: radius 1/sqrt(3).
 assert centre([(O,O),(one,O),(G.scale(one,2),O)]) is None
 assert centre([(G.scale(x,2),G.scale(y,2)) for x,y in circle]) is None
 translated=0
 for epsilon in (-1,1):
  u=(-18,-6,-30,6,3*epsilon,0,6*epsilon,epsilon)
  assert G.C.norm(u)==G.C.scale(G.C.ONE,72**2)
  ux=tuple(Q(u[i],72) for i in (0,1,4,5));uy=tuple(Q(u[i],72) for i in (2,3,6,7))
  t=((0,0,1,0),(1,0,0,1));points=[]
  for x,y in circle:
   X=G.add(t[0],G.sub(G.mul(ux,x),G.scale(G.mul(uy,y),3)))
   Y=G.add(t[1],G.add(G.mul(ux,y),G.mul(uy,x)));points.append((X,Y))
  assert centre(points)==t;translated+=1
 checks=0
 for A,B,edge in product(range(16),range(16),(False,True)):
  rule=bool(A and B) and not(edge and A==B and A.bit_count()==1)
  direct=any((not edge) or a!=b for a in range(4) if A>>a&1 for b in range(4) if B>>b&1)
  assert rule==direct;checks+=1
 P=G.host();ds,adj,edges=G.distances(P);rows,summary=G.screen(P,ds,adj,10007,283,6718,limit=32)
 def exact(i,j,k):
  a,b,c=ds[i][j],ds[i][k],ds[j][k]
  h=G.sub(G.scale(G.add(G.add(G.mul(a,b),G.mul(a,c)),G.mul(b,c)),2),G.add(G.add(G.mul(a,a),G.mul(b,b)),G.mul(c,c)))
  return G.mul(G.mul(a,b),c)==G.scale(h,G.D**2)
 expected=[t for t in combinations(range(32),3) if not(adj[t[0]]&adj[t[1]]&adj[t[2]]) and exact(*t)]
 assert [t for t in rows if exact(*t)]==expected
 color=list(map(int,(V.HERE/'host_colors.txt').read_text().strip()));bad=color.copy();bad[edges[0][1]]=bad[edges[0][0]]
 for row in [bad,[4]+color[1:]]:
  try:V.colour_lists(edges,[],[],row)
  except ValueError:pass
  else:raise AssertionError('invalid host colour accepted')
 print(json.dumps({'field_inverse_cases':inverses,'zero_inverse_rejected':True,'circle_fixtures':4,'translated_quadratic_rotations':translated,'complete_two_list_cases':checks,'exact_small_triple_scan':summary['triples'],'small_new_unit_circle_triples':len(expected),'invalid_colourings_rejected':2},indent=2))
if __name__=='__main__':main()
