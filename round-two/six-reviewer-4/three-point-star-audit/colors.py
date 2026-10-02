# Independent new greedy colors; no researcher executable imported.
from pathlib import Path
from itertools import combinations
import json,hashlib,time,random,sys
HERE=Path(__file__).resolve().parent
def need(ok,message):
 if not ok:raise RuntimeError(message)
def digest(z):return hashlib.sha256(json.dumps(z,separators=(',',':')).encode()).hexdigest()
def words_as_sets(words):return [set(v for v in range(18) if word>>v&1) for word in words]
def domain(core,y):
 owned=set()
 for w in words_as_sets(core):
  owned.update(combinations(sorted(w),3))
 need(len(owned)==360,'owned triples distinct')
 points=[v for v in range(18) if v not in (17,y)]
 candidates=[];tests=0
 for q in combinations(points,5):
  tests+=1
  if all(t not in owned for t in combinations(q,3)):candidates.append(sum(1<<v for v in q))
 need(tests==4368,'whole residual universe');candidates.sort()
 adj=[set() for v in candidates];edges=0
 for i,j in combinations(range(len(candidates)),2):
  if (candidates[i]&candidates[j]).bit_count()<=2:adj[i].add(j);adj[j].add(i);edges+=1
 return candidates,adj,edges

def coloring(adj,target):
 started=time.monotonic();n=len(adj);best=list(range(n));attempts=0
 for seed in range(64):
  if time.monotonic()-started>5:break
  rng=random.Random(73001+seed);ranks=list(range(n));rng.shuffle(ranks);priority={v:i for i,v in enumerate(ranks)}
  colors=[-1]*n;neighbor_colors=[set()for _ in adj];remaining=set(range(n))
  while remaining:
   v=max(remaining,key=lambda k:(len(neighbor_colors[k]),len(adj[k]),priority[k]));c=0
   while c in neighbor_colors[v]:c+=1
   colors[v]=c;remaining.remove(v)
   for w in adj[v]&remaining:neighbor_colors[w].add(c)
  attempts+=1
  if max(colors,default=-1)<max(best,default=-1):best=colors
  if max(best,default=-1)+1<=target:break
 return best,attempts


if __name__=='__main__':
 full=json.loads(Path(sys.argv[1]).read_text());records=[]
 for ix,(z,a) in enumerate((z,a)for z in full['products']for a in z['positives']):
  branch=str(z['u_replication'])+str(z['v_replication']);c,adj,e=domain(a['words'],z['first_mark'][2]);colors,attempts=coloring(adj,24 if branch[0]=='4'else 30)
  need(all(colors[i]!=colors[j]for i,v in enumerate(adj)for j in v),'all literal color constraints')
  records.append({'index':ix,'own_product':z['product'],'branch':branch,'first_fixture':z['first_fixture'],'first_mark':z['first_mark'],'second_fixture':z['second_fixture'],'second_mark':z['second_mark'],'map':a['map'],'words':a['words'],'candidate_count':len(c),'candidate_sha256':digest(c),'edges':e,'colors':colors,'capacity':max(colors,default=-1)+1,'attempts':attempts,'upper':36+max(colors,default=-1)+1})
 need(records==json.loads((HERE/'cores.json').read_text()),'entire newly generated core/color certificate')
 print(json.dumps({'cores':len(records),'sha256':digest(records)},sort_keys=True,separators=(',',':')))
