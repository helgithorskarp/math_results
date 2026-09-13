"""Exact arithmetic and pinned GMM490 seed. No solver or floating arithmetic."""
from pathlib import Path
import sys,json,hashlib
from functools import lru_cache
from itertools import combinations,product
from collections import Counter,defaultdict
R=Path(__file__).resolve().parents[1]
PIN_FILE=R/'hadwiger_nelson_independent_moser_sum_collisions/arithmetic.py'
PINS=json.loads((Path(__file__).resolve().parent/'SOURCE_PINS.json').read_text())
for rel,h in PINS.items():
 if hashlib.sha256((R/rel).read_bytes()).hexdigest()!=h:raise ValueError('source pin: '+rel)
sys.path.insert(0,str(PIN_FILE.parent))
from arithmetic import *
EZ=(ZERO,ZERO);EO=(ONE,ZERO);ALPHA=(F(0),F(0),F(1),F(0));BETA=(F(0),F(0),F(0),F(1))
def ea(x,y):return add(x[0],y[0]),add(x[1],y[1])
def es(x,y):return sub(x[0],y[0]),sub(x[1],y[1])
def ec(x):return conj(x[0]),conj(x[1])
def sc(x,z):return mul(x[0],z),mul(x[1],z)
def em(x,y):return add(mul(x[0],y[0]),scale(mul(x[1],y[1]),5)),add(mul(x[0],y[1]),mul(x[1],y[0]))
def en(x):return em(x,ec(x))
def ri(x):
 a,b=x;require(a[2:]==b[2:]==(0,0),'real inverse');q=inverse_real(sub(mul(a,a),scale(mul(b,b),5)));return mul(a,q),scale(mul(b,q),-1)
def ei(x):return em(ec(x),ri(en(x)))
def sign0(x):
 a,b,c,d=x;require(c==d==0,'real sign')
 if not a:return (b>0)-(b<0)
 if not b:return (a>0)-(a<0)
 if (a>0)==(b>0):return (a>0)-(a<0)
 z=a*a-33*b*b;return ((a>0)-(a<0))*((z>0)-(z<0))
def sgn(x):
 a,b=x;sa,sb=sign0(a),sign0(b)
 if not sa:return sb
 if not sb:return sa
 return sa if sa==sb else sa*sign0(sub(mul(a,a),scale(mul(b,b),5)))
def sq(x):
 a,b=x;require(a[2:]==b[2:]==(0,0),'real square root')
 if b==ZERO:
  z=sqrt_real(a)
  if z is not None:return z,ZERO
  z=sqrt_real(scale(a,F(1,5)));return None if z is None else(ZERO,z)
 h=sqrt_real(sub(mul(a,a),scale(mul(b,b),5)))
 if h is None:return None
 for eps in(-1,1):
  c=sqrt_real(scale(add(a,scale(h,eps)),F(1,2)))
  if c is not None and c!=ZERO:
   z=c,scale(mul(b,inverse_real(c)),F(1,2));require(em(z,z)==x,'square root identity');return z
 return None

def moser():
 rho=scale(add(ONE,ALPHA),F(1,2));eta=scale(add(scale(ONE,5),BETA),F(1,6))
 return [ZERO,ONE,rho,add(ONE,rho),eta,mul(eta,rho),mul(eta,add(ONE,rho))]
def golomb():
 rows=[(0,0,0,0),(36,0,0,0),(18,0,18,0),(-18,0,18,0),(-36,0,0,0),(-18,0,-18,0),(18,0,-18,0),(6,0,0,2),(-3,-3,3,-1),(-3,3,-3,-1)]
 return [(F(a,36),F(b,36),F(c,36),F(d,12))for a,b,c,d in rows]
def patterns(name):
 M=moser()if name=='M'else golomb();out=[]
 for reflect in range(2):
  A=[conj(z)if reflect else z for z in M]
  for i in range(len(A)):out.append([ZERO]+[sub(A[j],A[i])for j in range(len(A))if j!=i])
 return out

def seed():
 u=(scale(ONE,F(7,8)),scale(ALPHA,F(1,8)));v=(scale(ONE,F(-1,4)),scale(ALPHA,F(1,4)))
 require(en(u)==en(v)==EO,'unit seed phases')
 Q=sorted({ea((g,ZERO),sc(u,m))for g,m in product(golomb(),moser())})
 labels=[ea(q,sc(v,m))for q,m in product(Q,moser())];P=sorted(set(labels));require(len(P)==490,'seed order')
 fixture=json.loads((R/'hadwiger_nelson_mixed_atom_record_search/fixtures.json').read_text())['field_5_GMM_0'];word=fixture['seed_colour_word'];ix={z:i for i,z in enumerate(P)};cs=[None]*len(P)
 for z,c in zip(labels,word):
  require(cs[ix[z]]is None or cs[ix[z]]==c,'seed colour descent');cs[ix[z]]=c
 require(len(labels)==len(word)==490,'seed word order')
 return P,''.join(cs)

def parse(z):return tuple(map(F,z[:4])),tuple(map(F,z[4:]))
def ser(z):return [str(c)for v in z for c in v]
def digest(z):return hashlib.sha256(json.dumps(z,separators=(',',':')).encode()).hexdigest()
