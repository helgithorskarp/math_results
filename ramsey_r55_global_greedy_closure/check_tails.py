"""Independent vertex-to-bin assignment census and literal catalog checks."""
from itertools import combinations,permutations
from pathlib import Path
import json,time
HERE=Path(__file__).resolve().parent

def parse(line):
 values=[ord(c)-63 for c in line]
 if not values or any(v<0 or v>63 for v in values):raise ValueError('alphabet')
 n=values[0];m=n*(n-1)//2
 if n not in (3,6,9,12) or len(values)-1!=(m+5)//6:raise ValueError('order/length')
 packed=0
 for v in values[1:]:packed=packed*64+v
 pad=6*(len(values)-1)-m
 if packed&((1<<pad)-1):raise ValueError('padding')
 packed>>=pad;edges=set();position=m-1
 for j in range(1,n):
  for i in range(j):
   if packed>>position&1:edges.add((i,j))
   position-=1
 return n,edges

def properties(n,edges):
 for q in combinations(range(n),3):
  if all(p in edges for p in combinations(q,2)):raise ValueError('red triangle')
 for q in combinations(range(n),5):
  if all(p not in edges for p in combinations(q,2)):raise ValueError('blue five')

def assignments(n,edges):
 # Give every physical source vertex one of k+1 named bins of capacity three.
 # The first k bins must be independent. This enumerates color assignments,
 # without recursing on precomputed independent triples or remaining subsets.
 k=n//3-1;groups=[[] for _ in range(k+1)];out=[0]*4
 degrees=[sum(v in p for p in edges) for v in range(n)];order=sorted(range(n),key=lambda v:(-degrees[v],v))
 def edge(a,b):return (min(a,b),max(a,b)) in edges
 def visit(position,last_edges):
  if position==n:
   out[last_edges]+=1;return
  v=order[position]
  for index,group in enumerate(groups):
   if len(group)==3:continue
   new=sum(edge(v,u) for u in group)
   if index<k and new:continue
   group.append(v);visit(position+1,last_edges+(new if index==k else 0));group.pop()
 visit(0,0)
 return out

def check():
 expected=json.loads((HERE/'TAIL_COVERS.json').read_text());entries=0;totals=[];four_assignments=0
 for catalog in expected['catalogs']:
  n=catalog['n'];lines=(HERE/f'r35_{n}.g6').read_text().splitlines();sumcovers=[0]*4
  if len(lines)!=catalog['graphs']:raise ValueError('input cardinality')
  for index,(line,record) in enumerate(zip(lines,catalog['entries'])):
   order,edges=parse(line)
   if order!=n or record['index']!=index or record['graph6']!=line:raise ValueError('entry order')
   properties(n,edges);counts=assignments(n,edges)
   if counts!=record['partitions_by_last_red_edges']:raise ValueError(('entry partition mismatch',n,index,counts,record))
   weights=[]
   for mask in (0,1,3,7):
    local={p for j,p in enumerate(combinations(range(3),2)) if mask>>j&1}
    good=sum(all(((min(p[i],p[j]),max(p[i],p[j])) in local)==((i,j) in local) for i,j in combinations(range(3),2)) for p in permutations(range(3)))
    weights.append(good*len(list(permutations(range(3))))**(n//3-1))
   covers=[a*b for a,b in zip(counts,weights)]
   if covers!=record['embedding_covers_by_last_red_edges']:raise ValueError('embedding weight mismatch')
   triples=sum(all(p not in edges for p in combinations(q,2)) for q in combinations(range(n),3))
   if triples!=record['independent_triples']:raise ValueError('triple count')
   sumcovers=[a+b for a,b in zip(sumcovers,covers)];entries+=1;four_assignments+=sum(counts)
  if sumcovers!=catalog['embedding_cover_totals']:raise ValueError('catalog total')
  totals.append({'n':n,'cover_totals':sumcovers})
 controls=0
 for n,edges in [(6,set()),(6,set(combinations(range(6),2)))]:
  try:properties(n,edges)
  except ValueError:controls+=1
  else:raise ValueError('bad graph accepted')
 for bad in ('','??????','E~~~~','E????@'):
  try:parse(bad)
  except ValueError:controls+=1
  else:raise ValueError('bad encoding accepted')
 return {'status':'VERIFIED_INDEPENDENT_TAIL_COVER_CENSUS','graphs_checked':entries,'ordered_partitions_checked':four_assignments,'negative_controls':controls,'totals':totals,'catalog_completeness':'Imported, not regenerated','automorphism_quotients':0}

if __name__=='__main__':
 start=time.monotonic();d=check();(HERE/'TAIL_AUDIT.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(json.dumps({'seconds':time.monotonic()-start,**d}))
