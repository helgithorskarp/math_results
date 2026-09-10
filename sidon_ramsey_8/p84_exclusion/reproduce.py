#!/usr/bin/env python3
"""Regenerate and cross-check the complete balanced P84 exclusion."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parent
PARENT = SOURCE.parent
sys.path.insert(0, str(PARENT / 'p84_global_cases'))
from orbits import orbit_catalog

EXPECTED = dict(packings=62861452, calls1=2, calls2=11698, calls3=4048536,
                calls4=62861452, candidates1=0, candidates2=2,
                candidates3=11698, candidates4=4048536, found=0)

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def same(a, b):
    with a.open('rb') as x, b.open('rb') as y:
        while True:
            p, q = x.read(1 << 20), y.read(1 << 20)
            assert p == q, (a, b)
            if not p:
                return

def run(args):
    result = subprocess.run(list(map(str, args)), capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def build(source, target, sanitize=False):
    flags = ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer'] if sanitize else ['-O3']
    subprocess.run(['g++', '-std=c++20', '-Wall', '-Wextra', '-Wconversion', '-Wshadow', '-Werror',
                    *flags, str(source), '-o', str(target)], check=True)

def sidon(row):
    sums = [a + b for i, a in enumerate(row) for b in row[i:]]
    return len(sums) == len(set(sums))

def collision(row):
    seen = {}
    for i, a in enumerate(row):
        for b in row[i:]:
            s = a + b
            if s in seen:
                return [seen[s], [a, b]]
            seen[s] = [a, b]
    return None

def mask(row):
    return sum(1 << x for x in row)

def check_partition(domain, answer, size):
    assert all(len(row) == size and sidon(row) for row in answer)
    points = [x for row in answer for x in row]
    assert len(points) == len(set(points)) and set(points) == set(domain)

def small_controls(program, work):
    weights = [(17*x*x + 13*x + 5) % 997 for x in range(84)]
    wp = work / 'small_weights.txt'
    wp.write_text(' '.join(map(str, weights)) + '\n')
    reports = []
    for size, totals in [(3, [3, 6, 9, 12]), (4, [4, 8, 12])]:
        family = sorted((tuple(row) for row in combinations(range(12), size) if sidon(row)), key=mask)
        catalog = work / f'small_{size}.bin'
        catalog.write_bytes(bytes(x for row in family for x in row))
        fm = [mask(row) for row in family]
        @lru_cache(None)
        def exact(r):
            if not r:
                return True
            p = r & -r
            return any(a & p and a & r == a and exact(r ^ a) for a in fm)
        domains = [row for n in totals for row in combinations(range(12), n)]
        dp = work / f'small_domains_{size}.txt'
        dp.write_text(''.join(' '.join(map(str, row)) + '\n' for row in domains))
        expected = [exact(mask(row)) for row in domains]
        assert any(expected) and not all(expected)
        for method in [0, 1]:
            out = work / f'small_answers_{size}_{method}.jsonl'
            report = run([program, 'control', method, wp, catalog, size, dp, out])
            answers = [json.loads(line) for line in out.read_text().splitlines()]
            assert report['complete'] and len(answers) == len(domains) == report['domains']
            assert [row['found'] for row in answers] == expected
            for domain, answer in zip(domains, answers):
                if answer['found']:
                    check_partition(domain, answer['partition'], size)
            reports.append(dict(size=size, method=method, domains=len(domains),
                                positive=sum(expected), negative=len(expected)-sum(expected)))
        bad = work / f'bad_{size}.bin'
        bad.write_bytes(catalog.read_bytes() + catalog.read_bytes()[:size])
        result = subprocess.run(list(map(str, [program, 'control', 0, wp, bad, size, dp, work/'bad.jsonl'])),
                                capture_output=True, text=True)
        assert result.returncode != 0 and 'catalog' in result.stderr
    return reports

def positive_controls(program, generator, work, wp):
    seed = [[18,20,32,39,47,50,63,67,72,73], [11,12,17,21,34,37,45,52,64,66],
            [8,10,19,25,26,46,49,54,68,80], [6,9,16,27,35,40,60,62,76,77]]
    reports = []
    for shift in [0, 4]:
        classes = [[x-1+shift for x in row] for row in seed]
        domain = sorted(x for row in classes for x in row)
        check_partition(domain, classes, 10)
        dp = work/f'positive_{shift}.txt'; dp.write_text(' '.join(map(str, domain))+'\n')
        catalog = work/f'positive_{shift}.bin'
        generation = run([generator, 0, dp, catalog, 10, wp])
        for method in [0, 1]:
            out = work/f'positive_{shift}_{method}.jsonl'
            record = run([program, 'control', method, wp, catalog, 10, dp, out])
            answer = json.loads(out.read_text())
            assert record['complete'] and answer['found']
            check_partition(domain, answer['partition'], 10)
            reports.append(dict(shift=shift, method=method, ten_sets=generation['sets'], verified=True))
    return reports

def main():
    if not __debug__:
        raise SystemExit('Run without -O/PYTHONOPTIMIZE: assertions are proof checks.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--sanitizers', action='store_true')
    args = parser.parse_args()
    work = args.work.resolve()
    assert PARENT not in [work, *work.parents] and 1 <= args.jobs <= 12
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic(); reports = {}
    wp = PARENT/'p84_profiles/weights.txt'
    weights = list(map(int, wp.read_text().split()))
    assert len(weights) == 84 and sum(weights) == 15685948 and weights == weights[::-1]
    for source, target in [(SOURCE/'exclude.cpp', 'exclude'),
                           (PARENT/'p84_weight_certificates/weighted_catalog.cpp', 'catalog'),
                           (PARENT/'enumerate.cpp', 'enumerate'),
                           (PARENT/'p84_global_cases/complete40.cpp', 'complete40')]:
        build(source, work/target)
    reports['small_controls'] = small_controls(work/'exclude', work)
    reports['positive_controls'] = positive_controls(work/'exclude', work/'catalog', work, wp)
    if args.sanitizers:
        build(SOURCE/'exclude.cpp', work/'exclude_sanitized', True)
        reports['sanitizer_controls'] = small_controls(work/'exclude_sanitized', work)
    print('Control checks passed; regenerating full catalogs.', flush=True)
    reports['eleven_catalog'] = run([work/'enumerate', 84, 11, 'all', work/'sets84_11.txt', wp])
    assert reports['eleven_catalog']['sets'] == 30510 and reports['eleven_catalog']['max_weight'] == 1999990
    assert digest(work/'sets84_11.txt') == 'e1541890c78cb206076fbcd6067b2da24884b044f902c1c03ffc0da7ccdc0720'
    raw = [list(map(int, line.split())) for line in (work/'sets84_11.txt').read_text().splitlines()]
    ordered = orbit_catalog(raw, weights)
    (work/'orbit_catalog.txt').write_text(''.join(' '.join(map(str, row))+'\n' for row in ordered))
    assert digest(work/'orbit_catalog.txt') == '4cdac43dae88dfde56506152b01fce145bf2a7e878b486933f11b0c3dba4e3df'
    (work/'domain84.txt').write_text(' '.join(map(str, range(84)))+'\n')
    def catalogs(method):
        full, heavy = work/f'full_{method}.bin', work/f'heavy_{method}.bin'
        record = run([work/'catalog', method, work/'domain84.txt', full, 10, wp])
        assert record['complete'] and record['sets'] == 35250764 and record['max_weight'] == 1999990
        filtered = run([work/'exclude', 'filter', wp, full, heavy])
        assert filtered == dict(sets=35250764, kept=901286, cutoff=1842974, maximum=1999990, complete=True)
        return dict(generation=record, filter=filtered, full_sha256=digest(full), heavy_sha256=digest(heavy))
    with ThreadPoolExecutor(max_workers=min(2, args.jobs)) as pool:
        reports['ten_catalogs'] = list(pool.map(catalogs, [0, 1]))
    same(work/'full_0.bin', work/'full_1.bin'); same(work/'heavy_0.bin', work/'heavy_1.bin')
    print('Both full ten catalogs match bytewise; starting complete sweeps.', flush=True)
    def sweep(task):
        method, shard = task
        prefix = work/f'sweep_{method}_{shard}'
        marker = prefix.with_suffix('.done')
        if marker.exists(): marker.unlink()
        cmd = [work/'exclude', method, work/'orbit_catalog.txt', wp, work/f'heavy_{method}.bin',
               shard, args.jobs, prefix.with_suffix('.csv'), prefix.with_suffix('.bin'),
               prefix.with_suffix('.jsonl'), marker]
        record = run(cmd)
        assert record['complete'] and record['found'] == 0 and marker.read_text() == 'complete\n'
        record.update(shard=shard, parts=args.jobs, trace_sha256=digest(prefix.with_suffix('.bin')),
                      trace_bytes=prefix.with_suffix('.bin').stat().st_size)
        prefix.with_suffix('.record.json').write_text(json.dumps(record, indent=2)+'\n')
        print(f'Completed method {method}, shard {shard}: {record["packings"]} packings.', flush=True)
        return record
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        reports['sweeps'] = list(pool.map(sweep, [(m,s) for m in [0,1] for s in range(args.jobs)]))
    records = []
    for method in [0,1]:
        rows = []
        for shard in range(args.jobs):
            with (work/f'sweep_{method}_{shard}.csv').open() as stream:
                rows += [{key:int(value) for key,value in row.items()} for row in csv.DictReader(stream)]
        rows.sort(key=lambda row:row['orbit'])
        assert [row['orbit'] for row in rows] == list(range(1488))
        totals = {key:sum(row[key] for row in rows) for key in EXPECTED}
        assert totals == EXPECTED, totals
        records.append(rows)
    assert records[0] == records[1]
    prior = list(csv.DictReader((PARENT/'p84_global_cases/cases.csv').open()))
    assert all(row['packings'] == int(old['anchored_packings']) for row,old in zip(records[0],prior))
    for shard in range(args.jobs):
        same(work/f'sweep_0_{shard}.bin', work/f'sweep_1_{shard}.bin')
        same(work/f'sweep_0_{shard}.jsonl', work/f'sweep_1_{shard}.jsonl')
    casepath = work/'cases.csv'
    with casepath.open('w') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(records[0][0]),lineterminator='\n')
        writer.writeheader();writer.writerows(records[0])
    terminals=[]
    for shard in range(args.jobs):
        terminals += [json.loads(line) for line in (work/f'sweep_0_{shard}.jsonl').read_text().splitlines()]
    terminals.sort(key=lambda row:row['eleven_ids'])
    assert len(terminals)==2
    full_domains=[]
    for term in terminals:
        large=[ordered[i] for i in term['eleven_ids']]
        small=term['chosen_tens']; residual=term['residual']
        points=[x for row in [*large,*small,residual] for x in row]
        assert sorted(points)==list(range(84)) and len(set(points))==84
        assert all(len(a)==11 and sidon(a) for a in large)
        assert all(len(a)==10 and sidon(a) for a in small)
        assert len(residual)==10 and not sidon(residual) and not term['sidon']
        tw=[sum(weights[x] for x in a) for a in [*small,residual]]
        assert tw==sorted(tw,reverse=True)
        term['ten_weights']=tw;term['collision']=collision(residual)
        assert sum(term['collision'][0])==sum(term['collision'][1])
        full_domains.append(sorted(set(range(84))-set(x for row in large for x in row)))
    (work/'terminal_domains.txt').write_text(''.join(' '.join(map(str,row))+'\n' for row in full_domains))
    reports['terminal_direct_checks']=[]
    for method in [0,1]:
        record=run([work/'complete40',method,work/'terminal_domains.txt',work/f'direct_{method}.bin',work/f'direct_{method}.jsonl'])
        assert record['complete'] and record['domains']==2 and record['found']==0
        reports['terminal_direct_checks'].append(record)
    same(work/'direct_0.bin',work/'direct_1.bin');same(work/'direct_0.jsonl',work/'direct_1.jsonl')
    (work/'terminal_checks.json').write_text(json.dumps(terminals,indent=2)+'\n')
    if (SOURCE/'cases.csv').exists():same(casepath,SOURCE/'cases.csv')
    if (SOURCE/'terminal_checks.json').exists():same(work/'terminal_checks.json',SOURCE/'terminal_checks.json')
    reports.update(verified=True, totals=EXPECTED, cases=1488, complete_catalogs_bytewise_equal=True,
                   nonempty_query_traces_bytewise_equal=True, case_records_equal=True,
                   cases_sha256=digest(casepath), terminal_checks_sha256=digest(work/'terminal_checks.json'),
                   compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],
                   python=sys.version, jobs=args.jobs, seconds=time.monotonic()-start,
                   child_max_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   numerical_conclusion='81 <= SR(8) <= 84', imported_profile_theorem=True)
    (work/'verification.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps(dict(verified=True,packings=EXPECTED['packings'],found=0,seconds=reports['seconds'])))

if __name__=='__main__':main()
