"""Seven complete longest-run cases, with published root3 color cuts."""
import argparse
import json
from pathlib import Path
import time
from common import load_encoder, require, sha


def main(work):
    began = time.monotonic()
    require(not work.exists(), 'fresh external work directory required')
    work.mkdir(parents=True)
    # log_3(57)=19 modulo88; 19^-1=51 modulo88.
    edges = sorted({tuple(sorted(51*x % 88 for x in edge))
                    for edge in load_encoder().field_edges()}, key=lambda e:(len(e),e))
    field = []
    for edge in edges:
        values = tuple(i+1 for i in edge)
        field.extend((values, tuple(-v for v in values)))
    color = []
    for start in range(88):
        values = tuple((start+51*j) % 88+1 for j in range(7))
        color.extend((values, tuple(-v for v in values)))
    records = []
    for length in range(8,15):
        rows = list(field)+list(color)
        for start in range(88):
            values = tuple((start+j) % 88+1 for j in range(length+1))
            rows.extend((values, tuple(-v for v in values)))
        rows.extend((-i,) for i in range(1,length+1))
        rows.extend(((88,),(length+1,)))
        stem = f'run-{length}'
        cnf = work/(stem+'.cnf')
        cnf.write_text(f'p cnf 88 {len(rows)}\n'+
                       ''.join(' '.join(map(str,row))+' 0\n' for row in rows))
        records.append(dict(stem=stem,L=length,variables=88,clauses=len(rows),
                            cnf_sha256=sha(cnf),mathematical_exclusion=False))
    result = dict(agent='six-vdw-2',role='researcher',status='GENERATED_NOT_AUDITED',
                  records=records,producer_sha256=sha(Path(__file__)),
                  seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    main(parser.parse_args().work.absolute())
