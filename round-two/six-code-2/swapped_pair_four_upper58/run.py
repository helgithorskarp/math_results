"""Bounded reproducible lambda4 carrier checkpoint; not a completion claim."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import resource
import time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import maps4 as M
from paths import INPUTS


def encoded(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',required=True,type=Path)
    parser.add_argument('--fixture',type=int,nargs='*',default=list(range(23)))
    args=parser.parse_args();args.work.mkdir(parents=True,exist_ok=True)
    data=json.loads((INPUTS/'fixtures.json').read_text());started=time.monotonic();summaries=[]
    for fi in args.fixture:
        quads=tuple(tuple(q) for q in data['stars'][fi]);mates=tuple(v for v in range(17) if sum(v in q for q in quads)==4)
        rows=[];records=[]
        for mate in mates:
            begin=time.monotonic();first=M.tail_maps(quads,mate);second,nodes=M.point_maps(quads,mate)
            M.require(first==second,'point/tail maps differ entrywise')
            valid=[];fixed_counts=Counter()
            tails,left=M.common(quads,mate)
            for g in first:
                words=M.anchor(quads,mate,g)
                if words is None:continue
                normalized,transport=M.normalize(words,g,mate)
                fixed=M.check_map(g,tails,left,mate);fixed_counts[fixed]+=1
                rows.append({'mate':mate,'mapping':g,'words':words,'normalized':normalized,'transport':transport,'fixed_common_tails':fixed})
                valid.append((g,words))
            if time.monotonic()-begin>30:raise TimeoutError('INCOMPLETE per-mate30s guard')
            records.append({'mate':mate,'raw_maps':len(first),'point_nodes':nodes,'valid_maps':len(valid),
                'raw_sha256':hashlib.sha256(encoded(first)).hexdigest(),'valid_sha256':hashlib.sha256(encoded(valid)).hexdigest(),
                'valid_fixed_common_tail_histogram':sorted(fixed_counts.items())})
        record={'agent':'six-code-2','role':'researcher','status':'COMPLETE_LABELLED_LAMBDA4_STAR_UNION_CARRIER','fixture':fi,'mates':records,'rows':rows}
        (args.work/f'fixture-{fi:02d}.json').write_bytes(encoded(record))
        summary={'fixture':fi,'eligible_mates':len(mates),'raw_maps':sum(r['raw_maps'] for r in records),
                 'valid_maps':len(rows),'distinct_normalized_anchors':len({tuple(r['normalized']) for r in rows}),
                 'valid_fixed_common_tail_histogram':sorted(Counter(r['fixed_common_tails'] for r in rows).items())}
        summaries.append(summary);print(json.dumps(summary,sort_keys=True),flush=True)
        (args.work/'progress.json').write_bytes(encoded({'status':'PARTIAL_CARRIER_NO_COMPLETION_CLAIM','completed_fixtures':[s['fixture'] for s in summaries]}))
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_REQUESTED_LAMBDA4_CARRIER_ONLY','fixtures':summaries,
            'eligible_mates':sum(s['eligible_mates'] for s in summaries),'raw_maps':sum(s['raw_maps'] for s in summaries),
            'valid_maps':sum(s['valid_maps'] for s in summaries),'seconds':time.monotonic()-started,
            'peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'premise_source_commit':'0d6357edb0dc8bf703d380362830cccf6169e98c',
            'scope':'replication-four mates in requested generic20-star fixtures;2^8*1^2 exchanges saturated centers; no residual bound or global nonexistence claim'}
    (args.work/'summary.json').write_bytes(encoded(result));(args.work/'progress.json').write_bytes(encoded({'status':result['status'],'completed_fixtures':[s['fixture'] for s in summaries]}))
    print(json.dumps({k:v for k,v in result.items() if k!='fixtures'},sort_keys=True),flush=True)


if __name__=='__main__':main()
