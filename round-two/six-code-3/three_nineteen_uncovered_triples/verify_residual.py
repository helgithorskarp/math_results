"""Solver-free literal checker of every capacity tree and the positive witness."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
CENTERS=(15,16,17)


def check(ok,message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def sha(value):
    return hashlib.sha256(encode(value)).hexdigest()


def decode(masks,size):
    check(type(masks) is list and len(masks)==len(set(masks))==size,'literal capacity cardinality')
    check(all(type(b) is int and 0<=b<(1 << 18) for b in masks),'literal mask domain')
    words=[frozenset(i for i in range(18) if b & (1 << i)) for b in masks]
    check(all(len(w)==5 for w in words),'literal word weight')
    triples=[frozenset(t) for w in words for t in combinations(sorted(w),3)]
    check(len(triples)==len(set(triples))==10*size,'literal repeated triple')
    check(all(sum(c in w for w in words)==19 for c in CENTERS),'exact center degrees')
    check(all(sum(a in w and b in w for w in words)==5 for a,b in combinations(CENTERS,2)),
          'center-pair multiplicities')
    check(not any(set(CENTERS)<=w for w in words),'covered center triple')
    for c in CENTERS:
        links=[w-{c} for w in words if c in w]
        saturated=[i for i in range(18) if i!=c and sum(i in w for w in links)==5]
        missing=sum(not any({a,b}<=w for w in links) for a,b in combinations(saturated,2))
        check(missing==1,'m=1 center condition')
    return words


def candidates_graph(words):
    candidates=[q for q in combinations(range(15),5)
                if all(len(frozenset(q)&w)<=2 for w in words)]
    triple_sets=[{frozenset(t) for t in combinations(q,3)} for q in candidates]
    adjacent=[{j for j,b in enumerate(triple_sets) if i!=j and a.isdisjoint(b)}
              for i,a in enumerate(triple_sets)]
    return candidates,adjacent


def check_tree(adjacent,tree,limit):
    check(type(limit) is int and 0<=limit<=21,'residual capacity domain')
    counts=Counter();max_depth=0
    def visit(node,available,need,depth):
        nonlocal max_depth
        check(type(node) is dict and need>0,'negative-proof node domain')
        counts['nodes']+=1;max_depth=max(max_depth,depth)
        check(counts['nodes']<=100000,'INCOMPLETE certificate-size guard')
        kind=node.get('kind')
        if kind=='size':
            check(set(node)=={'kind'} and len(available)<need,'false cardinality leaf')
            counts['size']+=1
        elif kind=='color':
            check(set(node)=={'kind','colors'},'color-leaf shape')
            colors=node['colors']
            check(type(colors) is list and len(colors)==len(available),'coloring coverage')
            check(all(type(c) is int and 0<=c<need-1 for c in colors),'coloring capacity')
            check(all(colors[i]!=colors[j] for i,a in enumerate(available)
                      for j,b in enumerate(available) if b in adjacent[a]),'improper capacity coloring')
            counts['color']+=1
        elif kind=='branch':
            check(set(node)=={'kind','branches'} and type(node['branches']) is list,'branch shape')
            expected=[]
            for i,a in enumerate(available):
                future=[b for b in available[i+1:] if b in adjacent[a]]
                if len(future)>=need-1:
                    expected.append((a,future))
            branches=node['branches']
            check(all(type(row) is list and len(row)==2 and type(row[0]) is int for row in branches),
                  'branch index shape')
            check([row[0] for row in branches]==[a for a,future in expected],
                  'missing/duplicate/extra minimum-vertex branch')
            for (a,future),(index,child) in zip(expected,branches):
                visit(child,future,need-1,depth+1)
            counts['branch']+=1
        else:
            raise ValueError('unknown certificate action')
    visit(tree,list(range(len(adjacent))),limit+1,0)
    return {'counts':dict(counts),'max_depth':max_depth}


def check_one(core,certificate):
    masks=core['blocks']
    words=decode(masks,42)
    check(core['core_sha256']==certificate['core_sha256']==sha(sorted(masks)),'core/certificate binding')
    candidates,adjacent=candidates_graph(words)
    check(len(candidates)==certificate['candidate_count'] and sha(candidates)==certificate['candidate_sha256'],
          'complete literal residual universe')
    check(certificate['limit']==21,'uniform capacity bound')
    record=check_tree(adjacent,certificate['tree'],21)
    return {'core_sha256':core['core_sha256'],'candidate_count':len(candidates),**record}


def witness_record(witness,core):
    check(witness['center_triple']==list(CENTERS),'positive center labels')
    words=decode(witness['blocks'],63)
    check(witness['core_sha256']==core['core_sha256'],'witness core reference')
    check(set(core['blocks'])<=set(witness['blocks']),'witness does not extend its core')
    candidates,_=candidates_graph(decode(core['blocks'],42))
    indices=witness['residual_indices']
    check(type(indices) is list and len(indices)==len(set(indices))==21 and
          all(type(i) is int and 0<=i<len(candidates) for i in indices),'witness residual indices')
    residual=[frozenset(candidates[i]) for i in indices]
    check(set(words)=={frozenset(i for i in range(18) if b & (1 << i)) for b in core['blocks']}|set(residual),
          'literal positive-witness decoder')
    degrees=[sum(i in w for w in words) for i in range(18)]
    return {'words':63,'center_degrees':[19,19,19],'pair_multiplicities':[5,5,5],
            'm':[1,1,1],'degree_census':dict(sorted(Counter(degrees).items())),
            'witness_sha256':sha(witness)}


def run(work,certificate_path=HERE/'residual.json',witness_path=HERE/'witness63.json'):
    cores=[c for k in range(40) for c in json.loads((work/f'joints-{k}.json').read_text())]
    source=json.loads(certificate_path.read_text())
    check(source['status']=='COMPLETE' and source['format']==1 and source['limit']==21,'certificate status')
    certificates=source['certificates']
    check(len(cores)==len(certificates)==1501,'full residual certificate coverage')
    core_lookup={c['core_sha256']:c for c in cores}
    lookup={c['core_sha256']:c for c in certificates}
    check(len(core_lookup)==len(lookup)==1501 and set(core_lookup)==set(lookup),'duplicate or missing core')
    records=[check_one(c,lookup[c['core_sha256']]) for c in cores]
    witness=json.loads(witness_path.read_text())
    check(witness['core_sha256'] in core_lookup,'unknown positive core')
    positive=witness_record(witness,core_lookup[witness['core_sha256']])
    counts=Counter()
    for r in records:counts.update(r['counts'])
    result={'status':'COMPLETE_EXACT','cores':1501,'maximum_additional_bound':21,
            'maximum_total_bound':63,'certificate_kinds':dict(counts),
            'maximum_tree_depth':max(r['max_depth'] for r in records),
            'candidate_count_range':[min(r['candidate_count'] for r in records),max(r['candidate_count'] for r in records)],
            'record_sha256':sha(records),'certificate_sha256':hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
            'witness':positive}
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--certificate',type=Path,default=HERE/'residual.json')
    parser.add_argument('--witness',type=Path,default=HERE/'witness63.json')
    args=parser.parse_args()
    run(args.work,args.certificate,args.witness)
