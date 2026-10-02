"""Fresh reviewer checker: physical owned triples, no author module imports.
Written before new ownership/color fixtures or target executable/EXPECTED access.
"""
import itertools as it,collections,json,hashlib

def need(ok,message):
 if not ok:raise ValueError(message)

def encode(obj):return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(obj):return hashlib.sha256(encode(obj)).hexdigest()

def domain(base):
 base=tuple(sorted(base));need(len(set(base))==len(base)==68,'base68 distinct')
 triples=list(it.combinations(range(18),3));ids={t:i for i,t in enumerate(triples)}
 words={};owned={}
 for points in it.combinations(range(18),5):
  mask=sum(1<<p for p in points);ts=tuple(ids[t] for t in it.combinations(points,3));bits=sum(1<<t for t in ts)
  words[mask]=(points,ts,bits)
 for i,w in enumerate(base):
  need(w in words,'physical five-word')
  for t in words[w][1]:need(t not in owned,'base triple unique');owned[t]=i
 blockers={w:sum(1<<i for i in {owned[t] for t in ts if t in owned}) for w,(_,ts,_) in words.items()}
 need(all(blockers.values()),'all physical words blocked')
 need(all(blockers[w]==1<<i for i,w in enumerate(base)),'old-word reinsertion blocker singleton')
 hist=collections.Counter(mask.bit_count() for w,mask in blockers.items() if w not in base)
 records=[[w,blockers[w]] for w in sorted(words)]
 return {'base':base,'words':words,'blockers':blockers,'summary':{'words':len(words),'owned_triples':len(owned),'outside_blocker_histogram':dict(sorted(hist.items())),'whole_blocker_sha256':digest(records),'base_sha256':digest(list(base))}}

def audit(d,owners,patches):
 base=d['base'];words=d['words'];blockers=d['blockers'];old={w:i for i,w in enumerate(base)}
 expected={w for w in words if w not in old and blockers[w].bit_count()<=4}
 need(set(owners)==expected,'complete radius-four ownership domain')
 field={**old,**owners}
 for w,c in field.items():need(type(c) is int and 0<=c<68 and bool(blockers[w]&(1<<c)),'owner is real removed blocker')
 same=collections.defaultdict(list)
 for w,c in field.items():same[c].append(w)
 critical_words={mask for w,mask in blockers.items() if mask.bit_count()==5}
 collisions=set();pairs=0;small_pairs=0;collision_pairs=0
 for group in same.values():
  for a,b in it.combinations(sorted(group),2):
   pairs+=1;union=blockers[a]|blockers[b];compatible=not(words[a][2]&words[b][2])
   if union.bit_count()<=4:
    small_pairs+=1;need(not compatible,'four-field compatible collision')
   if union.bit_count()==5 and compatible:collisions.add(union);collision_pairs+=1
 critical=critical_words|collisions
 need(set(patches)==critical,'complete sparse five exception carrier')
 local_pairs=0;vertex_hist=collections.Counter();local=[]
 for D in sorted(critical):
  need(D.bit_count()==5,'five deleted distinct old indices')
  # Direct filter of the WHOLE physical domain, independent of author bucket/subset decoder.
  carrier=[w for w in sorted(words) if blockers[w]&~D==0]
  patch=patches[D];need(set(patch)<=set(carrier),'patch cannot invent vertices')
  colors={}
  for w in carrier:
   c=patch.get(w,field.get(w));need(type(c) is int and 0<=c<68 and bool((1<<c)&D&blockers[w]),'all carrier vertices have a valid deleted blocker color')
   need(w not in old or c==old[w],'old reinsertion color unchanged');colors[w]=c
  old_vertices={base[i] for i in range(68) if D&(1<<i)}
  need(old_vertices<=set(carrier) and len(old_vertices)==5,'every old word included')
  for a,b in it.combinations(carrier,2):
   local_pairs+=1
   if colors[a]==colors[b]:need(bool(words[a][2]&words[b][2]),'critical coloring physical compatible collision')
  vertex_hist[len(carrier)]+=1
  local.append([D,[[w,colors[w]] for w in carrier]])
 return {'eligible_owner_words':len(owners),'same_owner_pairs':pairs,'small_union_pairs':small_pairs,'five_blocker_carriers':len(critical_words),'collision_carriers':len(collisions),'collision_pairs':collision_pairs,'complete_critical_domains':len(critical),'carrier_kind_overlap':len(critical_words&collisions),'local_physical_pair_checks':local_pairs,'critical_vertex_histogram':dict(sorted(vertex_hist.items())),'whole_domain_coloring_sha256':digest(local),'exact_local_clique_and_chromatic':'For every deletion D with |D|<=5, alpha-compatible-clique=chi=|D|; old words attain it. Ordinary sparse-cover proof required.'}

def first(inputs):
 records=[]
 for row in inputs['classes']:
  d=domain(row['words']);records.append({'id':row['id'],**d['summary']})
 return {'agent':'six-reviewer-5','role':'independent mathematical reviewer','method':'unique owned triples; full five-word domain generated without point-intersection blockers','literal_eight_bases':records,'new_owner_color_fixtures_unread':True,'target_executable_expected_unread':True,'dependency':'Prior9351/9387 base coverage, not a new census audit'}
if __name__=='__main__':
 import pathlib
 p=pathlib.Path(__file__).resolve().parent;rec=first(json.loads((p/'BASES.json').read_text()));(p/'first-record.json').write_bytes(encode(rec));print(json.dumps(rec,indent=2));print('first_record_sha256',digest(rec))
