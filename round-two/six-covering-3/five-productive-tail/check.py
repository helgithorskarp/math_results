"""Independent full physical AP audit; no producer or research-module imports."""
from pathlib import Path
from itertools import combinations
from math import lcm
from hashlib import sha256
import json
import struct
import time


def require(test,message):
    if not test:raise ValueError(message)


started=time.monotonic()
P=[(8,0),(9,0),(10,1),(14,1),(12,10)]
B=sorted(2**i*3**j*5**k*7**ell for i in range(4) for j in range(3)
         for k in range(2) for ell in range(2)
         if 2**i*3**j*5**k*7**ell >= 8 and 2**i*3**j*5**k*7**ell not in (8,9,10,12,14))
require(len(B)==36 and sum(B)==9279 and 21 in B and 16 not in B,'Wrong originalBASE inventory')
unavailable={x for n,a in P for x in range(a,2520,n)}
required=sorted(set(range(2520))-unavailable)
R=sum(1<<x for x in required)
require(len(required)==1398,'Wrong full literalP residual')
actions={n:[sum(1<<x for x in range(a,2520,n))&R for a in range(n)] for n in reversed(B)}
D=sorted(3**i*5**j*7**k for i in range(3) for j in range(2) for k in range(2))
capacities=[]
for a,b,c,d in combinations(D,4):
    for first,second in [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]:
        capacities.extend([315//lcm(*first)+315//lcm(*second)]*2)
require(len(capacities)==2970 and max(capacities)==126,'Independent four-original matching capacity differs')
target=len(required)-126
audits=[]


def audit(fixed,tuples,records,expected):
    remaining=[n for n in B if n not in fixed]
    require(records.stat().st_size==76*len(tuples),'Omitted/extra/truncated rawrecord')
    lo,hi=65536,-1;retained=[];digest=sha256();largest_pruned=-1
    with records.open('rb') as stream:
        for index,phases in enumerate(tuples):
            U=0
            for n,a in reversed(list(zip(fixed,phases))):U |= actions[n][a]
            residual=R^U
            gain=len(required)-residual.bit_count()
            caps=[]
            for n in remaining:
                best=0
                for a in range(n-1,-1,-1):
                    hit=(residual&actions[n][a]).bit_count()
                    if hit>best:best=hit
                caps.append(best)
            K=gain+sum(caps)
            row=[*phases,gain,*caps,K]
            raw=stream.read(76)
            require(list(struct.unpack('<38H',raw))==row,'PhysicalAP field mismatch at record'+str(index))
            digest.update(raw);lo,hi=min(lo,K),max(hi,K)
            if K>=target:retained.append(phases)
            else:largest_pruned=max(largest_pruned,K)
        require(stream.read(1)==b'','Extra rawrecord')
    if expected is not None:
        require(expected['fixed_originals']==fixed and expected['target']==1272
                and expected['records']==len(tuples) and expected['range']==[lo,hi]
                and expected['retained_tuples']==retained and expected['retained']==len(retained)
                and expected['stream_sha256']==digest.hexdigest()
                and expected['all_extension_phases_complete'] is True,'Complete stage metadata/frontier differs')
    audits.append({'fixed_originals':fixed,'records':len(tuples),'range':[lo,hi],
                   'retained_tuples':retained,'retained':len(retained),
                   'largest_pruned_upper':largest_pruned,'all_rows38H_sha256':digest.hexdigest(),
                   'original_marginal_entries':len(tuples)*len(remaining),
                   'phase_intersections':len(tuples)*sum(remaining),
                   'all_records_entrywise_equal':True,'retention_cutoff':target})
    return retained


root_tuples=[list(divmod(j,18)) for j in range(270)]
retained=audit([15,18],root_tuples,Path('scratch/four-tail-global-base-pilot.bin'),None)
root_meta=json.loads(Path('scratch/four-tail-global-base-pilot.json').read_text())
require(root_meta['required_fullP_points']==1398 and root_meta['complete_raw_pairs']==270
        and root_meta['capacity_range']==audits[0]['range']
        and root_meta['stream_sha256']==audits[0]['all_rows38H_sha256'], 'Root metadata differs')
fixed=[15,18]
folder=Path('scratch/full-base-threshold-pilot')
for next_n in (24,36):
    previous=retained
    data=json.loads((folder/('stage'+str(next_n)+'.json')).read_text())
    require(data['previous_tuples']==previous,'Omitted or altered previous complete frontier')
    fixed=fixed+[next_n]
    tuples=[[*previous[j//next_n],j%next_n] for j in range(len(previous)*next_n)]
    retained=audit(fixed,tuples,folder/('stage'+str(next_n)+'.bin'),data)
require(not retained,'Final complete frontier is not closed')
require(all(a['largest_pruned_upper']<=1271 for a in audits),'Cutoff was not preserved at every pruning stage')
result={'agent':'six-covering-3','role':'researcher','literalP':P,
        'required_fullP_points':1398,'fixed_cutoff_every_stage':1272,
        'stages':audits,'all_complete_records':sum(a['records'] for a in audits),
        'original_marginal_entries':sum(a['original_marginal_entries'] for a in audits),
        'phase_intersections':sum(a['phase_intersections'] for a in audits),
        'independent_original_matchings':2970,'four_tail_maximum_BASE_holes':126,
        'uniform_BASE_holes_at_least':127,
        'uniform_five_productive_TAIL_proof_needs_published9762_two_parents':True,
        'same_author_independent_literal_AP_algorithm':True,'external_review':False,
        'ordinary_bridges_unformalized':True,'seconds':time.monotonic()-started}
print(json.dumps(result,indent=2))
