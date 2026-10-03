"""Newton recurrence producer. Whole rational Phi36 records, no native inputs."""
import json,sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from field36 import K,c,I,w,need,real_coeff
# Jets modulo t^4, linear symbols V,B,J. Five slots retain every zero.
slots=[(0,0),(2,0),(3,1),(3,2),(3,3)]
class A:
 def __init__(self,v=0):self.d=dict(v.d)if isinstance(v,A)else{a:K(x)for a,x in v.items()if K(x)!=0}if isinstance(v,dict)else({(0,0):K(v)}if K(v)!=0 else{})
 def __add__(self,o):
  d=dict(self.d)
  for a,x in A(o).d.items():d[a]=d.get(a,K(0))+x
  return A(d)
 __radd__=__add__
 def __neg__(self):return A({a:-x for a,x in self.d.items()})
 def __sub__(self,o):return self+-A(o)
 def __mul__(self,o):
  d={}
  for (a,b),x in self.d.items():
   for (e,f),y in A(o).d.items():
    if a+e<4:
     need(not(b and f),'unsupported symbol product');key=(a+e,b or f);d[key]=d.get(key,K(0))+x*y
  return A(d)
 __rmul__=__mul__
 def __truediv__(self,o):return A({a:x/o for a,x in self.d.items()})
 def __pow__(self,n):
  v=A(1)
  for _ in range(n):v=v*self
  return v
 def encode(self):
  need(set(self.d)<=set(slots),'complete jet slot coverage');return [self.d.get(a,K(0)).encode()for a in slots]
y=1/(3*(1+c));x=K(F(2,3))-y;H=14*y;U=-8*x;k=-7*(1+2*c)/18
P=[A(0),A({(2,0):U,(3,1):I}),A({(2,0):-H,(3,2):I}),A({(3,3):-I})]+[A(0)]*5
e=[A(1)]
for n in range(1,9):e.append(sum(((-1)**(r-1)*e[n-r]*P[r]for r in range(1,n+1)),A(0))/n)
p=[A(0)for _ in range(10)]
for n in range(9):p[9-n]=(-1)**n*e[n]*F(9,9-n)
anchor=A({(0,0):1,(2,0):-1});p[0]=-sum((p[n]*anchor**n for n in range(1,10)),A(0));primitive_record=[a.encode()for a in p]
roots=[];norms=[];rows=[]
for j in range(9):
 r=w**j;jet=-sum((p[n]*r**n for n in range(10)),A(0))/(9*r**8)
 L=jet.d.get((2,0),K(0));v=jet.d.get((3,1),K(0));b=jet.d.get((3,2),K(0));q=jet.d.get((3,3),K(0));W=v*(8*k/7)+b*(2*k)+q
 roots.append({'label':j,'L':L.encode(),'raw':[v.encode(),b.encode(),q.encode()],'W':W.encode()});norms.append(real_coeff(W*W.conj()))
 sin=lambda n:(r**n-(r**n).conj())/(2*I)
 rows.append([sin(1).encode(),sin(2).encode(),sin(6).encode()])
rho=(c-5)/3;alpha=K(F(-527,360))+41*c/90+13*c*c/90;tau=(k+rho)**2/2
Bstar=K(F(2311,108))+4934*c/27-1976*c*c/9;K1=Bstar-alpha*H*H/2;KE=K1+(43*alpha/56+9*tau/14)*H*H
lam=12*(1+c);d=2*c*c-1;w4=1/(c+d);w3=F(2,3)*(7-(1-d)/(c+d));Mstar=-(512+1684*c+1328*c*c)/9;betastar=(86-261*c-172*c*c)/18
M0=Mstar-(1+2*d)/(3*(c+d));beta0=betastar+(2*c-1)/(24*(c+d))
normstar=(16+50*c+40*c*c)/324
scalars={'H':H,'lambda':lam,'k':k,'tau':tau,'KE':KE,'Jstar_squared':9*H**3/14,'Astar_squared':9*H**3*normstar/14,'gamma_squared':2*H*normstar/7,'w3':w3,'w4':w4,'M0':M0,'beta0':beta0,'repair_determinant':12*(c+d)}
# Polynomial identities in eight real v_i and a positive scale b.
def mono(i,n,bn=0):a=[0]*9;a[i]=n;a[8]=bn;return tuple(a)
def plus(p,key,value):p[key]=p.get(key,F(0))+F(value)
polys=[]
for index in range(8):
 p={};zero=(0,)*9
 # Direct expansion of sum(7b-v)(v+b)^2 -(336b^3-sum v^3).
 for i in range(8):
  for va,ba,ca in ((0,1,7),(1,0,-1)):
   for vb,bb,cb in ((2,0,1),(1,1,2),(0,2,1)):
    plus(p,mono(i,va+vb,ba+bb),ca*cb)
  plus(p,mono(i,3),1)
 plus(p,mono(0,0,3),-336)
 # Subtract 5b(sum v^2-56b^2)+13b^2 sum v.
 for i in range(8):plus(p,mono(i,2,1),-5);plus(p,mono(i,1,2),-13)
 plus(p,mono(0,0,3),280)
 need(all(x==0 for x in p.values()),'global polynomial certificate')
 # Squared distance to extremal vector: sum(v+b-8b delta_i)^2.
 q={}
 for i in range(8):
  shift=-7 if i==index else 1
  plus(q,mono(i,2),1);plus(q,mono(i,1,1),2*shift);plus(q,mono(0,0,2),shift*shift)
 plus(q,mono(0,0,2),-112);plus(q,mono(index,1,1),16)
 for i in range(8):plus(q,mono(i,2),-1);plus(q,mono(i,1,1),-2)
 plus(q,mono(0,0,2),56)
 need(all(x==0 for x in q.values()),'all-index distance identity')
 polys.append({'index':index,'deficit_residual':[[list(a),str(p[a])]for a in sorted(p)],'distance_residual':[[list(a),str(q[a])]for a in sorted(q)]})
out={'schema':'cubic-motion-audit-v1','slots':[list(a)for a in slots],'elementary':[a.encode()for a in e],'primitive':primitive_record, 'roots':roots,'norms':norms,'active_rows':rows,'scalars':{a:real_coeff(v)for a,v in scalars.items()},'multiplicity_ratios':[str(F((8-2*r)**2,8*r*(8-r)))for r in range(1,8)],'polynomial_certificates':polys}
if len(sys.argv)!=2:raise ValueError('usage produce.py OUTPUT')
Path(sys.argv[1]).write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps({'status':'produced','roots':9,'elementary_rows':9,'primitive_rows':10,'field_coordinates':12,'certificate_indices':8}))
