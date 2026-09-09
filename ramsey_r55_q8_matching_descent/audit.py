"""Replay physical edits and independently certify endpoint stationarity."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import time

from verify import costs, finite_difference, matchings, read, toggle


def bit_string(a, pairs):
    return ''.join(str(a[u] >> v & 1) for u, v in pairs)


def audit_one(scratch, r, checker):
    trial = scratch / f'trial-r{r}.txt'
    run = scratch / f'run-r{r}'
    n, k, tail, pairs, a, fixed = read(trial)
    original = a.copy()
    initial = sum(costs(a, k, tail))
    ms = matchings(n, pairs, fixed)
    score = initial
    accepted = []
    with (run / 'trace.tsv').open() as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    for i, row in enumerate(rows):
        sweep, index, before, after, mask = [int(row[x]) for x in ('sweep','matching','before','after','mask')]
        if (sweep, index) != (i // len(ms) + 1, i % len(ms)) or before != score:
            raise ValueError('trace sequence or cost')
        m = ms[index]
        if mask < 0 or mask >= 1 << len(m) or after > before or (after == before and mask):
            raise ValueError('invalid edit')
        if after < before:
            c, linear, b = finite_difference(a, k, tail, pairs, m)
            selected = [j for j in range(len(m)) if mask >> j & 1]
            polynomial = c + sum(linear[j] for j in selected) + sum(b[j][h] for j in selected for h in selected if h < j)
            for j in selected:
                toggle(a, pairs[m[j]])
            actual = sum(costs(a, k, tail))
            if actual != after or polynomial != actual:
                raise ValueError('physical edit or finite difference')
            accepted.append({'sweep':sweep,'matching':index,'mask':mask,'before':before,'after':after})
            score = actual
    final_data = read(run / 'endpoint.txt')
    if final_data[:4] != (n,k,tail,pairs) or final_data[4:] != (a,fixed):
        raise ValueError('endpoint not reached by exact trajectory')
    for (u,v), f in zip(pairs,fixed):
        if f == '1' and (a[u] >> v & 1) != (original[u] >> v & 1):
            raise ValueError('fixed edge changed')
    receipt = json.loads((run / 'EXECUTION_RECEIPT.json').read_text())
    direct = costs(a,k,tail)
    if direct != receipt['independent_literal_endpoint_costs'] or receipt['final'] != score:
        raise ValueError('literal endpoint receipt')
    if score and (len(rows) % len(ms) or any(int(row['mask']) for row in rows[-len(ms):])):
        raise ValueError('no complete final stationary sweep')
    if (receipt['initial'], receipt['accepted_moves'], receipt['exact_kernels']) != (initial,len(accepted),len(rows)):
        raise ValueError('trajectory totals')
    if score == 0:
        return {'r':r,'status':'VERIFIED_ZERO_OBSTRUCTION_TRAJECTORY','costs':direct,'accepted_path':accepted}
    # Coefficients are obtained from independent physical finite differences.
    path = run / 'stationary-polynomials.txt'
    with path.open('x') as f:
        f.write(str(len(ms)) + '\n')
        for m in ms:
            c, linear, b = finite_difference(a,k,tail,pairs,m)
            if c != score:
                raise ValueError('constant')
            f.write(f'{len(m)} {c}\n')
            f.write(' '.join(map(str,linear)) + '\n')
            for row in b:
                f.write(' '.join(map(str,row)) + '\n')
    t = time.monotonic()
    result = subprocess.run([str(checker),str(path)],text=True,capture_output=True)
    (run / 'stationarity-checker.log').write_text(result.stdout + result.stderr)
    if result.returncode != 0:
        raise ValueError(('stationarity counterexample or checker failure', result.stdout, result.stderr))
    checked = [line.split() for line in result.stdout.splitlines()]
    if len(checked) != len(ms) or any(row[0] != 'NONNEGATIVE' or int(row[1]) != i for i,row in enumerate(checked)):
        raise ValueError('incomplete stationarity audit')
    return {'r':r,'status':'VERIFIED_NONZERO_MATCHING_STATIONARY_ENDPOINT',
            'initial':initial,'final':score,'costs':direct,'sweeps':len(rows)//len(ms),
            'accepted_moves':len(accepted),'exact_matching_minimizations':len(rows),
            'matching_sizes':list(map(len,ms)), 'stationary_matchings_checked':len(ms),
            'stationarity_nodes':sum(int(row[2]) for row in checked),
            'stationarity_seconds':time.monotonic()-t,
            'stationary_polynomials_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'endpoint_red_pair_bits':bit_string(a,pairs),'accepted_path':accepted}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('scratch',type=Path)
    p.add_argument('checker',type=Path)
    args = p.parse_args()
    gate = json.loads((args.scratch / 'GATE_RESULT.json').read_text())
    result = {'status':'VERIFIED_FOUR_TRIAL_CONSTRUCTION_BOUNDARY',
              'trials':[audit_one(args.scratch,x['r'],args.checker.resolve()) for x in gate['trials']],
              'task_exclusions':0,'new_solver_calls':0,
              'independent_reviewer_verdict':False}
    (args.scratch / 'AUDIT.json').write_text(json.dumps(result,indent=2) + '\n')
    print(json.dumps({**result,'trials':[{k:v for k,v in x.items() if k not in ('accepted_path','endpoint_red_pair_bits','matching_sizes')} for x in result['trials']]},indent=2))


if __name__ == '__main__':
    main()
