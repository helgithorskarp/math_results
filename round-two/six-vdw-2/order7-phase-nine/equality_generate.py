"""Two fixed-phase equality176 cases; retain all44 color orientations."""
import argparse
import json
from pathlib import Path
import sys
import time
from common import load_encoder,require,sha,endpoint_generator
put = endpoint_generator().put

def main(work):
    began = time.monotonic()
    require(not work.exists(),'fresh work directory required')
    work.mkdir(parents=True)
    gaps = [1]+[5]*7
    positions = [sum(gaps[:j])+j for j in range(8)]
    edges = load_encoder().field_edges()
    records = []
    for background in (0,1):
        phase = [background ^ int(i in positions) for i in range(44)]
        colors = list(range(1,45))+[
            (i+1)*(-1 if phase[i] else 1) for i in range(44)]
        field,color,extra = set(),set(),set()
        for edge in edges:
            values = [colors[i] for i in edge]
            put(field,values);put(field,[-v for v in values])
        for i in range(88):
            values = [colors[(i+j)%88] for j in range(7)]
            put(color,values);put(color,[-v for v in values])
            values = [colors[(i+19*j)%88] for j in range(8)]
            put(extra,values);put(extra,[-v for v in values])
        rows = sorted(field|color|extra,key=lambda c:(len(c),c))+[(-1,)]
        stem = f'e176-b-{background}';cnf=work/(stem+'.cnf')
        cnf.write_text(f'p cnf 44 {len(rows)}\n'+
                       ''.join(' '.join(map(str,row))+' 0\n' for row in rows))
        records.append(dict(stem=stem,background=background,
            phase_K=36 if background else 8,majority_gaps=gaps,
            minority_positions=positions,gap_square_sum=176,variables=44,
            clauses=len(rows),cnf_sha256=sha(cnf),mathematical_exclusion=False))
    result = dict(agent='six-vdw-2',role='researcher',status='GENERATED_NOT_AUDITED',
        records=records,producer_sha256=sha(Path(__file__)),seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    main(p.parse_args().work.absolute())
