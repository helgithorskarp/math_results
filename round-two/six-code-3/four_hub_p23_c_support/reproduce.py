"""Cold, serial, source-only reproduction; explicit 60-second child limits."""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from decimal import Decimal
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_check(root):
    path = root / 'MANIFEST.json'
    manifest = json.loads(path.read_text())
    require(manifest['agent'] == 'six-code-3' and manifest['role'] == 'researcher',
            'actual source author')
    for item in manifest['files']:
        rel = Path(item['path'])
        require(len(rel.parts) == 1 and rel.name != 'MANIFEST.json', 'flat source packet')
        require((root / rel).is_file() and not (root / rel).is_symlink(), 'literal source file')
        require((root / rel).stat().st_size == item['bytes'] and
                digest(root / rel) == item['sha256'], 'entire source/input seal: ' + str(rel))
    return digest(path)


def campaign_gate(state):
    if state is None:
        return None
    for root in [state, state / 'monitor']:
        for name in ['PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json']:
            path = root / name
            if path.exists():
                if name == 'HANDOVER.json' and json.loads(path.read_text()).get('phase') == 'completed':
                    continue
                raise ValueError('active operations barrier')
    health = json.loads((state / 'monitor/health.json').read_text())
    budget = health['credit_budget']
    age = (datetime.datetime.now(datetime.timezone.utc) -
           datetime.datetime.fromisoformat(health['checked_at'].replace('Z', '+00:00'))).total_seconds()
    require(0 <= age <= 180 and not health['reasons'] and budget['status'] == 'authorized' and
            Decimal(budget['observed_spent_credits']) < Decimal(budget['stop_at_observed_spend_credits']),
            'fresh authorized operations health')
    return health['checked_at']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path)
    parser.add_argument('--campaign-state', type=Path,
                        help='optional read-only operational gate for this research campaign')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    seal = manifest_check(source)
    if args.work is None:
        work = Path(tempfile.mkdtemp(prefix='four-hub-c-support-'))
    else:
        work = args.work.resolve()
        require(not work.exists(), 'fresh external output tree')
        work.mkdir(parents=True)
    require(source != work and source not in work.parents, 'outputs outside source packet')
    cold = work / 'source'
    cold.mkdir()
    files = json.loads((source / 'MANIFEST.json').read_text())['files']
    for name in ['MANIFEST.json'] + [item['path'] for item in files]:
        shutil.copyfile(source / name, cold / name)
    require(manifest_check(cold) == seal, 'whole cold source copy')
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS']:
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    receipts = []
    for mode in ['normal', 'O']:
        out = work / mode
        out.mkdir()
        prefix = [sys.executable] + (['-O'] if mode == 'O' else [])
        for name in ['literal', 'dual', 'verify']:
            require(manifest_check(source) == seal and manifest_check(cold) == seal,
                    'source seal before every child')
            health_checked = campaign_gate(args.campaign_state)
            output = out / (name + '.json')
            command = prefix + [str(cold / (name + '.py')), '--output', str(output)]
            if name == 'verify':
                command += ['--literal', str(out / 'literal.json'), '--dual', str(out / 'dual.json'),
                            '--expected', str(cold / 'EXPECTED.json')]
            started = time.monotonic()
            timed_out, returncode = False, None
            with (out / (name + '.stdout')).open('wb') as stdout:
                with (out / (name + '.stderr')).open('wb') as stderr:
                    try:
                        returncode = subprocess.run(command, cwd=cold, env=env, stdout=stdout,
                                                    stderr=stderr, timeout=60).returncode
                    except subprocess.TimeoutExpired:
                        timed_out = True
            receipt = dict(mode=mode, kernel=name, returncode=returncode, timed_out=timed_out,
                           elapsed_seconds=time.monotonic() - started,
                           explicit_child_timeout_seconds=60, native_threads=1, serial=True,
                           health_checked_at=health_checked,
                           source_before=seal, source_after=manifest_check(source),
                           cold_source_after=manifest_check(cold))
            (out / (name + '-receipt.json')).write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
            receipts.append(receipt)
            require(not timed_out and returncode == 0,
                    'INCOMPLETE reproduction; timeout/failure is not mathematical absence')
            require(receipt['source_after'] == seal and receipt['cold_source_after'] == seal,
                    'source seal after every child')
            print(json.dumps(dict(mode=mode, kernel=name, completed=True,
                                  elapsed_seconds=receipt['elapsed_seconds']), sort_keys=True), flush=True)
    for name in ['literal', 'dual', 'verify']:
        require((work / 'normal' / (name + '.json')).read_bytes() ==
                (work / 'O' / (name + '.json')).read_bytes(), 'all whole normal/optimized output bytes')
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_COLD_SOURCE_ONLY_REPRODUCTION',
                  python=sys.version.split()[0], source_manifest_sha256=seal,
                  serial_children=len(receipts), all_whole_mode_outputs_equal=True,
                  children=receipts,
                  mathematics=json.loads((work / 'normal/verify.json').read_text()),
                  no_private_inputs_or_modules=True, ordinary_bridges_formalized=False,
                  independent_person_review=False)
    (work / 'COMPLETE.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=result['status'], work=str(work), source_manifest_sha256=seal,
                          complete_math_cases=result['mathematics']['cases']), sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
