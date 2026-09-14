"""Controls for square-root completeness, field arithmetic and the direct audit."""
from fractions import Fraction as F
from itertools import product,combinations
from math import isqrt
from pathlib import Path
import argparse,json,subprocess
import model as m
from verify import flatmul,need

def altmul(a,b):
 z=[0]*len(a)
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   t=x*y
   if i&j&1:t*=33
   if i&j&2:t*=5
   z[i^j]+=t
 return tuple(z)
def altinv(a):
 if len(a)==1:return(1/F(a[0]),)
 h=len(a)//2;d=33 if h==1 else 5;x,y=a[:h],a[h:]
 ni=altinv(m.sub(altmul(x,x),m.scale(altmul(y,y),d)))
 return altmul(x,ni)+m.neg(altmul(y,ni))
def altsqrt(a):
 if not any(a):return a
 if len(a)==1:
  q=F(a[0])
  if q<0:return None
  n,d=isqrt(q.numerator),isqrt(q.denominator)
  return(F(n,d),)if n*n==q.numerator and d*d==q.denominator else None
 h=len(a)//2;d=33 if h==1 else 5;A,B=a[:h],a[h:];zero=(F(0),)*h
 if not any(B):
  x=altsqrt(A)
  if x is not None:return x+zero
  y=altsqrt(m.scale(A,F(1,d)))
  return zero+y if y is not None else None
 t=altsqrt(m.sub(altmul(A,A),m.scale(altmul(B,B),d)))
 if t is None:return None
 for u in(t,m.neg(t)):
  x=altsqrt(m.scale(m.add(A,u),F(1,2)))
  if x is not None and any(x):
   y=altmul(B,altinv(m.scale(x,2)));r=x+y
   if altmul(r,r)==a:return r
 return None

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--audit-binary',type=Path,required=True);args=ap.parse_args()
 basis=[tuple(int(i==j)for i in range(8))for j in range(8)]
 for a,b in product(basis,repeat=2):need(flatmul(a,b)==m.mul(a,b),'basis product')
 squares=0
 for a in product(range(-2,3),repeat=4):
  r=tuple(F(x,3)for x in a);s=m.mul(r,r);q=m.square_root(s)
  need(q is not None and m.mul(q,q)==s,'missed square');squares+=1
 den,M,B=m.construction();N=lambda G:{m.norm(m.sub(a,b))for a,b in combinations(G,2)}
 checks=0
 for a,b in product(N(B),N(M)):
  S=m.sub(m.add(a,b),(den*den,0,0,0));d=m.scale(m.sub(m.scale(m.mul(a,b),4),m.mul(S,S)),F(1,3))
  x=m.square_root(d);y=altsqrt((d[0],d[2],d[1],d[3]))
  need((x is None)==(y is None),'different real towers disagree')
  if x is not None:need(m.mul(x,x)==d,'returned root invalid')
  checks+=1
 def fixture(kind):
  points=[([0]*8,0),([1]+[0]*7,1)]+[([0]*8,0)]*341
  D=1;n=2;E=[(0,1)]
  if kind=='unit_missing':E=[]
  if kind=='spurious':points[1]=([2]+[0]*7,1)
  if kind=='colour':points[1]=([1]+[0]*7,0)
  if kind=='collision_colour':points[-1]=([0]*8,1)
  if kind=='count':n=3
  if kind=='overflow':points[1]=([1<<50]+[0]*7,1)
  if kind=='denominator':D=0
  return f'1\n343 {D} {n} {len(E)}\n'+''.join(' '.join(map(str,p))+f' {c}\n'for p,c in points)+''.join(f'{a} {b}\n'for a,b in E)
 for kind in ['valid','unit_missing','spurious','colour','collision_colour','count','overflow','denominator']:
  r=subprocess.run([str(args.audit_binary.resolve())],input=fixture(kind),text=True,capture_output=True)
  need((r.returncode==0)==(kind=='valid'),'audit corruption '+kind)
 print(json.dumps({'status':'CONTROLS_PASS','basis_products':64,'constructed_squares':squares,'different_tower_discriminants':checks,'positive_audit_control':1,'audit_corruptions_rejected':7},indent=2,sort_keys=True))
if __name__=='__main__':main()
