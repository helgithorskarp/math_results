from paths import INPUTS, WORK
"""Checkpoint the complete labelled lambda5 two-star involution carrier."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import time
from carrier import anchor, check_code, normalize, point_maps, tail_maps

HERE = Path(__file__).resolve().parent
INPUT = INPUTS/'fixtures.json'
INPUT_SHA256 = 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--fixture', type=int, nargs='*', default=list(range(23)))
    args = parser.parse_args()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
                'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        os.environ[key] = '1'
    if hashlib.sha256(INPUT.read_bytes()).hexdigest() != INPUT_SHA256:
        raise ValueError('changed fixture input')
    data = json.loads(INPUT.read_text())
    args.work.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    summaries = []
    for fi in args.fixture:
        target = args.work/f'fixture-{fi:02d}.json'
        quads = tuple(tuple(q) for q in data['stars'][fi])
        mates = tuple(v for v in range(17) if sum(v in q for q in quads) == 5)
        fs = time.monotonic()
        rows, mate_records = [], []
        for mate in mates:
            ms = time.monotonic()
            first = tail_maps(quads, mate)
            second, nodes = point_maps(quads, mate)
            if first != second:
                raise ValueError('point/tail map discrepancy')
            valid = []
            for g in first:
                words = anchor(quads, mate, g)
                if words is None:
                    continue
                normalized, transport = normalize(words, g, mate)
                row={'mate':mate,'mapping':g,'words':words,'normalized':normalized,'transport':transport}
                rows.append(row)
                valid.append((g, words))
            # Predeclared operational cap; an incomplete case gives no absence.
            if time.monotonic()-ms > 30:
                raise TimeoutError('INCOMPLETE per-mate30s guard')
            mate_records.append({'mate':mate,'raw_maps':len(first),'point_nodes':nodes,
                                 'valid_maps':len(valid),'raw_digest':hashlib.sha256(encoded(first)).hexdigest(),
                                 'valid_digest':hashlib.sha256(encoded(valid)).hexdigest()})
        record={'agent':'six-code-2','role':'researcher','status':'COMPLETE_LABELLED_LAMBDA5_STAR_UNION_CARRIER',
                'fixture':fi,'source_fixture_sha256':INPUT_SHA256,'mates':mate_records,'rows':rows,
                'seconds':time.monotonic()-fs}
        target.write_bytes(encoded(record))
        summary={'fixture':fi,'mates':len(mates),'raw_maps':sum(x['raw_maps'] for x in mate_records),
                 'valid_maps':len(rows),'distinct_normalized_anchors':len({tuple(r['normalized']) for r in rows}),
                 'seconds':record['seconds'],'record_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
        summaries.append(summary)
        print(json.dumps(summary,sort_keys=True),flush=True)
        (args.work/'progress.json').write_bytes(encoded({'status':'PARTIAL_CARRIER_NO_COMPLETION_CLAIM',
                'completed_fixtures':[s['fixture'] for s in summaries],'requested_fixtures':args.fixture}))
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_REQUESTED_CARRIER_ONLY',
            'fixtures':summaries,'seconds':time.monotonic()-started,
            'peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'claim':'exact compatible35-word two-star unions at lambda5; no residual completion or nonexistence theorem'}
    (args.work/'summary.json').write_bytes(encoded(result))
    (args.work/'progress.json').write_bytes(encoded({'status':'COMPLETE_REQUESTED_CARRIER_ONLY','completed_fixtures':args.fixture,'requested_fixtures':args.fixture}))
    print(json.dumps({k:v for k,v in result.items() if k!='fixtures'},sort_keys=True),flush=True)


if __name__ == '__main__':
    main()
