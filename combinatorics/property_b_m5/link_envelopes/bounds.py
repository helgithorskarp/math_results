"""Conditional greedy failure bound with exact link-union envelopes."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import model as M
from fractions import Fraction as F
from itertools import permutations
from star_envelope import envelope

def envelope_bound(v,x,positions=None,max_excess=3):
 x=tuple(x);s=(len(x)-1).bit_length();N=v-s
 positions=tuple(range((v-s)//2,(v-s)//2+s)) if positions is None else tuple(positions)
 den,cs=M.coefficients(v,s,positions=positions);total=0
 for k,(one,two,pairs,mark,L,R) in enumerate(cs):
  a=sum(x[A]*c for A,c in one);b=sum(x[A]*c for A,c in two)
  q=sum(x[A]*(x[B]-(A==B))*c for A,B,c in pairs)
  if mark:
   left=sum(1<<i for i,p in enumerate(positions) if p<k)
   right=sum(1<<i for i,p in enumerate(positions) if p>k)
   rows=[]
   for A,n in enumerate(x):
    if A&mark:
     flags=(1 if A&~(left|mark)==0 else 0)|(2 if A&~(right|mark)==0 else 0)
     rows.extend([(5-A.bit_count(),flags)]*n)
   ee=envelope(tuple(sorted(rows)),N,L,max_excess)
   if ee is not None:
    num,dd,nt=ee;assert den%dd==0
    q=min(q,num*(den//dd))
  total+=min(a,b,q,den)
 return F(total,den)
