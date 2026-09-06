#!/usr/bin/env python3
"""Exhaust all nine-omission sets on the remaining H517 support.

This producer uses only certificate omission sets.  The separate checker
reconstructs exact geometry and decodes every original colouring.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
FREE_L = {130,189,192,194,211,228,245,254,285,325,332,338,470}


def require(ok, message):
    if not ok: raise ValueError(message)


def read_json(path): return json.loads(path.read_text())


def inputs():
    for name, digest in read_json(HERE/'manifest.json').items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == digest, ('input hash',name))
    prior = read_json(REPO/'hadwiger_nelson_heule517_family_pilot/certificate.json')['rows']
    c133 = read_json(REPO/'hadwiger_nelson_heule517_small_pilot/certificate.json')['rows']
    c134 = read_json(REPO/'hadwiger_nelson_heule517_small134/certificate.json')
    groups = [('prior',prior),('small',[(c133 if k == 'initial' else c134['new_rows'])[i]
                                     for k,i in c134['final_rows']])]
    for name, directory in [('large2','large2_pilot'),('large3','large3'),('large4','large4')]:
        groups.append((name,read_json(REPO/f'hadwiger_nelson_heule517_{directory}/certificate.json')['rows']))
    rows = [dict(source=name,index=i,D=row['D']) for name,group in groups for i,row in enumerate(group)]
    require(len(rows) == 955, 'input row count')
    for row in rows:
        d = row['D']
        require(d and d == sorted(set(d)) and all(type(v) is int and 0 <= v < 517 for v in d), 'omission set')
    minimal = []
    for row in sorted(rows,key=lambda r:(len(r['D']),r['D'])):
        if not any(set(q['D']) <= set(row['D']) for q in minimal): minimal.append(row)
    forced = {r['D'][0] for r in minimal if len(r['D']) == 1}
    free = sorted(set(range(517))-forced)
    cuts = [r for r in minimal if len(r['D']) > 1]
    require(len(minimal) == 555 and len(forced) == 490 and len(free) == 27, 'library normalization')
    require(all(set(r['D']) <= set(free) for r in cuts), 'free cut support')
    require(FREE_L <= set(free), 'free L support')
    return dict(published_rows=955,antichain_rows=555,forced_vertices=sorted(forced),
                free_vertices=free,free_large=sorted(FREE_L),cuts=cuts)


def enumerate_family(data,out):
    start = time.monotonic()
    free = data['free_vertices']; position = {v:i for i,v in enumerate(free)}
    masks = [sum(1 << position[v] for v in r['D']) for r in data['cuts']]
    bits = {v:1 << position[v] for v in free}
    total = residual = 0; histogram = Counter(); first_cover = Counter(); examples = []
    stream = sha256()
    with (out/'frontier.txt').open('wb') as f:
        for omitted in combinations(free,9):
            total += 1; value = sum(bits[v] for v in omitted)
            for i,cut in enumerate(masks):
                if value & cut == cut:
                    first_cover[i] += 1
                    break
            else:
                residual += 1; histogram[sum(v in FREE_L for v in omitted)] += 1
                raw = (','.join(map(str,omitted))+'\n').encode('ascii')
                f.write(raw); stream.update(raw)
                if len(examples) < 3: examples.append(list(omitted))
    require(total == comb(27,9) and total == sum(first_cover.values())+residual, 'complete enumeration')
    return dict(status='LIBRARY_COVER_COMPLETE' if not residual else 'EXACT_LIBRARY_RESIDUAL',
                record_improvement=False,unrestricted_at_most508_family_closed=(residual == 0),
                total_nine_sets=total,covered=sum(first_cover.values()),residual=residual,
                residual_by_large_omissions=dict(sorted(histogram.items())),
                first_cover_counts={str(i):first_cover[i] for i in range(len(masks))},
                frontier_sha256=stream.hexdigest(),frontier_bytes=(out/'frontier.txt').stat().st_size,
                first_residuals=examples,seconds=time.monotonic()-start,
                peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                new_colouring_queries=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args(); args.out.mkdir(parents=True,exist_ok=False)
    data = inputs(); (args.out/'hypergraph.json').write_text(json.dumps(data,indent=2)+'\n')
    result = enumerate_family(data,args.out)
    (args.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
