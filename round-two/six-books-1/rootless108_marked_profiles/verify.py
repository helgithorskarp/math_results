from itertools import combinations,permutations
from collections import defaultdict,Counter
from pathlib import Path
import json,time
BASE=Path(__file__).resolve().parent
START=time.monotonic();DEADLINE=START+45

def require(v,msg):
 if not v:raise ValueError(msg)
def decode(n,key):
 g=[set() for _ in range(n)]
 for bit,(i,j) in enumerate(combinations(range(n),2)):
  if key>>bit&1:g[i].add(j);g[j].add(i)
 return tuple(frozenset(row) for row in g)
def signature(g,marked=None):
 cells=[];unused=set(range(len(g)))
 while unused:
  start=min(unused);seen={start};todo=[start]
  while todo:
   i=todo.pop()
   for j in g[i]-seen:seen.add(j);todo.append(j)
  unused-=seen;cells.append(tuple(sorted(len(g[i]) for i in seen)))
 return tuple(sorted(cells)),tuple(sorted((len(g[i]),tuple(sorted(len(g[j]) for j in g[i])),i==marked) for i in range(len(g))))
def iso(g,h,marked=False):
 if len(g)!=len(h) or signature(g,0 if marked else None)!=signature(h,0 if marked else None):return None
 n=len(g);colors=lambda f,i:(len(f[i]),tuple(sorted(len(f[j]) for j in f[i])),marked and i==0)
 domain=[{j for j in range(n) if colors(g,i)==colors(h,j)} for i in range(n)];mapping={};used=set()
 def visit():
  if len(mapping)==n:
   require(all({mapping[j] for j in g[i]}==set(h[mapping[i]]) for i in range(n)),'isomorphism decoder error');return dict(mapping)
  current={i:[j for j in domain[i]-used if all((a in g[i])==(b in h[j]) for a,b in mapping.items())] for i in range(n) if i not in mapping}
  i=min(current,key=lambda x:(len(current[x]),-len(g[x]),x))
  for j in sorted(current[i]):
   mapping[i]=j;used.add(j);result=visit()
   if result is not None:return result
   used.remove(j);del mapping[i]
  return None
 return visit()
def good(g):
 return all(len(row)<=3 for row in g) and all(not(j in g[i] and g[i]&g[j]) and len(g[i]&g[j])<=1 for i,j in combinations(range(len(g)),2))
def additions(g):
 n=len(g)
 for i,j in combinations(range(n),2):
  if len(g[i])==3 or len(g[j])==3 or j in g[i] or g[i]&g[j]:continue
  if any(g[a]&g[j] for a in g[i]):continue # A length-three path would close a four-cycle.
  result=list(g);result[i]=g[i]|{j};result[j]=g[j]|{i};yield tuple(result)
