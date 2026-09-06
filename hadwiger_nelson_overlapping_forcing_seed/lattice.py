"""Exact unit displacement enumeration in the integer coordinate lattice."""
from math import isqrt
import json,time
from pathlib import Path

def directions(den=1):
 out=[];bound=1296*den*den
 for a in range(-isqrt(bound//3),isqrt(bound//3)+1):
  for b in range(-isqrt((bound-3*a*a)//11),isqrt((bound-3*a*a)//11)+1):
   for d in range(-isqrt((bound-3*a*a-11*b*b)//33),isqrt((bound-3*a*a-11*b*b)//33)+1):
    q=bound-3*a*a-11*b*b-33*d*d;c=isqrt(q)
    if c*c!=q:continue
    for cc in sorted({c,-c}):
     if a*b+cc*d==0:out.append((a,b,cc,d))
 return sorted(out)

def edges(pts,den=1):
 idx={tuple(p):i for i,p in enumerate(pts)};es=[];ds=directions(den)
 if len(idx)!=len(pts):raise ValueError('Repeated points')
 for i,(a,b,c,d) in enumerate(pts):
  for e,f,h,k in ds:
   j=idx.get((a+e,b+f,c+h,d+k))
   if j is not None and i<j:es.append([i,j])
 return sorted(es)
