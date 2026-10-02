#!/usr/bin/env python3
"""Serial, guarded native census; complete streams regenerate in scratch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parent

def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()

def require(value, reason):
    if not value:
        raise ValueError(reason)

def stage(argv, cwd):
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[name] = '1'
    start = time.monotonic()
    p = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, start_new_session=True)
    try:
        out, err = p.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        p.communicate()
        raise RuntimeError('INCOMPLETE: fixed 60-second stage guard; no exclusion')
    require(p.returncode == 0, f'child failure {p.returncode}: {err.decode()}')
    return {'seconds': round(time.monotonic()-start, 6), 'stdout': out.decode(),
            'stderr': err.decode(), 'peak_child_rss_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}

def read_rows(path, length):
    rows = []
    for line in path.read_text().splitlines():
        row = [int(v) for v in line.split()]
        require(len(row) == length, f'wrong record width in {path.name}')
        rows.append(row)
    rows.sort()
    require(len({tuple(r) for r in rows}) == len(rows), f'duplicate record in {path.name}')
    return rows

def summarize(prefix):
    rows = {name: read_rows(Path(str(prefix)+'-'+name+'.txt'), n)
            for name, n in [('x', 20), ('frames', 27), ('joins', 44)]}
    meta = {}
    for line in Path(str(prefix)+'-meta.txt').read_text().splitlines():
        parts = line.split()
        if parts[0] == 'x':
            meta['x_stage_'+parts[1]] = dict(zip(
                ['column_words', 'tagged_column_words', 'fourteen_point_survivors',
                 'sy_row_pairs', 'rank_survivors', 'interfaces'], map(int, parts[2:])))
        else:
            require(len(parts) == 2, 'metadata width')
            meta[parts[0]] = int(parts[1])
    full = {'coordinates': ['u','v','a']+[f'X{i}' for i in range(6)]+
            ['SX0','SX1','SY0','SY1','T0','T1','T2']+[f'Y{i}' for i in range(6)],
            'metadata': meta, 'records': rows}
    record = canonical(full)
    Path(str(prefix)+'-full.json').write_bytes(record)
    summary = {'complete': True, 'algorithm': 'native physical colored-neighbor census',
               'record_bytes': len(record), 'record_sha256': hashlib.sha256(record).hexdigest(),
               'metadata': meta, 'domains': {name: {'count': len(v), 'sha256': hashlib.sha256(canonical(v)).hexdigest()}
                                           for name,v in rows.items()},
               'join_flag_words': sorted({tuple(r[1:6]) for r in rows['joins']}),
               'join_Q_low_words': sorted({tuple(r[33:39]) for r in rows['joins']}),
               'first_join': rows['joins'][0] if rows['joins'] else None}
    return summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--compare', type=Path)
    args = ap.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    binary = out/'census'
    build = stage(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',
                   str(ROOT/'census.cpp'),'-o',str(binary)], ROOT)
    run = stage([str(binary), str(out/'census')], ROOT)
    result = summarize(out/'census')
    (out/'RESULTS.json').write_bytes(canonical(result))
    (out/'RUN.json').write_bytes(canonical({'build': build,'census': run}))
    if args.compare:
        require(canonical(result) == canonical(json.loads(args.compare.read_text())), 'whole summary mismatch')
    print(json.dumps({'summary': result, 'timing': {'build':build,'census':run}}, indent=2))

if __name__ == '__main__':
    main()