def complete(n):
 level=[tuple(frozenset() for _ in range(n))];allmodels=[];stats=[]
 for e in range(n*3//2+1):
  allmodels.extend(level);stats.append({'edges':e,'classes':len(level)})
  if not level:break
  buckets=defaultdict(list)
  for g in level:
   for candidate in additions(g):
    key=signature(candidate);bucket=buckets[key]
    if not any(iso(candidate,old) is not None for old in bucket):bucket.append(candidate)
    if time.monotonic()>DEADLINE:raise TimeoutError('INCOMPLETE edge augmentation')
  level=[g for key in sorted(buckets) for g in buckets[key]]
 return allmodels,stats
def run():
 models,stats=complete(9)
 require(all(good(g) for g in models),'edge-generator invalid graph')
 records=json.loads((BASE/'model.json').read_text());marked=defaultdict(list);raw=0
 for F in models:
  edges=sum(map(len,F))//2
  for size in range(4):
   if edges+size not in (13,14,15):continue
   for S in combinations([i for i in range(9) if len(F[i])<3],size):
    if any(j in F[i] for i,j in combinations(S,2)):continue
    J=(frozenset(i+1 for i in S),)+tuple(frozenset(j+1 for j in F[i])|({0} if i in S else set()) for i in range(9));raw+=1;bucket=marked[signature(J,0)]
    if not any(iso(J,K,True) is not None for K in bucket):bucket.append(J)
 independent=[g for key in sorted(marked) for g in marked[key]];actual=[decode(10,r['key']) for r in records];coverage=[]
 for g in independent:
  hits=[i for i,h in enumerate(actual) if iso(g,h,True) is not None];require(len(hits)==1,'marked generation entry mismatch');coverage.extend(hits)
 require(len(coverage)==len(set(coverage))==len(records),'marked generation coverage mismatch')
 # Independent degree-placement dynamic program for the convex packing lower bound.
 def floor(total,width):
  dp={0:0}
  for _ in range(11):
   fresh={}
   for old,cost in dp.items():
    for t in range(width+1):
     if old+t<=total:fresh[old+t]=min(fresh.get(old+t,10**9),cost+t*(t-1)//2)
   dp=fresh
  return dp.get(total,10**9)
 lower_cache={};survivors=[];rejected=0
 def validate_record(rec):
  require(type(rec['key']) is int and 0<=rec['key']<1<<45,'invalid graph word')
  g=decode(10,rec['key'])
  h=list(map(len,g));w=[h[i]+2+(i==0) for i in range(10)];caps={}
  require(rec['local_degrees']==h and rec['marked_degree']==h[0] and rec['edges']==sum(h)//2,'incorrect graph degree fields')
  for i,j in combinations(range(10),2):
   c=len(g[i]&g[j])
   if j in g[i]:caps[i,j]=3-(1+c)+(w[i]+w[j]-11)
   else:caps[i,j]=6-(sum(k not in g[i] and k not in g[j] for k in range(10) if k not in (i,j)))
  witness=rec['packing_rejection']
  if witness:
   T=witness['subset']
   require(2<=len(T)<=10 and T==sorted(set(T)) and all(type(i) is int and 0<=i<10 for i in T),'invalid subset')
   total=sum(w[i] for i in T);key=(total,len(T))
   if key not in lower_cache:lower_cache[key]=floor(*key)
   low=lower_cache[key];up=sum(caps[i,j] for i,j in combinations(T,2));require(up<low and total==witness['column_incidences'] and (low,up)==(witness['lower'],witness['upper']),'invalid packing certificate')
  else:
   for size in range(2,11):
    for T in combinations(range(10),size):
     total=sum(w[i] for i in T);key=(total,size)
     if key not in lower_cache:lower_cache[key]=floor(*key)
     require(sum(caps[i,j] for i,j in combinations(T,2))>=lower_cache[key],'survivor packing mismatch')
  return witness is not None
 for rec in records:
  if validate_record(rec):rejected+=1
  else:survivors.append(rec['key'])

 # Direct primary fixture, integer deficit partitions, and low-pair multiplicity signature.
 lines=(BASE/'baseline21.rows').read_text().splitlines()
 G=[set(j for j,c in enumerate(line) if c=='1') for line in lines]
 require(len(G)==21 and all(len(line)==21 and set(line)<=set('01') for line in lines),'bad baseline format')
 require(all(i not in G[i] and ((j in G[i])==(i in G[j])) for i in range(21) for j in range(21)),'bad baseline graph')
 blue=[set(range(21))-{i}-G[i] for i in range(21)]
 baseline={'red_edges':sum(map(len,G))//2,'red_pages':max(len(G[i]&G[j]) for i,j in combinations(range(21),2) if j in G[i]),'blue_pages':max(len(blue[i]&blue[j]) for i,j in combinations(range(21),2) if j not in G[i])}
 require(baseline=={'red_edges':93,'red_pages':3,'blue_pages':6},'literal primary baseline mismatch')
 pair_types=list(combinations(range(4),2));signatures=[]
 from itertools import product
 for x in product(range(5),repeat=6):
  if all(sum(x[k] for k,pair in enumerate(pair_types) if i in pair)==9 for i in range(4)):
   require(x[0]==x[5] and x[1]==x[4] and x[2]==x[3],'opposite low-pair identity failed')
   signatures.append(tuple(sorted(x[:3])))
 require(len(signatures)==10 and sorted(set(signatures))==[(1,4,4),(2,3,4),(3,3,3)],'low multiplicity signature mismatch')
 # Each deliberate malformed record must fail the same checker as valid evidence.
 from copy import deepcopy
 base=next(r for r in records if r['packing_rejection'])
 corrupt=[]
 bad=deepcopy(base);bad['key']=1<<45;corrupt.append(bad)
 bad=deepcopy(base);bad['local_degrees'][0]+=1;corrupt.append(bad)
 bad=deepcopy(base);bad['marked_degree']+=1;corrupt.append(bad)
 bad=deepcopy(base);bad['edges']+=1;corrupt.append(bad)
 for field in ('lower','upper','column_incidences'):
  bad=deepcopy(base);bad['packing_rejection'][field]+=1;corrupt.append(bad)
 bad=deepcopy(base);bad['packing_rejection']['subset']=[0,0];corrupt.append(bad)
 damages=0
 for bad in corrupt:
  try:validate_record(bad)
  except ValueError:damages+=1
  else:raise ValueError('malformed certificate accepted')
 result={'complete':True,'independent_order9_classes':len(models),'edge_level_classes':[s['classes'] for s in stats],'independent_marked_classes':len(independent),'marked_entrywise_matches':len(records),'raw_marked_additions':raw,'packing_rejected':rejected,'survivor_keys':survivors,'packing_dynamic_program_states':len(lower_cache),'literal_baseline':baseline,'low_pair_labelled_signatures':len(signatures),'low_pair_unordered_signatures':[list(x) for x in sorted(set(signatures))],'integrity_controls':damages}
 require(result==json.loads((BASE/'expected.json').read_text())['independent'],'expected independent result mismatch')
 return result
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
