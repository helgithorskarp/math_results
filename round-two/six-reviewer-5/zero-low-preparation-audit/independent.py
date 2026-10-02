"""Own whole original scalar domains and row-function/DAG preparation audit."""
from itertools import combinations,product
from collections import deque
import json,pathlib,hashlib

PREFIX=((0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
 (0,2),(3,6),(4,12),(5,7),(8,10),
 (0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),
 (9,11),(11,12),(3,6),(6,7),(5,7),(9,10),(10,11),(7,11))
DEAD=(5,6,7,9,10)
GATES=tuple(combinations(range(5),2))
def need(ok,message):
 if not ok:raise ValueError(message)
def gate(row,a,b):
 if row[a]>row[b]:row[a],row[b]=row[b],row[a]
def simulate(row,word=PREFIX):
 row=list(row)
 for a,b in word:gate(row,a,b)
 return row
def dead_pattern(row):return sum(row[a]<<j for j,a in enumerate(DEAD))
def original_domains():
 roots=[((i,s),) for i in range(13) for s in ('L','H')]
 roots += [tuple(zip(pair,sides)) for pair in combinations(range(13),2) for sides in product(('L','H'),repeat=2)]
 summaries=[];tight=[];low={};high={};assignments=0
 for root in roots:
  constants={}; lows=[i for i,s in root if s=='L']; highs=[i for i,s in root if s=='H']
  for j,i in enumerate(lows):constants[i]=-len(lows)+j
  for j,i in enumerate(highs):constants[i]=2+j
  free=[i for i in range(13) if i not in constants];k=len(free)
  rows=[]
  for word in range(1<<k):
   row=[0]*13
   for j,i in enumerate(free):row[i]=(word>>j)&1
   for i,v in constants.items():row[i]=v
   rows.append(row)
  tags=[constants.get(i) for i in range(13)];D=R=0
  for a,b in PREFIX:
   marked=tags[a] is not None or tags[b] is not None
   changes=0
   for row in rows:
    if row[a]>row[b]:row[a],row[b]=row[b],row[a];changes+=1
   if marked:
    D+=1
    va=tags[a] if tags[a] is not None else 0
    vb=tags[b] if tags[b] is not None else 0
    if va>vb:tags[a],tags[b]=tags[b],tags[a]
   elif changes==0:R+=1
  assignments+=len(rows)
  marked_ports=[i for i,t in enumerate(tags) if t is not None]
  need(all(all(row[i]==tags[i] for i in marked_ports) for row in rows),'marked routing independent of original free cube')
  image=0;maxreq=0;minreq=0
  unmarked=[i for i in range(13) if i not in marked_ports]
  for row in rows:
   pat=dead_pattern(row);need(0<=pat<32,'unmarked dead ports')
   image|=1<<pat
   if max(row[i] for i in unmarked)==1:maxreq|=1<<pat
   if min(row[i] for i in unmarked)==0:minreq|=1<<pat
  summary=dict(root=root,k=k,D=D,R=R,marks=marked_ports,image=image,maximum_req=maxreq,minimum_req=minreq)
  summaries.append(summary)
  if D+R==(5 if k==12 else 9):
   need(all(i not in DEAD for i in marked_ports),'tight marks outside preparation ports')
   summary['minimum_free_port']=min(unmarked);summary['maximum_free_port']=max(unmarked)
   tight.append(summary)
  if len(root)==2 and len(lows)==2:
   need(marked_ports[0]==0,'held LOW0')
   low[marked_ports[1]]=max(low.get(marked_ports[1],-1),D)
  if len(root)==2 and len(highs)==2:
   need(marked_ports[1]==12,'held HIGH12')
   high[marked_ports[0]]=max(high.get(marked_ports[0],-1),D)
 need(len(summaries)==338 and assignments==745472,'whole original domain census')
 need(len(tight)==90 and len({s['image'] for s in tight})==9,'entire tight activity domain')
 need(low=={1:7,2:7,3:6,4:6,8:6} and high=={11:9},'ordinary dyadic inventories')
 return summaries,tight,dict(low=low,high=high,low_mass=sum(2**c for c in low.values()),high_mass=sum(2**c for c in high.values()),scalar_assignments=assignments)

def inversion(row):
 return sum(((row>>i)&1) and not ((row>>j)&1) for i,j in GATES)
def potential(f):return sum(inversion(row) for row in f)
def step(f,a,b):
 changed=0;out=[]
 for i,row in enumerate(f):
  if ((row>>a)&1) and not ((row>>b)&1):row^=(1<<a)|(1<<b);changed|=1<<i
  out.append(row)
 return tuple(out),changed

def parent():
 raw=[simulate([(word>>i)&1 for i in range(13)]) for word in range(8192)]
 for word,row in enumerate(raw):
  sorted_row=[0]*(13-word.bit_count())+[1]*word.bit_count()
  need(all(row[i]==sorted_row[i] for i in (0,11,12)),'all literal held ranks')
 need(len({tuple(r[1:11]) for r in raw})==136,'literal ten-wire image')
 return raw

def closure(tight,raw,all_cuts=False):
 subsets=sorted({s['image'] for s in tight})
 if not all_cuts:
  cuts=[next(s for s in tight if s['root']==((0,'H'),(1,'H'))),next(s for s in tight if s['root']==((8,'H'),(9,'H')))]
 else:cuts=[s for s in tight if s['maximum_free_port']==10]
 # Whole original wrong-rank witnesses are found in increasing raw-input order.
 first_bad={}
 for word,row in enumerate(raw):
  pattern=dead_pattern(row);correct=int(word.bit_count()>=3)
  first_bad.setdefault((pattern,1-correct),word)
 def obstruction(f):
  bad=[first_bad[(s,(v>>4)&1)] for s,v in enumerate(f) if (s,(v>>4)&1) in first_bad]
  if not bad:return None
  word=min(bad)
  for s in cuts:
   if all((f[p]>>4)&1 for p in range(32) if (s['maximum_req']>>p)&1):
    need(s['D']==9 and s['R']==0 and s['marks']==[11,12],'whole-cube tight maximum cut premise')
    return dict(root=s['root'],input=word,physical_port=10)
  return None
 states=[tuple(range(32))];indices={states[0]:0};words=[()];distances=[0];exits={};edges=[];queue=deque([0])
 while queue:
  i=queue.popleft();f=states[i];cut=obstruction(f)
  if cut is not None:exits[i]=cut;continue
  for a,b in GATES:
   child,changed=step(f,a,b)
   if not all(changed&s for s in subsets):continue
   need(potential(f)-potential(child)==changed.bit_count()*(b-a)>0,'strict full-function inversion potential')
   if child not in indices:
    if len(states)>=20000:raise RuntimeError('INCOMPLETE: unchanged20000-state operational guard reached')
    j=len(states);indices[child]=j;states.append(child);words.append(words[i]+((a,b),));distances.append(distances[i]+1);queue.append(j)
   j=indices[child];edges.append((i,j,a,b))
  need(len(states)<20000,'bounded complete closure')
 # Increasing physical sortedness topologically orders every admissible edge.
 longest=[-1]*len(states);longest[0]=0
 incoming=[[] for _ in states]
 for i,j,a,b in edges:incoming[j].append(i)
 for j in sorted(range(len(states)),key=lambda v:-potential(states[v])):
  if j:longest[j]=max(longest[i]+1 for i in incoming[j])
  need(longest[j]>=distances[j]>=0,'all physical states reachable')
 kept=[i for i in range(len(states)) if i not in exits]
 return dict(states=states,words=words,shortest=distances,longest=longest,potentials=[potential(f) for f in states],edges=edges,exits=exits,
  retained=kept,retained_count=len(kept),max_retained_shortest=max(distances[i] for i in kept),max_retained_longest=max(longest[i] for i in kept),all_cuts=all_cuts)

def build():
 profiles,tight,inventory=original_domains();raw=parent()
 base=closure(tight,raw)
 need((len(base['states']),len(base['exits']),len(base['edges']),base['retained_count'],max(base['shortest']),base['max_retained_shortest'])==(374,193,446,181,7,6),'complete defining cover counts: seven includes excluded functions')
 need(potential(tuple(range(32)))==80,'initial exact inversion potential')
 stronger=closure(tight,raw,True)
 return dict(prefix=PREFIX,dead_ports=DEAD,original_profiles=profiles,tight_profiles=tight,inventory=inventory,parent_inputs=8192,parent_ten_wire_image=136,
  defining_cover=base,all_tight_maximum_cover=stronger,initial_inversion_potential=80)

def evidence(data):
 """Lossless compact rows; no stored truth-table hash replaces row comparison."""
 b=data['defining_cover'];a=data['all_tight_maximum_cover']
 need(all(b[k]==a[k] for k in b if k!='all_cuts'),'enlarged tight-maximum scan has exactly the same complete cover')
 fields=('root','k','D','R','marks','image','maximum_req','minimum_req')
 return dict(format='whole original cubes; complete 32-byte row functions encoded as hex',
  prefix=data['prefix'],dead_ports=data['dead_ports'],profile_fields=fields,
  profiles=[[s[k] for k in fields] for s in data['original_profiles']],
  tight_profile_indices=[i for i,s in enumerate(data['original_profiles']) if s in data['tight_profiles']],
  inventory=data['inventory'],parent_inputs=data['parent_inputs'],parent_ten_wire_image=data['parent_ten_wire_image'],
  functions=[bytes(f).hex() for f in b['states']],words=b['words'],shortest=b['shortest'],longest=b['longest'],potentials=b['potentials'],edges=b['edges'],exits=b['exits'],retained=b['retained'],
  max_retained_shortest=b['max_retained_shortest'],max_retained_longest=b['max_retained_longest'],
  enlarged_cut_census=sum(s['maximum_free_port']==10 for s in data['tight_profiles']),enlarged_cut_cover_equal=True,initial_inversion_potential=data['initial_inversion_potential'])
if __name__=='__main__':
 data=build();raw=(json.dumps(evidence(data),sort_keys=True,separators=(',',':'))+'\n').encode();path=pathlib.Path(__file__).with_name('EVIDENCE.json');path.write_bytes(raw)
 print(json.dumps(dict(profiles=len(data['original_profiles']),tight=len(data['tight_profiles']),inventory=data['inventory'],
  base={**{k:data['defining_cover'][k] for k in ('retained_count','max_retained_shortest','max_retained_longest')},'states':len(data['defining_cover']['states']),'exits':len(data['defining_cover']['exits']),'max_all_shortest':max(data['defining_cover']['shortest']),'max_all_longest':max(data['defining_cover']['longest'])},
  stronger={**{k:data['all_tight_maximum_cover'][k] for k in ('retained_count','max_retained_shortest','max_retained_longest')},'states':len(data['all_tight_maximum_cover']['states']),'exits':len(data['all_tight_maximum_cover']['exits'])},
  sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)),sort_keys=True))
