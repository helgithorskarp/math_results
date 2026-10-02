"""Complete cold source-only T1 replay, one guarded child at a time."""
import argparse
import datetime
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE / 'source'))
from normalization import canonical, mathematical

R = Path('round-two/six-code-3')
S = R / 'scratch'
B = R / 'four_hub_p21_endpoint_cut'

def need(c, m):
    if not c:
        raise ValueError(m)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--operations-state', type=Path)
    args = parser.parse_args()
    work = args.work.resolve()
    need(not work.exists(), 'fresh work directory required; preserve failed prefixes')
    expected = json.loads((SOURCE / 'EXPECTED.json').read_text())
    manifest = json.loads((SOURCE / 'SOURCE_MANIFEST.json').read_text())['files']

    def source_check():
        need(all(sha(SOURCE / name) == digest for name, digest in manifest.items()),
             'frozen source/input changed')

    def operations():
        if args.operations_state is None:
            return
        state = args.operations_state
        for root in [state, state / 'monitor']:
            for name in ['PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json']:
                p = root / name
                if p.exists() and not (name == 'HANDOVER.json' and
                                     json.loads(p.read_text()).get('phase') == 'completed'):
                    raise ValueError('operations barrier; stop without a mathematical absence claim')
        h = json.loads((state / 'monitor/health.json').read_text())
        b = h['credit_budget']
        age = (datetime.datetime.now(datetime.timezone.utc) -
               datetime.datetime.fromisoformat(h['checked_at'].replace('Z', '+00:00'))).total_seconds()
        need(0 <= age <= 180 and b['status'] == 'authorized' and
             Decimal(b['observed_spent_credits']) < Decimal(b['stop_at_observed_spend_credits']),
             'operations stop or stale health; preserve checkpoint')

    source_check()
    operations()
    work.mkdir(parents=True)
    for p in sorted((SOURCE / 'source').glob('*.py')):
        q = work / S / p.name
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)
    for p in sorted((SOURCE / 'baseline').iterdir()):
        q = work / B / p.name
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)
    interpreter = [sys.executable] + (['-O'] if sys.flags.optimize else [])
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[key] = '1'
    stages = []
    begun = time.monotonic()

    def run(name, arguments=(), label=None):
        operations()
        stage = label or name
        started = time.monotonic()
        command = interpreter + [str(S / (name + '.py'))] + list(arguments)
        try:
            result = subprocess.run(command, cwd=work, env=env, capture_output=True,
                                    text=True, timeout=60)
        except subprocess.TimeoutExpired as exc:
            (work / (stage + '.stdout')).write_bytes(exc.stdout or b'')
            (work / (stage + '.stderr')).write_bytes(exc.stderr or b'')
            raise RuntimeError('INCOMPLETE fixed 60-second guard; no mathematical absence: ' + stage) from exc
        (work / (stage + '.stdout')).write_text(result.stdout)
        (work / (stage + '.stderr')).write_text(result.stderr)
        need(result.returncode == 0, 'failed/incomplete stage is not mathematical absence: ' + stage + '\n' + result.stderr)
        stages.append(dict(stage=stage, elapsed_seconds=time.monotonic() - started))
        (work / 'PROGRESS.json').write_text(json.dumps(dict(status='IN_PROGRESS_NO_EXCLUSION_CLAIM',
                                                          stages=stages), sort_keys=True, indent=2) + '\n')
        print(json.dumps(dict(stage=stage, status='PASS')), flush=True)

    for name in ['pass16-first-engine-low-friends', 'pass16-check-low-friends',
                 'pass21-T1-polynomial', 'pass21-T1-produce',
                 'pass21-T1-hub-friend-catalogue', 'pass21-T1-check-friend-catalogue', 'prepare_scope']:
        run(name)
    scope_path = work / S / 'pass21-T1-column-scope.json'
    scope = json.loads(scope_path.read_text())
    need(scope['partitions'] == [[i, min(i + 64, 1787)] for i in range(0, 1787, 64)],
         'all 28 fixed intervals exactly once')
    progress = dict(agent='six-code-3', role='researcher', scope_sha256=sha(scope_path), complete_intervals=[])
    progress_path = work / S / 'pass21-T1-column-progress.json'
    for start, stop in scope['partitions']:
        stem = 'pass21-T1-N-%04d-%04d' % (start, stop)
        author = S / (stem + '.json')
        checker = S / (stem + '-check.json')
        run('pass21-T1-N-produce', ['--output', str(author), '--start', str(start), '--stop', str(stop)], stem + '-author')
        run('pass21-T1-N-check', ['--author', str(author), '--output', str(checker)], stem + '-checker')
        first = json.loads((work / author).read_text())
        second = json.loads((work / checker).read_text())
        need(first['status'] == 'PRIVATE_COMPLETE_JOINT_N_SUPPLIED_INTERVAL' and
             second['status'] == 'PRIVATE_COMPLETE_TWO_ALGORITHM_JOINT_N_INTERVAL' and
             first['checked_interval'] == second['checked_interval'] == [start, stop] and
             len(first['records']) == len(second['records']) == stop - start,
             'complete actual interval coverage')
        need(second['author_result_sha256'] == sha(work / author), 'raw author provenance before normalization')
        progress['complete_intervals'].append(dict(interval=[start, stop], author=str(author), checker=str(checker),
                                                  author_sha256=sha(work / author), checker_sha256=sha(work / checker)))
        progress_path.write_text(json.dumps(progress, sort_keys=True, indent=2) + '\n')
    for name in ['merge_columns', 'prepare_capacity', 'pass21-T1-capacity-produce',
                 'pass21-T1-capacity-check', 'check_damages']:
        run(name)

    # Every volatile raw reference is checked before removing it from the
    # mathematical comparison. Interval hashes were checked in merge_columns.
    live = json.loads((work / S / 'pass21-T1-live-column-cases.json').read_text())
    need(live['scope_sha256'] == sha(scope_path), 'raw final live-scope provenance')
    seal = json.loads((work / S / 'pass21-T1-capacity-source-preparation.json').read_text())
    first = json.loads((work / S / 'pass21-T1-capacity-producer.json').read_text())
    second = json.loads((work / S / 'pass21-T1-capacity-independent.json').read_text())
    need(first['input_live_cases_sha256'] == seal['live_cases_sha256'] ==
         sha(work / S / 'pass21-T1-live-column-cases.json'), 'raw final capacity-input provenance')
    need(second['author_result_sha256'] == sha(work / S / 'pass21-T1-capacity-producer.json'),
         'raw final independent capacity provenance')
    hashes = {}
    whole = hashlib.sha256()
    byte_count = 0
    with (work / 'MATHEMATICAL.jsonl').open('wb') as stream:
        for name in expected['outputs']:
            p = work / S / (name + '.json')
            data = mathematical(name, json.loads(p.read_text()))
            encoded = canonical(data)
            digest = hashlib.sha256(encoded).hexdigest()
            need(digest == expected['mathematical_output_sha256'][name], 'entire mathematical output differs: ' + name)
            hashes[name] = digest
            line = canonical(dict(name=name, mathematical=data)) + b'\n'
            stream.write(line)
            whole.update(line)
            byte_count += len(line)
    need(whole.hexdigest() == expected['whole_mathematical_sha256'] and
         byte_count == expected['whole_mathematical_bytes'], 'whole mathematical stream differs')
    source_check()
    validation = dict(agent='six-code-3', role='researcher', status='COMPLETE_PUBLIC_SOURCE_T1_REPLAY_PASS',
                      mode='optimized' if sys.flags.optimize else 'normal', python=sys.version,
                      complete_mathematical_sha256=whole.hexdigest(), complete_mathematical_bytes=byte_count,
                      whole_outputs_matched=len(hashes), elapsed_seconds=time.monotonic() - begun,
                      peak_RUSAGE_CHILDREN_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                      peak_RUSAGE_SELF_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      native_threads=1, serial_children=True, child_timeout_seconds=60,
                      original_kernel_guards_unchanged=True, stages=stages,
                      source_seal=manifest, raw_provenance_checked_before_normalization=True,
                      actual_semantic_damages_per_mode=11, independent_person_review=False,
                      ordinary_bridges_formalized=False)
    (work / 'VALIDATION.json').write_text(json.dumps(validation, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: v for k, v in validation.items() if k not in ['source_seal', 'stages', 'python']}, sort_keys=True))

if __name__ == '__main__':
    main()
