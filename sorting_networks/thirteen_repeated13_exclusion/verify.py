"""Independent data/encoding audit and solver-free compact RUP replay."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import signal
import time

from audit_data import audit_data, check_parent
from audit_encoding import Audit, SHAPES, truth_controls
from watched_rup import WatchedRUP, replay, self_check

HERE = Path(__file__).resolve().parent


def bounded(call, *args):
    def stop(signum, frame):
        raise TimeoutError('45-second stage limit: incomplete checking is not an exclusion')
    previous = signal.signal(signal.SIGALRM, stop)
    signal.alarm(45)
    try:
        return call(*args)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


def read_cnf(path):
    clauses, variables, count = [], None, None
    with path.open() as stream:
        for line in stream:
            if line.startswith('c') or not line.strip():
                continue
            if line.startswith('p '):
                assert variables is None
                _, kind, n, m = line.split()
                assert kind == 'cnf'
                variables, count = int(n), int(m)
            else:
                values = list(map(int, line.split()))
                assert values[-1] == 0 and all(0 < abs(v) <= variables for v in values[:-1])
                clauses.append(tuple(values[:-1]))
    assert len(clauses) == count
    return variables, clauses


def proof_check(expected, full_path):
    core_path, proof_path = HERE / expected['core_file'], HERE / expected['proof_file']
    assert hashlib.sha256(core_path.read_bytes()).hexdigest() == expected['core_sha256']
    assert hashlib.sha256(proof_path.read_bytes()).hexdigest() == expected['proof_sha256']
    n, core = read_cnf(core_path)
    assert n == expected['variables'] and len(core) == expected['core_clauses']
    needed = Counter(tuple(sorted(set(clause))) for clause in core)
    available = Counter()
    with full_path.open() as stream:
        for line in stream:
            if line.startswith('p '):
                continue
            values = list(map(int, line.split()))
            assert values[-1] == 0
            available[tuple(sorted(set(values[:-1])))] += 1
    assert all(available[clause] >= count for clause, count in needed.items())
    assert not WatchedRUP(n, core).entails_by_rup(())
    additions, deletions = replay(n, core, proof_path)
    assert additions == expected['proof_additions']
    return dict(status='COMPACT_CORE_MEMBERSHIP_AND_PYTHON_RUP_VERIFIED',
                core_clauses=len(core), RUP_additions=additions,
                deletions_ignored=deletions, premature_empty_rejected=True)


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, default=HERE)
    parser.add_argument('--out', type=Path, default=HERE / 'out')
    args = parser.parse_args()
    start = time.monotonic()
    fixture = json.loads((HERE / 'tail_fixture.json').read_text())
    certificate = json.loads((HERE / 'certificate.json').read_text())
    data = json.loads((args.out / 'data.json').read_text())
    check_parent(fixture, args.parent)
    data_audit = bounded(audit_data, fixture, data, certificate)
    print(json.dumps(data_audit), flush=True)
    tiny_RUP_controls = bounded(self_check)
    gadget_truth_controls = truth_controls()
    cases = []
    for expected in certificate['records']:
        stem = args.out / f"class{expected['parent_index']}"
        metadata = json.loads(stem.with_suffix('.metadata.json').read_text())
        instance = next(r for r in data['instances'] if
                        (r['record']['parent_index'], r['record']['image']) ==
                        (expected['parent_index'], expected['image']))
        assert metadata['record'] == instance['record'] and metadata['caps'] == instance['caps']
        coverage = bounded(lambda: Audit(metadata, stem.with_suffix('.cnf'), expected).run())
        proof = bounded(proof_check, expected, stem.with_suffix('.cnf'))
        case = dict(parent_index=expected['parent_index'], image=expected['image'],
                    coverage=coverage, proof=proof)
        cases.append(case)
        print(json.dumps(case), flush=True)
    assert len(cases) == 2
    common = json.loads((args.parent / 'fixture.json').read_text())
    assert certificate['newly_excluded_classes'] == [[i,c] for i,c,e,n in common['classes']]
    assert certificate['newly_excluded_effective_orders'] == 6 * 5385 == 32310
    assert certificate['all_six_repeated13_classes'] == 6
    assert certificate['all_six_effective_orders'] == 32310
    result = dict(agent='six-sorting-1', role='researcher',
                  status='COMPLETE_REPEATED13_EXCLUSION_INDEPENDENTLY_VERIFIED',
                  cases=cases, boundary_cases=1, data_audit=data_audit,
                  tiny_RUP_controls=tiny_RUP_controls, gadget_truth_controls=gadget_truth_controls,
                  cardinality_shapes=list(SHAPES.values()),
                  exact_cardinality_assignments=sum(r['tests'] for r in SHAPES.values()),
                  seconds=time.monotonic() - start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  trust='Written unformalized pruning/normalization/zero-one bridges and known smaller-size bounds; algorithmic checks are not external-person review')
    (args.out / 'checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('cases', 'cardinality_shapes', 'data_audit')}), flush=True)


if __name__ == '__main__':
    main()
