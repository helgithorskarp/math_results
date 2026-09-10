"""Complete degree/high-neighbor-count profiles from the exact pair deficit."""

def rows(d,n,total,D):
 costs=[(c-3)*(c-4)//2 if d==6 else (c-1)*(c-2)//2 for c in range(d+1)]
 free=[c for c,q in enumerate(costs) if q==0];bad=[c for c,q in enumerate(costs) if 0<q<=D]
 out=[]
 def rec(i,left,counts):
  if i==len(bad):
   N=n-sum(counts.values());S=total-sum(c*v for c,v in counts.items());a,b=free
   nb=S-a*N;na=N-nb
   if na>=0 and nb>=0:
    r=[0]*(d+1)
    for c,v in counts.items():r[c]=v
    r[a]=na;r[b]=nb;out.append((D-left,r))
   return
  c=bad[i]
  for k in range(min(n,left//costs[c])+1):counts[c]=k;rec(i+1,left-k*costs[c],counts)
  del counts[c]
 rec(0,D,{})
 return out

def profiles(m,k):
 D=22-3*m-k
 return [(r,s) for q,r in rows(6,17,39+2*m,D) for t,s in rows(7,24,65-4*m,D) if q+t==D]
