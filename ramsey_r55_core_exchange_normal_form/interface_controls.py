"""Whole old-family strictness templates and independent destination checks."""
from pathlib import Path
from itertools import combinations
from copy import deepcopy
import json
from catalog import Lookup,obtain,adjacency
from exchange import need,decode,clique,augment
from destination import run
from strict_witness import witness
from verify_destination import verify
HERE=Path(__file__).resolve().parent


def check(data):
    lookup=Lookup(data);lines=obtain(data);sources=json.loads((HERE/'FIXTURES.json').read_text())
    strict=0;local_five_sets=0
    for q in range(7,11):
        n=43-4*q
        index=next(i for i,raw in enumerate(lines[n]) if min(map(sum,adjacency(raw)))<n-1)
        source=witness(data,q,index);a=decode(source);sources.append(source)
        # Literal pair palettes, all block/core five-sets (stronger than required except q9),
        # and all two-edge augmentations. Red maximality was checked in the producer.
        for b,c in combinations(source['red'],2):
            need(all(clique(a,b+c,5,color) is None for color in (0,1)),'old pair domain')
        for B in source['red']:
            need(all(clique(a,B+source['core'],5,color) is None for color in (0,1)),'old local contacts')
            from math import comb
            local_five_sets+=comb(len(B+source['core']),5)
        need(augment(a,source['red'],source['core']) is None,'old selected augmentation')
        # Each non-root matrix row and column has two red entries: all old 3+1+1 events absent.
        for i,j in combinations(range(1,q),2):
            need(all(sum(a[u][v] for v in source['red'][j])==2 for u in source['red'][i]),'non-root row')
            need(all(sum(a[u][v] for u in source['red'][i])==2 for v in source['red'][j]),'non-root column')
        # Root column and equal-key block ordering are explicit in the template.
        for b in range(1,q):
            sig=[sum(a[u][4*b+j]<<u for u in range(4)) for j in range(4)]
            need(sig==sorted(sig,reverse=True),'source root order')
        strict+=1
    checked=0;packets=[]
    for source in sources:
        packet=run(source,lookup);verify(source,packet,data);packets.append(packet);checked+=1
    source,packet=sources[-1],packets[-1]
    corrupt=[]
    x=deepcopy(packet);x['destination']['new_to_old'][0]=x['destination']['new_to_old'][1];corrupt.append(x)
    x=deepcopy(packet);x['destination']['graph']['red_hex']=format(int(x['destination']['graph']['red_hex'],16)^1,'0226x');corrupt.append(x)
    x=deepcopy(packet);x['destination']['task']=x['destination']['task'][:-6]+'999999';corrupt.append(x)
    x=deepcopy(packet);x['packing']['core'].append(x['packing']['red'][0][0]);corrupt.append(x)
    for x in corrupt:
        try:verify(source,x,data)
        except (ValueError,IndexError):pass
        else:raise ValueError('corrupt destination accepted')
    keys=json.loads((HERE/'KEYS.json').read_text())
    schema=sum(k['multiplicity'] for k in keys if min(k['degrees'])<k['n']-1)
    need(schema==547361,'whole strictness schema count')
    return dict(status='STRICTNESS_AND_STANDALONE_DESTINATION_VERIFIED',literal_strictness_controls=strict,
                all_red_tasks_with_proved_strictness_schema=schema, literal_block_core_five_sets=local_five_sets,
                standalone_destination_checks=checked,corrupt_destination_packets_rejected=len(corrupt),
                templates_are_good43=False,original_task_decisions=0)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('out');a=p.parse_args()
    result=check(a.data);Path(a.out).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
