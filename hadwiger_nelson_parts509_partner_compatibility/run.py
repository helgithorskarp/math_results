#!/usr/bin/env python3
"""One bounded audit of saved colourings, with checked SAT/UNSAT evidence."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from data import build, list_cnf, check_S, composition, require


def save(path, value):
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temp.replace(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--kissat', type=Path, required=True)
    ap.add_argument('--drat-trim', type=Path, required=True)
    args = ap.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    resource.setrlimit(resource.RLIMIT_AS, (4294967296, 4294967296))
    start = time.monotonic()
    data = build()
    save(work / 'preflight.json', data['facts'])
    (work / 'composition.cnf').write_bytes(composition(data))
    result = dict(status='running', preflight=data['facts'], cases=data['cases'], instances={})
    save(work / 'result.json', result)
    for case in data['cases']:
        digest = case['cnf_sha256']
        if digest in result['instances']:
            continue
        masks = case['masks']
        row = dict(masks=masks)
        if 0 in masks:
            row.update(status='EMPTY_LIST_CHECKED', blocked_vertex=374 + masks.index(0))
        else:
            path = work / digest
            path.mkdir()
            cnf = list_cnf(masks, data['S_edges'])
            (path / 'input.cnf').write_bytes(cnf)
            t = time.monotonic()
            r = subprocess.run([str(args.kissat.resolve()), '--time=10', str(path / 'input.cnf'), str(path / 'proof.drat')],
                               capture_output=True, text=True)
            (path / 'solver.log').write_text(r.stdout + r.stderr)
            row['solver'] = dict(exit_code=r.returncode, wall_seconds=time.monotonic() - t)
            if r.returncode == 10:
                literals = {int(v) for line in r.stdout.splitlines() if line.startswith('v ') for v in line.split()[1:] if int(v) > 0}
                colours = ''.join(str(next(c for c in range(4) if 4 * i + c + 1 in literals)) for i in range(135))
                check_S(colours, masks, data['S_edges'])
                row.update(status='SAT_CHECKED', S_colouring=colours)
            elif r.returncode == 20:
                t = time.monotonic()
                check = subprocess.run([str(args.drat_trim.resolve()), str(path / 'input.cnf'), str(path / 'proof.drat')],
                                       capture_output=True, text=True)
                (path / 'checker.log').write_text(check.stdout + check.stderr)
                require(check.returncode == 0 and 's VERIFIED' in check.stdout, ('UNSAT proof rejected', digest))
                row.update(status='UNSAT_DRAT_CHECKED', proof_sha256=sha256((path / 'proof.drat').read_bytes()).hexdigest(),
                           proof_bytes=(path / 'proof.drat').stat().st_size,
                           checker=dict(exit_code=check.returncode, wall_seconds=time.monotonic() - t))
            else:
                require(r.returncode == 0, ('unexpected native exit', r.returncode))
                row.update(status='UNKNOWN')
        result['instances'][digest] = row
        save(work / 'result.json', result)
        print(json.dumps(dict(instance=len(result['instances']), digest=digest, status=row['status'])), flush=True)
    result['status'] = 'BOUNDED COMPATIBILITY AUDIT FINISHED'
    result['wall_seconds'] = time.monotonic() - start
    result['counts'] = {kind: {answer: sum(c['kind'] == kind and result['instances'][c['cnf_sha256']]['status'] == answer
                                         for c in data['cases'])
                              for answer in ['SAT_CHECKED', 'EMPTY_LIST_CHECKED', 'UNSAT_DRAT_CHECKED', 'UNKNOWN']}
                        for kind in ['interface', 'full']}
    save(work / 'result.json', result)
    print(json.dumps(dict(preflight=data['facts'], counts=result['counts'], wall_seconds=result['wall_seconds']), indent=2), flush=True)


if __name__ == '__main__':
    main()
