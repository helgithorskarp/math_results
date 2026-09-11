"""Complete quad families modulo high-point permutations, preserving degree roles."""
from itertools import combinations,permutations,product
from functools import lru_cache

def transform(mask,p):
 return sum(1<<p[i] for i in range(len(p)) if mask>>i&1)
@lru_cache(None)
def role_perms(degrees):
 groups=[[i for i,d in enumerate(degrees) if d==a] for a in sorted(set(degrees))]
 out=[]
 for ps in product(*(list(permutations(g)) for g in groups)):
  p=list(range(len(degrees)))
  for g,pp in zip(groups,ps):
   for i,j in zip(g,pp):p[i]=j
  out.append(tuple(p))
 return tuple(out)

def key(colors,degrees):
 return min(tuple(sorted(transform(c,p) for c in colors)) for p in role_perms(degrees))

@lru_cache(None)
def reps(n6,n7):
 q=n6+n7;degrees=(6,)*n6+(7,)*n7
 pairs=list(combinations(range(q),2))
 masks=[x for x in range(1,1<<q) if x.bit_count()>=2]
 edge_masks={x:sum(1<<j for j,(a,b) in enumerate(pairs) if x>>a&1 and x>>b&1) for x in masks}
 out={}
 def visit(start,used,counts,shared):
  private=[4-c for c in counts];union=len(shared)+sum(private)
  if union<=12:
   colors=tuple(shared)+tuple(1<<i for i,n in enumerate(private) for _ in range(n))+(0,)*(12-union)
   code=key(colors,degrees)
   if code not in out:out[code]=tuple(frozenset(t for t,c in enumerate(code) if c>>i&1) for i in range(q))
  for j in range(start,len(masks)):
   x=masks[j];E=edge_masks[x]
   if used&E or any(counts[i]==4 and x>>i&1 for i in range(q)):continue
   visit(j+1,used|E,[counts[i]+bool(x>>i&1) for i in range(q)],shared+(x,))
 visit(0,0,[0]*q,())
 return tuple(out[x] for x in sorted(out))
