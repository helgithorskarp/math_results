"""Complete compact-source replay with fresh serial normal/optimized children.

Actual author six-downset-1 / researcher. Adapted from own source7fa verifier.
The ordinary infinite-parameter and real/spectral proof is in PROOF.md.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

SOURCES = (
    'exact.py', 'linear.py', 'probe.py', 'trivariate.py', 'pack_certificate.py',
    'three_mark.py', 'three_sector.py', 'three_spread.py',
    'second_control.py', 'third_control.py', 'three_five_allq.py',
    'check_three_five.py', 'damage_three_five.py', 'damage_three_original.py',
    'bind_three_forms.py',
)
CERT = 'THREE-EVEN-FIVE-ALLQ-CERTIFICATE.json'
SEALED = set(SOURCES) | {CERT, 'PROOF.md', 'README.md', 'EXPECTED.json',
                         'CREDITS.json', 'DEPENDENCIES.json', '.gitignore', 'verify.py'}
STAGES = (
    'three_mark.py', 'three_sector.py', 'three_spread.py',
    'second_control.py', 'third_control.py', 'three_five_allq.py',
    'check_three_five.py', 'damage_three_five.py', 'damage_three_original.py',
    'bind_three_forms.py',
)
GENERATED = {
    'THREE-MARK-FIRST-MATRIX.json', 'THREE-MARK-FIRST-RESULT.json',
    'THREE-MARK-FIRST-SECTOR.json', 'THREE-MARK-FIRST-SECTOR-RESULT.json',
    'THREE-MARK-FIRST-SPREAD-RESULT.json', 'THREE-MARK-SECOND-MATRIX.json',
    'THREE-MARK-SECOND-RESULT.json', 'THREE-MARK-THIRD-MATRIX.json',
    'THREE-MARK-THIRD-RESULT.json', 'THREE-EVEN-FIVE-ALLQ-RESULT.json',
    'THREE-EVEN-FIVE-ALLQ-CHECKED.json', 'THREE-FIVE-DAMAGES.json',
    'THREE-ORIGINAL-DAMAGES.json', 'THREE-ORIGINAL-FORM-BINDINGS.json',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()
                if k not in ('seconds', 'peak_KiB', 'optimized', 'status', 'execution')}
    if isinstance(obj, list):
        return [clean(v) for v in obj]
    return obj


def read(folder, name):
    return json.loads((folder/name).read_text())


def integrity(source):
    # Unexpected importable input must not enter either cold copy.
    allowed = SEALED | {'SHA256SUMS'} | GENERATED | {'__pycache__', 'replay-output'}
    require(all(p.name in allowed for p in source.iterdir()),
            'all and only declared source/runtime entries')
    lines = (source/'SHA256SUMS').read_text().splitlines()
    require(len(lines) == len(SEALED), 'whole sealed source census')
    hashes = {}
    for line in lines:
        expected, name = line.split(maxsplit=1)
        require(name in SEALED and name not in hashes and Path(name).name == name,
                'unique plain sealed filename')
        require(len(expected) == 64 and set(expected) <= set('0123456789abcdef'),
                'canonical full SHA256')
        p = source/name
        require(p.is_file() and not p.is_symlink(), 'regular entire source '+name)
        require(digest(p) == expected, 'whole source integrity '+name)
        hashes[name] = expected
    require(set(hashes) == SEALED, 'complete source seal')
    credited = read(source, 'CREDITS.json')['files']
    require(len(credited) == 5 and len({x['file'] for x in credited}) == 5,
            'all five unique verbatim credits')
    for row in credited:
        name = row['file']
        require(name in SOURCES and row['copied_verbatim'] is True
                and (source/name).stat().st_size == row['bytes']
                and hashes[name] == row['sha256'], 'whole credited original utility '+name)
    return hashes


def checked_mode(folder, expected):
    producer = read(folder, 'THREE-EVEN-FIVE-ALLQ-RESULT.json')
    require(producer['status'].startswith('ALL5 PIVOTS COEFFICIENT POSITIVE')
            and producer['traceback'] is None and producer['pivots'] == 5
            and producer['local_updates'] == 30 and producer['complete_form_fields'] == 25,
            'completed all coefficient fields; incomplete producer is not success')
    require(digest(folder/CERT) == expected['certificate_sha256'],
            'entire regenerated coefficient certificate')
    records = {}
    for name, value in expected['records'].items():
        actual = clean(read(folder, name))
        require(actual == value, 'whole mathematical record '+name)
        records[name] = actual
    for name in ('THREE-FIVE-DAMAGES.json', 'THREE-ORIGINAL-DAMAGES.json'):
        d = records[name]
        require(d['all_rejected'] is True and len(d['cases']) == 6
                and all(x['rejected'] is True for x in d['cases']),
                'all six actual semantic rejections '+name)
    checked = records['THREE-EVEN-FIVE-ALLQ-CHECKED.json']
    require(checked['complete'] is True and checked['original_form_fields'] == 25
            and checked['local_updates'] == 30 and checked['positive_pivot_coefficients'] == 265,
            'complete separate whole coefficient reader')
    binding = records['THREE-ORIGINAL-FORM-BINDINGS.json']
    require(binding['complete'] is True and binding['actual_original_form_positions'] == 75,
            'all original even-five positions on all three controls')
    controls = [dict(seed=records['THREE-MARK-FIRST-RESULT.json'],
                     sector=records['THREE-MARK-FIRST-SECTOR-RESULT.json'],
                     repair=records['THREE-MARK-FIRST-SPREAD-RESULT.json']),
                records['THREE-MARK-SECOND-RESULT.json'],
                records['THREE-MARK-THIRD-RESULT.json']]
    for expected_N, d in zip((50, 58, 76), controls):
        a, b, c = d['seed'], d['sector'], d['repair']
        N = a['N']
        require(N == expected_N and a['full_core'] == dict(psd=True, rank=N-3)
                and a['original_lower'] == dict(psd=True, rank=N-2)
                and a['original_cap'] == dict(psd=True, rank=N-1)
                and a['original_cap_floor_one'] == dict(psd=True, rank=N-1)
                and a['whole_physical_cap_floor_one'] == dict(psd=True, rank=N-3),
                'whole original seed/empty/physical cap and ranks')
        require(a['all_actual_empty_equations_checked'] is True
                and a['all_original_rows_spanned'] is True
                and b['all_cross_sector_positions_checked'] is True
                and b['both_light_means_retained'] is True
                and b['aggregate_dimension'] == 15
                and c['all_original_inverse_positions'] == N-1,
                'whole original physical/empty/dual/inverse coverage')
        require(len(c['repaired']) == 2 and all(x['lower_rank'] == x['upper_rank'] == N-1
                for x in c['repaired']), 'both interior original greatest ranks')
    for name, row in expected['whole_generated_files'].items():
        p = folder/name
        require(p.is_file() and p.stat().st_size == row['bytes']
                and digest(p) == row['sha256'], 'whole generated original data '+name)
    return dict(records=records, whole_generated_files=expected['whole_generated_files'],
                certificate_sha256=expected['certificate_sha256'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir', type=Path, default=Path('replay-output'))
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    hashes = integrity(source)
    if args.integrity_only:
        print(json.dumps(dict(complete=True, sealed_files=len(hashes),
            source_integrity_verified=True, optimized=not __debug__)))
        return
    require(sys.version_info[:3] == (3, 12, 14), 'recorded CPython3.12.14 runtime')
    require(not args.work_dir.exists(), 'fresh work directory required')
    work = args.work_dir.resolve()
    require(work != source, 'cold output distinct from source')
    work.mkdir(parents=True)
    expected = read(source, 'EXPECTED.json')
    environment = os.environ.copy()
    for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        environment[name] = '1'
    environment.pop('PYTHONPATH', None)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    children, results = [], []
    start = time.monotonic()
    for optimized in (False, True):
        folder = work/('optimized' if optimized else 'normal')
        folder.mkdir()
        for name in SOURCES+(CERT,):
            shutil.copyfile(source/name, folder/name)
            require(digest(folder/name) == hashes[name], 'complete cold input '+name)
        for stage in STAGES:
            require(integrity(source) == hashes, 'entire public source unchanged')
            require(all(digest(folder/name) == hashes[name] for name in SOURCES),
                    'all cold mathematical source bytes unchanged')
            command = [sys.executable, '-B']+(['-O'] if optimized else [])+[stage]
            child_start = time.monotonic()
            try:
                completed = subprocess.run(command, cwd=folder, env=environment,
                    capture_output=True, text=True, timeout=60)
            except subprocess.TimeoutExpired as failure:
                (work/'INCOMPLETE.json').write_text(json.dumps(dict(complete=False,
                    reason='60s child timeout; not mathematical absence',
                    program=stage, optimized=optimized), indent=2)+'\n')
                raise ValueError('incomplete guarded child '+stage) from failure
            elapsed = time.monotonic()-child_start
            (folder/(stage+'.stdout')).write_text(completed.stdout)
            (folder/(stage+'.stderr')).write_text(completed.stderr)
            require(completed.returncode == 0 and not completed.stderr,
                    'actual complete child exit '+stage)
            output = json.loads(completed.stdout.strip().splitlines()[-1])
            children.append(dict(program=stage, optimized=optimized,
                seconds=elapsed, exit_code=completed.returncode, actual_child_exit_waited=True,
                peak_KiB=output.get('peak_KiB', output.get('execution',{}).get('peak_KiB'))))
            print(json.dumps(dict(stage=stage, optimized=optimized,
                completed=True, seconds=elapsed)), flush=True)
        results.append(checked_mode(folder, expected))
    require(results[0] == results[1], 'entire normal/optimized mathematical agreement')
    for name in (CERT,)+tuple(expected['whole_generated_files']):
        require((work/'normal'/name).read_bytes() == (work/'optimized'/name).read_bytes(),
                'whole normal/optimized generated bytes '+name)
    require(integrity(source) == hashes, 'final full unchanged source seal')
    canonical = json.dumps(results[0], sort_keys=True, separators=(',',':'))+'\n'
    (work/'WHOLE-REPLAY.json').write_text(canonical)
    out = dict(agent='six-downset-1', role='researcher', complete=True,
        runtime=sys.version.split()[0], children=children, children_completed=len(children),
        native_threads=1, serial_intensive_children=1, child_seconds_limit=60,
        source_hashes=hashes, whole_normal_optimized_mathematics_agree=True,
        whole_normal_optimized_generated_bytes_agree=True,
        semantic_defects_rejected_each_mode=12, total_semantic_defect_rejections=24,
        controls=[50,58,76], complete_original_form_positions=75,
        whole_replay_bytes=len(canonical.encode()),
        whole_replay_sha256=sha256(canonical.encode()).hexdigest(),
        certificate_sha256=expected['certificate_sha256'],
        generated_artifacts_are_not_published_inputs=True,
        ordinary_infinite_parameter_bridges_unformalized=True, independent_review=False,
        seconds=time.monotonic()-start, verified_utc=datetime.now(timezone.utc).isoformat())
    (work/'VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('children','source_hashes')}),flush=True)


if __name__ == '__main__':
    main()
