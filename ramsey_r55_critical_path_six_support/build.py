"""Exact joint outside-layer kernel and a six-footprint obstruction certificate."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

CORE = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),
        (3,4),(3,5),(3,6),(3,7),(4,5),(4,6),(4,8),(5,7),(5,8),(5,9),
        (6,7),(6,8),(6,10),(7,9),(7,10),(8,9),(8,10),(9,10)]
TYPES = [333,359,587,773,1579,1583]


def need(ok, message):
    if not ok:raise ValueError(message)


def kernel(ncore, red_core, types, layer=3):
    """Exactly forbid monochromatic K5s using at most `layer` outside vertices.

    Primary i+1 is the red edge on outside pair i in lexicographic order.
    Fixed K5s produce an empty clause. Repeated footprint types are allowed.
    No normalization, degree assumptions or support-only projection is used.
    """
    need(type(ncore) is int and ncore>=0 and type(layer) is int and 0<=layer<=5,'dimensions')
    need(all(type(t) is int and 0<=t<(1<<ncore) for t in types),'footprint masks')
    red_core=set(map(tuple,red_core))
    need(all(len(e)==2 and 0<=e[0]<e[1]<ncore for e in red_core),'core edges')
    pairs=list(it.combinations(range(len(types)),2));index={e:i+1 for i,e in enumerate(pairs)}
    fixed=red_core|{(u,ncore+i) for i,t in enumerate(types) for u in range(ncore) if t>>u&1}
    clauses={}
    for five in it.combinations(range(ncore+len(types)),5):
        if sum(v>=ncore for v in five)>layer:continue
        known=[e for e in it.combinations(five,2) if e[0]<ncore]
        outside=[(u-ncore,v-ncore) for u,v in it.combinations(five,2) if u>=ncore]
        for color in (False,True):
            if all((e in fixed)==color for e in known):
                clause=tuple(sorted((-1 if color else 1)*index[e] for e in outside))
                clauses.setdefault(clause,{'clause':list(clause),'five':list(five),'red':color})
    return pairs,[clauses[c] for c in sorted(clauses)]


def refute(records):
    clauses=[r['clause'] for r in records];values={};reasons={};trace=[]
    while True:
        changed=False
        for i,row in enumerate(clauses):
            if any(values.get(abs(l))==(l>0) for l in row):continue
            free=[l for l in row if abs(l) not in values]
            if len(free)>1:continue
            if not free:
                used={i};stack=list(map(abs,row))
                while stack:
                    v=stack.pop();r=reasons[v]
                    if r not in used:
                        used.add(r);stack.extend(abs(l) for l in clauses[r] if abs(l)!=v)
                return {'steps':[s for s in trace if s[0] in used],
                        'conflict_clause':i,'used_clauses':sorted(used)}
            lit=free[0];values[abs(lit)]=lit>0;reasons[abs(lit)]=i
            trace.append([i,lit]);changed=True
        need(changed,'no unit refutation')


def complete(types):
    pairs,records=kernel(11,CORE,types,5)
    for value in range(1<<len(pairs)):
        if all(any(bool(value>>(abs(l)-1)&1)==(l>0) for l in r['clause']) for r in records):
            return value
    raise ValueError('no deletion completion')


def build(example):
    _,records=kernel(11,CORE,TYPES,3)
    return {'format':'r55-critical-path-six-support-v1','core_order':11,
            'core_red_edges':list(map(list,CORE)),'types':TYPES,
            'kernel_layer':3,'kernel_variables':15,'kernel_clauses':records,
            'unit_refutation':refute(records),
            'deletion_completions':[{'deleted_type':t,'tail_mask':complete(TYPES[:i]+TYPES[i+1:])}
                                    for i,t in enumerate(TYPES)],
            'presence_cut':{'types':TYPES,'relation':'sum of nonzero-count indicators <= 5'},
            'example_sha256':hashlib.sha256(example.read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--example',type=Path,default=Path(__file__).with_name('EXAMPLE43.json'))
    a=p.parse_args();need(not a.output.exists(),'fresh output')
    result=build(a.example);a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('kernel',len(result['kernel_clauses']),'proof',len(result['unit_refutation']['used_clauses']))
