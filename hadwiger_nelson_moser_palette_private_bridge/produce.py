"""Regenerate one frozen exact physical graph and its complete terminal relation."""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import sys
import argparse
from hashlib import sha256
from math import factorial

# Basis s^a t^b y^c, s^2=3,t^2=11,y^2=2-s/2, a,b,c in {0,1}.
def scalar(x): return (F(x),)+(F(0),)*7
Z=scalar(0); ONE=scalar(1)
S=(F(0),F(1))+(F(0),)*6
T=(F(0),)*2+(F(1),)+(F(0),)*5
Y=(F(0),)*4+(F(1),)+(F(0),)*3
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,k):return tuple(x*k for x in a)
def mul(a,b):
 out=[F(0)]*8
 for i,x in enumerate(a):
  if not x:continue
  for j,y in enumerate(b):
   if not y:continue
   k=i^j;coef=x*y*(3 if i&j&1 else 1)*(11 if i&j&2 else 1)
   if i&j&4:
    out[k]+=2*coef
    out[k^1]-=coef*F(3 if k&1 else 1,2)
   else:out[k]+=coef
 return tuple(out)
def psub(p,q):return sub(p[0],q[0]),sub(p[1],q[1])
def padd(p,q):return add(p[0],q[0]),add(p[1],q[1])
def cmul(p,q):return sub(mul(p[0],q[0]),mul(p[1],q[1])),add(mul(p[0],q[1]),mul(p[1],q[0]))
def norm(p):return add(mul(p[0],p[0]),mul(p[1],p[1]))

MROWS=((0,0,0,0),(12,0,0,0),(6,0,6,0),(18,0,6,0),(10,0,0,2),(5,-1,5,1),(15,-1,5,3),(6,0,-6,0),(12,0,12,0),(20,0,0,4),(-5,-1,5,-1))
def geometry():
 m=[(scale(add(scalar(a),scale(mul(S,T),b)),F(1,12)),scale(add(scale(S,c),scale(T,d)),F(1,12))) for a,b,c,d in MROWS]
 caps=[(Z,Z),(scale(add(ONE,S),F(1,2)),Y),(scale(sub(ONE,S),F(1,2)),Y),(ONE,Z)]
 p=caps[1:3]
 for a,b in zip(caps,caps[1:]):
  dx,dy=psub(b,a);mid=tuple(scale(v,F(1,2)) for v in padd(a,b));off=(scale(mul(neg(dy),S),F(1,6)),scale(mul(dx,S),F(1,6)))
  p.extend([padd(mid,off),psub(mid,off)])
 u=(scale(S,F(-1,2)),scalar(F(-1,2)))
 p=[padd((Z,ONE),cmul(u,psub(v,caps[1]))) for v in p]
 raw=m+p;pts=list(dict.fromkeys(raw));mp=[pts.index(v) for v in raw]
 edges=[(i,j) for i,j in combinations(range(len(pts)),2) if norm(psub(pts[i],pts[j]))==ONE]
 inherited=set()
 for block in [mp[:11],mp[11:]]:
  for i,j in combinations(block,2):
   if norm(psub(pts[i],pts[j]))==ONE:inherited.add(tuple(sorted((i,j))))
 return pts,mp,edges,sorted(inherited)

def solve(n,edges,k,pins=()):
 adj=[set() for _ in range(n)]
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 word=[-1]*n
 for a,c in pins:
  if word[a]>=0 and word[a]!=c:return None
  word[a]=c
 if any(word[a]>=0 and word[a]==word[b] for a,b in edges):return None
 def rec():
  free=[i for i,c in enumerate(word) if c<0]
  if not free:return tuple(word)
  domains={i:[c for c in range(k) if all(word[j]!=c for j in adj[i])] for i in free}
  v=min(free,key=lambda i:(len(domains[i]),-len(adj[i]),i))
  for c in domains[v]:
   word[v]=c;r=rec()
   if r:return r
  word[v]=-1
  return None
 return rec()

def patterns(n):
 def rec(w,hi):
  if len(w)==n:
   yield tuple(w);return
  for c in range(min(hi+1,3)+1):
   yield from rec(w+[c],max(hi,c))
 yield from rec([], -1)

def isolated(w):
 a,b,c,d=w[:4];e=[set(w[4+2*i:6+2*i]) for i in range(3)]
 return not (a==b and c==d) and all(len(x)==2 for x in e) and bool(e[0]&e[1]) and bool(e[1]&e[2])

def digest(x):return sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def produce():
 pts,mp,edges,base=geometry();term=[mp[i] for i in (7,8,9,10,13,14,15,16,17,18)]
 if len(pts)!=19 or mp!=list(range(19)):raise ValueError('frozen collision gate')
 if len(edges)!=34 or len(base)!=30:raise ValueError('frozen contact gate')
 if sorted(set(edges)-set(base))!=[(0,11),(1,16),(2,15),(3,12)]:raise ValueError('frozen new edges')
 counts={'all_canonical_patterns':0,'baseline_canonical':0,'full_canonical':0,'gain_canonical':0,'baseline_named':0,'full_named':0,'gain_named':0}
 stream=sha256();gains=[];marg_m=set();marg_p=set()
 def canon(word):
  names={};return tuple(names.setdefault(c,len(names)) for c in word)
 for w in patterns(10):
  counts['all_canonical_patterns']+=1;b=isolated(w);full=False
  weight=factorial(4)//factorial(4-(max(w)+1))
  if b:
   counts['baseline_canonical']+=1;counts['baseline_named']+=weight
   word=solve(19,edges,4,zip(term,w));full=word is not None
   if full:
    if any(word[a]==word[b] for a,b in edges) or tuple(word[t] for t in term)!=w:raise ValueError('producer witness')
    counts['full_canonical']+=1;counts['full_named']+=weight
    marg_m.add(canon(w[:4]));marg_p.add(canon(w[4:]))
   else:
    gains.append(''.join(map(str,w)));counts['gain_canonical']+=1;counts['gain_named']+=weight
  stream.update((''.join(map(str,w))+f':{int(b)}{int(full)}\n').encode())
 four=solve(19,edges,4);five=list(four);five[0]=4
 witness=(0,0,1,2,2,3,0,2,0,1);baseline=solve(19,base,4,zip(term,witness))
 if solve(19,edges,4,zip(term,witness)) is not None:raise ValueError('gain witness')
 coordinates=[[[str(x) for x in v] for v in p] for p in pts]
 certificate={'schema':'moser-palette-private-bridge-v1','basis':'s^a*t^b*y^c indexed a+2b+4c; s=sqrt3,t=sqrt11,y=sqrt((4-s)/2), all positive','coordinates':coordinates,'edges':edges,'inherited_edges':base,'new_edges':sorted(set(edges)-set(base)),'terminals':term,'four_colouring':four,'five_colouring':five,'newly_forbidden_terminal_word':witness,'isolated_extension':baseline,'relation':counts|{'canonical_truth_stream_sha256':stream.hexdigest(),'gain_words_sha256':digest(gains),'full_moser_projection_canonical':len(marg_m),'full_palette_projection_canonical':len(marg_p)}}
 return certificate

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
 if args.out.exists():raise ValueError('output already exists')
 result=produce();args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result['relation'],indent=2,sort_keys=True))
