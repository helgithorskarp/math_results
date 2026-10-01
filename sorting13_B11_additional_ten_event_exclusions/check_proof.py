"""Independent native DRAT plus Python RUP replay; no solver is imported."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import signal
import subprocess
import time

H = Path(__file__).resolve().parent
P = H.parent / 'sorting13_maximum_preparation'


def main():
    assert __debug__
    parser = argparse.ArgumentParser()
    parser.add_argument('cnf', type=Path)
    parser.add_argument('--drat-trim', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    from audit_data import check_dependencies
    check_dependencies()
    meta = json.loads(args.cnf.with_suffix('.metadata.json').read_text())
    expected = next(r for r in json.loads((H / 'certificate.json').read_text())['records'] if r['code']==meta['record']['code'])
    assert hashlib.sha256(args.cnf.read_bytes()).hexdigest() == expected['cnf_sha256']
    raw = args.cnf.with_suffix('.drat')
    assert hashlib.sha256(raw.read_bytes()).hexdigest() == expected['raw_drat_sha256']
    command = [str(args.drat_trim.resolve()),str(args.cnf),str(raw),
               '-c',str(args.cnf.with_suffix('.core.cnf')),
               '-l',str(args.cnf.with_suffix('.trimmed.drat')),
               '-L',str(args.cnf.with_suffix('.lrat')),'-t','40']
    checked = subprocess.run(command,capture_output=True,text=True,timeout=45)
    assert checked.returncode == 0 and 's VERIFIED' in checked.stdout, checked.stdout[-1000:]
    assert '0 RAT lemmas in core' in checked.stdout
    args.cnf.with_suffix('.native-check.log').write_text(checked.stdout+checked.stderr)
    print(json.dumps(dict(status='NATIVE_DRAT_VERIFIED',checker='drat-trim',proof_RAT_lemmas=0)),flush=True)
    spec = importlib.util.spec_from_file_location('credited_peer_rup', P / 'watched_rup.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    controls = module.self_check()
    n, core = None, []
    corepath = args.cnf.with_suffix('.core.cnf')
    proofpath = args.cnf.with_suffix('.trimmed.drat')
    with corepath.open() as stream:
        for line in stream:
            if line.startswith('c') or not line.strip():
                continue
            word = line.split()
            if word[0] == 'p':
                _, _, v, count = word
                n, count = int(v), int(count)
            else:
                lits = list(map(int, word))
                assert lits[-1] == 0
                core.append(tuple(sorted(set(lits[:-1]))))
    assert n == meta['variables'] and len(core) == count == expected['core_clauses']
    assert hashlib.sha256(corepath.read_bytes()).hexdigest() == expected['core_sha256']
    assert hashlib.sha256(proofpath.read_bytes()).hexdigest() == expected['trimmed_drat_sha256']
    assert hashlib.sha256(args.cnf.read_bytes()).hexdigest() == meta['cnf_sha256']
    needed = set(core)
    with args.cnf.open() as stream:
        for line in stream:
            if line.startswith(('p', 'c')):
                continue
            values = list(map(int, line.split()))
            assert values[-1] == 0
            needed.discard(tuple(sorted(set(values[:-1]))))
    assert not needed
    assert not module.WatchedRUP(n, core).entails_by_rup(())
    def stop_replay(signum, frame):
        raise TimeoutError('Python RUP replay hit40s; no checked proof claim')
    signal.signal(signal.SIGALRM, stop_replay)
    signal.alarm(40)
    try:
        additions, deletions = module.replay(n, core, proofpath)
    finally:
        signal.alarm(0)
    assert additions == expected['RUP_additions']
    result = dict(agent='six-sorting-2', role='researcher', status='PYTHON_RUP_CORE_AND_FULL_MEMBERSHIP_VERIFIED',
                  core_clauses=len(core), proof_additions=additions, proof_deletions=deletions,
                  tiny_truth_controls=controls, premature_empty_rejected=True,
                  core_sha256=hashlib.sha256(corepath.read_bytes()).hexdigest(),
                  proof_sha256=hashlib.sha256(proofpath.read_bytes()).hexdigest(),
                  cnf_sha256=meta['cnf_sha256'], seconds=time.monotonic() - started,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  checker_credit='six-sorting-1/source5ad75ecb80164da04c921f1898cf62334668a027/graph7452, via sorting13_maximum_preparation/watched_rup.py',
                  trust='Algorithmic independence, not external-person review; encoding and mathematical coverage checked separately')
    args.cnf.with_suffix('.proof-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__ == '__main__':
    main()
