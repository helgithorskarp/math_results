"""Cold source-only serial reproduction; outputs remain outside this directory."""
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


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def check_source(root):
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    for item in manifest['files']:
        path = root / item['path']
        require(path.is_file() and not path.is_symlink() and path.stat().st_size == item['bytes']
                and digest(path) == item['sha256'], 'whole source seal: ' + item['path'])
    return digest(root / 'MANIFEST.json')


def check_health(state):
    if state is None:
        return None
    for root in [state, state / 'monitor']:
        for name in ['PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json']:
            path = root / name
            if path.exists():
                if name == 'HANDOVER.json' and json.loads(path.read_text()).get('phase') == 'completed':
                    continue
                raise RuntimeError('ACTIVE_OPERATIONS_BARRIER; no mathematical child started')
    raw = json.loads((state / 'monitor/health.json').read_text())
    age = (datetime.datetime.now(datetime.timezone.utc) -
           datetime.datetime.fromisoformat(raw['checked_at'].replace('Z', '+00:00'))).total_seconds()
    budget = raw['credit_budget']
    require(0 <= age <= 180 and not raw['reasons'] and budget['status'] == 'authorized' and
            Decimal(budget['observed_spent_credits']) < Decimal(budget['stop_at_observed_spend_credits']),
            'fresh clear authorized operations reading')
    return raw['checked_at']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path)
    ap.add_argument('--campaign-state', type=Path)
    a = ap.parse_args()
    source = Path(__file__).resolve().parent
    parameters = json.loads((source / 'PARAMETERS.json').read_text())
    seal = check_source(source)
    require(sys.version.split()[0] == parameters['python'], 'declared CPython version')
    work = Path(tempfile.mkdtemp(prefix='three-c-support-')) if a.work is None else a.work.resolve()
    if a.work is not None:
        require(not work.exists(), 'fresh external output directory')
        work.mkdir(parents=True)
    require(work != source and source not in work.parents, 'outputs outside source packet')
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']:
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    manifest = json.loads((source / 'MANIFEST.json').read_text())
    receipts, controls, generated = [], [], []
    stages = ['anchor', 'ordered', 'full', 'rooted', 'filter', 'images', 'pairs']
    for mode in ['normal', 'O']:
        out = work / mode
        out.mkdir()
        cold = out / 'source'
        cold.mkdir()
        for name in ['MANIFEST.json'] + [x['path'] for x in manifest['files']]:
            target = cold / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, target)
        require(check_source(cold) == seal, 'whole isolated source copy')
        prefix = [sys.executable] + (['-O'] if mode == 'O' else [])

        def run(stage, name, command, output, claim=True):
            require(check_source(source) == seal and check_source(cold) == seal,
                    'immutable source before each child')
            checked = check_health(a.campaign_state)
            input_record = None
            if name != 'materialize':
                input_record = json.loads((out / stage / 'materialize.json').read_text())
                for item in input_record['files']:
                    path = cold / item['path']
                    require(path.stat().st_size == item['bytes'] and digest(path) == item['sha256'],
                            'declared generated input before child')
            started = time.monotonic()
            timed_out = False
            returncode = None
            with (out / stage / (name + '.stdout')).open('wb') as stdout:
                with (out / stage / (name + '.stderr')).open('wb') as stderr:
                    try:
                        returncode = subprocess.run(command, cwd=cold, env=env, stdout=stdout,
                                                    stderr=stderr, timeout=60).returncode
                    except subprocess.TimeoutExpired:
                        timed_out = True
            receipt = dict(mode=mode, stage=stage, kernel=name, returncode=returncode,
                timed_out=timed_out, elapsed_seconds=time.monotonic()-started,
                child_timeout_seconds=60, native_threads=1, serial=True,
                health_checked_at=checked, source_manifest_before=seal,
                source_manifest_after=check_source(source), cold_manifest_after=check_source(cold))
            write(out / stage / (name + '-receipt.json'), receipt)
            require(not timed_out and (returncode == 0 if claim else returncode != 0),
                    'INCOMPLETE child; failure or timeout is not absence')
            require(receipt['source_manifest_after'] == receipt['cold_manifest_after'] == seal,
                    'source unchanged after child')
            if input_record is not None:
                for item in input_record['files']:
                    require(digest(cold / item['path']) == item['sha256'],
                            'generated input unchanged after child')
            if claim:
                require(output.is_file(), 'whole completed output')
                receipts.append(receipt)
            else:
                require(not output.exists() and b'RuntimeError: INCOMPLETE: original500000/20 guard'
                        in (out / stage / (name + '.stderr')).read_bytes(),
                        'incomplete guard propagates past damage handler without claim output')
                controls.append(receipt)
            print(json.dumps(dict(mode=mode, stage=stage, kernel=name,
                completed=claim, explicit_incomplete_control=not claim,
                elapsed_seconds=receipt['elapsed_seconds']), sort_keys=True), flush=True)

        for stage in stages:
            folder = out / stage
            folder.mkdir()
            materialized = folder / 'materialize.json'
            run(stage, 'materialize', prefix + [str(cold / 'materialize.py'), '--work', str(out),
                '--stage', stage, '--output', str(materialized)], materialized)
            generated.append(dict(mode=mode, stage=stage,
                                  files=json.loads(materialized.read_text())['files']))
            for name in parameters['stages'][stage]['kernels']:
                output = folder / (name + '.json')
                command = prefix + [str(cold / stage / (name + '.py')), '--output', str(output)]
                if name == 'verify':
                    command += ['--literal', str(folder / 'literal.json'), '--dual', str(folder / 'dual.json'),
                                '--expected', str(cold / stage / 'EXPECTED.json')]
                run(stage, name, command, output)
            if stage in parameters['expected_math']:
                result = json.loads((folder / 'literal.json').read_text())
                require(result['common_math_sha256'] == parameters['expected_math'][stage],
                        'entire original mathematical fingerprint: ' + stage)
            if stage == 'filter':
                require(json.loads((folder / 'filter.json').read_text())['whole_result_math_sha256'] ==
                        parameters['expected_filter_whole_result_sha256'], 'whole necessary-filter fingerprint')
            if stage == 'images':
                output = folder / 'incomplete-control.json'
                run(stage, 'incomplete-control', prefix + [str(cold / stage / 'verify.py'),
                    '--literal', str(folder / 'literal.json'), '--dual', str(folder / 'dual.json'),
                    '--expected', str(cold / stage / 'EXPECTED.json'), '--output', str(output),
                    '--force-incomplete-damage-control'], output, claim=False)

    for stage in stages:
        for name in ['materialize'] + parameters['stages'][stage]['kernels']:
            require((work / 'normal' / stage / (name + '.json')).read_bytes() ==
                    (work / 'O' / stage / (name + '.json')).read_bytes(),
                    'entire normal/-O output: ' + stage + '/' + name)
        records = json.loads((work / 'normal' / stage / 'materialize.json').read_text())['files']
        for item in records:
            require((work / 'normal/source' / item['path']).read_bytes() ==
                    (work / 'O/source' / item['path']).read_bytes(), 'whole normal/-O generated input')
    summary = dict(agent='six-code-3', role='researcher',
        status='COMPLETE_COLD_CANONICAL_SOURCE_ONLY_REPRODUCTION',
        python=sys.version.split()[0], source_manifest_sha256=seal,
        all_whole_mode_outputs_equal=True, all_whole_generated_inputs_equal=True,
        private_generated_inputs_read=False, native_threads=1, serial=True,
        ordinary_bridges_formalized=False, independent_person_review=False,
        completed_children=len(receipts), incomplete_controls=controls,
        children=receipts, generated_input_records=generated,
        mathematical_fingerprints=parameters['expected_math'],
        pair_summary=json.loads((work / 'normal/pairs/verify.json').read_text()),
        no_unrestricted_endpoint_improvement=True)
    write(work / 'COMPLETE.json', summary)
    print(json.dumps(dict(status=summary['status'], completed_children=len(receipts),
                         work=str(work), source_manifest_sha256=seal), sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
