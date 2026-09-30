"""Solver-free scalar/rank/port and RUP/full-source certificate checking.

The published7474 scalar/port and watched RUP algorithms are reused with
explicit credit. Watched implementation originates with six-sorting-1,
source5ad75ecb/7452; its occurrence-index provenance reaches7306.
No native solver is imported by this checker.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'sorting13_maximum_preparation'
sys.path.insert(0, str(PRIOR))
from check_proof import clauses, source_membership
from watched_rup import WatchedRUP, replay, self_check


def marker_audit():
    spec = importlib.util.spec_from_file_location('scalar_middle_ports', PRIOR / 'check_structure.py')
    scalar = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scalar)
    f = json.loads((PRIOR / 'fixture.json').read_text())
    extra = json.loads((HERE / 'additional_witnesses.json').read_text())
    assert len(extra) == 92 and len({(r['x'], r['y']) for r in extra}) == 92
    assert all(r['cap'] <= 8 and r['x'] in f['states'] and r['y'] in f['states'] for r in extra)
    old = {(r['x'], r['y']) for r in f['critical_single_bounds'] +
           f['selected_mixed_bounds'] + f['designated_bounds']}
    assert len(old) == 53 and not old & {(r['x'], r['y']) for r in extra}
    f.update(critical_single_bounds=[], selected_mixed_bounds=extra, designated_bounds=[])
    result = scalar.witnesses(f)
    assert result == dict(witnesses=92, assignments=10936, distinct_rank_controls=184)
    return result


def main():
    if not __debug__:
        raise RuntimeError('Run without Python optimization')
    p = argparse.ArgumentParser()
    p.add_argument('--full', type=Path)
    a = p.parse_args()
    start = time.monotonic()
    cert = json.loads((HERE / 'certificate.json').read_text())
    corepath, proofpath = HERE / 'core.cnf', HERE / 'proof.rup'
    assert hashlib.sha256(corepath.read_bytes()).hexdigest() == cert['core_sha256']
    assert hashlib.sha256(proofpath.read_bytes()).hexdigest() == cert['rup_sha256']
    assert hashlib.sha256((HERE / 'additional_witnesses.json').read_bytes()).hexdigest() == cert['additional_witnesses_sha256']
    audit = marker_audit()
    n, core = clauses(corepath)
    assert n == cert['cnf']['variables'] and len(core) == cert['core_clauses']
    assert not WatchedRUP(n, core).entails_by_rup(())
    tiny = self_check()
    additions, deletions = replay(n, core, proofpath)
    assert additions == cert['proof_additions'] and deletions == 0
    full = source_membership(core, a.full, cert['cnf']) if a.full else None
    print(json.dumps(dict(agent='six-sorting-2', role='researcher', status='VERIFIED',
                         claim='No16-comparator L sorter at any depth; s(L)=17 or18',
                         additional_marker_audit=audit, core_clauses=len(core),
                         proof_additions=additions, tiny_truth_controls=tiny,
                         full_source_membership_verified=bool(a.full),
                         full_cnf_clauses_checked=full, premature_empty_rejected=True,
                         seconds=time.monotonic()-start,
                         peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                         trust_boundary='Published7474 structural necessity and source fixture; imported small-size bounds, pruning/commutation and sequential encoder correspondence')))


if __name__ == '__main__':
    main()
