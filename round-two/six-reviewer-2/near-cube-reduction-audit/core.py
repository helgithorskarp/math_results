"""Fresh full star system and sectors; previous reviewer linear primitives only.

Computations have bounded n6..32; the all-order proof is ordinary, not an
extrapolation of this computational guard. Original dense allocation is separate.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import comb
from linear import need,inverse,mv,psd,digest

def choose(n,k):return comb(n,k)if 0<=k<=n else 0

def constants(n):
 need(type(n)is int and 6<=n<=32,'fixed computational n6..32 guard');N=2**n-n-1;s=2**(n-1)-n;return n-2,N,s,N-s

def architecture(n,k):
 r,N,s,h=constants(n);need(type(k)is int and 1<=k<=r,'full original cutoff domain');d=n//2;q=min(d,max(k,3 if n%2==0 else 2));return d,q

def pairs(n):
 r,*_=constants(n);return[(a,b)for a in range(1,r+1)for b in range(a,r+1)if a+b<=n]

def free_pairs(n,k=None):
 out=[p for p in pairs(n)if p[0]>=2]
 if k is not None:architecture(n,k);out=[p for p in out if not(sum(p)<n and p[0]>k)]
 return out

@lru_cache(None)
def star_inverse(n):
 r,N,s,h=constants(n);unknown=[(1,b)for b in range(1,r+1)];A=[]
 for a in range(1,r+1):
  row=[F(0)]*r
  for b in range(1,r+1):
   key=tuple(sorted((a,b)))
   if key in unknown:row[unknown.index(key)]+=b*choose(n-a,b)
  A.append(row)
 return inverse(A)

def complete(n,free):
 r,N,s,h=constants(n);need(sorted(free)==free_pairs(n),'entire supported free coordinate census');need(all(type(v)is int or isinstance(v,F)for v in free.values()),'exact rational affine inputs');rhs=[]
 for a in range(1,r+1):rhs.append(F((n-a)*s)-sum(b*choose(n-a,b)*free.get(tuple(sorted((a,b))),F(0))for b in range(2,r+1)))
 beta={p:F(v)for p,v in free.items()};beta.update({(1,b):v for b,v in enumerate(mv(star_inverse(n),rhs),1)})
 for a in range(1,r+1):need(sum(beta.get(tuple(sorted((a,b))),F(0))*choose(n-a-1,b-1)for b in range(1,r+1))==s,'EVERY actual excluded-point star row')
 return beta

def supported(n,k,beta):
 architecture(n,k);need(sorted(beta)==pairs(n),'whole supported table');need(all(v==0 for(a,b),v in beta.items()if a+b<n and a>k),'EVERY proper original S_k zero')

def sector(n,beta,j):
 r,N,s,h=constants(n);need(type(j)is int and 0<=j<=n//2,'ALL surviving degree domain');aa=list(range(max(1,j),min(r,n-j)+1));g=[choose(n-2*j,a-j)for a in aa];need(all(v>0 for v in g),'all physical norms');K=[];U=[];Q=[]
 for a in aa:
  low=[];up=[];metric=[]
  for b in aa:
   dis=(-1)**j*beta.get(tuple(sorted((a,b))),F(0))*choose(n-a-j,b-j);mean=choose(n,b)if j==0 else 0
   low.append(F(s*(a==b)-mean)+dis);up.append(F(h*(a==b))-dis);metric.append(F(a==b)-F(mean,N))
  K.append(low);U.append(up);Q.append(metric)
 G=[[g[i]*v for v in row]for i,row in enumerate(K)];H=[[g[i]*v for v in row]for i,row in enumerate(U)];W=[[g[i]*v for v in row]for i,row in enumerate(Q)]
 need(all(A[i][t]==A[t][i]for A in[G,H,W]for i in range(len(aa))for t in range(len(aa))),'complete physical lower/upper/projected-metric symmetries')
 return {'degree':j,'layers':aa,'metric':g,'multiplicity':choose(n,j)-choose(n,j-1),'K':K,'U':U,'Q':Q,'G':G,'H':H,'W':W}

def projected_upper_form(g,epsilon):return[[g['H'][i][t]-epsilon*g['W'][i][t]for t in range(len(g['layers']))]for i in range(len(g['layers']))]
def core_upper_form(g,epsilon):return[[g['H'][i][t]-epsilon*g['metric'][i]*(i==t)for t in range(len(g['layers']))]for i in range(len(g['layers']))]

def embedding(n,k,beta,all_sectors=None):
 d,q=architecture(n,k);supported(n,k,beta);sectors=all_sectors or[sector(n,beta,j)for j in range(d+1)];positions=0;norms=0;rows=[]
 for j in range(q+1,d+1):
  high=sectors[j];ell=(2 if j%2==0 else 3)if n%2==0 else 2;low=sectors[ell];aa=high['layers'];ix=[low['layers'].index(a)for a in aa];sg=[(-1 if n%2 and j%2 and a>n//2 else 1)for a in aa]
  for i,a in enumerate(aa):
   for t,b in enumerate(aa):
    for field in['K','U']:
     x=high[field][i][t];y=sg[i]*sg[t]*low[field][ix[i]][ix[t]];need(x==y,'ENTIRE signed high/low physical principal action')
     if i!=t and x:need(high['metric'][i]==high['metric'][t]and low['metric'][ix[i]]==low['metric'][ix[t]],'both physical complementary norms agree; orthonormal embedding');norms+=int(i!=t and x!=0)
     positions+=1
  rows.append([j,ell,aa,sg,digest([high['K'],high['U']])])
 return {'positions':positions,'nonzero_complement_norm_checks':norms,'complete_embeddings':rows}
