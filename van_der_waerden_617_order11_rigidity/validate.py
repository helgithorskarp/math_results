"""Independent encoding checks for the bounded native exhaustive proof.

Python 3.11+ standard library. Generated edge dumps live in a temporary
directory, not the source repository. Run after compiling orbit_exact.cpp.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

P = 617


def coset_edges(m):
    # Direct coset multiplication, independently of C++'s successive log map.
    subgroup = {pow(3, m*j, P) for j in range(616//m)}
    assert len(subgroup) == 616//m
    ids = [-1]*P
    ids[0] = m
    for v in range(m):
        for x in {pow(3, v, P)*h % P for h in subgroup}:
            assert ids[x] == -1
            ids[x] = v
    assert all(v >= 0 for v in ids)
    edges = set()
    for a in range(P):
        for d in range(1, P):
            edges.add(sum(1 << v for v in {ids[(a+j*d) % P] for j in range(7)}))
    return sorted(edges)


def scaling_edges(m):
    # A second enumeration uses only spacing-one progressions and coset shifts.
    ids = [m]*P
    for exponent in range(616):
        ids[pow(3, exponent, P)] = exponent % m
    base = {tuple(sorted({ids[(a+j) % P] for j in range(7)})) for a in range(P)}
    return sorted({sum(1 << v for v in {(w+t) % m if w<m else m for w in edge})
                   for edge in base for t in range(m)})


def invoke(checker, *args, expected_exit=0):
    run = subprocess.run([str(checker), *map(str, args)], capture_output=True,
                         text=True, timeout=140, check=False)
    assert run.returncode == expected_exit, (run.returncode,run.stderr,run.stdout)
    assert not run.stderr, run.stderr
    return [json.loads(line) for line in run.stdout.splitlines()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--checker', type=Path, required=True)
    args = parser.parse_args()
    checker = args.checker.resolve(strict=True)
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    assert all(P % divisor for divisor in range(2,25))
    assert len({pow(3,j,P) for j in range(616)}) == 616
    self_test = invoke(checker,'--self-test')[0]
    assert self_test['status'] == 'SELF_TEST_PASSED'
    assert self_test['random_brute_force_comparisons'] == expected['self_test_brute_force_comparisons']
    assert self_test['surviving_masks'] == expected['m8_admissible_masks']
    records = []
    with tempfile.TemporaryDirectory(prefix='vdw617-order11-') as temp:
        for record in expected['cases']:
            m = record['m']
            dump = Path(temp)/f'edges-{m}.txt'
            run = invoke(checker,'--m',m,'--nodes',1000000,'--seconds',120,'--dump',dump)
            summary = run[-1]
            assert summary['status'] == 'RIGIDITY_CERTIFIED'
            assert summary['first'] == 1 and summary['last'] == m-1
            assert all(case['status']=='UNSAT' for case in run[1:-1])
            assert [[case['first_deviation'],case['nodes']] for case in run[1:-1]] == record['first_deviation_nodes']
            for field in ('nodes','conflicts','propagations'):
                assert summary[field] == record[field]
            native = [int(line) for line in dump.read_text().splitlines()]
            direct = coset_edges(m)
            reduced = scaling_edges(m)
            assert native == direct == reduced  # Entry-level equality, not counts.
            digest = hashlib.sha256('\n'.join(map(str,direct)).encode()).hexdigest()
            assert digest == record['direct_edge_masks_sha256']
            nz = [edge for edge in direct if not edge & (1<<m)]
            assert len(direct) == run[0]['full_edges'] == record['full_edges']
            assert len(nz) == run[0]['nonzero_edges'] == record['nonzero_edges']
            alternating = sum(1 << v for v in range(m) if v % 2)
            assert all(edge & alternating and edge & ~alternating for edge in nz)
            records.append({'m':m,'entire_edge_sets_equal':True,'nodes':summary['nodes'],
                            'nonzero_edges':len(nz),'edge_masks_sha256':digest})
            print(json.dumps({'verified_case':records[-1]}),flush=True)
    # Fail-closed controls: an unfinished computation and a partial case range
    # must never receive the complete classification status.
    incomplete = invoke(checker,'--m',56,'--nodes',1,'--seconds',120,expected_exit=2)
    assert incomplete[-1]['status'] == 'INCOMPLETE_NODE_BUDGET'
    timed = invoke(checker,'--m',56,'--nodes',1000000,'--seconds','1e-12',expected_exit=2)
    assert timed[-1]['status'] == 'INCOMPLETE_TIME_BUDGET'
    partial = invoke(checker,'--m',56,'--first',54,'--last',55)
    assert partial[-1]['status'] == 'CASE_RANGE_CERTIFIED'
    # The finite-group bridge: all indices for subgroup order >=11 refine into
    # one of the two fully certified indices. Odd original periods cannot QR.
    indices = [m for m in range(1,57) if 616 % m == 0]
    assert indices == [1,2,4,7,8,11,14,22,28,44,56]
    assert all(any(M % m == 0 for M in (44,56)) for m in indices)
    print(json.dumps({'verified':True,'multiplicative_subgroup_order_threshold':11,
                      'non_quadratic_stabilizer_order_at_most':8,
                      'covered_indices':indices,'case_records':records,
                      'native_small_brute_force_comparisons':1000,'fail_closed_controls':3},sort_keys=True))


if __name__ == '__main__':
    main()
