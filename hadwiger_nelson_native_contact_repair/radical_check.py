"""Independent Cartesian radical algebra and geometric reconstruction.

Coordinates use the bit-mask basis of Q(sqrt3,sqrt5,sqrt11).
No discovery generator, scalar norm formula, CAS or SAT package is imported.
"""
from pathlib import Path
from hashlib import sha256
from itertools import combinations
RAD=(1,3,5,15,11,33,55,165)
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv'
PIN='4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02'

def require(test,msg):
 if not test:raise ValueError(msg)

def multiply(a,b):
 out=[0]*8
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:out[i^j]+=x*y*RAD[i&j]
 return tuple(out)
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def norm16(p):return plus(multiply(p[:8],p[:8]),multiply(p[8:],p[8:]))
def short(p):
 val=norm16(p);require(all(not val[k] for k in (1,2,3,4,6,7)),'non-native norm')
 a,b=val[0]-576,val[5]
 if b==0:return a<=0
 if b>0:return a<0 and a*a>=33*b*b
 return a<=0 or a*a<=33*b*b

def source():
 raw=SOURCE.read_bytes();require(sha256(raw).hexdigest()==PIN,'source pin')
 out=[tuple(map(int,s.split())) for s in raw.decode().splitlines() if s and not s.startswith('#')]
 require(len(out)==159 and len(set(out))==159,'source points')
 require(all(len(p)==16 for p in out),'source format')
 return out

def generate(truncate=True):
 A=source();dirs=set()
 for a,b in combinations(A,2):
  d=minus(a,b)
  if norm16(d)==(144,0,0,0,0,0,0,0):dirs.update((d,tuple(-x for x in d)))
 require(len(dirs)==30,'directions')
 candidates=set(A)
 for a in A:
  for d in dirs:candidates.add(plus(a,d))
 L=sorted((p for p in candidates if not truncate or short(p)),key=lambda p:(p[0],p[5],p[9],p[12]))
 native=[tuple(8*x for x in p) for p in L]
 q=(0,0,0,1,0,0,0,0) # sqrt15
 images=[]
 for p in L:
  x,y=p[:8],p[8:]
  images.append(minus(tuple(7*v for v in x),multiply(q,y))+plus(multiply(q,x),tuple(7*v for v in y)))
 pts=list(dict.fromkeys(native+images))
 require((len(L),len(pts))==((1525,3049) if truncate else (1960,3919)),'host sizes')
 # Convert only the display format, after Cartesian construction.
 compact=[(p[0],p[2],p[5],p[7],p[9],p[11],p[12],p[14]) for p in pts]
 require(all(all(not p[i] for i in (1,3,4,6,8,10,13,15)) for p in pts),'compact subspace')
 return compact

# Generate every coefficient of x^2+y^2 from basis multiplication.
POSITIONS=((0,2,5,7),(1,3,4,6))
TERMS=[[] for _ in range(8)]
for offset,pos in ((0,POSITIONS[0]),(4,POSITIONS[1])):
 for i,si in enumerate(pos):
  for j in range(i+1):
   sj=pos[j];TERMS[si^sj].append((offset+i,offset+j,RAD[si&sj]*(1 if i==j else 2)))

def norm_compact(v):
 return tuple(sum(c*v[i]*v[j] for i,j,c in ts) for ts in TERMS)

def unit(v):
 if sum(c*v[i]*v[j] for i,j,c in TERMS[0])!=9216:return False
 return all(sum(c*v[i]*v[j] for i,j,c in TERMS[k])==0 for k in range(1,8) if TERMS[k])

def edges(pts):
 out=[]
 for i,p in enumerate(pts):
  for j in range(i):
   if unit(minus(p,pts[j])):out.append((j,i))
 return out

def encode(n,edges):
 rows=[];adj=[set() for _ in range(n)]
 for vertex in range(n):
  variables=[4*vertex+colour+1 for colour in range(4)];rows.append(variables)
  for a in range(4):
   for b in range(a):rows.append([-variables[a],-variables[b]])
 for a,b in edges:
  adj[a].add(b);adj[b].add(a)
  for colour in range(4):rows.append([-(4*a+colour+1),-(4*b+colour+1)])
 triangle=None
 for a,b in edges:
  cs=[c for c in range(b+1,n) if c in adj[a] and c in adj[b]]
  if cs:triangle=(a,b,cs[0]);break
 require(triangle is not None,'triangle exists')
 rows.extend([[4*v+c+1] for c,v in enumerate(triangle)])
 return f'p cnf {4*n} {len(rows)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in rows),triangle
