"""Fresh star-system completion and every full physical sector."""
from fractions import Fraction as F
from math import comb
from exact import need,rref,digest

def choose(n,k):return comb(n,k)if 0<=k<=n else 0
def names(n,active):
 t=set(active)|{n-a for a in active}|{n//2}
 return ['d'+str(a)for a in sorted(active)+[n//2]]+['t'+str(a)+'_'+str(b)for a in range(2,n-1)for b in range(a,n-1)if a+b<n and a in t and b in t]
def table(case,values=None):
 n=case['n'];r=n-2;s=2**(n-1)-n;need(n in (12,16),'orders');active=case['active'];need(active==([3,4,5]if n==12 else [4,5,6,7]),'active');expected=names(n,active);need(case['names']==expected,'complete named coordinates')
 vals=case['values']if values is None else values;need(len(vals)==len(expected),'complete coordinates');need(all(type(v)in(str,int,F)for v in vals),'exact rational inputs');v={k:F(x)for k,x in zip(expected,vals,strict=True)}
 b=[[F(0)for _ in range(r)]for _ in range(r)]
 for a in range(2,n//2+1):b[a-1][n-a-1]=b[n-a-1][a-1]=s-v.get('d'+str(a),0)
 for key,x in v.items():
  if key.startswith('t'):
   a,c=map(int,key[1:].split('_'));b[a-1][c-1]=b[c-1][a-1]=x
 # Complete full original point-star equations, not the author's one-way decoder.
 eq=[]
 for a in range(1,r+1):
  coeff=[F(0)]*r;rhs=F(s)
  for c in range(1,r+1):
   count=choose(n-a-1,c-1)
   if a==1:coeff[c-1]+=count
   elif c==1:coeff[a-1]+=count
   else:rhs-=count*b[a-1][c-1]
  eq.append(coeff+[rhs])
 rows,piv=rref(eq);need(piv==list(range(r)),'unique star face')
 for a in range(1,r+1):b[0][a-1]=b[a-1][0]=rows[a-1][-1]
 need(all(sum(choose(n-a-1,c-1)*b[a-1][c-1]for c in range(1,r+1))==s for a in range(1,r+1)),'whole star')
 return b

def sectors(n,b):
 N=2**n-n-1;s=2**(n-1)-n;out=[]
 for j in range(n//2+1):
  layers=list(range(max(1,j),min(n-2,n-j)+1));g=[choose(n-2*j,a-j)for a in layers]
  K=[[F(s*(a==c)-(choose(n,c)if j==0 else 0))+(-1)**j*b[a-1][c-1]*choose(n-a-j,c-j)for c in layers]for a in layers]
  U=[[F(N*(a==c)-(choose(n,c)if j==0 else 0))-K[u][v]for v,c in enumerate(layers)]for u,a in enumerate(layers)]
  lower=[[g[u]*x for x in row]for u,row in enumerate(K)];upper=[[g[u]*x for x in row]for u,row in enumerate(U)]
  kernels=[]
  if j==0:kernels.append(list(map(F,layers)))
  if j==1:kernels.append([F(1)]*len(layers))
  for a in range(2,n//2):
   if a in layers and a not in ([3,4,5]if n==12 else [4,5,6,7]):kernels.append([F((x==a)-(-1)**j*(x==n-a))for x in layers])
  _,piv=rref(kernels);need(len(piv)==len(kernels),'kernel independent');keep=[i for i in range(len(layers))if i not in piv]
  out.append(dict(j=j,layers=layers,g=g,K=K,U=U,lower=lower,upper=upper,kernels=kernels,keep=keep,multiplicity=choose(n,j)-choose(n,j-1)))
 return out

def original_rows(n,b):
 N=2**n-n-1;s=2**(n-1)-n;r=n-2
 c=[F(s-(N-1))+sum(choose(n-a,t)*b[a-1][t-1]for t in range(1,r+1))for a in range(1,r+1)]
 empty=[1-x for x in c];loop=1+sum(choose(n,a)*c[a-1]for a in range(1,r+1))
 need(loop+sum(choose(n,a)*empty[a-1]for a in range(1,r+1))==N,'empty original row')
 for a in range(1,r+1):
  need(s+empty[a-1]+sum(choose(n-a,t)*b[a-1][t-1]for t in range(1,r+1))==N,'original size row')
  need(sum(choose(n-a-1,t-1)*b[a-1][t-1]for t in range(1,r+1))==s,'excluding point star')
 need(sum(choose(n-1,a-1)*empty[a-1]for a in range(1,r+1))==s,'actual empty star')
 return dict(empty_loop=str(loop),empty_rows=list(map(str,empty)),centered=not any(c))
