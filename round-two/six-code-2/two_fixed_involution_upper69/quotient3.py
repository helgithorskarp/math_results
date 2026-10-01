import maps3
from paths import INPUTS, WORK
"""Positive group-action coverage of every compatible labelled lambda3 map."""
from collections import deque
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
from maps3 import image, require

HERE = Path(__file__).resolve().parent
IDENTITY = tuple(range(18))


def compose(p, q):
    return tuple(p[q[v]] for v in range(18))


def inverse(p):
    result = [0]*18
    for v, w in enumerate(p):
        result[w] = v
    return tuple(result)


def generators(group):
    allowed = set(group)
    require(IDENTITY in allowed, 'missing group identity')
    span, result = {IDENTITY}, []
    while span != allowed:
        result.append(min(allowed-span))
        span, queue = {IDENTITY}, deque([IDENTITY])
        while queue:
            p = queue.popleft()
            for q in result:
                r = compose(p, q)
                require(r in allowed, 'supplied group not closed')
                if r not in span:
                    span.add(r)
                    queue.append(r)
    return tuple(result)


def encoded(v):
    return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--inventory',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    started=time.monotonic()
    fixture_path=INPUTS/'fixtures.json'
    data=json.loads(fixture_path.read_text())
    gd=json.loads((WORK/'swapped-full-groups.json').read_text())
    require(gd['status']=='COMPLETE_ACTUAL_FULL_FIXTURE_GROUPS','full fixture group replay')
    all_roots, all_coverage, summaries=[], [], []
    for fi in range(23):
        source_path=args.inventory/f'fixture-{fi:02d}.json'
        source=json.loads(source_path.read_text())
        require(source['status']=='COMPLETE_LABELLED_LAMBDA3_STAR_UNION_CARRIER' and source['fixture']==fi,
                'incomplete carrier')
        group=tuple(tuple(p)+(17,) for p in gd['groups'][fi])
        star={tuple(sorted(q)) for q in data['stars'][fi]}
        require(all(sorted(p)==list(range(18)) and p[17]==17 and
                    {tuple(sorted(p[v] for v in q)) for q in star}==star for p in group),
                'false fixture automorphism')
        gens=generators(group)
        valid={(r['mate'],tuple(r['mapping'])):r for r in source['rows']}
        require(len(valid)==len(source['rows']),'duplicate valid raw map')
        remaining=set(valid)
        start_root=len(all_roots)
        while remaining:
            root_key=min(remaining)
            root=valid[root_key]
            ri=len(all_roots)
            orbit={root_key:IDENTITY}
            queue=deque([root_key])
            while queue:
                key=queue.popleft()
                mate,g=key
                root_map=orbit[key]
                for p in gens:
                    ip=inverse(p)
                    moved=(p[mate],tuple(p[g[ip[v]]] for v in range(18)))
                    require(moved in valid,'valid carrier not preserved by group')
                    words=tuple(sorted(image(w,p) for w in valid[key]['words']))
                    require(words==tuple(valid[moved]['words']),'literal group action on words')
                    if moved not in orbit:
                        orbit[moved]=compose(p,root_map)
                        queue.append(moved)
            require(set(orbit)<=remaining,'orbits overlap')
            remaining-=set(orbit)
            for key,p in sorted(orbit.items()):
                mate,g=key
                ip=inverse(p)
                require(p[root['mate']]==mate and
                        tuple(p[root['mapping'][ip[v]]] for v in range(18))==g and
                        tuple(sorted(image(w,p) for w in root['words']))==tuple(valid[key]['words']),
                        'bad positive root transport')
                all_coverage.append({'fixture':fi,'mate':mate,'mapping':g,'root':ri,'from_root':p})
            all_roots.append({'fixture':fi,'orbit_size':len(orbit),**root})
        summaries.append({'fixture':fi,'raw_maps':sum(r['raw_maps'] for r in source['mates']),
                          'valid_maps':len(valid),'group_order':len(group),'generators':len(gens),
                          'rooted_cases':len(all_roots)-start_root,
                          'source_record_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest()})
        print(json.dumps(summaries[-1],sort_keys=True),flush=True)
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_POSITIVE_ROOT_COVER_ONLY',
            'roots':all_roots,'coverage':all_coverage,'fixtures':summaries,
            'raw_maps':sum(s['raw_maps'] for s in summaries),'valid_maps':len(all_coverage),
            'rooted_cases':len(all_roots),'seconds':time.monotonic()-started,
            'peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'all lambda3 swapped saturated two-star unions with2^8*1^2, conditional on imported23-fixture cover; residual completions unsearched'}
    args.output.write_bytes(encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('roots','coverage','fixtures')},sort_keys=True))


if __name__=='__main__': main()
