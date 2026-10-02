"""Exact threshold-preserving BASE record extension; check separately."""
from pathlib import Path
from hashlib import sha256
import json
import struct
import time

start = time.monotonic()
P = [(8,0),(9,0),(10,1),(14,1),(12,10)]
B = [n for n in range(8,2521) if 2520 % n == 0 and n not in (8,9,10,12,14)]
points = [x for x in range(2520) if all(x % n != a for n,a in P)]
target = len(points)-126
actions = {n:[0]*n for n in B}
for i,x in enumerate(points):
    for n in B:actions[n][x%n] |= 1<<i
roots = [list(struct.unpack('<38H',Path('scratch/four-tail-global-base-pilot.bin').read_bytes()[76*i:76*(i+1)]))
         for i in range(270)]
retained = [row[:2] for row in roots if row[-1] >= target]
results = [{'fixed_originals':[15,18],'records':270,'retained':len(retained),'target':target}]
fixed = [15,18]
out = Path('scratch/full-base-threshold-pilot');out.mkdir(exist_ok=True)
for next_n in (24,36,20):
    previous = retained
    new_fixed = fixed+[next_n]
    remaining = [n for n in B if n not in new_fixed]
    retained = []
    low,high=65536,-1
    count=0;digest=sha256()
    with (out/('stage'+str(next_n)+'.bin')).open('wb') as stream:
        for root in previous:
            before=0
            for n,a in zip(fixed,root):before |= actions[n][a]
            for a in range(next_n):
                U=before|actions[next_n][a]
                caps=[max((v&~U).bit_count() for v in actions[n]) for n in remaining]
                K=U.bit_count()+sum(caps)
                phases=root+[a]
                row=[*phases,U.bit_count(),*caps,K]
                raw=struct.pack('<38H',*row);stream.write(raw);digest.update(raw);count+=1
                low,high=min(low,K),max(high,K)
                if K>=target:
                    retained.append(phases)
                    if len(retained)>300:raise RuntimeError('Frontier300 cap: incomplete, NO exclusion')
    result={'fixed_originals':new_fixed,'previous_tuples':previous,'records':count,'target':target,
            'range':[low,high],'retained':len(retained),'retained_tuples':retained,
            'stream_sha256':digest.hexdigest(),'all_extension_phases_complete':count==len(previous)*next_n}
    (out/('stage'+str(next_n)+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    results.append(result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('previous_tuples','retained_tuples')}),flush=True)
    fixed=new_fixed
    if not retained:break
result={'agent':'six-covering-3','role':'researcher','required':len(points),'retention_cutoff_ALL_stages':target,
        'claim_status':'PRODUCER_ONLY_SEPARATE_CHECKER_REQUIRED','stages':results,
        'complete_producer_frontier_closed':not retained,'universal_holes127_claimed':False,
        'uniform_five_productive_TAIL_claimed':False,'seconds':time.monotonic()-start}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='stages'},indent=2))
