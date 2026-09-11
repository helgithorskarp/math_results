"""Complete marked-trace coloring certificates for 34 edges."""
import sys,time,json
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations,combinations
from math import comb
base=Path(__file__).resolve().parents[1]
sys.path.append(str(base/'link_envelopes'))
from bounds import M,envelope_bound
from forest import tail
from star_envelope import envelope

def row_types(x,order):
 s=(len(x)-1).bit_length();out=[]
 for j,u in enumerate(order):
  left=sum(1<<i for i in order[:j]);right=sum(1<<i for i in order[j+1:]);mark=1<<u
  rows=[]
  for A,n in enumerate(x):
   if A&mark:
    f=(1 if A&~(left|mark)==0 else 0)|(2 if A&~(right|mark)==0 else 0)
    rows.extend([(5-A.bit_count(),f)]*n)
  out.append(tuple(sorted(rows)))
 return tuple(out)

@lru_cache(None)
def pivot_basic(N,L,rows):
 den=comb(N,L)
 left=sum(comb(N-a,L-a) if 0<=L-a<=N-a else 0 for a,f in rows if f&1)
 right=sum(comb(N-a,L) if L<=N-a else 0 for a,f in rows if f&2)
 pair=0
 for i,(a,fi) in enumerate(rows):
  for j,(b,fj) in enumerate(rows):
   if i!=j and fi&1 and fj&2 and 0<=L-a<=N-a-b:pair+=comb(N-a-b,L-a)
 b=min(left,right,pair,den)
 ee=envelope(rows,N,L,max_excess=4)
 if ee is not None:b=min(b,ee[0])
 return F(b,den)


KNOWN={};USED=set()
for z in json.loads((Path(__file__).with_name("certificates.json")).read_text()):
 KNOWN[z["N"],z["L"],tuple(map(tuple,z["rows"]))]=z
from itertools import product
def admissible(v,x):
 s=(len(x)-1).bit_length();N=v-s
 if any(n and A.bit_count()>5 for A,n in enumerate(x)):return False
 for i in range(s):
  if sum(n*(5-A.bit_count()) for A,n in enumerate(x) if A>>i&1)<N:return False
  for j in range(i):
   if sum(n for A,n in enumerate(x) if A>>i&1 and A>>j&1)<1:return False
 return sum(n*comb(5-A.bit_count(),2) for A,n in enumerate(x) if A.bit_count()<=3)>=comb(N,2)

@lru_cache(None)
def pv(N,L,rows):
 b=pivot_basic(N,L,rows);key=N,L,rows
 if key in KNOWN and F(KNOWN[key]['bound'])<b:return F(KNOWN[key]['bound']),key
 return b,None
@lru_cache(None)
def good(v,x):
 s=(len(x)-1).bit_length()
 for i in range(s):
  d=sum(n for A,n in enumerate(x) if A>>i&1);key=v-1,(v-1)//2,((4,3),)*d
  if key in KNOWN and tail(v-1,(v-1)//2,5,34-d)+F(KNOWN[key]['bound'])<1:
   USED.add(key);return True
 q,den=M.bound(v,x)
 if q<den:return True
 if s>1:
  for i in range(s):
   if good(v,M.reindex(x,tuple(j for j in range(s) if i!=j))):return True
 N=v-s;L=N//2
 for order in permutations(range(s)):
  vals=[pv(N,L,r) for r in row_types(x,order)]
  if tail(N,L,5,x[0])+sum(z[0] for z in vals)<1:
   USED.update(z[1] for z in vals if z[1] is not None);return True
 # Existing exact marked-pivot bound retains its tighter individual free-position minima.
 for order in permutations(range(s)):
  if envelope_bound(v,M.reindex(x,order),max_excess=4)<1:return True
 return False

def pair2_four():
 ts=list(combinations(range(4),3));out=[]
 for q in range(3):
  for vals in product(range(3),repeat=4):
   x=[0]*16;x[15]=q
   for S,t in zip(ts,vals):x[sum(1<<i for i in S)]=t
   for i,j in combinations(range(4),2):x[(1<<i)|(1<<j)]=2-q-sum(t for S,t in zip(ts,vals) if i in S and j in S)
   if min(x)<0:continue
   for i in range(4):x[1<<i]=7-sum(x[A] for A in range(16) if A.bit_count()>=2 and A>>i&1)
   x[0]=34-sum(x)
   if min(x)>=0:out.append(tuple(x))
 return out

def pbd_four(degree):
 out=[]
 for blocks in [[(i,j) for i,j in combinations(range(4),2)],[(0,1,2),(0,3),(1,3),(2,3)],[(0,1,2,3)]]:
  x=[0]*16
  for S in blocks:x[sum(1<<i for i in S)]=1
  for i in range(4):x[1<<i]=degree-sum(i in S for S in blocks)
  x[0]=34-sum(x);out.append(tuple(x))
 return out
