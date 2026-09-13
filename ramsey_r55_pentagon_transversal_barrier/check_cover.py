from pathlib import Path
from itertools import combinations,permutations
import sys,json,hashlib
rows=[list(map(int,z.split())) for z in Path(sys.argv[1]).read_text().splitlines()]
n,m=rows[0]
if not 1<=n<=43 or len(rows)!=m+1:raise ValueError('graph header')
edge=set()
for row in rows[1:]:
 if len(row)!=2:raise ValueError('edge row')
 u,v=row
 if not 0<=u<v<n or (u,v) in edge:raise ValueError('edge')
 edge.add((u,v))
# This checker recognizes the twelve explicit labeled cycle edge masks.
pairs=list(combinations(range(5),2));cycle_codes=set()
for perm in permutations(range(1,5)):
 cyc=(0,)+perm;es={tuple(sorted((cyc[i],cyc[(i+1)%5]))) for i in range(5)}
 cycle_codes.add(sum(1<<i for i,p in enumerate(pairs) if p in es))
P=[];by_vertex=[[] for _ in range(n)];by_pair={pair:[] for pair in combinations(range(n),2)}
for S in combinations(range(n),5):
 code=sum(1<<i for i,(j,k) in enumerate(pairs) if (S[j],S[k]) in edge)
 if code not in cycle_codes:continue
 h=sum(1<<v for v in S);P.append(h)
 for v in S:by_vertex[v].append(h)
 for u,v in combinations(S,2):by_pair[u,v].append(h^(1<<u)^(1<<v))
proof=iter(Path(sys.argv[2]).open());header=next(proof).split()
if header!=['C5COVER','1',str(n),'21']:raise ValueError('proof header')
nodes=leaves=pair_checks=0;maximum_selected=0

def bits(x):
 while x:
  b=x&-x;yield b.bit_length()-1;x^=b

def check(S,C):
 global nodes,leaves,pair_checks,maximum_selected
 nodes+=1;maximum_selected=max(maximum_selected,S.bit_count())
 row=next(proof).split()
 if row[0]=='B':
  if len(row)!=2:raise ValueError('branch arity')
  v=int(row[1])
  if not 0<=v<n:raise ValueError('branch vertex')
  vb=1<<v
  if not C&vb:raise ValueError('branch vertex')
  D=C^vb;T=S|vb;blocked=0
  for h in by_vertex[v]:
   k=(h&T).bit_count()
   if k==5:raise ValueError('selected set is not C5-free')
   if k==4:blocked|=h&~T
  check(T,D&~blocked)
  check(S,D)
 elif row[0]=='L':
  k=int(row[1]);groups=list(map(int,row[2:]))
  if len(groups)!=k or S.bit_count()+k>=21:raise ValueError('leaf bound')
  used=0
  for group in groups:
   if group<=0 or group&~C or group&used:raise ValueError('leaf partition')
   used|=group
   for u,v in combinations(bits(group),2):
    pair_checks+=1
    if not any(t&S==t for t in by_pair[u,v]):raise ValueError('invalid forbidden pair')
  if used!=C:raise ValueError('incomplete leaf partition')
  leaves+=1
 else:raise ValueError('unknown proof node')
check(0,(1<<n)-1)
try:next(proof);raise ValueError('trailing proof')
except StopIteration:pass
print(json.dumps({'status':'INDEPENDENTLY_CHECKED_COMPLETE_21_SET_COVER','n':n,'target':21,'pentagons':len(P),'nodes':nodes,'leaves':leaves,'leaf_pair_witness_checks':pair_checks,'maximum_selected':maximum_selected,'proof_bytes':Path(sys.argv[2]).stat().st_size,'proof_sha256':hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest()},indent=2))
