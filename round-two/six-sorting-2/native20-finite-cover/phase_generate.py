"""Exact generated paired-profile phase before the first touch on port6."""
import hashlib,importlib.util,json,resource,time
from collections import deque
from itertools import combinations
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
BASE=HERE.parent/'native24-kernel-cover'
spec=importlib.util.spec_from_file_location('paired_pre6_numeric',BASE/'p21_verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def key(low,high):return tuple(map(tuple,low)),tuple(map(tuple,high))
def mass(rows):return sum(2**r[2] for r in rows)
def support(rows):return {p for lo,hi,d in rows for p in range(13) if (lo|hi)>>p&1}
def main():
 start=time.monotonic();intake=json.loads((ROOT/'p20-intake.json').read_text());root=intake['cases'][1]
 initial=key(root['families']['two_minima']['ordinary']['envelope'],root['families']['two_maxima']['ordinary']['envelope'])
 states={initial:0};todo=deque([initial]);edges={};phase_transitions=joint_transitions=0
 while todo:
  state=todo.popleft();low,high=state;sid=states[state];out=[]
  v.need(mass(low)==mass(high)==480,'pre6 equality phase mass changed')
  v.need(any((lo,hi,d)==(17,0,6) for lo,hi,d in low) and any((lo,hi,d)==(65,0,5) for lo,hi,d in low),'LOW4/6 changed before6')
  v.need(any((lo,hi,d)==(0,4160,5) for lo,hi,d in high),'HIGH6 changed before6')
  dead=sorted(set(range(13))-support(low)-support(high))
  v.need(len(dead)<=4,'more than four preparation ports before6')
  for gate in combinations(range(13),2):
   if 6 in gate:continue
   nl=v.ordinary_transition(low,gate);nh=v.ordinary_transition(high,gate)
   phase_transitions+=1
   if mass(nl)>512 or mass(nh)>512:continue
   ns=key(nl,nh)
   if ns==state:
    v.need(not set(gate)&(support(low)|support(high)),'changed-free selfloop not a preparation')
   else:
    v.need(4 not in gate and len(nl)+len(nh)<len(low)+len(high),'non6 event is not a class-decreasing merge')
    if ns not in states:states[ns]=len(states);todo.append(ns)
   out.append([list(gate),states[ns],ns==state])
  edges[sid]=out
 ordered=[None]*len(states)
 for state,i in states.items():ordered[i]=state
 joint=[];partners=set()
 for i,state in enumerate(ordered):
  low,high=state;cases=[]
  for r in range(13):
   if r==6:continue
   gate=tuple(sorted((6,r)));nl=v.ordinary_transition(low,gate);nh=v.ordinary_transition(high,gate);joint_transitions+=1
   if mass(nl)<=512 and mass(nh)<=512:
    v.need(mass(nl)==mass(nh)==512,'accepted first6 did not saturate both families')
    v.need(not (support(nl)-{0})&(support(nh)-{12}),'postjoint live sets overlap')
    partners.add(r);cases.append({'partner':r,'low':nl,'high':nh,'native4_branch_excluded':r==4})
  v.need(any(c['partner']==4 for c in cases),'native4 branch missing')
  joint.append({'state_id':i,'cases':cases})
 # Retain ALL merge-event histories. A representative profile alone is not a Boolean-function cover.
 words=[]
 def paths(sid,word):
  words.append({'state_id':sid,'event_word':word})
  for gate,destination,selfloop in edges[sid]:
   if not selfloop:paths(destination,word+[gate])
 paths(0,[])
 v.need(max(len(w['event_word']) for w in words)<=4,'pre6 event history too long')
 result={'status':'COMPLETE_EXACT_PRE6_PAIRED_PROFILE_AND_EVENT_WORD_COVER','agent':'six-sorting-2','role':'researcher','states':[{'id':i,'low':list(map(list,state[0])),'high':list(map(list,state[1])),'preparation_ports':sorted(set(range(13))-support(state[0])-support(state[1])),'transitions':edges[i]} for i,state in enumerate(ordered)],'all_event_words':words,'first6_cases':joint,'state_count':len(states),'event_word_count':len(words),'maximum_event_word_length':max(len(w['event_word']) for w in words),'maximum_preparation_ports':max(len(set(range(13))-support(state[0])-support(state[1])) for state in ordered),'first6_partner_union':sorted(partners),'post_native_exclusion_partner_union':sorted(partners-{4}),'phase_transition_controls':phase_transitions,'first6_transition_controls':joint_transitions,'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'warning':'Current-profile equality does not imply equality of Boolean prefix functions. Every event word is retained, and arbitrary preparation functions still require complete semantic closure.'}
 (ROOT/'pre6-cover.json').write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({k:z for k,z in result.items() if k not in ['states','all_event_words','first6_cases']},sort_keys=True))
if __name__=='__main__':main()
