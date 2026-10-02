"""Exact native46 P20 intake with full scalar/column comparison."""
import hashlib,importlib.util,json,resource,time
from pathlib import Path
from itertools import combinations
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
BASE=HERE.parent/'native24-kernel-cover'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 start=time.monotonic();v=load('native20_scalar',BASE/'p21_verify.py');g=load('native20_packed',BASE/'generate.py')
 fixture=json.loads((HERE/'fixture.json').read_text());word=fixture['native46_control'];v.need(word[:20]==fixture['prefix20'],'declared native20 prefix differs');selected=[768,2560,4608,160,4224,130]
 cases=[]
 for name,gates in [('N46_P20',word[:20]),('N46_P20_HIGH22',word[:20]+[[9,11],[11,12]])]:
  families={}
  for fname,l,h in [('two_minima',2,0),('two_maxima',0,2)]:
   scalar=sorted(v.family(13,gates,lo,hi,'p20') for lo,hi in v.placements(13,l,h))
   packed=g.semantic.analyze_family(13,gates,l,h)
   v.need(scalar==packed['records'],'P20 full scalar/packed rows differ '+fname)
   families[fname]={'records':scalar,'records_sha256':v.digest(scalar),'ordinary':v.ordinary(scalar)}
  routes=[]
  for p in range(13):
   tags=[0]*13;tags[p]=2;D=0
   for a,b in gates:
    D+=v.marked(tags[a]) or v.marked(tags[b])
    if tags[a]>tags[b]:tags[a],tags[b]=tags[b],tags[a]
   routes.append([p,tags.index(2),D])
  high=families['two_maxima']['ordinary']['envelope']
  anchors=[[p,sum(2**d for lo,hi,d in high if hi>>p&1)] for p in sorted({r[1] for r in routes})]
  costs={r[1]:r for r in families['two_maxima']['records']}
  original=[costs[m] for m in selected]
  outputs=[];free_rows=set();full=set()
  for x in range(8192):
   before=[x>>i&1 for i in range(13)];row=v.simulate(before,gates)
   full.add(sum(bit*2**i for i,bit in enumerate(row)))
   if name.endswith('HIGH22'):
    v.need(row[0]==min(before) and row[12]==max(before),'HIGH22 did not hold min0/max12')
    free_rows.add(sum(row[i]*2**(i-1) for i in range(1,12)))
  v.need(sorted(full)==g.boolean_image(13,gates),'P20 complete Boolean images differ')
  cases.append({'name':name,'gates':gates,'prefix_sha256':v.digest(gates),'families':families,'unary_high_routes':routes,'ordinary_high_anchors':anchors,'selected_six':original,'full_boolean_outputs':len(full),'middle_image':sorted(free_rows),'middle_image_sha256':v.digest(sorted(free_rows))})
 native=cases[0]
 (ROOT/'p20-raw-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 v.need([max(t for t in range(10) if 2**t*mass<=512) for port,mass in native['ordinary_high_anchors']]==[3,2,1], 'P20 necessary generic route budgets not present')
 v.need([r[2:5] for r in native['selected_six']]==[[0,1536,4],[0,2560,4],[0,4608,5],[0,4128,5],[0,4224,5],[0,4352,5]],'P20 six-history hypotheses not present')
 # Explicit disjoint swaps, preserving the native46 word's complete function.
 normalized=word[:20]+[[9,11],[11,12]]+[gate for i,gate in enumerate(word[20:],20) if i not in (21,27)]
 v.need(word[21]==[9,11] and word[27]==[11,12],'native control positions changed')
 v.need(not set(word[20])&{9,11},'first control commute invalid')
 v.need(all(not set(word[i])&{11,12} for i in [20,22,23,24,25,26]),'second control commute invalid')
 v.need(len(normalized)==46 and all(1<=a<b<=11 for a,b in normalized[22:]),'control suffix leaves active wires')
 for x in range(8192):
  before=[x>>i&1 for i in range(13)]
  v.need(v.simulate(before,normalized)==v.simulate(before,word)==sorted(before),'normalized46 control differs')
 suffix=[[a-1,b-1] for a,b in normalized[22:]]
 for x in cases[1]['middle_image']:
  before=[x>>i&1 for i in range(11)]
  v.need(v.simulate(before,suffix)==sorted(before),'24-gate image control fails')
 # All standard first gates satisfying BOTH ordinary ceilings, at the actual root.
 accepted=[]
 for gate in combinations(range(13),2):
  low=v.ordinary_transition(cases[1]['families']['two_minima']['ordinary']['envelope'],gate)
  high=v.ordinary_transition(cases[1]['families']['two_maxima']['ordinary']['envelope'],gate)
  if sum(2**r[2] for r in low)<=512 and sum(2**r[2] for r in high)<=512:
   accepted.append(list(gate))
 result={'status':'NATIVE20_INITIAL_GENERIC_MAXIMUM_REDUCTION_PREMISES_AND_TARGET_REPLAYED_NOT_EXCLUDED','agent':'six-sorting-2','role':'researcher','source_commit':'dce3955b2880381edb2884b7446d282bf7bdeda5','generic_graph_parent':'bafkreigyiwnzlza2aetdtlaoctzrvsare6jh6onf5mxb7yzftmmm7xqk4u','cases':cases,'normalized46_word':normalized,'middle11_upper_control':suffix,'initial_target_comparator_interval':[22,24],'root_first_gate_ordinary_candidates':accepted,'root_first_gate_candidate_count':len(accepted),'metrics':v.METRICS,'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'prior_art_boundary':'The published historical thirteen_twenty_prefix_exclusion concerns the45-gate incumbent, not native46 prefix N46_P20.'}
 (ROOT/'p20-intake.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:x for k,x in result.items() if k not in ['cases','normalized46_word','middle11_upper_control']}))
 for c in cases:print(json.dumps({'name':c['name'],'low':c['families']['two_minima']['ordinary']['envelope'],'low_mass':c['families']['two_minima']['ordinary']['mass'],'high':c['families']['two_maxima']['ordinary']['envelope'],'high_mass':c['families']['two_maxima']['ordinary']['mass'],'anchors':c['ordinary_high_anchors'],'full_outputs':c['full_boolean_outputs'],'middle_rows':len(c['middle_image']),'middle_sha256':c['middle_image_sha256']}))
if __name__=='__main__':main()
