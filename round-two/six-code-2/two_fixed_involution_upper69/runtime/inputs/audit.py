"""Independent literal rooted classification, not an author-module import."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import hashlib, json, time
from math import factorial
CELLS=tuple((r,c) for r in range(4) for c in range(4) if r!=c)
CELL={rc:i for i,rc in enumerate(CELLS)}
def require(cond,msg):
 if not cond: raise ValueError(msg)
def blocks(q):
 q=tuple(sorted(tuple(sorted(b)) for b in q))
 require(len(q)==20 and len(set(q))==20,'bad block count')
 require(all(len(b)==4 and len(set(b))==4 and all(type(x)==int and 0<=x<17 for x in b) for b in q),'bad block')
 pairs=[a for b in q for a in combinations(b,2)]
 require(len(pairs)==len(set(pairs))==120,'repeated covered pair')
 return q
ANCHORS=tuple(sorted([(12,13,15,16)]+[tuple(sorted([i for i,(r,c) in enumerate(CELLS) if r==k]+[15])) for k in range(4)]+[tuple(sorted([i for i,(r,c) in enumerate(CELLS) if c==k]+[16])) for k in range(4)]))
def model():
 used={p for b in ANCHORS for p in combinations(b,2)}
 cols=tuple(b for b in combinations(range(15),4) if not used.intersection(combinations(b,2)))
 alt=tuple(b for b in combinations(range(15),4) if not {12,13}<=set(b) and len({CELLS[i][0] for i in b if i<12})==sum(i<12 for i in b) and len({CELLS[i][1] for i in b if i<12})==sum(i<12 for i in b))
 require(cols==alt and len(cols)==225,'candidate reduction')
 adj=tuple(tuple(j for j,d in enumerate(cols) if i!=j and len(set(b)&set(d))<=1) for i,b in enumerate(cols))
 return cols,adj
COLS,ADJ=model(); COLINDEX={b:i for i,b in enumerate(COLS)}
def key(q):
 require(set(ANCHORS)<=set(q),'missing anchors')
 k=tuple(sorted(COLINDEX[b] for b in q if b not in ANCHORS))
 require(len(k)==11,'wrong clique size')
 return k
GROUP=[]
for sigma in permutations(range(4)):
 for transpose in (False,True):
  for swap in (False,True):
   g=[]
   for r,c in CELLS:
    rc=(sigma[c],sigma[r]) if transpose else (sigma[r],sigma[c])
    g.append(CELL[rc])
   g += [13,12] if swap else [12,13]
   g += [14,16,15] if transpose else [14,15,16]
   require(sorted(g)==list(range(17)),'nonbijection anchor map')
   require(tuple(sorted(tuple(sorted(g[x] for x in b)) for b in ANCHORS))==ANCHORS,'anchor moved')
   GROUP.append(tuple(g))
require(len(set(GROUP))==96,'anchor group size')
def properties(q):
 rho=tuple(sum(x in b for b in q) for x in range(17))
 require(max(rho)<=5 and sum(5-r for r in rho)==5,'replication')
 used={p for b in q for p in combinations(b,2)}
 leave=set(combinations(range(17),2))-used
 low={x for x in range(17) if rho[x]==5}
 high=set(range(17))-low
 require(not any(a in low and b in low for a,b in leave),'low-low leave')
 friends={p:tuple(v for v in sorted(low) if tuple(sorted((p,v))) in leave) for p in high}
 require(sum(len(v) for v in friends.values())==len(low),'low partition')
 roots=tuple((p,v,w) for p in sorted(high) for v,w in combinations(friends[p],2))
 require(roots,'no carrier root')
 return rho,leave,roots

def normalized(q):
 """All literal point bijections from q into the fixed carrier."""
 rho,leave,roots=properties(q)
 for p,v,w in roots:
  shared=[b for b in q if v in b and w in b]
  require(len(shared)==1,'shared low pair not unique')
  a,b=sorted(set(shared[0])-{v,w})
  require(p not in shared[0],'hub in shared block')
  rows=sorted(tuple(x for x in B if x!=v) for B in q if v in B and w not in B)
  cs=sorted(tuple(x for x in B if x!=w) for B in q if w in B and v not in B)
  require(len(rows)==len(cs)==4,'anchor degree')
  missing=[tuple(r for r,R in enumerate(rows) if not set(R)&set(C)) for C in cs]
  require(all(len(z)==1 for z in missing) and sorted(z[0] for z in missing)==list(range(4)),'complement matching')
  cols=[None]*4
  for C,(r,) in zip(cs,missing): cols[r]=C
  f=[None]*17
  for i,(r,c) in enumerate(CELLS):
   meet=set(rows[r])&set(cols[c]); require(len(meet)==1,'cell multiplicity')
   x=next(iter(meet)); require(f[x] is None,'repeated cell');f[x]=i
  for x,y in ((a,12),(b,13),(p,14),(v,15),(w,16)):
   require(f[x] is None,'special in cell');f[x]=y
  require(sorted(f)==list(range(17)),'incomplete normalization')
  for g in GROUP:
   fg=tuple(g[y] for y in f)
   image=tuple(sorted(tuple(sorted(fg[x] for x in B)) for B in q))
   yield key(image),fg

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def classify(lines,fixtures):
 require(len(lines)==len(set(lines)),'duplicate census leaves')
 universe=set(lines);stars={}
 for k in universe:
  require(tuple(sorted(k))==k and len(k)==11 and len(set(k))==11 and all(0<=i<225 for i in k),'malformed leaf')
  q=blocks(ANCHORS+tuple(COLS[i] for i in k));properties(q);stars[k]=q
 fixtures=[blocks(q) for q in fixtures]
 ownership={};rows=[];proof=[]
 for i,q in enumerate(fixtures):
  seen={};maps=0
  rho,leave,roots=properties(q)
  for k,g in normalized(q):
   require(k in universe,'fixture normalization absent from census')
   maps+=1
   if k not in seen:seen[k]=g
  require(maps==96*len(roots),'root map coverage')
  common=set(seen)&set(ownership)
  require(not common,'isomorphic fixture duplication')
  require(maps%len(seen)==0,'orbit-stabilizer denominator')
  aut=maps//len(seen)
  # Fiber over this fixture's own carrier embedding independently lists every automorphism.
  own=key(q); automorphisms=[g for k,g in normalized(q) if k==own]
  require(len(automorphisms)==aut and len(set(automorphisms))==aut,'automorphism fiber')
  require(all(tuple(sorted(tuple(sorted(g[x] for x in B)) for B in q))==q for g in automorphisms),'false automorphism')
  for k,g in seen.items():
   # Positive inverse map, supplied independently of the census and author outputs.
   inv=[None]*17
   for x,y in enumerate(g):inv[y]=x
   require(tuple(sorted(tuple(sorted(inv[x] for x in B)) for B in stars[k]))==q,'positive map failed')
   ownership[k]=i;proof.append([list(k),i,inv])
  rows.append(dict(fixture=i,deficit_profile=sorted([5-r for r in rho if r<5],reverse=True),carrier_roots=len(roots),embeddings=maps,rooted_packings=len(seen),full_automorphism_order=aut,automorphisms_sha256=digest(sorted(automorphisms))))
 require(set(ownership)==universe,'uncovered labelled star')
 result=dict(agent='six-reviewer-5',role='independent mathematical reviewer',status='COMPLETE',graph=dict(vertices=225,edges=sum(map(len,ADJ))//2,target=11),labelled_stars=len(stars),labelled_stars_sha256=digest(sorted(stars)),class_count=len(rows),classes=rows,full_labelled_count=sum(factorial(17)//r['full_automorphism_order'] for r in rows),positive_maps_sha256=digest(sorted(proof)),profile_counts=[dict(deficit_profile=list(p),count=c) for p,c in sorted(Counter(tuple(sorted([5-r for r in properties(q)[0] if r<5],reverse=True)) for q in stars.values()).items())])
 result['deficit_quotient']=quotient(stars)
 return result,sorted(proof)

def move(d,g):
 out=[0]*15
 for x in range(15):out[g[x]]=d[x]
 return tuple(out)
def quotient(stars):
 # Four stars and fourteen bars give nonnegative parts summing to four;
 # adding one to last part forces d_14 >= 1.
 raw=[]
 for bars in combinations(range(18),14):
  b=(-1,)+bars+(18,)
  d=tuple(b[i+1]-b[i]-1 for i in range(15))
  raw.append(d[:-1]+(d[-1]+1,))
 require(len(set(raw))==3060 and all(sum(d)==5 and d[14]>=1 for d in raw),'raw assignment count')
 remaining=set(raw);reps=[];orbits={}
 for d in sorted(raw):
  if d not in remaining:continue
  orbit={move(d,g) for g in GROUP}
  require(orbit<=remaining,'overlapping deficit orbits')
  remaining-=orbit;reps.append(d);orbits[d]=len(orbit)
 require(not remaining and len(reps)==108,'deficit quotient size')
 lookup={d:i for i,d in enumerate(reps)};bycase={d:[] for d in reps}
 for k,q in stars.items():
  d=tuple(5-r for r in properties(q)[0][:15])
  if d in lookup:bycase[d].append(k)
 records=[];rooted=[]
 for i,d in enumerate(reps):
  # Optional profile readout follows the public local column indexing.
  h={x for x in range(15) if d[x]};budget=(len(h)-1)*(len(h)-2)//2
  used={p for b in ANCHORS for p in combinations(b,2)}
  used_high=sum(set(p)<=h for p in used)
  budget_columns=tuple(b for b in COLS if sum(set(p)<=h for p in combinations(b,2))<=budget-used_high)
  index={b:j for j,b in enumerate(budget_columns)}
  quota=[5-d[x]-sum(x in b for b in ANCHORS) for x in range(15)]
  direct=min(quota)<0 or used_high>budget
  covers=sorted(tuple(sorted(index[COLS[j]] for j in k)) for k in bycase[d])
  # Public readout convention: compact JSON followed by one newline.
  import hashlib
  sha=hashlib.sha256((json.dumps(covers,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
  record=dict(case=i,count=len(covers),orbit_size=orbits[d],direct=direct)
  if not direct:record['covers_sha256']=sha
  records.append(record)
  for cover in covers:
   Q=tuple(sorted(ANCHORS+tuple(budget_columns[j] for j in cover)))
   rooted.append((i,cover,Q))
 rooted_sha=hashlib.sha256((json.dumps(rooted,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
 result=dict(rooted_packings_sha256=rooted_sha,raw_assignments=3060,deficit_orbits=108,representative_packings=sum(r['count'] for r in records),records=records,profile_counts=Counter(tuple(sorted([x for x in d if x],reverse=True)) for d in reps for k in bycase[d]))
 result['profile_counts']=[dict(deficit_profile=list(p),count=c) for p,c in sorted(result['profile_counts'].items())]
 return result
