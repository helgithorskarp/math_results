"""Entrywise performance-port validation on three complete representative cases."""
import argparse
from pathlib import Path
import json
import time

from produce import p


def run(work):
    records=[]
    for case in (0,24,25):
        begun=time.monotonic()
        header=json.loads((work/f'header-{case}.json').read_text())
        queries=0;nodes=0
        with (work/f'carrier-{case}.jsonl').open() as stream:
            for ci,cover in enumerate(header['covers']):
                if time.monotonic()-begun>60:
                    raise RuntimeError('INCOMPLETE Python port-validation case guard')
                line=stream.readline()
                p.require(bool(line),'truncated port-validation carrier')
                item=json.loads(line)
                p.require(item['cover']==ci,'port-validation interval ordering')
                got,n=p.cliques(header['y_adjacent'],sum(1 << i for i in item['y_candidates']),target=11)
                p.require(p.canonical(got)==p.canonical(item['y_eleven']),'Python/native y-clique mismatch')
                queries+=1;nodes+=n
                for z in item['z_cases']:
                    got,n=p.cliques(header['z_adjacent'],sum(1 << i for i in z['z_candidates']),target=11)
                    p.require(p.canonical(got)==p.canonical(z['z_eleven']),'Python/native z-clique mismatch')
                    queries+=1;nodes+=n
            p.require(not stream.readline(),'extra port-validation carrier')
        row={'case':case,'status':'COMPLETE_ENTRYWISE_PYTHON_PORT_VALIDATION',
             'covers':len(header['covers']),'queries':queries,'nodes':nodes,'seconds':time.monotonic()-begun}
        records.append(row)
        print(json.dumps(row),flush=True)
    result={'status':'COMPLETE','cases':records,'covers':sum(r['covers'] for r in records)}
    (work/'python-port-validation.json').write_bytes(p.canonical(result))
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--work',type=Path,required=True)
    args=ap.parse_args()
    run(args.work)
