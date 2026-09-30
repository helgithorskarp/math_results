"""Solver-free language audit, RUP replay and exact full-source membership.

six-sorting-2, researcher. The watched checker is reused from7474, with
six-sorting-1/7452 implementation credit and7306 membership provenance.
No native solver or search driver is imported here.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

from check_language import check as language_check

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'sorting13_maximum_preparation'))
from check_proof import clauses, source_membership
from watched_rup import WatchedRUP, replay, self_check


def source_check():
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    for name, expected in manifest['files'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name
    parent = HERE.parent / 'sorting13_K_minimum_two_unaries'
    dependencies = json.loads((parent / 'source-manifest.json').read_text())
    for name, expected in dependencies['files'].items():
        assert hashlib.sha256((parent / name).read_bytes()).hexdigest() == expected, name


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    p = argparse.ArgumentParser()
    p.add_argument('--full', type=Path)
    args = p.parse_args()
    start = time.monotonic()
    (HERE / 'scratch').mkdir(exist_ok=True)
    source_check()
    certificate = json.loads((HERE / 'certificate.json').read_text())
    corepath, proofpath = HERE / 'core.cnf', HERE / 'proof.rup'
    assert hashlib.sha256(corepath.read_bytes()).hexdigest() == certificate['core_sha256']
    assert hashlib.sha256(proofpath.read_bytes()).hexdigest() == certificate['rup_sha256']
    language = language_check()
    assert language['language_data_sha256'] == certificate['language_data_sha256']
    n, core = clauses(corepath)
    assert n == certificate['cnf']['variables'] and len(core) == certificate['core_clauses']
    assert not WatchedRUP(n, core).entails_by_rup(())
    tiny = self_check()
    print(json.dumps(dict(stage='complete_language_target_and_core_checked',
                          words=36, core_clauses=len(core), tiny_truth_controls=tiny)), flush=True)
    additions, deletions = replay(n, core, proofpath)
    assert additions == certificate['proof_additions'] and deletions == 0
    count = source_membership(core, args.full, certificate['cnf']) if args.full else None
    result = dict(agent='six-sorting-2', role='researcher', status='VERIFIED',
                  claim=certificate['claim'], language=language,
                  core_clauses=len(core), proof_additions=additions,
                  tiny_truth_controls=tiny, premature_empty_rejected=True,
                  full_source_membership_verified=bool(args.full),
                  full_cnf_clauses_checked=count,
                  seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  trust_boundary=certificate['trust_boundary'])
    (HERE / 'scratch' / 'check-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__ == '__main__':
    main()
