"""Generate four small pruning witnesses and all three maximum kernels."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def run(values, network):
    values = list(values)
    for a, b in network:
        values[a], values[b] = min(values[a],values[b]), max(values[a],values[b])
    return values


def packed_image(n, network):
    return sorted({sum(bit << i for i,bit in enumerate(run([(x >> j)&1 for j in range(n)],network)))
                   for x in range(1 << n)})


def digest(values):
    return hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()


def prune(n, network, inputs):
    ports=[]
    for i in range(n):
        ports.append(None if i in inputs else sum(j not in inputs for j in range(i)))
    retained=[];deleted=0
    for a,b in network:
        if ports[a] is not None and ports[b] is not None:
            retained.append([ports[a],ports[b]])
        else:
            deleted += 1
            if ports[a] is None:
                ports[a],ports[b] = ports[b],None
    return {'inputs':list(inputs),'output_holes':[i for i,p in enumerate(ports) if p is None],
            'deleted_gates':deleted,'retained_network':retained,
            'output_order':[p for p in ports if p is not None]}


def build(fixture):
    n=fixture['channels'];prefix=fixture['incumbent'][:fixture['prefix_length']]
    full_image=packed_image(n,prefix)
    assert all(x==0 or x & (1 << (n-1)) for x in full_image)
    residual=sorted({x & ((1 << (n-1))-1) for x in full_image})
    candidates=[i for i in range(n-1) if 1 << i in residual]
    witnesses=[]
    for i in candidates:
        options=[prune(n,prefix,A) for A in itertools.combinations(range(n),2)]
        options=[w for w in options if w['output_holes']==[i,n-1]]
        d=max(w['deleted_gates'] for w in options)
        w=next(w for w in options if w['deleted_gates']==d)
        source_image=[]
        for x in range(1 << (n-2)):
            out=run([(x >> j)&1 for j in range(n-2)],w['retained_network'])
            source_image.append(sum(out[p] << j for j,p in enumerate(w['output_order'])))
        source_image=sorted(set(source_image))
        target=sorted({(x & ((1 << i)-1)) | ((x >> (i+1)) << i)
                       for x in residual if x & (1 << i)})
        assert set(source_image) <= set(target)
        w['source_image_count']=len(source_image)
        w['source_image_sha256']=digest(source_image)
        w['target_image_count']=len(target)
        w['target_image_sha256']=digest(target)
        witnesses.append(w)
    kernels=[]
    smallest=candidates[0]
    for partner in candidates[1:]:
        pair=[smallest,partner];other=[i for i in candidates if i not in pair]
        first=sorted([pair,other])
        root=sorted([max(pair),max(other)])
        kernels.append({'child_gates':first,'root_gate':root})
    return {'channels':n,'prefix_length':len(prefix),'residual_channels':n-1,
            'residual_count':len(residual),'residual_sha256':digest(residual),
            'maximum_candidates':candidates,'pruning_witnesses':witnesses,
            'maximum_kernels':kernels}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--check',action='store_true')
    ap.add_argument('--export-channel',type=int,choices=(6,9,10,11))
    args=ap.parse_args()
    base=Path(__file__).resolve().parent
    result=build(json.loads((base/'fixture.json').read_text()))
    if args.export_channel is not None:
        fixture=json.loads((base/'fixture.json').read_text())
        residual=sorted({x & 4095 for x in packed_image(13,fixture['incumbent'][:21])})
        i=args.export_channel
        target=sorted({(x & ((1 << i)-1)) | ((x >> (i+1)) << i)
                       for x in residual if x & (1 << i)})
        print(json.dumps({'residual_wires':11,'residual_states':target,
                          'pruned_parent_channel':i,'known_size_interval':[21,22],
                          'exclusion_target_comparators':21},sort_keys=True))
        raise SystemExit(0)
    if args.check:
        assert result==json.loads((base/'certificate.json').read_text()),'certificate mismatch'
    else:
        (base/'certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'maximum_candidates':result['maximum_candidates'],
                      'residual_count':result['residual_count'],
                      'deleted_gates':[w['deleted_gates'] for w in result['pruning_witnesses']],
                      'maximum_kernels':len(result['maximum_kernels'])},sort_keys=True))
