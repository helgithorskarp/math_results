from paths import INPUTS, WORK
"""Exact weighted maxima at each requested rooted two-star union."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import sys
import time
import carrier as C
from quotient import encoded
import weighted

HERE=Path(__file__).resolve().parent
import model as M


def graph(anchor, resources, rows):
    available=tuple(r for r in M.residual(anchor,resources,rows) if r['replications'][0]==r['replications'][1]==0)
    literal=C.literal_residual(anchor)
    C.require(tuple(sorted(tuple(r['words']) for r in available))==literal,'literal residual orbit census')
    used=tuple(sum(1<<j for j in r['resources']) for r in available)
    adjacency=tuple(sum(1<<j for j in range(len(available)) if i!=j and not used[i]&used[j])
                    for i in range(len(available)))
    for i,a in enumerate(available):
        for j,b in enumerate(available):
            if i==j: continue
            actual=all((v&w).bit_count()<=2 for v in a['words'] for w in b['words'])
            C.require(actual==bool(adjacency[i]>>j&1),'literal weighted graph edge')
    # A fixed deterministic ordering makes the proper-color bounds tighter.
    order=tuple(sorted(range(len(available)),key=lambda i:(-available[i]['weight'],-adjacency[i].bit_count(),i)))
    available=tuple(available[i] for i in order)
    adjacency=tuple(sum(1<<j for j,b in enumerate(order) if adjacency[a]>>b&1) for a in order)
    return available,adjacency


def controls():
    cases=0
    for n in range(5):
        edges=tuple(combinations(range(n),2))
        for code in range(1<<len(edges)):
            adj=[0]*n
            for k,(i,j) in enumerate(edges):
                if code>>k&1: adj[i]|=1<<j; adj[j]|=1<<i
            for pattern in range(1<<n):
                weights=tuple(1+(pattern>>i&1) for i in range(n))
                best=max(sum(weights[i] for i in range(n) if s>>i&1) for s in range(1<<n)
                         if all(adj[i]>>j&1 for i,j in edges if s>>i&1 and s>>j&1))
                value,chosen,_,status=weighted.maximum(tuple(adj),weights)
                C.require(value==best and status=='COMPLETE_MAXIMUM' and
                          sum(weights[i] for i in chosen)==value,'small weighted graph discrepancy')
                cases+=1
    try: weighted.maximum((0,),(1,),node_cap=0)
    except weighted.Incomplete: pass
    else: raise ValueError('failed node-guard control')
    try: weighted.maximum((2,0),(1,2))
    except ValueError: pass
    else: raise ValueError('failed asymmetric-input control')
    return cases


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--roots',type=Path,default=(WORK/'swapped-m5-roots.json'))
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--cases',type=int,nargs='+')
    args=parser.parse_args(); args.work.mkdir(parents=True,exist_ok=True)
    started=time.monotonic(); ncontrols=controls()
    data=json.loads(args.roots.read_text()); roots=data['roots']
    resources,rows=M.orbit_carrier()
    baseline=json.loads((WORK/'swapped-classical68.json').read_text())
    indices=args.cases if args.cases is not None else list(range(len(roots)))
    records=[]
    for ri in indices:
        root=roots[ri]; anchor=tuple(root['normalized'])
        available,adjacency=graph(anchor,resources,rows)
        seed=()
        if ri==baseline['root']:
            extension=set(baseline['words'])-set(anchor)
            seed=tuple(i for i,r in enumerate(available) if set(r['words'])<=extension)
            C.require({w for i in seed for w in available[i]['words']}==extension,'baseline seed')
        begin=time.monotonic()
        try:
            value,chosen,nodes,status=weighted.maximum(adjacency,tuple(r['weight'] for r in available),seed,
                                                       target=35)
        except weighted.Incomplete as exc:
            value,chosen,nodes,status=exc.weight,exc.best,exc.nodes,'INCOMPLETE'
        witness=tuple(sorted(anchor+tuple(w for i in chosen for w in available[i]['words'])))
        replications=C.check_code(witness,C.STANDARD_G)
        C.require(replications[:2]==(20,20) and len(witness)==35+value,'weighted witness decoding')
        record={'root':ri,'fixture':root['fixture'],'vertices':len(available),
                'fixed_vertices':sum(r['weight']==1 for r in available),'paired_vertices':sum(r['weight']==2 for r in available),
                'status':status,'residual_weight':value,'words':len(witness),'witness':witness,
                'replications':replications,'nodes':nodes,'seconds':time.monotonic()-begin,
                'graph_sha256':hashlib.sha256(encoded({'vertices':[r['words'] for r in available],
                                                      'adjacency':adjacency})).hexdigest(),
                'absence_claim':status=='COMPLETE_MAXIMUM','scope':'this single rooted35-word anchor only'}
        (args.work/f'case-{ri:03d}.json').write_bytes(encoded(record));records.append(record)
        print(json.dumps({k:v for k,v in record.items() if k not in ('witness','replications')},sort_keys=True),flush=True)
        if status=='FOUND_TARGET':
            break
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_SELECTED_PILOT_ONLY',
            'inventory_roots':len(roots),'requested_cases':indices,'records':records,
            'small_weighted_controls':ncontrols,'seconds':time.monotonic()-started,
            'peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'only selected roots; any INCOMPLETE root gives no absence or optimum claim'}
    (args.work/'summary.json').write_bytes(encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k!='records'},sort_keys=True),flush=True)


if __name__=='__main__':main()
