"""Full cold T0 source replay: one guarded exact child at a time."""
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
                if p.exists() and not (name == 'HANDOVER.json' and json.loads(p.read_text()).get('phase') == 'completed'):
                    raise ValueError('active operations barrier; preserve prefix without absence claim')
        health = json.loads((state / 'monitor/health.json').read_text())
        budget = health['credit_budget']
        age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(
            health['checked_at'].replace('Z', '+00:00'))).total_seconds()
        need(0 <= age <= 180 and budget['status'] == 'authorized' and
             Decimal(budget['observed_spent_credits']) < Decimal(budget['stop_at_observed_spend_credits']),
             'operations stop or stale health')

    source_check()
    operations()
    work.mkdir(parents=True)
    for p in sorted((SOURCE / 'source').glob('*.py')):
        q = work / S / p.name
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, q)
    for p in sorted((SOURCE / 'baseline').iterdir()):
        q = work / B / p.name
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, q)
    shutil.copyfile(SOURCE / 'CERTIFICATE.json', work / S / 'CERTIFICATE.json')
    interpreter = [sys.executable] + (['-O'] if sys.flags.optimize else [])
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[name] = '1'
    if args.operations_state is not None:
        env['MATH_RESEARCH_OPERATIONS_STATE'] = str(args.operations_state.resolve())
    stages = []
    begun = time.monotonic()
    status = dict(agent='six-code-3', role='researcher', status='RUNNING_NO_EXCLUSION_CLAIM', stages=stages)

    def run(name, arguments=(), label=None):
        operations()
        stage = label or name
        started = time.monotonic()
        command = interpreter + [str(S / (name + '.py'))] + list(arguments)
        try:
            result = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired as exc:
            (work / (stage + '.stdout')).write_bytes(exc.stdout or b'')
            (work / (stage + '.stderr')).write_bytes(exc.stderr or b'')
            raise RuntimeError('INCOMPLETE fixed60s child guard; no absence: ' + stage) from exc
        (work / (stage + '.stdout')).write_text(result.stdout)
        (work / (stage + '.stderr')).write_text(result.stderr)
        need(result.returncode == 0, 'failed/incomplete stage is no mathematical absence: ' + stage + '\n' + result.stderr)
        stages.append(dict(stage=stage, elapsed_seconds=time.monotonic() - started))
        (work / 'PROGRESS.json').write_text(json.dumps(status, sort_keys=True, indent=2) + '\n')
        if not stage.startswith('pass23-T0-N-') or len(stages) % 32 == 0:
            print(json.dumps(dict(stage=stage, completed_stages=len(stages), status='PASS')), flush=True)

    try:
        for name in ['pass16-first-engine-low-friends', 'pass16-check-low-friends',
                     'pass23-T0-polynomial', 'pass23-T0-produce',
                     'pass23-T0-hub-friend-catalogue', 'pass23-T0-check-friend-catalogue',
                     'pass23-T0-prepare-scope']:
            run(name)
        scope_path = work / S / 'pass23-T0-column-scope.json'
        scope = json.loads(scope_path.read_text())
        need(scope['partitions'] == [[i, min(i + 64, 11077)] for i in range(0, 11077, 64)],
             'all174 fixed intervals exactly once')
        progress = dict(agent='six-code-3', role='researcher', scope_sha256=sha(scope_path), complete_intervals=[])
        progress_path = work / S / 'pass23-T0-column-progress.json'
        for start, stop in scope['partitions']:
            stem = 'pass23-T0-N-%04d-%04d' % (start, stop)
            author = S / (stem + '.json')
            checker = S / (stem + '-check.json')
            run('pass23-T0-N-produce', ['--output', str(author), '--start', str(start), '--stop', str(stop)], stem + '-author')
            run('pass23-T0-N-check', ['--author', str(author), '--output', str(checker)], stem + '-checker')
            first = json.loads((work / author).read_text())
            second = json.loads((work / checker).read_text())
            need(first['status'] == 'PRIVATE_COMPLETE_JOINT_N_SUPPLIED_INTERVAL' and
                 second['status'] == 'PRIVATE_COMPLETE_TWO_ALGORITHM_JOINT_N_INTERVAL' and
                 first['checked_interval'] == second['checked_interval'] == [start, stop] and
                 len(first['records']) == len(second['records']) == stop - start,
                 'complete actual interval coverage')
            need(second['author_result_sha256'] == sha(work / author), 'raw independent interval provenance')
            progress['complete_intervals'].append(dict(interval=[start, stop], author=str(author), checker=str(checker),
                                                      author_sha256=sha(work / author), checker_sha256=sha(work / checker)))
            progress_path.write_text(json.dumps(progress, sort_keys=True, indent=2) + '\n')
        run('merge_columns')
        run('pass23-T0-capacity-produce')
        run('pass23-T0-capacity-check')
        run('pass23-T0-row-projections-v2', ['--output', str(S / 'pass23-T0-row-base.json')])
        run('pass23-T0-check-row-projections', ['--author', str(S / 'pass23-T0-row-base.json'),
                                              '--output', str(S / 'pass23-T0-row-base-independent.json')])
        run('check_certificate')
        run('check_damages')

        # Check every volatile raw execution link BEFORE its documented removal.
        livepath = work / S / 'pass23-T0-live-column-cases.json'
        coverage = json.loads((work / S / 'pass23-T0-column-coverage.json').read_text())
        live = json.loads(livepath.read_text())
        need(live['scope_sha256'] == sha(scope_path) and coverage['live_cases_sha256'] == sha(livepath),
             'raw final scope/live provenance')
        need(live['catalogue_sha256'] == sha(work / S / 'pass23-T0-hub-friend-catalogue.json'),
             'raw catalogue provenance')
        capa = work / S / 'pass23-T0-capacity-producer.json'
        capb = work / S / 'pass23-T0-capacity-independent.json'
        first = json.loads(capa.read_text())
        second = json.loads(capb.read_text())
        need(first['input_live_cases_sha256'] == second['input_live_cases_sha256'] == sha(livepath),
             'raw final capacity/live provenance')
        need(second['author_result_sha256'] == sha(capa), 'raw independent capacity provenance')
        rowa = work / S / 'pass23-T0-row-base.json'
        rowb = work / S / 'pass23-T0-row-base-independent.json'
        first = json.loads(rowa.read_text())
        second = json.loads(rowb.read_text())
        need(first['input_live_sha256'] == sha(livepath) and first['input_capacity_sha256'] == sha(capa),
             'raw same-row inputs')
        need(first['catalogue_sha256'] == sha(work / S / 'pass23-T0-hub-friend-catalogue.json') and
             second['author_sha256'] == sha(rowa), 'raw independent row provenance')
        need(coverage['all174_intervals_exactly_once'] and
             coverage['all66462_actual_carrier_records_independently_compared'], 'complete whole column image')

        hashes = {}
        whole = hashlib.sha256()
        byte_count = 0
        with (work / 'MATHEMATICAL.jsonl').open('wb') as stream:
            for name in expected['outputs']:
                path = work / S / (name + '.json')
                data = mathematical(name, json.loads(path.read_text()))
                encoded = canonical(data)
                digest = hashlib.sha256(encoded).hexdigest()
                need(digest == expected['mathematical_output_sha256'][name], 'entire mathematical output differs: ' + name)
                hashes[name] = digest
                line = canonical(dict(name=name, mathematical=data)) + b'\n'
                stream.write(line)
                whole.update(line)
                byte_count += len(line)
        need(whole.hexdigest() == expected['whole_mathematical_sha256'] and
             byte_count == expected['whole_mathematical_bytes'], 'entire mathematical stream differs')
        source_check()
        status.update(status='COMPLETE_PUBLIC_SOURCE_T0_REPLAY_PASS',
                      mode='optimized' if sys.flags.optimize else 'normal', python=sys.version,
                      complete_mathematical_sha256=whole.hexdigest(), complete_mathematical_bytes=byte_count,
                      whole_outputs_matched=len(hashes), elapsed_seconds=time.monotonic() - begun,
                      peak_RUSAGE_CHILDREN_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                      peak_RUSAGE_SELF_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      native_threads=1, serial_children=True, child_timeout_seconds=60,
                      original_kernel_guards_unchanged=True, source_seal=manifest,
                      raw_provenance_checked_before_normalization=True,
                      actual_semantic_damages_per_mode=17, actual_valid_controls_per_mode=3,
                      independent_person_review=False, ordinary_bridges_formalized=False)
        (work / 'VALIDATION.json').write_text(json.dumps(status, sort_keys=True, indent=2) + '\n')
        print(json.dumps({k:v for k,v in status.items() if k not in ['source_seal', 'stages', 'python']}, sort_keys=True))
    except BaseException as exc:
        status.update(status='INCOMPLETE_OR_FAILED_NO_MATHEMATICAL_ABSENCE', failure=type(exc).__name__ + ': ' + str(exc))
        (work / 'VALIDATION.json').write_text(json.dumps(status, sort_keys=True, indent=2) + '\n')
        raise

if __name__ == '__main__':
    main()
