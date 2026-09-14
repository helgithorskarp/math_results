"""Polymath16 source and exact chord reflections in Q(sqrt(-3),sqrt(-11))."""
from fractions import Fraction as Q
from itertools import combinations

KEEP=(0,5,6,9,12,13,16,17,18,19,20,22,24,25,26,27,28,30,31,33,34,35,36,37,38,39,40,41,42)
def p(a=0,b=0,c=0,d=0):return tuple(map(Q,(a,b,c,d)))
ZERO=p();ONE=p(1)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def sub(x,y):return add(x,neg(y))
def conj(x):return x[0],x[1],-x[2],-x[3]
def mul(x,y):
 a,b,c,d=x;A,B,C,D=y
 return (a*A+33*b*B-3*c*C-11*d*D,a*B+b*A-c*D-d*C,
         a*C+c*A+11*(b*D+d*B),a*D+d*A+3*(b*C+c*B))
def is_unit(x):return mul(x,conj(x))==ONE
def sources():
 w=p(Q(1,2),0,Q(1,2));eta=p(0,Q(1,6),Q(1,6));powers=[ONE]
 for _ in range(5):powers.append(mul(powers[-1],w))
 seeds=[ONE,sub(eta,conj(eta)),sub(eta,mul(conj(eta),w)),eta,
        add(ONE,mul(eta,powers[2])),conj(eta),add(ONE,conj(mul(eta,powers[2])))]
 full=[ZERO]+sorted({mul(a,b)for a in seeds for b in powers})
 return full,[full[i]for i in KEEP]
def edges(points):
 return [(j,i)for i in range(len(points))for j in range(i)if is_unit(sub(points[i],points[j]))]
def reflect(z,A,B):
 # For |A|=|B|=1 this is reflection in the line AB.
 return sub(add(A,B),mul(mul(A,B),conj(z)))
def frames():
 _,S=sources();N=[i for i,z in enumerate(S)if is_unit(z)]
 for a,b in combinations(N,2):
  A,B=S[a],S[b]
  if add(A,B)==ZERO:continue
  moved=[reflect(z,A,B)for z in S]
  P=list(S)+sorted(set(moved)-set(S));root=P.index(add(A,B))
  yield (a,b),P,edges(P),(0,root,a,b)
def partitions(n):
 def rec(word):
  if len(word)==n:yield tuple(word);return
  for c in range(min(4,max(word,default=-1)+2)):
   yield from rec(word+[c])
 return rec([])
def bare_patterns(E,T):
 es=set(E)
 return [p for p in partitions(len(T))if all(p[i]!=p[j]for i in range(len(T))for j in range(i)
   if tuple(sorted((T[i],T[j])))in es)]
