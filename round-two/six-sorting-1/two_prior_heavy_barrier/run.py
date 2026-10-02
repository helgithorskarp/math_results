"""Regenerate the ten heavy routes and independently check every obstruction.

Standard-library Python, one serial mathematical child, 55s per child.
An unsuccessful stage terminates reproduction without a negative claim.
The old9590 theorem is imported; only its exact kernel vectors are rebuilt.
"""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from controls import operations_allow

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def read(name):
    return json.loads((WORK/name).read_text())


def finite(record):
    return record.get('finite', {k: v for k, v in record.items()
                               if k not in ('seconds', 'maximum_rss_kib')})


def verify_pins():
    for directory in (ROOT, ROOT/'prior'):
        manifest = json.loads((directory/'source-manifest.json').read_text())
        for row in manifest['files']:
            need(hashlib.sha256((directory/row['path']).read_bytes()).hexdigest() == row['sha256'],
                 'Source pin differs: '+str(directory/row['path']))


def stage(name, args=(), optimize=False, receipt=None):
    operations_allow()
    command = [sys.executable]+(['-O'] if optimize else [])+[str(ROOT/name), *map(str, args)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=55, check=False)
    need(result.returncode == 0, 'Failed/incomplete '+name+': '+result.stderr[-2200:])
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
    need(rows, 'Missing exact stage record: '+name)
    if receipt:
        (WORK/receipt).write_text(json.dumps(rows[0], indent=2)+'\n')
    print(json.dumps({'stage': name, 'args': list(args), 'optimized': optimize,
                      'status': 'EXACT_STAGE_COMPLETE'}, sort_keys=True), flush=True)
    return rows[0]


def both(name, args=(), paths=None, receipts=None):
    a = stage(name, args, receipt=receipts[0] if receipts else None)
    b = stage(name, args, True, receipt=receipts[1] if receipts else None)
    if paths:
        a, b = (read(n) for n in paths)
    need(finite(a) == finite(b), 'Complete normal/O finite records differ: '+name)
    return a


