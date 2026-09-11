#!/usr/bin/env python3
"""Replay both stages of 81 <= SR(8) <= 83, then check their interface.

With --check-existing, aggregate completed driver runs without rerunning them.
This mode is an audit of those runs, not a new exhaustive search.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SIDON = HERE.parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def same(a, b):
    with a.open('rb') as f, b.open('rb') as g:
        while True:
            x, y = f.read(1 << 20), g.read(1 << 20)
            require(x == y, f'Files differ: {a}, {b}')
            if not x:
                return


def read_json(path):
    return json.loads(path.read_text())


def sidon(points):
    sums = [x + y for i, x in enumerate(points) for y in points[i:]]
    return len(points) == len(set(points)) and len(sums) == len(set(sums))


def inputs():
    manifest = read_json(HERE / 'source_manifest.json')
    for name, expected in manifest['files'].items():
        require(sha256(ROOT / name) == expected, f'Source/input digest mismatch: {name}')
    witness = SIDON / 'p80_extension_barrier/partition80.txt'
    classes = [list(map(int, line.split())) for line in witness.read_text().splitlines()]
    require(len(classes) == 8 and all(len(a) == 10 and sidon(a) for a in classes),
            'The lower-bound classes are not eight Sidon tens')
    require(sorted(x for a in classes for x in a) == list(range(1, 81)),
            'The lower-bound classes do not partition [80]')
    weights = list(map(int, (SIDON / 'p83_profiles/weights.txt').read_text().split()))
    require(len(weights) == 83 and weights == weights[::-1] and min(weights) >= 0
            and sum(weights) == 31134774 and max(weights) == 444444, 'Invalid weights')
    printed = {}
    for line in (HERE / 'weights_table.tex').read_text().splitlines():
        if re.fullmatch(r'[0-9&]+\\\\', line):
            values = list(map(int, line[:-2].split('&')))
            require(len(values) == 6, 'Malformed printed weight row')
            for point, value in zip(values[::2], values[1::2]):
                require(point not in printed, 'Duplicate printed weight entry')
                printed[point] = value
    require(printed == dict(enumerate(weights[:42])), 'Printed weight table mismatch')
    manuscript = (HERE / 'manuscript.tex').read_text()
    appendix = manuscript.split(r'\section{The known lower-bound partition}', 1)[1]
    table = appendix.split(r'\begin{tabular}{rrrrrrrrrr}', 1)[1].split(r'\end{tabular}', 1)[0]
    printed_classes = [list(map(int, line.strip().rstrip('\\').split('&')))
                       for line in table.splitlines() if '&' in line]
    require(printed_classes == classes, 'Printed lower-bound witness mismatch')
    hash_appendix = manuscript.split(r'\section{Compact artifact identities}', 1)[1]
    fragments = re.findall(r'\\texttt\{([0-9a-f]{20,64})\}', hash_appendix)
    require(len(fragments) == 4, 'Printed digest layout changed')
    for digest, path in zip([fragments[0] + fragments[1], fragments[2] + fragments[3]],
                            [SIDON / 'p83_profiles/cases_three.csv',
                             SIDON / 'p83_exclusion/cases.csv']):
        require(sha256(path) == digest, 'Printed case-ledger digest mismatch')
    return dict(source_manifest_sha256=sha256(HERE / 'source_manifest.json'),
                source_file_count=len(manifest['files']), P80_witness_verified=True,
                printed_weights_witness_and_ledger_digests_verified=True,
                witness_sha256=sha256(witness), weight_sum=sum(weights),
                maximum_point_weight=max(weights))


def driver(command, log):
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    with log.open('w') as f:
        subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, check=True)
    return dict(command=command, log=log.name, started_utc=started,
                seconds=time.monotonic() - start, returncode=0)


def aggregate(work):
    p, e = work / 'profiles', work / 'exclusion'
    pr, er = read_json(p / 'verification.json'), read_json(e / 'verification.json')
    pe = read_json(SIDON / 'p83_profiles/expected.json')
    ee = read_json(SIDON / 'p83_exclusion/expected.json')
    require(pr['verified'] is True and er['verified'] is True, 'A stage did not verify')
    require(pr['profile_only'] is True and er['imported_p83_profile'] is True,
            'Unexpected proof-stage scopes')
    require(pr['landscape']['only_remaining_profile'] == ee['imported_profile'],
            'Profile/completion interface mismatch')
    for key in ['eleven', 'eleven_reference', 'twelve', 'twelve_reference']:
        require(pr[key]['complete'] is True, f'Incomplete enumeration: {key}')
    require(pr['eleven']['sets'] == pr['eleven_reference']['sets'] == 15958
            and pr['twelve']['sets'] == pr['twelve_reference']['sets'] == 0,
            'Unexpected class catalog counts')
    require(all(r['complete'] and r['packings'] == 2142
                for r in [pr['five_packing'], pr['five_reference']]), 'Five-tuple cover')
    require(all(r['complete'] and r['domains'] == 2142 and r['found'] == 0
                for r in pr['five_completion']), 'Five-tuple completions')
    require(all(r['complete'] and r['found'] == 0 for r in pr['four_sweeps']),
            'Four-eleven completion')
    require(pr['terminal_occurrences'] == 380 and er['terminal_occurrences'] == 1771,
            'Terminal counts')
    require(er['totals'] == ee['totals'] and er['cases'] == 5364
            and er['nonempty_cases'] == 5157 and er['complete_query_traces_bytewise_equal']
            and er['case_records_equal'] and er['P80_witness_verified'], 'Balanced completion')
    require(all(r['complete'] and r['domains'] == 1754 and r['ten_sets'] == 4040
                and r['found'] == 0 for r in er['terminal20_direct_checks']), 'Two-ten audit')
    require(all(k in pr for k in ['sanitizer28', 'sanitizer39'])
            and all(k in er for k in ['sanitizer_controls', 'sanitizer20']),
            'Both complete replays must include sanitizer controls')
    shared = {}
    for a, b in [('raw11.txt', 'raw11.txt'), ('orbit11.txt', 'orbit11.txt'),
                 ('full_0.bin', 'catalog_full_0.bin'), ('heavy_0.bin', 'catalog_heavy_0.bin')]:
        same(p / a, e / b)
        shared[a] = sha256(p / a)
    require(shared['full_0.bin'] == pr['ten_catalogs'][0]['full_sha256']
            == er['catalogs'][0]['full_sha256'], 'Full catalog record mismatch')
    require(shared['heavy_0.bin'] == pr['ten_catalogs'][0]['heavy_sha256']
            == er['catalogs'][0]['heavy_sha256'], 'Heavy catalog record mismatch')
    for catalogs in [pr['ten_catalogs'], er['catalogs']]:
        require(len(catalogs) == 2 and all(r['generation']['complete']
                    and r['generation']['sets'] == 24751806
                    and r['generation']['max_weight'] == 3999980
                    and r['filter']['kept'] == 4832138
                    and r['filter']['cutoff'] == 3567387 for r in catalogs),
                'Unexpected ten catalog')
    rows_p = list(csv.DictReader((p / 'cases_three.csv').open()))
    rows_e = list(csv.DictReader((e / 'cases.csv').open()))
    require(len(rows_p) == len(rows_e) == 5364, 'Incomplete case interface')
    require([int(r['orbit']) for r in rows_p] == list(range(5364)), 'Anchor coverage')
    require(all(a['orbit'] == b['orbit'] and a['packings'] == b['packings']
                for a, b in zip(rows_p, rows_e)), 'Case-by-case interface mismatch')
    require(sum(int(r['packings']) for r in rows_p) == 65073232, 'Triple cover count')
    four = list(csv.DictReader((p / 'cases_four.csv').open()))
    require([int(r['orbit']) for r in four] == list(range(2701)), 'Four-anchor coverage')
    require({k: sum(int(r[k]) for r in four) for k in pe['four_totals']}
            == pe['four_totals'], 'Four-eleven totals')
    artifacts = {}
    for path, record_key in [(p / 'all_terminals.json', 'all_terminals_sha256'),
                              (e / 'all_terminals.json', 'all_terminals_sha256')]:
        require(sha256(path) == (pr if path.parent == p else er)[record_key], 'Terminal digest')
    for base, names in [(p, ['verification.json', 'cases_three.csv', 'cases_four.csv',
                             'all_terminals.json']),
                        (e, ['verification.json', 'cases.csv', 'all_terminals.json'])]:
        for name in names:
            path = base / name
            artifacts[str(path.relative_to(work))] = sha256(path)
    # The committed ledgers are reproducibility controls, not a replacement for traversal.
    for base, relative, names in [(p, 'p83_profiles', ['cases_three.csv', 'cases_four.csv']),
                                  (e, 'p83_exclusion', ['cases.csv'])]:
        for name in names:
            same(base / name, SIDON / relative / name)
    return dict(verified=True, numerical_conclusion='81 <= SR(8) <= 83',
                upper_bound_scope='All partitions of [83] into eight Sidon classes',
                exact_SR8_determined=False, interface_cases=5364,
                anchored_triples=65073232, shared_files_bytewise_equal=True,
                shared_file_sha256=shared, artifact_sha256=artifacts,
                stage_seconds=dict(profiles=pr['seconds'], exclusion=er['seconds']),
                compiler=dict(profiles=pr['compiler'], exclusion=er['compiler']),
                python=dict(profiles=pr['python'], exclusion=er['python']))


def main():
    require(__debug__, 'Do not use Python -O or PYTHONOPTIMIZE: driver assertions are proof checks')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check-existing', action='store_true')
    mode.add_argument('--check-inputs', action='store_true')
    parser.add_argument('--profiles-jobs', type=int, default=4)
    parser.add_argument('--exclusion-jobs', type=int, default=6)
    parser.add_argument('--exclusion-workers', type=int, default=6)
    args = parser.parse_args()
    initial = inputs()
    if args.check_inputs:
        print(json.dumps(dict(**initial, scope='Inputs only; no upper-bound replay'), indent=2))
        return
    require(args.work is not None, '--work is required')
    work = args.work.resolve()
    require(ROOT not in [work, *work.parents], 'Use a work directory outside the repository')
    for value in [args.profiles_jobs, args.exclusion_jobs, args.exclusion_workers]:
        require(1 <= value <= 12, 'Parallelism must be between 1 and 12')
    commands = []
    started = datetime.now(timezone.utc).isoformat()
    if not args.check_existing:
        require(not work.exists(), 'Fresh mode requires a new work directory')
        work.mkdir(parents=True)
        specifications = [('p83_profiles', 'profiles', ['--jobs', str(args.profiles_jobs)]),
                          ('p83_exclusion', 'exclusion', ['--jobs', str(args.exclusion_jobs),
                                                        '--workers', str(args.exclusion_workers)])]
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(driver, [sys.executable, str(SIDON / source / 'reproduce.py'),
                        '--work', str(work / stage), '--sanitizers', *options],
                        work / (stage + '.log')) for source, stage, options in specifications]
            commands = [future.result() for future in futures]
    result = aggregate(work)
    require(inputs() == initial, 'Source/input set changed during verification')
    result.update(initial)
    result.update(started_utc=started, finished_utc=datetime.now(timezone.utc).isoformat(),
                  mode='aggregate_existing_completed_runs' if args.check_existing else 'fresh_full_replay',
                  commands_launched_by_this_invocation=commands,
                  trust_boundary='Exact integer programs and coverage reductions; compiler/runtime/hardware trusted. No formal proof assistant.')
    (work / 'paper_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
