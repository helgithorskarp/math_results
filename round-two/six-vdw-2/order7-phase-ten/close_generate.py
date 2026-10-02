"""Four exact K9/35 minimum-distance-four/three cases; all color orientations."""
import argparse
import json
from pathlib import Path
import sys
import time

from common import load_encoder, require, sha, endpoint_generator
old = endpoint_generator()
fixed_neighborhood, neg, put = old.fixed_neighborhood, old.neg, old.put


def prefix(inputs, base):
    previous = {0:True}
    rows = set()
    cursor = base
    for i, value in enumerate(inputs,1):
        current = {0:True}
        for k in range(1,min(i,8)+1):
            cursor += 1
            a,b,z = previous.get(k,False),previous[k-1],cursor
            for row in ((neg(a),z),(neg(value),neg(b),z),
                        (a,value,-z),(a,b,-z)):
                put(rows,row)
            current[k] = z
        previous = current
    put(rows,[previous[7]])
    put(rows,[-previous[8]])
    return rows,cursor


def main(work):
    began = time.monotonic()
    require(not work.exists(),'fresh work directory required')
    work.mkdir(parents=True)
    edges = load_encoder().field_edges()
    records = []
    for distance in (4,3):
        for background in (0,1):
            fixed = fixed_neighborhood(distance,background)
            free = [i for i in range(44) if i not in fixed]
            n = len(free)
            index = {i:j for j,i in enumerate(free)}
            colors = list(range(1,45)) + [
                (i+1)*(-1 if fixed[i] else 1) if i in fixed else 45+index[i]
                for i in range(44)]
            phases = [bool(fixed[i]) if i in fixed else 45+n+index[i]
                      for i in range(44)]
            field,color,phase,spacing,xor = (set() for _ in range(5))
            for edge in edges:
                values = [colors[i] for i in edge]
                put(field,values);put(field,[-v for v in values])
            for i in range(88):
                values = [colors[(i+j)%88] for j in range(7)]
                put(color,values);put(color,[-v for v in values])
            for i in range(44):
                values = [phases[(i+j)%44] for j in range(8)]
                put(phase,values);put(phase,[neg(v) for v in values])
                for step in range(1,distance):
                    values = [phases[i],phases[(i+step)%44]]
                    put(spacing,values if background else [neg(v) for v in values])
            for i in free:
                a,b,s = i+1,45+index[i],45+n+index[i]
                xor.update(tuple(sorted(row)) for row in (
                    (a,b,-s),(a,-b,s),(-a,b,s),(-a,-b,-s)))
            # Universal necessary color-eight windows from graph9069.
            for i in range(88):
                values = [colors[(i+19*j)%88] for j in range(8)]
                put(color,values);put(color,[-v for v in values])
            counter,variables = prefix([phases[i]*(-1 if background else 1)
                                       for i in free],44+2*n)
            require(variables == 16+10*n,'wrong eight-level counter dimension')
            rows = sorted(field|color|phase|spacing|xor|counter,
                          key=lambda c:(len(c),c))+[(-1,)]
            stem = f'd-{distance}-b-{background}'
            cnf = work/(stem+'.cnf')
            cnf.write_text(f'p cnf {variables} {len(rows)}\n'+
                ''.join(' '.join(map(str,row))+' 0\n' for row in rows))
            records.append(dict(stem=stem,minimum_distance=distance,background=background,
                phase_K=35 if background else 9,free_phase_indices=free,variables=variables,
                clauses=len(rows),cnf_sha256=sha(cnf),free_minority_count=7,root57_color_cut=True,
                mathematical_exclusion=False))
    result = dict(status='GENERATED_NOT_AUDITED',agent='six-vdw-2',role='researcher',
        records=records,producer_sha256=sha(Path(__file__)),seconds=time.monotonic()-began)
    (work/'models.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    main(parser.parse_args().work.absolute())
