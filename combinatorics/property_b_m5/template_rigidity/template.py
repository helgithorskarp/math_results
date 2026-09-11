"""Unequal-core AHT templates and the exact coloring criterion in proof.md."""
from itertools import combinations

def bitset(xs):return sum(1<<i for i in xs)
def transversal(r,w,t):return sum(1<<(w+2*i+((t>>i)&1)) for i in range(r))
def edges(r,w,cores,T):
 assert r>=3 and len(cores)==r
 out=[]
 for i,C in enumerate(cores):
  for E in C:
   assert E.bit_count()==r-2 and E>>w==0
   out.append(E|(3<<(w+2*i)))
 out.extend(transversal(r,w,t) for t in T)
 assert len(out)==len(set(out))
 return tuple(sorted(out))

def proper(r,w,es,red):
 full=(1<<(w+2*r))-1
 return all(E&red and E&(full^red) for E in es)

def decide(r,w,cores,T):
 """Return (noncolorable, witness); a negative result supplies a proper coloring."""
 T=set(T);allwords=(1<<r)-1;X=(1<<w)-1
 for t in range(1<<r):
  if t not in T and (t^allwords) not in T:
   return False,X|transversal(r,w,t)
 for t in range(1<<r):
  for i in range(r):
   if t not in T and (t^(1<<i)) not in T:
    return False,transversal(r,w,t)|(3<<(w+2*i))
 for S in range(1<<w):
  left=[i for i,C in enumerate(cores) if not any(E&S==E for E in C)]
  right=[i for i,C in enumerate(cores) if not any(E&(X^S)==E for E in C)]
  for i in left:
   for j in right:
    if i==j:continue
    red=S|(3<<(w+2*i))
    for h in range(r):
     if h not in [i,j]:red|=1<<(w+2*h)
    return False,red
 return True,None

def fano_planes():
 pairs=list(combinations(range(7),2));idx={p:i for i,p in enumerate(pairs)}
 options=[]
 for E in combinations(range(7),3):options.append((bitset(E),sum(1<<idx[p] for p in combinations(E,2))))
 choices=[[x for x in options if x[1]>>i&1] for i in range(21)];out=[]
 def rec(rem,selected):
  if not rem:out.append(tuple(sorted(selected)));return
  i=(rem&-rem).bit_length()-1
  for E,P in choices[i]:
   if P&rem==P:rec(rem^P,selected+[E])
 rec((1<<21)-1,[])
 return tuple(sorted(out))
