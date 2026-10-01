"""84 fixed-phase H7 models for K8/36, minimum minority distance5."""
import argparse
import itertools
import json
from pathlib import Path
import sys
import time

from common import load_encoder, require, sha, endpoint_generator
put = endpoint_generator().put


def main(work):
    start = time.monotonic()
    require(not work.exists(), 'fresh work directory required')
    work.mkdir(parents=True)
    rooted = [t for t in itertools.product(range(4), repeat=8) if sum(t) == 4]
    canonical = sorted({min(t[j:]+t[:j] for j in range(8)) for t in rooted})
    require(len(rooted) == 322 and len(canonical) == 42, 'wrong complete gap cover')
    edges = load_encoder().field_edges()
    records = []
    for case, extras in enumerate(canonical, 1):
        gaps = tuple(4+t for t in extras)
        positions = [0]
        for value in gaps[:-1]:
            positions.append(positions[-1]+value+1)
        require(positions[-1]+gaps[-1]+1 == 44, 'wrong phase cycle')
        for background in (0, 1):
            phases = [background ^ int(i in positions) for i in range(44)]
            colors = list(range(1, 45)) + [
                (i+1)*(-1 if phases[i] else 1) for i in range(44)]
            field, color = set(), set()
            for edge in edges:
                values = [colors[i] for i in edge]
                put(field, values)
                put(field, [-v for v in values])
            for i in range(88):
                values = [colors[(i+j) % 88] for j in range(7)]
                put(color, values)
                put(color, [-v for v in values])
            rows = sorted(field | color, key=lambda c: (len(c), c)) + [(-1,)]
            stem = f'case-{case:02d}-b-{background}'
            cnf = work / (stem+'.cnf')
            cnf.write_text(f'p cnf 44 {len(rows)}\n'+
                ''.join(' '.join(map(str, row))+' 0\n' for row in rows))
            records.append(dict(stem=stem, case=case, background=background,
                phase_K=36 if background else 8, minority_positions=positions,
                majority_gaps=gaps, variables=44, clauses=len(rows),
                field_clauses=len(field), color_clauses=len(color),
                cnf_sha256=sha(cnf), mathematical_exclusion=False))
    data = dict(agent='six-vdw-2', role='researcher',
        status='GENERATED_NOT_AUDITED', models=len(records), rooted_profiles=322,
        cyclic_orbits_per_background=42, records=records,
        producer_sha256=sha(Path(__file__)), seconds=time.monotonic()-start)
    (work / 'models.json').write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k: v for k, v in data.items() if k != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
