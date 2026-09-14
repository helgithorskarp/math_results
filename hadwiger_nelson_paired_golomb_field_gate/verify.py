"""Solver-free complete pair coverage by greedy words and 191 exceptions."""
from prepare import *
from colour import greedy,checked
import copy,hashlib

def seed_edges(P):
 rows=[]
 for z in P:
  a,b,c,d=z[0];A,B,C,D=z[1];rows.append((a,b,A,B,c,d/3,C,D/3))
 den=lcm(*(x.denominator for row in rows for x in row));rows=[tuple(int(x*den)for x in row)for row in rows]
 def square(r):
  a,b,c,d=r;return(a*a+33*b*b+5*c*c+165*d*d,2*a*b+10*c*d,2*a*c+66*b*d,2*a*d+2*b*c)
 out=[]
 for i,j in combinations(range(len(rows)),2):
  z=tuple(a-b for a,b in zip(rows[i],rows[j]));a=square(z[:4]);b=square(z[4:])
  if tuple(x+3*y for x,y in zip(a,b))==(den*den,0,0,0):out.append((i,j))
 return out

def main():
 st=time.time();inv=json.loads((W/'inventory.json').read_text());geo=json.loads((W/'geometry.json').read_text());P,old=seed();base=seed_edges(P);require(len(base)==2435 and all(old[a]!=old[b]for a,b in base),'seed metric/word')
 require(digest(inv['points'])==geo['points_sha256'] and digest(geo['edges'])==geo['edges_sha256'] and digest(geo['neighbours'])==geo['neighbours_sha256'],'geometry streams')
 points=inv['points'];N=len(points);copies=[tuple(v['points'])for v in inv['copies']];k=len(copies);require(len(set(copies))==k and all(len(c)==9 and len(set(c))==9 for c in copies),'copy census');require(len(set(tuple(c)for c in copies))==k,'copy uniqueness')
 adj=[set()for _ in points];owners=[set()for _ in points];domains=[]
 for a,b in geo['edges']:require(0<=a<b<N,'edge range');adj[a].add(b);adj[b].add(a)
 for i,C in enumerate(copies):
  for v in C:owners[v].add(i)
 for ns in geo['neighbours']:
  require(len(set(ns))==len(ns) and all(0<=r<490 for r in ns),'old neighbours');forbidden=0
  for r in ns:forbidden|=1<<int(old[r])
  domains.append(15^forbidden)
 exceptions=json.loads((Path(__file__).resolve().parent/'exceptions.json').read_text());ex={}
 for v in exceptions:
  key=tuple(v['domains']),tuple(v['adjacency']);require(key not in ex,'duplicate exception');checked(v['word'],*key);require(greedy(*key)is None,'exception is not exceptional');ex[key]=v['word']
 used=set();cache={};counts=Counter();sizes=Counter();templatesizes=Counter();selection_hash=hashlib.sha256();word_hash=hashlib.sha256();first_fixture=None;selection_file=(W/'verified_pair_choices.txt').open('w')
 def choose(dom,aa):
  key=dom,aa
  if key not in cache:
   w=greedy(dom,aa)
   if w is None:require(key in ex,'uncovered greedy failure');w=ex[key];used.add(key);counts['exception_templates']+=1
   else:counts['greedy_templates']+=1
   checked(w,dom,aa);cache[key]=w;templatesizes[len(dom)]+=1
  return cache[key]
 def query(a,b):
  nonlocal first_fixture
  vs=tuple(sorted(set(copies[a])|(set(copies[b])if b>=0 else set())));n=len(vs);ix={v:i for i,v in enumerate(vs)};dom=tuple(domains[v]for v in vs);aa=tuple(sum(1<<ix[u]for u in adj[v]if u in ix)for v in vs);word=choose(dom,aa)
  # Every decoded witness is independently checked against the actual graph.
  checked(word,dom,aa);selection_hash.update(f'{a} {b}\n'.encode());selection_file.write(f'{a} {b}\n');word_hash.update((f'{a} {b} '+word+'\n').encode());sizes[n]+=1;counts['queries']+=1
  if b>=0:counts['interacting_pairs']+=1
  else:counts['single_copies']+=1
  if first_fixture is None and b>=0 and (dom,aa)in ex:
   newedges=[(i,j)for i in range(n)for j in range(i)if aa[i]>>j&1];first_fixture={'copies':[a,b],'new_point_ids':vs,'vertices':490+n,'edges':len(base)+sum(len(geo['neighbours'][v])for v in vs)+len(newedges),'four_colouring':old+word,'class_ids':sorted({points[v][0]for v in vs})}
 for i in range(k):query(i,-1)
 for i,C in enumerate(copies):
  touched=set()
  for v in C:
   touched.update(owners[v])
   for u in adj[v]:touched.update(owners[u])
  for j in sorted(touched):
   if j>i:query(i,j)
 selection_file.close();require(used==set(ex),'unused/missing exception coverage')
 # Distinct quadratic fields cannot collide. Geometry proved there are no cross-class edges.
 require(geo['counts'].get('different_class',0)==0,'cross-field edges exist')
 paircount=k*(k-1)//2;noninteracting=paircount-counts['interacting_pairs'];require(noninteracting>=0,'pair count')
 controls=0
 for v in exceptions[:3]:
  for bad in [v['word'][:-1],'0'*len(v['word'])]:
   try:checked(bad,v['domains'],v['adjacency'])
   except ValueError:controls+=1
   else:raise ValueError('bad certificate accepted')
 key=next(iter(ex));saved=ex.pop(key)
 try:
  require(key in ex,'uncovered greedy failure')
 except ValueError:controls+=1
 else:raise ValueError('missing exception accepted')
 ex[key]=saved
 # Sharp analytic cross-field control: sqrt(1/2) and alpha sqrt(1/6).
 s=(scale(ONE,F(1,2)),ZERO);t=(scale(ONE,F(1,6)),ZERO)
 require(sq(s)is None and sq(t)is None and sq(em(s,ri(t)))is None,'control square classes');require(ea(s,sc(t,scale(ONE,3)))==EO,'perpendicular radius control')
 out={'status':'PASS','seed_vertices':490,'seed_edges':2435,'copies':k,'new_points':N,'quadratic_classes':len(inv['classes']),'source_radicals':inv['source_radicals'],'raw_rooted_copies':inv['raw_copies'],'point_sha256':digest(inv['points']),'copy_sha256':digest(inv['copies']),'geometry_edges_sha256':geo['edges_sha256'],'old_neighbours_sha256':geo['neighbours_sha256'],'geometry_counts':geo['counts'],'same_class_pair_instances':sum(v['pair_instances']for v in geo['classes']),'all_unordered_pairs':paircount,'noninteracting_pairs':noninteracting,'all_zero_one_two_copy_choices':1+k+paircount,'counts':dict(counts),'new_order_counts_on_tested_queries':dict(sizes),'template_new_order_counts':dict(templatesizes),'selection_stream_sha256':selection_hash.hexdigest(),'word_stream_sha256':word_hash.hexdigest(),'fixture':first_fixture,'rejected_controls':controls,'record_improvement':False}
 expected=Path(__file__).resolve().parent/'EXPECTED.json'
 require(json.loads(json.dumps(out))==json.loads(expected.read_text()),'expected result')
 out['seconds']=time.time()-st;(W/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print('VERIFIED',dict(counts),'noninteracting',noninteracting,'seconds',out['seconds'])
if __name__=='__main__':main()
