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
    check([sum(c in w for w in words) for c in (17,15,16)]==[19,20,20], 'exact center degrees')
    check([sum({a,b}<=w for w in words) for a,b in ((17,15),(17,16),(15,16))]==[5,5,4],
          'center pair multiplicities')
    check(not any(set(CENTERS)<=w for w in words),'covered center triple')
    return words


def candidates_graph(words):
    candidates=[q for q in combinations(range(15),5)
                if all(len(frozenset(q)&w)<=2 for w in words)]
    triple_sets=[{frozenset(t) for t in combinations(q,3)} for q in candidates]
    adjacent=[{j for j,b in enumerate(triple_sets) if i!=j and a.isdisjoint(b)}
              for i,a in enumerate(triple_sets)]
    return candidates,adjacent


def check_tree(adjacent,tree,limit):
    check(type(limit) is int and 0<=limit<=45,'residual capacity domain')
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
    words=decode(core['blocks'],45)
    check(core['core_sha256']==certificate['core_sha256']==sha(sorted(core['blocks'])),'core binding')
    candidates,adjacent=candidates_graph(words)
    check(len(candidates)==certificate['candidate_count'] and sha(candidates)==certificate['candidate_sha256'],
          'literal complete residual universe')
    record=check_tree(adjacent,certificate['tree'],certificate['limit'])
    return {'core_sha256':core['core_sha256'],'candidate_count':len(candidates),
            'limit':certificate['limit'],**record}


def run(work,certificate_path):
    summary=json.loads((work/'summary.json').read_text())
    check(summary['status']=='COMPLETE' and len(summary['cases'])==46,'primary coverage')
    cores=[c for k in range(46) for c in json.loads((work/f'joints-{k}.json').read_text())]
    core_lookup={c['core_sha256']:c for c in cores}
    source=json.loads(certificate_path.read_text())
    check(source['status']=='COMPLETE' and source['format']==1,'capacity status')
    check(source['primary_summary_sha256']==sha(summary),'capacity/primary binding')
    check(source['raw_core_count']==len(cores) and source['distinct_core_count']==len(core_lookup), 'core counts')
    certificates=source['certificates']
    lookup={c['core_sha256']:c for c in certificates}
    check(len(lookup)==len(certificates)==len(core_lookup) and set(lookup)==set(core_lookup), 'capacity coverage')
    records=[check_one(c,lookup[key]) for key,c in core_lookup.items()]
    maximum=max((r['limit'] for r in records),default=0)
    check(source['maximum_additional_bound']==maximum,'declared capacity bound')
    counts=Counter()
    for row in records:counts.update(row['counts'])
    result={'status':'COMPLETE_EXACT_CAPACITY_ONLY','raw_cores':len(cores),'distinct_cores':len(core_lookup),
            'maximum_additional_bound':maximum,'maximum_total_bound':45+maximum,
            'certificate_kinds':dict(counts),'record_sha256':sha(records),
            'certificate_sha256':hashlib.sha256(certificate_path.read_bytes()).hexdigest()}
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--certificate',type=Path,required=True)
    args=ap.parse_args()
    run(args.work,args.certificate)
