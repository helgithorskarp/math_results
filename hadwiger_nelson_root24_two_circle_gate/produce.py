import json,sys
from pathlib import Path
from itertools import combinations
Z=(0,0,0,0)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def mul(a,b):
 c=[0]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b): c[i^j]+=x*y*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
 return tuple(c)
def cmul(a,b):return (sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0])))
def norm(p): return add(mul(p[0],p[0]),mul(p[1],p[1]))
def psub(a,b): return sub(a[0],b[0]),sub(a[1],b[1])
root=((0,1,0,1),(0,-1,0,1)); q=((4,0,0,0),Z); U=[]
for k in range(24):
 U.append(q)
 a=cmul(q,root); assert all(v%4==0 for t in a for v in t)
 q=tuple(tuple(v//4 for v in t) for t in a)
assert q==U[0] and len(set(U))==24
origin=(Z,Z); d=((0,2,0,2),Z)
labels=[origin,d]+U+[(add(x,d[0]),y) for x,y in U]
pts=list(dict.fromkeys(labels)); E=[]; norms=[]
for i,j in combinations(range(len(pts)),2):
 n=norm(psub(pts[i],pts[j])); norms.append(n)
 if n==(16,0,0,0):E.append((i,j))
print('points edges',len(pts),len(E),flush=True)
colours={origin:0,d:0}
for k,z in enumerate(U):
 for point in [z,(add(z[0],d[0]),z[1])]:
  value=1+(k//4)%2
  if point in colours and colours[point]!=value:
   raise ValueError('Inconsistent collision colour')
  colours[point]=value
same=''.join(str(colours[p]) for p in pts)
other='01'+same[2:].replace('1','3')
for word in [same,other]:
 if not all(word[a]!=word[b] for a,b in E):
  raise ValueError('Formula fails a physical edge')
certificate={'schema':'root24-two-circle-v1','equal_three':same,'different_four':other}
Path(sys.argv[1]).write_text(json.dumps(certificate,indent=2)+'\n')
