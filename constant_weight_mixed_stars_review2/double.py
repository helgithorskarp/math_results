"""Independent double-row coupling by all240 degree markings and pair covers.

This replaces the author's 58,786,560 template maps by a complete degree
carrier, and directly compares the resulting148 actual stars to the pinned
published canonical stream. No second-star template transport is assumed.
"""
from pathlib import Path
from itertools import permutations,combinations
import argparse,json,time,resource
from exact import insist,encoded
from first import digest,run_native,transport
import carrier


def secondary_shape(star):
    ds={z:5-sum(w>>z&1 for w in star) for z in range(1,18)}
    q=next(z for z in range(1,17) if ds[z]==2)
    b=next(z for z in range(1,17) if ds[z]==1)
    high=(17,q,b)
    uncovered={e for e in combinations(sorted(high),2) if not any(all(w>>z&1 for z in e) for w in star)}
    insist(len(uncovered)==2,'classified second-star high path')
    center=next(z for z in high if sum(z in e for e in uncovered)==2)
    return 0 if center==17 else 1 if center==q else 2


def run(args):
    started=time.monotonic()
    first=json.loads((args.work/'first.json').read_text())
    expected=json.loads((args.classification/'expected.json').read_text())
    results=[];stats=[];states=0;maximum=0
    for shape in range(3):
        template=tuple(first['templates'][shape]);base=carrier.baseline(template)
        candidates=tuple(sorted(w>>1 for w in base['candidates']))
        stars=[set(),set(),set()];fibers=0;degree_states=0
        for ci,(q,b) in enumerate(permutations(carrier.D,2)):
            domain,metrics=carrier.double_graphs(base,q,b)
            degree_states+=metrics['states'];fibers+=len(domain)
            for lo in range(0,len(domain),512):
                batch=domain[lo:lo+512]
                exclusions=[frozenset((a-1,b-1) for a,b in set(g)|base['common_pairs']) for g in batch]
                out=run_native(args.work,16,candidates,exclusions,'double-active')
                for leave,row in zip(batch,out):
                    states+=row['states'];maximum=max(maximum,row['states'])
                    for cov in row['covers']:
                        words=tuple(w<<1 for w in cov)
                        star=carrier.second(template,base,words,leave,[1,2,2])
                        insist(5-sum(w>>q&1 for w in star)==2 and 5-sum(w>>b&1 for w in star)==1,'ordered degree marking')
                        index=secondary_shape(star)
                        insist(star not in stars[index],'double-star repeated across unique degree models')
                        stars[index].add(star)
            if (ci+1)%60==0:print(json.dumps({'double_first_shape':shape,'ordered_markings_complete':ci+1,'fibers':fibers}),flush=True)
        insist(fibers==28665,'double-row full degree-carrier count')
        for secondary in range(3):results.append({'first':shape,'second':secondary,'stars':sorted(stars[secondary])})
        stats.append({'first':shape,'ordered_degree_markings':240,'fibers':fibers,'degree_states':degree_states})
    insist([len(r['stars']) for r in results]==expected['joint_branch_counts'],'all actual double-row stars differ')
    insist(digest([r['stars'] for r in results])==expected['joint_star_stream_sha256'],'complete double-row star stream differs')
    orbits=[];offset=0
    for branch in results:
        shape,second=branch['first'],branch['second']
        group=tuple(map(tuple,first['groups'][shape]));pending=set(branch['stars']);position={s:i for i,s in enumerate(branch['stars'])}
        while pending:
            rep=min(pending);orbit={transport(rep,p) for p in group}
            insist(orbit<=pending,'double joint-star orbit cover');pending-=orbit
            orbits.append({'first':shape,'second':second,'star':rep,'orbit_size':len(orbit),'capacity_index':offset+position[rep]})
        offset+=len(branch['stars'])
    insist(len(orbits)==31 and digest(orbits)==expected['joint_orbit_stream_sha256'],'complete double joint-star orbit stream differs')
    result={'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'COMPLETE independent degree-carrier double-row coupling','stats':stats,'branches':results,'orbits':orbits,'states':states,'max_case_states':maximum,'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (args.work/'double.json').write_bytes(encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('branches','orbits')},sort_keys=True),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--classification',type=Path,required=True)
    run(p.parse_args())
