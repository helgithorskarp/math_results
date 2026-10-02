"""Independent carrier pruning, full original exit cubes, and calibration controls."""
import json,pathlib,collections
import independent as I

def check_pruning(root):
 lows=[i for i,s in root if s=='L'];highs=[i for i,s in root if s=='H']
 constants={i:-len(lows)+j for j,i in enumerate(lows)}
 constants.update({i:2+j for j,i in enumerate(highs)})
 free=[i for i in range(13) if i not in constants]
 rows=[]
 for word in range(1<<len(free)):
  row=[0]*13
  for j,i in enumerate(free):row[i]=(word>>j)&1
  for i,v in constants.items():row[i]=v
  rows.append(row)
 tags=[constants.get(i) for i in range(13)]
 carriers=[free.index(i) if i in free else None for i in range(13)]
 retained=[];D=R=0
 for a,b in I.PREFIX:
  touched=tags[a] is not None or tags[b] is not None
  changed=False
  for row in rows:
   if row[a]>row[b]:row[a],row[b]=row[b],row[a];changed=True
  if touched:
   D+=1
   if (tags[a] if tags[a] is not None else 0)>(tags[b] if tags[b] is not None else 0):
    tags[a],tags[b]=tags[b],tags[a];carriers[a],carriers[b]=carriers[b],carriers[a]
  elif changed:retained.append((carriers[a],carriers[b]))
  else:R+=1
 I.need(len(retained)==27-D-R,'disjoint deletion sets')
 for word,row in enumerate(rows):
  pruned=I.simulate([(word>>j)&1 for j in range(len(free))],retained)
  I.need(all(pruned[c]==row[i] for i,c in enumerate(carriers) if c is not None),'whole original carrier quotient')
 return D,R,len(rows),len(retained)

def run(data):
 profiles=data['original_profiles'];b=data['defining_cover']
 pruning_assignments=pruning_gates=0
 for p in profiles:
  D,R,n,g=check_pruning(p['root']);I.need((D,R)==(p['D'],p['R']),'original deletions crosscheck')
  pruning_assignments+=n;pruning_gates+=g
 exit_assignments=0;witnesses=0;outside=0
 for i,c in b['exits'].items():
  roots=[j for j,s in c['root']];free=[j for j in range(13) if j not in roots]
  word=tuple((I.DEAD[a],I.DEAD[z]) for a,z in b['words'][i])
  for assignment in range(2048):
   row=[0]*13
   for j,p in enumerate(free):row[p]=(assignment>>j)&1
   row[roots[0]]=2;row[roots[1]]=3
   result=I.simulate(row,I.PREFIX+word)
   I.need(result[11:]==[2,3] and result[10]==max(result[:11]),'entire immutable original maximum cube')
   exit_assignments+=1
  raw=c['input'];row=I.simulate([(raw>>j)&1 for j in range(13)],I.PREFIX+word)
  I.need(row[10]!=int(raw.bit_count()>=3),'full original wrong-rank witness')
  witnesses+=1
  # A Boolean witness is necessarily outside a distinct-rank 2/3 clamping.
  outside+=1
 five=((0,1),(3,4),(2,4),(2,3),(1,4),(0,3),(0,2),(1,3),(1,2))
 from itertools import product,permutations
 controls=0
 for row in list(product((0,1),repeat=5))+list(product((-7,0,11),repeat=5))+list(permutations(range(5))):
  I.need(I.simulate(row,five)==sorted(row),'known five-input sorter: whole Boolean/ternary/distinct domains')
  controls+=1
 # Two distinct immutable domains have identical marker/cost records but
 # different activity sets. Thus marker-only deduplication is unsound.
 conflation=None
 for a in data['tight_profiles']:
  for z in data['tight_profiles']:
   if a['marks']==z['marks'] and (a['D'],a['R'])==(z['D'],z['R']) and a['image']!=z['image']:
    conflation=dict(left=a['root'],right=z['root'],marks=a['marks'],D=a['D'],R=a['R'],images=[a['image'],z['image']]);break
  if conflation:break
 I.need(conflation is not None,'original-domain conflation negative control')
 # Standard orientation is required by the maximum-cut induction.
 row=[0]*13;row[10]=1;row[11]=2;row[12]=3
 reversed_touch=I.simulate(row,((10,9),))
 I.need(reversed_touch[10]==0 and row[10]==1,'dropping standard orientation defeats the local invariant')
 # Complete graph grading, rather than only a BFS bound.
 I.need(all(a==z for a,z in zip(b['shortest'],b['longest'])),'every exit-avoiding admissible path has its function-determined length')
 depths=collections.Counter(b['shortest'][i] for i in b['retained'])
 I.need(dict(depths)=={0:1,1:5,2:16,3:36,4:57,5:51,6:15},'complete retained grading census')
 for i,j,a,z in b['edges']:
  I.need(b['shortest'][j]==b['shortest'][i]+1,'every full directed edge advances grading by one')
 return dict(whole_original_pruning_assignments=pruning_assignments,retained_carrier_gates=pruning_gates,
  exit_cube_assignments=exit_assignments,whole_wrong_rank_witnesses=witnesses,
  outside_distinct_rank_clamping_witnesses=outside,positive_sorter_controls=controls,
  marker_conflation_control=conflation,standard_orientation_countercontrol=True,
  retained_depths=dict(sorted(depths.items())),all_edges_graded=True)

if __name__=='__main__':
 data=I.build();record=run(data)
 raw=json.dumps(record,sort_keys=True,separators=(',',':'))+'\n'
 pathlib.Path(__file__).with_name('CONTROLS.json').write_text(raw)
 print(raw,end='')
