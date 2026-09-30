"""Solver-free scalar audits and monotone RUP/full-source verification.

Author: six-sorting-2, researcher. Reuses7474's published watched checker,
whose implementation is credited to six-sorting-1/7452 and membership
provenance to7306. This is independent of the native solver implementation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

from check_structure import check as structure_check

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'sorting13_maximum_preparation'))
from check_proof import clauses, source_membership
from watched_rup import WatchedRUP, replay, self_check


def source_check():
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    for path, expected in manifest['files'].items():
        assert hashlib.sha256((HERE / path).read_bytes()).hexdigest() == expected, path


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    p = argparse.ArgumentParser()
    p.add_argument('--full', type=Path)
    args = p.parse_args()
    start = time.monotonic()
    source_check()
    certificate = json.loads((HERE / 'certificate.json').read_text())
    corepath, proofpath = HERE / 'core.cnf', HERE / 'proof.rup'
    assert hashlib.sha256(corepath.read_bytes()).hexdigest() == certificate['core_sha256']
    assert hashlib.sha256(proofpath.read_bytes()).hexdigest() == certificate['rup_sha256']
    structure = structure_check()
    n, core = clauses(corepath)
    assert n == certificate['cnf']['variables'] and len(core) == certificate['core_clauses']
    assert not WatchedRUP(n, core).entails_by_rup(())
    tiny = self_check()
    print(json.dumps(dict(stage='scalar_inputs_language_and_core_checked',
                          core_clauses=len(core), tiny_truth_controls=tiny)), flush=True)
    additions, deletions = replay(n, core, proofpath)
    assert additions == certificate['proof_additions'] and deletions == 0
    count = source_membership(core, args.full, certificate['cnf']) if args.full else None
    result = dict(agent='six-sorting-2', role='researcher', status='VERIFIED',
                  claim='Every K18 sorter has exactly two unary minimum events; all six one-unary words excluded',
                  structure=structure, core_clauses=len(core), proof_additions=additions,
                  tiny_truth_controls=tiny, premature_empty_rejected=True,
                  full_source_membership_verified=bool(args.full),
                  full_cnf_clauses_checked=count,
                  seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  trust_boundary=certificate['trust_boundary'])
    (HERE / 'scratch' / 'check-result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
