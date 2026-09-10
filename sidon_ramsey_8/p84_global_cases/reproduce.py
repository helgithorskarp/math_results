#!/usr/bin/env python3
"""Verify complete P84 anchor coverage and the 213 closed nonempty cases."""
import argparse
import concurrent.futures
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from orbits import prepare as prepare_orbits, sidon
from prepare_residuals import prepare as prepare_residuals

SOURCE = Path(__file__).resolve().parent

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def run(command):
    result = subprocess.run(list(map(str, command)), capture_output=True,
                            text=True, check=True)
    return json.loads(result.stdout)

def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def rows(path):
    return [{k: int(v) for k, v in row.items()}
            for row in csv.DictReader(path.open())]

def main():
    if not __debug__:
        raise SystemExit('Run without -O/PYTHONOPTIMIZE: assertions verify evidence.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--sat-checks', action='store_true',
                        help='requires python-sat; checks encoding semantics')
    args = parser.parse_args()
    assert 1 <= args.jobs <= 12
    work = args.work.resolve()
    assert SOURCE.parent not in [work, *work.parents]
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    report = {}
    programs = {'coverage': SOURCE/'coverage.cpp',
                'complete40': SOURCE/'complete40.cpp',
                'enumerate': SOURCE.parent/'enumerate.cpp',
                'reference': SOURCE.parent/'reference.cpp'}
    for name, path in programs.items():
        subprocess.run(['g++', '-O3', '-std=c++20', '-Wall', '-Wextra',
                        '-Wconversion', '-Wshadow', '-Werror', str(path),
                        '-o', str(work/name)], check=True)
    weights_path = SOURCE.parent/'p84_profiles/weights.txt'
    shutil.copyfile(weights_path, work/'weights.txt')
    weights = list(map(int, weights_path.read_text().split()))
    assert len(weights) == 84 and weights == weights[::-1]
    assert min(weights) >= 0 and sum(weights) == 15685948
    for k in [10, 11]:
        output = work/'sets84_11.txt' if k == 11 else '-'
        result = run([work/'enumerate', 84, k, 'all', output, weights_path])
        assert result['complete']
        assert result['sets'] == {10: 35250764, 11: 30510}[k]
        assert result['max_weight'] == 1999990
        report[f'catalog_{k}'] = result
    reference = run([work/'reference', 84, 11, work/'reference_sets.txt'])
    assert reference['complete'] and reference['sets'] == 30510
    def catalog(path):
        return {tuple(map(int, line.split())) for line in path.read_text().splitlines()}
    assert catalog(work/'sets84_11.txt') == catalog(work/'reference_sets.txt')
    report['reference_catalog'] = reference
    report['orbits'] = prepare_orbits(work/'sets84_11.txt', weights_path, work)
    assert report['orbits']['eligible_orbits'] == 1488
    assert report['orbits']['raw_catalog_sha256'] == 'e1541890c78cb206076fbcd6067b2da24884b044f902c1c03ffc0da7ccdc0720'
    for mode in ['global', 'anchored']:
        report[mode] = run([work/'coverage', mode, work/'orbit_catalog.txt',
                            weights_path, work/f'{mode}.csv'])
        assert report[mode]['complete']
    global_rows, anchored_rows = rows(work/'global.csv'), rows(work/'anchored.csv')
    assert len(global_rows) == len(anchored_rows) == 1488
    for g, a in zip(global_rows, anchored_rows):
        assert g['orbit'] == a['orbit'] and g['weight'] == a['weight']
        assert g['count'] == 2*a['count'] - a['both_orientations']
        assert g['reflection_fixed'] == a['reflection_fixed']
    assert report['global']['packings'] == 125576811
    assert report['anchored']['packings'] == 62861452
    assert report['anchored']['both_orientations'] == 146093
    assert report['global']['reflection_fixed'] == 2639
    assert sum(r['count'] > 0 for r in global_rows) == 1424
    selected = {r['orbit'] for r in anchored_rows if 0 < r['count'] <= 100}
    assert len(selected) == 213
    (work/'selected_cases.txt').write_text(''.join(f'{j}\n' for j in sorted(selected)))
    report['selected'] = run([work/'coverage', 'anchored', work/'orbit_catalog.txt',
                              weights_path, work/'selected.csv',
                              work/'selected_cases.txt', work/'selected_tuples.txt'])
    assert report['selected']['complete'] and report['selected']['packings'] == 5959
    report['residuals'] = prepare_residuals(work, args.jobs)
    assert report['residuals']['distinct_residuals'] == 5959
    fixtures = json.loads((SOURCE/'positive_controls.json').read_text())
    for fixture in fixtures:
        part = fixture['partition_zero_based']
        assert len(part) == 4 and all(len(r) == 10 and sidon(r) for r in part)
        assert sorted(x for r in part for x in r) == fixture['points']
        assert len(set(fixture['points'])) == 40
    (work/'positive_domains.txt').write_text(''.join(
        ' '.join(map(str, f['points'])) + '\n' for f in fixtures))
    report['positive_controls'] = []
    for method in [0, 1]:
        record = run([work/'complete40', method, work/'positive_domains.txt',
                      work/f'positive_{method}.bin', work/f'positive_{method}.jsonl'])
        assert record['complete'] and record['domains'] == record['found'] == 6
        for fixture, line in zip(fixtures, (work/f'positive_{method}.jsonl').read_text().splitlines()):
            part = [[x-1 for x in row] for row in json.loads(line)['partition']]
            assert len(part) == 4 and all(len(r) == 10 and sidon(r) for r in part)
            assert sorted(x for r in part for x in r) == fixture['points']
        report['positive_controls'].append(record)
    assert digest(work/'positive_0.bin') == digest(work/'positive_1.bin')
    def decide(i):
        records = []
        for method in [0, 1]:
            base = work/f'completion_{i}_{method}'
            r = run([work/'complete40', method, work/f'domains_{i}.txt',
                     base.with_suffix('.bin'), base.with_suffix('.jsonl')])
            save(base.with_suffix('.json'), r)
            assert r['complete'] and r['found'] == 0
            records.append(r)
        a, b = records
        assert a['domains'] == b['domains'] and a['ten_sets'] == b['ten_sets']
        assert digest(work/f'completion_{i}_0.bin') == digest(work/f'completion_{i}_1.bin')
        assert (work/f'completion_{i}_0.jsonl').read_bytes() == (work/f'completion_{i}_1.jsonl').read_bytes()
        print(json.dumps({'chunk': i, 'verified': True, 'domains': a['domains']}), flush=True)
        return {'chunk': i, 'methods': records,
                'trace_sha256': digest(work/f'completion_{i}_0.bin'),
                'trace_bytes': (work/f'completion_{i}_0.bin').stat().st_size}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        report['completions'] = list(pool.map(decide, range(args.jobs)))
    assert sum(r['methods'][0]['domains'] for r in report['completions']) == 5959
    assert sum(r['methods'][0]['ten_sets'] for r in report['completions']) == 999039
    with (work/'cases.csv').open('w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(['orbit', 'weight', 'global_packings', 'anchored_packings',
                         'both_orientations', 'reflection_fixed', 'status'])
        for g, a in zip(global_rows, anchored_rows):
            status = 'packing_empty' if a['count'] == 0 else 'cover_excluded' if a['orbit'] in selected else 'unresolved'
            writer.writerow([a['orbit'], a['weight'], g['count'], a['count'],
                             a['both_orientations'], a['reflection_fixed'], status])
    assert (work/'cases.csv').read_bytes() == (SOURCE/'cases.csv').read_bytes()
    for script in ['encode.py']:
        report['global_encoding'] = run([sys.executable, SOURCE/script, '--output', work/'p84_difference.cnf'])
    assert report['global_encoding']['variables'] == 62340
    assert report['global_encoding']['clauses'] == 181236
    if args.sat_checks:
        report['encoding_checks'] = {}
        for script in ['check_encoding.py', 'check_cases.py', 'check_known.py']:
            report['encoding_checks'][script] = run([sys.executable, SOURCE/script])
    report.update({'verified': True, 'global_cases': 1488, 'packing_empty': 64,
                   'cover_excluded': 213, 'unresolved_cases': 1211,
                   'numerical_bound_improved': False, 'seconds': time.monotonic()-start})
    save(work/'verification.json', report)
    print(json.dumps({k: report[k] for k in ['verified', 'unresolved_cases', 'seconds']}))

if __name__ == '__main__':
    main()
