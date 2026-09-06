"""Positive extension certificate for the full108-point exterior union."""
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement,product,permutations
from collections import Counter
from pathlib import Path
import argparse,hashlib,json,time

def need(ok,message):
 if not ok:raise ValueError(message)

Z=(F(0),)*4
ONE=(F(1),F(0),F(0),F(0))
def scalar(x):return (F(x),F(0),F(0),F(0))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 r=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   common=i&j
   r[i^j]+=x*y*(3 if common&1 else 1)*(11 if common&2 else 1)
 return tuple(r)
def inv(a):
 c=tuple(x*(-1 if i&2 else 1) for i,x in enumerate(a))
 n=mul(a,c);need(n[2:]==Z[2:],"norm subfield")
 cc=tuple(x*(-1 if i&1 else 1) for i,x in enumerate(n))
 q=mul(n,cc);need(q[1:]==Z[1:] and q[0],"nonzero norm")
 return tuple(x/q[0] for x in mul(c,cc))
def div(a,b):return mul(a,inv(b))
def pa(a,b):return (add(a[0],b[0]),add(a[1],b[1]))
def ps(a,b):return (sub(a[0],b[0]),sub(a[1],b[1]))
def pm(a,b):return (sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0])))
def norm(a):return add(mul(a[0],a[0]),mul(a[1],a[1]))
def det(a,b):return sub(mul(a[0],b[1]),mul(a[1],b[0]))
O=(Z,Z);R=(scalar(F(1,2)),(F(0),F(1,2),F(0),F(0)))
D=[O,(ONE,Z),R]
U=[(ONE,Z)]
for _ in range(5):U.append(pm(U[-1],R))
def orbit(z):return [pm(z,r) for r in U]
def canon(z):return min(orbit(z))
def serial(z):return [[[x.numerator,x.denominator] for x in v] for v in z]


def encode(z):
 values=[12*x for axis in z for x in axis]
 need(all(x.denominator==1 for x in values),'coordinate denominator')
 return [int(x) for x in values]


PARENT = Path(__file__).resolve().parent.parent/'hadwiger_nelson_triangle_coupled_orbits/certificate.json'
PARENT_SHA = '8680dc794ddb0543fd89f93fa61e6119521ebba51c422a74c4eae0dcf7f5a23a'

def decode(v):
 need(len(v)==8 and all(type(x) is int for x in v),'parent coordinate')
 return (tuple(F(x,12) for x in v[:4]),tuple(F(x,12) for x in v[4:]))

STATES=[s for s in permutations(range(4),3) if all(s[i]!=i for i in range(3))]
COMPAT=[[all(a[i]!=b[i] for i in range(3)) for b in STATES] for a in STATES]

def cycle_oracle(forbidden):
 masks=[set(range(4))-{i} for i in range(3) for _ in range(6)]
 for v,c in forbidden:masks[v].discard(c)
 allowed=[[s for s,p in enumerate(STATES) if all(p[i] in masks[6*i+j] for i in range(3))] for j in range(6)]
 for start in allowed[0]:
  paths={start:[start]}
  for j in range(1,6):
   new={}
   for t in allowed[j]:
    for prev,path in paths.items():
     if COMPAT[prev][t]:new[t]=path+[t];break
   paths=new
  for last,path in paths.items():
   if COMPAT[last][start]:return [STATES[path[j]][i] for i in range(3) for j in range(6)]
 return None

def generate():
 raw=PARENT.read_bytes()
 need(hashlib.sha256(raw).hexdigest()==PARENT_SHA,'parent certificate hash')
 parent=json.loads(raw)
 V=list(map(decode,parent['vertices']));idx={v:i for i,v in enumerate(V)}
 normals=list(map(decode,parent['normal_representatives']))
 patch={pa(d,r) for d in D for r in U}
 dirs=list(map(decode,parent['directions']))
 generic={pa(d,r) for u in dirs if u not in U for d in D for r in orbit(u)}
 exterior=[v for v in V if v not in patch|generic]
 need(len(exterior)==108,'full exterior support')
 groups=[[] for n in normals]
 for w in exterior:
  for i,d in enumerate(D):
   a=ps(w,d);n=canon(a)
   groups[normals.index(n)].append([idx[w],i,orbit(n).index(a)])
 rows=[]
 for h,events in enumerate(groups):
  forbidden=[(6*i+j,parent['colouring'][w]) for w,i,j in events]
  colour=cycle_oracle(forbidden)
  need(colour is not None,'fixed-colouring extension unresolved')
  rows.append({'class':h,'events':events,'colouring':colour})
 return {'parent_certificate_sha256':PARENT_SHA,'blocks':rows,
  'moser_spindle':{'root':0,'tips':[22,35],'middle_pairs':[[1,8],[4,14]]}}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);parser.add_argument('--discover',action='store_true');a=parser.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 data=generate();raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
 if not a.discover:need(raw==(Path(__file__).parent/'certificate.json').read_bytes(),'published certificate mismatch')
 (out/'certificate.json').write_bytes(raw)
 report={'status':'PASS','certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start,'native_solver_calls':0}
 (out/'build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
