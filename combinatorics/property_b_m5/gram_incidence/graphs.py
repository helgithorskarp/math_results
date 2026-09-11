from itertools import combinations,permutations,product

def canonical(n,edges):
 adj=[0]*n
 for u,v in edges:adj[u]|=1<<v;adj[v]|=1<<u
 colors=[a.bit_count() for a in adj]
 while True:
  palette=sorted(set(colors))
  keys=[(colors[i],tuple(sum(bool(adj[i]>>j&1) and colors[j]==c for j in range(n)) for c in palette)) for i in range(n)]
  rank={k:i for i,k in enumerate(sorted(set(keys)))};new=[rank[k] for k in keys]
  stable=all((colors[i]==colors[j])==(new[i]==new[j]) for i in range(n) for j in range(i))
  colors=new
  if stable:break
 groups=[[i for i in range(n) if colors[i]==c] for c in sorted(set(colors))]
 options=[]
 for group in groups:
  # Swapping true or false twins is an automorphism; keep their relative order.
  precede={i:[] for i in group}
  for i,j in combinations(group,2):
   if adj[i]==adj[j] or (adj[i]|1<<i)==(adj[j]|1<<j):precede[j].append(i)
  pp=[]
  def rec(order,left):
   if not left:pp.append(tuple(order));return
   for i in sorted(left):
    if all(j not in left for j in precede[i]):rec(order+[i],left-{i})
  rec([],set(group));options.append(pp)
 best=None
 for parts in product(*options):
  order=sum(parts,());rev=[0]*n
  for i,u in enumerate(order):rev[u]=i
  z=tuple(sorted((min(rev[u],rev[v]),max(rev[u],rev[v])) for u,v in edges))
  if best is None or z<best:best=z
 return best

def all_graphs(d,max_edges):
 level={()};counts=[]
 for n in range(1,d+1):
  nxt=set()
  for edges in level:
   for k in range(min(n-1,max_edges-len(edges))+1):
    for nei in combinations(range(n-1),k):nxt.add(canonical(n,edges+tuple((u,n-1) for u in nei)))
  level=nxt;counts.append(len(level))
 return tuple(sorted(level,key=lambda z:(len(z),z))),counts
