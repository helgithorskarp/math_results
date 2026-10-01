"""Exact scalar identities; the written graph and Gram premises are external."""
from fractions import Fraction
import json

def run():
 # Target D-degree zero/two and no cycle of length three are written premises.
 s=[x for x in range(23) if x%3==0 and x!=3]
 red=[(330-x)//3 for x in s];blue=[(660+x)//3 for x in s]
 if s!=[0,6,9,12,15,18,21]:raise ValueError('defect counts')
 values=[]
 for x,t,u in zip(s,red,blue):
  if 3*t!=330-x or 3*u!=660+x or t+u!=330:raise ValueError('triangle identities')
  values.append(dict(defect_edges=x,red_triangles=t,blue_triangles=u,red_triangles_one_defect=2*x,red_triangles_no_defect=t-2*x,blue_deficit_mass=66-x,blue_codegree6_edge_lower=55+x))
 # Exact coefficients for eliminating the Gram row direction:
 # z=36q-k1, R1=4d, sum(d)=36, k=q.d.
 if 2*36*4-144!=144:raise ValueError('centered witness coefficients')
 # Nonprincipal eigenvalue bounds follow from |4-3t-t^2|<=6.
 for t in [Fraction(-5),Fraction(-2),Fraction(-1),Fraction(2)]:
  if abs(4-3*t-t*t)!=6:raise ValueError('spectral endpoints')
 return dict(agent='six-reviewer-2',role='independent mathematical reviewer',status='COMPLETE scalar identity checks; ordinary graph/spectral premises unformalized',rows=values,Gram_centered_negative_identity='z=36*q-(q.d)*1; z.d=0; z^T R z=1296*q^T R q-144*(q.d)^2',red_nonprincipal_eigenvalue_intervals=[[-5,-2],[-1,2]],blue_nonprincipal_eigenvalue_intervals=[[-3,0],[1,4]])
if __name__=='__main__':print(json.dumps(run(),indent=2))
