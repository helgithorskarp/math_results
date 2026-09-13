"""Bounded actual <=505-point search, guided by exact colour extension failures."""
from geometry51 import *
from functools import lru_cache
from collections import deque

@lru_cache(maxsize=200000)
def list_count(dom,adj):
 # Count only up to two; zero is an exact extension obstruction.
 def rec(ds,live):
  if not live:return 1
  cand=[i for i in range(len(ds))if live>>i&1];v=min(cand,key=lambda i:(ds[i].bit_count(),-adj[i].bit_count()))
  if ds[v]==0:return 0
  total=0;avail=ds[v];remain=live^(1<<v)
  while avail:
   c=avail&-avail;avail-=c;dd=list(ds)
   for j in cand:
    if j!=v and adj[v]>>j&1:dd[j]&=~c
   total+=rec(tuple(dd),remain)
   if total>=2:return 2
  return total
 return rec(dom,(1<<len(dom))-1)

def run(tag,width=8,limit=600):
 st=time.time();x=json.loads((W/f'placements_{tag}.json').read_text());h=json.loads((W/f'host_edges_{tag}.json').read_text());oldnew={p:490+i for i,p in enumerate(h['new_point_ids'])};N=490+len(oldnew);edges=h['edges'];adj=[set()for _ in range(N)]
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 copies=[tuple(sorted(oldnew[j]for j in x['placements'][i]['new']))for i in h['placements']];qualities=[sum(len(adj[v]&set(range(490)))for v in C)/len(C)for C in copies];old=set(range(490));records=[];frontier=deque([((),tuple(range(490)),x['seed_word'])]);seen={frozenset()};unknown=[];tally=Counter();scans=[]
 # Validate the list-colouring primitive against exhaustive tiny assignments.
 for dom in product(range(1,16),repeat=2):
  for a in [(0,0),(2,1)]:
   exact=min(2,sum(bool(dom[0]>>c&1)and bool(dom[1]>>d&1)and(not a[0]or c!=d)for c,d in product(range(4),repeat=2)));require(list_count(dom,a)==exact,'list-colour control')
 while frontier and len(records)<limit:
  chosen,verts,word=frontier.popleft();depth=len(chosen);col=[-1]*N
  for i,v in enumerate(verts):col[v]=int(word[i])
  if depth==3:continue
  blocked=[];other=[];counts=Counter()
  for ci,C in enumerate(copies):
   new=[v for v in C if col[v]<0]
   if not new:continue
   dom=[];inside=[]
   for v in new:
    forbidden=0
    for a in adj[v]:
     if col[a]>=0:forbidden|=1<<col[a]
    dom.append(15^forbidden);inside.append(sum(1<<j for j,u in enumerate(new)if u in adj[v]))
   count=list_count(tuple(dom),tuple(inside));counts[count]+=1
   mutual=sum(sum(col[a]>=0 and a>=490 for a in adj[v])for v in new);rank=(-mutual,-qualities[ci],len(new),ci)
   if count==0:blocked.append((rank,ci))
   else:other.append(((count,)+rank,ci))
  scans.append({'chosen':chosen,'extension_counts':dict(counts)});print('SCAN',tag,'depth',depth,'chosen',chosen,'extensions',dict(counts),'seconds',time.time()-st,flush=True)
  options=sorted(blocked)if blocked else sorted(other);added=0
  for rank,ci in options:
   newchosen=tuple(sorted(chosen+(ci,)));newverts=tuple(sorted(old|{v for k in newchosen for v in copies[k]}));key=frozenset(newverts[490:])
   if key in seen:continue
   seen.add(key);require(len(newverts)<=505,'physical budget');ii={v:i for i,v in enumerate(newverts)};es=sorted((ii[a],ii[b])for a in newverts for b in adj[a]if a<b and b in ii)
   status,c,stats=solve(es,len(newverts),100000);tally[status]+=1;r={'chosen':newchosen,'placement_indices':[h['placements'][k]for k in newchosen],'vertices':len(newverts),'edges':len(es),'status':status,'word':c,'vertex_ids':newverts,'solver_stats':stats,'parent_colour_obstructed':bool(blocked)};records.append(r);added+=1
   print('SMALL',tag,len(records),'depth',depth+1,'n',len(newverts),status,stats.get('conflicts'),'seconds',time.time()-st,flush=True)
   if status!='SAT':
    r['edge_list']=es;(W/f'small_candidate_{tag}_{len(records)}.json').write_text(json.dumps(r,separators=(',',':'))+'\n');unknown.append(len(records))
   if status=='UNSAT':frontier.clear();break
   if status=='SAT'and depth+1<3:frontier.append((newchosen,newverts,c))
   if added>=width or len(records)>=limit:break
  out={'tag':tag,'width':width,'limit':limit,'tally':dict(tally),'records':records,'scans':scans,'frontier_size':len(frontier),'unresolved_or_candidates':unknown,'list_cache':str(list_count.cache_info()),'seconds':time.time()-st};(W/f'guided_{tag}.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
  if tally.get('UNSAT'):break
 print('GUIDED_DONE',tag,dict(tally),'frontier',len(frontier),'seconds',time.time()-st,flush=True)
if __name__=='__main__':run(sys.argv[1],int(sys.argv[2])if len(sys.argv)>2 else 8,int(sys.argv[3])if len(sys.argv)>3 else 600)
