"""Clean public-source replay, serial bounded children, full-record comparisons.

Every mathematical reconstruction is checked before expected summaries/hashes.
The all-count real/spectral/span argument is in PROOF.md, not this finite replay.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse, json, os, shutil, subprocess, sys, time

SOURCES = (
    'exact.py', 'linear.py', 'probe.py', 'completion_harmonic.py',
    'sectors_harmonic.py', 'sector_control_harmonic.py', 'trivariate.py',
    'pack_certificate.py', 'five_highq.py', 'check_five.py',
    'spread_repair.py', 'highq_control.py', 'damages_five.py',
)
CERT = 'FIVE-HIGHQ-CERTIFICATE.json'
SEALED = set(SOURCES) | {CERT, 'PROOF.md', 'README.md', 'EXPECTED.json',
                          'DEPENDENCIES.json', '.gitignore', 'verify.py',
                          'VALIDATION.json'}
STAGES = ('five_highq.py', 'check_five.py', 'damages_five.py',
          'completion_harmonic.py', 'sector_control_harmonic.py',
          'spread_repair.py', 'highq_control.py')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def clean(record):
    return {k: v for k, v in record.items()
            if k not in ('seconds', 'peak_KiB', 'optimized', 'status', 'execution')}


def integrity(source):
    rows = (source / 'SHA256SUMS').read_text().splitlines()
    require(len(rows) == len(SEALED), 'whole sealed file census')
    names = set()
    hashes = {}
    for line in rows:
        expected, name = line.split(maxsplit=1)
        require(name in SEALED and name not in names and Path(name).name == name,
                'unique plain source filename')
        require(len(expected) == 64 and set(expected) <= set('0123456789abcdef'),
                'full canonical SHA256')
        path = source / name
        require(path.is_file() and not path.is_symlink(), 'regular complete source ' + name)
        require(digest(path) == expected, 'whole source integrity ' + name)
        hashes[name] = expected
        names.add(name)
    require(names == SEALED, 'all and only sealed public source')
    return hashes


def read(folder, name):
    return json.loads((folder / name).read_text())


def checked_mode(folder, expected):
    # Each child itself pays the exact identities/forms before these comparisons.
    producer = read(folder, 'FIVE-HIGHQ-RESULT.json')
    require(producer['status'].startswith('ALL5 PIVOTS COEFFICIENT POSITIVE')
            and producer['traceback'] is None and producer['pivots'] == 5
            and producer['local_updates'] == 30 and producer['complete_form_fields'] == 25,
            'whole completed coefficient production; incomplete is not success')
    require(digest(folder / CERT) == expected['certificate_sha256'],
            'entire regenerated compact certificate')
    checked = clean(read(folder, 'FIVE-HIGHQ-CHECKED.json'))
    require(checked.get('complete') is True and checked == expected['coefficient'],
            'separate complete coefficient reader and expected identities')
    defects = clean(read(folder, 'FIVE-DAMAGES.json'))
    require(defects == expected['semantic_damages'] and len(defects['cases']) == 6
            and all(row['rejected'] is True for row in defects['cases']),
            'all six mathematical defects actually rejected')
    seed = clean(read(folder, 'UNRESTRICTED-FIRST-RESULT.json'))
    require(seed == expected['seed'], 'complete original seed/support/baseline result')
    spread = clean(read(folder, 'SPREAD-RESULT.json'))
    require(spread == expected['spread'], 'whole spread/dual/inverse/lift/rank control')
    physical = []
    for name in ('UNRESTRICTED-FIRST-SECTOR-CONTROL.json', 'HIGHQ-ORIGINAL-CONTROL.json'):
        record = read(folder, name)
        physical.append({k: v for k, v in record.items()
                         if k not in ('basis', 'metric', 'frame', 'cap',
                                      'residual_dual', 'blocks', 'status')})
    require(physical == expected['physical_controls'],
            'entire original physical controls and coverage')
    for name, row in expected['whole_generated_files'].items():
        path = folder / name
        require(path.is_file() and path.stat().st_size == row['bytes']
                and digest(path) == row['sha256'],
                'whole regenerated original record ' + name)
    return dict(coefficient=checked, seed=seed, spread=spread,
                semantic_damages=defects, physical_controls=physical,
                whole_generated_files=expected['whole_generated_files'])


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
    require(sys.version_info[:3] == (3, 12, 14), 'recorded CPython 3.12.14 runtime')
    require(not args.work_dir.exists(), 'fresh work directory required')
    work = args.work_dir.resolve()
    work.mkdir(parents=True)
    expected = read(source, 'EXPECTED.json')
    environment = os.environ.copy()
    for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        environment[name] = '1'
    environment.pop('PYTHONPATH', None)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    start = time.monotonic()
    children, results = [], []
    for optimized in (False, True):
        mode = 'optimized' if optimized else 'normal'
        folder = work / mode
        folder.mkdir()
        for name in SOURCES + (CERT,):
            shutil.copyfile(source / name, folder / name)
            require(digest(folder / name) == hashes[name], 'entire cold input ' + name)
        for stage in STAGES:
            require(integrity(source) == hashes, 'public source unchanged before child')
            for name in SOURCES:
                require(digest(folder / name) == hashes[name],
                        'entire cold mathematical source unchanged ' + name)
            command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [stage]
            child_start = time.monotonic()
            try:
                completed = subprocess.run(command, cwd=folder, env=environment,
                                           capture_output=True, text=True, timeout=60)
            except subprocess.TimeoutExpired as failure:
                (work / 'INCOMPLETE.json').write_text(json.dumps(dict(
                    complete=False, reason='child timeout, not mathematical absence',
                    program=stage, optimized=optimized), indent=2)+'\n')
                raise ValueError('incomplete 60-second child ' + stage) from failure
            elapsed = time.monotonic() - child_start
            (folder / (stage + '.stdout')).write_text(completed.stdout)
            (folder / (stage + '.stderr')).write_text(completed.stderr)
            require(completed.returncode == 0 and not completed.stderr,
                    'actual complete child exit ' + stage)
            # Compact child resource metadata is not a mathematical premise.
            output = json.loads(completed.stdout.strip().splitlines()[-1])
            receipt = dict(program=stage, optimized=optimized, seconds=elapsed,
                           exit_code=completed.returncode, actual_child_exit_waited=True,
                           peak_KiB=output.get('peak_KiB',
                               output.get('execution', {}).get('peak_KiB')))
            children.append(receipt)
            print(json.dumps(dict(stage=stage, optimized=optimized,
                                  completed=True, seconds=elapsed)), flush=True)
        results.append(checked_mode(folder, expected))
    require(results[0] == results[1], 'complete normal/optimized mathematical agreement')
    for name in (CERT,) + tuple(expected['whole_generated_files']):
        require((work/'normal'/name).read_bytes() == (work/'optimized'/name).read_bytes(),
                'ENTIRE normal/optimized output bytes ' + name)
    require(integrity(source) == hashes, 'final unchanged public source')
    canonical = json.dumps(results[0], sort_keys=True, separators=(',', ':'))+'\n'
    (work/'WHOLE-REPLAY.json').write_text(canonical)
    out = dict(agent='six-downset-1', role='researcher', complete=True,
        runtime=sys.version.split()[0], children=children,
        children_completed=len(children), native_threads=1, serial_intensive_children=1,
        child_seconds_limit=60, source_hashes=hashes,
        whole_normal_optimized_mathematics_agree=True,
        whole_normal_optimized_generated_bytes_agree=True,
        mathematical_defects_rejected_each_mode=6,
        whole_replay_bytes=len(canonical.encode()),
        whole_replay_sha256=sha256(canonical.encode()).hexdigest(),
        certificate_sha256=expected['certificate_sha256'],
        generated_artifacts_are_not_published_inputs=True,
        ordinary_infinite_parameter_bridges_unformalized=True, independent_review=False,
        seconds=time.monotonic()-start, verified_utc=datetime.now(timezone.utc).isoformat())
    (work/'VALIDATION.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('children', 'source_hashes')}),
          flush=True)


if __name__ == '__main__':
    main()
