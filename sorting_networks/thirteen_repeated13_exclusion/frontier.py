"""Exact cumulative class incidence, importing published peer/prior exclusions.

This script audits counts and identities, not imported proof certificates.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
PAIRS=tuple(itertools.combinations(range(11),2))

def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def pinned(path,sha):
 raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==sha
 return json.loads(raw)

def main():
 if not __debug__:raise RuntimeError('Assertions must be enabled')
 parser=argparse.ArgumentParser()
 parser.add_argument('--quotient',type=Path,default=HERE.parent/'thirteen_extreme_multiset_quotient/certificate.json')
 parser.add_argument('--peer-certificate',type=Path,default=HERE.parent.parent/'sorting13_B11_ten_event_branch_exclusion/certificate.json')
 parser.add_argument('--prior-certificate',type=Path,default=HERE.parent/'thirteen_repeated23_exclusion/certificate.json')
 args=parser.parse_args()
 table=pinned(args.quotient,'d670b600ed1c2e31990d6e2458b748d160a257b5dacf4bf15d3e270414202047')['class_table']
 peer=pinned(args.peer_certificate,'47ec194a3decff3508ffb5d0279aea2352de1921b790287a5c2212c62ef74bee')
 prior=pinned(args.prior_certificate,'e28e4321d899da978b301f9af5f43df37c71339658765a13c41253206d5ef773')
 current=json.loads((HERE/'certificate.json').read_text());fixture=json.loads((HERE/'fixture.json').read_text())
 assert len(table)==480 and peer['complete_branch_enrolled'] is True
 assert peer['proof_status']=='ALL_RECORDS_ACTUALLY_SCALAR_CLAUSE_NATIVE_AND_PYTHON_CHECKED'
 ten={c:n for c,e,n in table if e==10}
 assert len(ten)==135 and sum(ten.values())==751950
 assert len(peer['coverage'])==77 and len({r['code'] for r in peer['coverage']})==77
 assert all(ten[r['code']]==r['effective_orders'] for r in peer['coverage'])
 assert sum(r['effective_orders'] for r in peer['coverage'])==432186
 assert prior['all_six_repeated23_classes']==6 and prior['all_six_effective_orders']==32310
 assert [i for i,c in prior['newly_excluded_classes']]==[40,155,243]
 assert current['newly_excluded_classes']==[[i,c] for i,c,e,n in fixture['classes']]
 categories=Counter();excluded=Counter();remaining=[];new=[];old=[];groups={}
 for index,(code,length,orders) in enumerate(table):
  counts=[int(code)>>(2*k)&3 for k in range(55)]
  doubled=[gate for gate,count in zip(PAIRS,counts) if count==2]
  assert sum(counts)==length and max(counts)<=2 and len(doubled)<=1
  if length==10:
   assert not doubled;excluded['ten']+=1;continue
  assert length==11
  if doubled==[(0,1)]:excluded['repeated01']+=1;continue
  if index==13:
   assert code=='349871875148001158693749134458897' and doubled==[(1,2)]
   excluded['class13']+=1;continue
  if doubled==[(2,3)]:old.append(index);excluded['repeated23']+=1;continue
  if doubled==[(1,3)]:
   new.append([index,code,length,orders]);excluded['repeated13']+=1;continue
  categories['eleven_repeated' if doubled else 'eleven_distinct']+=1
  remaining.append([code,length,orders])
  if doubled:groups.setdefault(str(doubled[0]),[]).append(index)
 assert old==[34,40,149,155,237,243]
 assert new==fixture['classes'] and sum(r[3] for r in new)==32310
 assert excluded==dict(ten=135,repeated01=18,class13=1,repeated23=6,repeated13=6)
 assert categories==dict(eleven_distinct=297,eleven_repeated=17)
 assert len(remaining)==314 and sum(r[2] for r in remaining)==2153985
 print(json.dumps(dict(agent='six-sorting-1',role='researcher',status='EXACT_CONDITIONAL_FRONTIER_INCIDENCE_VERIFIED',remaining_classes=len(remaining),counts=dict(categories),effective_orders=sum(r[2] for r in remaining),class_table_sha256=digest(remaining),repeated_groups=groups,trust='Peer8321 and prior8340 proof suites imported; this script checks exact class incidence.')))
if __name__=='__main__':main()