def main():
    started = time.monotonic()
    operations_allow()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '1'
    WORK.mkdir(exist_ok=True)
    verify_pins()
    certificate = json.loads((ROOT/'certificate.json').read_text())
    # These first stages rebuild literal old images, not the imported old
    # negative theorem's selected nested lower-bound certificates.
    stage('prior/base.py')
    base = both('prior/verify_base.py')
    stage('prior/preparations.py', ('--partner', 4))
    both('prior/verify_preparations.py')
    stage('prior/minimum.py')
    both('prior/verify_minimum.py')
    stage('prior/fronts.py')
    old_cover = both('prior/verify_fronts.py')
    old_certificate = json.loads((ROOT/'prior/certificate.json').read_text())
    need(old_cover['producer_records_sha256'] == old_certificate['front_records_sha256'],
         'Imported old kernel vectors differ')
    need(base['core_image_sha256'] == certificate['base_complete_core_sha256'], 'Base image differs')
    stage('cover.py')
    seeds = both('verify_seeds.py', receipts=('seeds-normal.json', 'seeds-O.json'))
    need(seeds['finite']['independent_original_cube_cache_sha256'] ==
         certificate['independent_original_cube_cache_sha256'], 'Original scalar cubes differ')

    preparation_counts, front_counts, front_metrics = Counter(), Counter(), Counter()
    front_hashes = []
    branches = [r['branch_index'] for r in certificate['heavy_routes']]
    need(branches == [0, 6, 11, 15, 16, 19, 21, 22, 23, 24], 'Incomplete heavy route list')
    for expected in certificate['heavy_routes']:
        i = expected['branch_index']
        stage('preparations.py', (i, i+1))
        prep = both('verify_preparations.py', (i, i+1),
                    paths=(f'checked{i:02}.json', f'checked{i:02}-O.json'))
        need(prep['finite_sha256'] == expected['finite_sha256'], 'Complete preparation records differ')
        producer = read(f'branch{i:02}.json')
        need(producer['HIGH_word'] == expected['HIGH_word'] and producer['complete'] and
             producer['queue_unexpanded'] == 0 and producer['full_functions_seen'] == expected['functions'],
             'Preparation route or full closure differs')
        preparation_counts.update(producer['census'])
        stage('screen_cuts.py', (i, i+1))
        both('verify_cuts.py', (i, i+1), paths=(
            f'two-prior-free-cut-independent-{i:02}-{i+1:02}.json',
            f'two-prior-free-cut-independent-{i:02}-{i+1:02}-O.json'))
        stage('fronts.py', (i,))
        front = both('verify_fronts.py', (i,),
                     paths=(f'heavy-checked{i:02}.json', f'heavy-checked{i:02}-O.json'))
        front_counts.update(front['finite']['census'])
        front_metrics.update(front['finite']['metrics'])
        front_hashes.append([i, front['finite_sha256']])
    need(dict(preparation_counts) == certificate['preparation_census'], 'Full preparation census differs')
    need(dict(front_counts) == certificate['front_census'] and
         dict(front_metrics) == certificate['front_metrics'] and
         digest(front_hashes) == certificate['front_finite_sha256'], 'Complete front cover differs')

    stage('inherit.py')
    inherited = both('verify_inherited.py', paths=(
        'two-prior-heavy-inheritance-independent.json', 'two-prior-heavy-inheritance-independent-O.json'))
    need(inherited['finite_sha256'] == certificate['inherited_finite_sha256'] and
         inherited['finite']['census']['PUBLISHED_ONE_PRIOR_KERNEL_INCLUSION_EXCLUDES_STANDARD_SIZE44'] ==
         certificate['inherited_excluded_fronts'], 'Inherited exact obstruction cover differs')
    for i in branches:
        stage('select_constant.py', (i,))

    constant_rows = []
    constant_counts, constant_metrics = Counter(), Counter()
    constant_minimum = None
    for i in branches:
        count = len(read(f'residual-constant{i:02}.json')['cases'])
        for first in range(0, count, 1000):
            last = min(first+1000, count)
            record = both('verify_constant.py', (i, first, last), paths=(
                f'constant-checked{i:02}-{first:05}-{last:05}.json',
                f'constant-checked{i:02}-{first:05}-{last:05}-O.json'))
            f = record['finite']
            constant_counts.update(f['census'])
            constant_metrics.update(f['metrics'])
            if f['minimum_selected_mass'] is not None:
                constant_minimum = f['minimum_selected_mass'] if constant_minimum is None else min(
                    constant_minimum, f['minimum_selected_mass'])
            constant_rows.append([i, first, last, record['finite_sha256']])
    need(digest(constant_rows) == certificate['constant_finite_sha256'] and
         constant_counts['independently_constant16_excluded_cases'] == certificate['constant_excluded_fronts'] and
         constant_counts['selected_outer_occurrences'] == certificate['constant_selected_outer_occurrences'] and
         dict(constant_metrics) == certificate['constant_outer_metrics'] and
         constant_minimum == certificate['minimum_selected_mass'], 'Complete constant certificate differs')
    stage('select_inner.py')
    inner = both('verify_inner.py', paths=(
        'two-prior-seven-inner-independent.json', 'two-prior-seven-inner-independent-O.json'))
    need(inner['finite_sha256'] == certificate['inner_finite_sha256'] and
         inner['finite']['census']['independently_inner_excluded_cases'] == certificate['inner_excluded_fronts'] and
         dict(inner['finite']['metrics']) == certificate['inner_metrics'], 'Complete inner certificate differs')
    need(sum(certificate[k] for k in ('inherited_excluded_fronts', 'constant_excluded_fronts',
                                     'inner_excluded_fronts')) == front_counts['surviving_complete_fronts'] and
         constant_minimum > certificate['size44_ceiling'], 'Obstruction partition incomplete or not strict')
    verify_pins()
    report = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'TEN_HEAVY_TWO_PRIOR_ROUTES_EXCLUDED_ALL_FINITE_PREMISES_VERIFIED_NORMAL_AND_O',
              'certificate_sha256': hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest(),
              'preparation_functions': sum(r['functions'] for r in certificate['heavy_routes']),
              'front_census': dict(front_counts), 'front_metrics': dict(front_metrics),
              'front_finite_sha256': digest(front_hashes),
              'inherited_finite_sha256': inherited['finite_sha256'],
              'constant_finite_sha256': digest(constant_rows),
              'inner_finite_sha256': inner['finite_sha256'],
              'verified_remaining_core_targets': front_counts['surviving_complete_fronts'],
              'minimum_selected_mass': constant_minimum, 'size44_ceiling': 1 << 44,
              'normal_optimized_all_finite_records_equal': True,
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False,
              'written_bridges_formalized': False, 'imported_old_negative_theorem_reproved': False,
              'seconds': time.monotonic()-started, 'python': sys.version.split()[0]}
    (WORK/'verified-summary.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
