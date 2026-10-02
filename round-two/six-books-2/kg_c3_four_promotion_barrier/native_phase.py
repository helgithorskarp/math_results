"""Run one bounded p=4 labeled-case phase; save exact completion boundaries."""
from collections import Counter
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import literal
import model


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    work = Path(sys.argv[1]).resolve()
    phase_limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    need(0 < phase_limit <= 50000, 'phase limit')
    work.mkdir(parents=True, exist_ok=True)
    for name in ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json'):
        need(not (Path('/scratch/research-team-sol61-six-20260929/state') / name).exists(), 'pause/handover barrier')
    need(not (work / 'operational-limit.json').exists(), 'previous operational limit; do not blindly resume')
    sources = {p.name: digest(p) for p in (HERE / 'native.cpp', Path(__file__))}
    plan_path = work / 'plan.json'
    if plan_path.exists():
        plan = json.loads(plan_path.read_text())
        need(plan['sources'] == sources, 'source hash drift')
    else:
        plan = dict(sources=sources, total=1832600, threads=1, phase_seconds=25, child_deadline_seconds=30,
                    family='KG(7,2), ground(012)(345), J3, P4, arbitrary original-red deletion subsets')
        plan_path.write_text(json.dumps(plan, indent=2) + '\n')
        env = dict(os.environ)
        env.update({name: '1' for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                                        'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')})
        args = ['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion',
                '-Wshadow', str(HERE / 'native.cpp'), '-o', str(work / 'native')]
        result = subprocess.run(args, capture_output=True, text=True, env=env, timeout=30)
        (work / 'compile.stdout').write_text(result.stdout)
        (work / 'compile.stderr').write_text(result.stderr)
        result.check_returncode()
        need(not result.stderr, 'compiler warning')
        plan['binary_sha256'] = digest(work / 'native')
        plan_path.write_text(json.dumps(plan, indent=2) + '\n')
    need(digest(work / 'native') == plan['binary_sha256'], 'binary hash drift')
    first = 0
    for old in sorted(work.glob('native-*.jsonl')):
        items = [json.loads(line) for line in old.read_text().splitlines()]
        footer = items.pop()
        need(footer.get('segment') is True and footer['first'] == first and
             footer['next'] - first == len(items), 'completed prefix boundary')
        need([x['index'] for x in items] == list(range(first, footer['next'])), 'completed prefix indices')
        first = footer['next']
    need(first < plan['total'], 'all cases already completed')
    stem = f'native-{first:07d}'
    out_path = work / (stem + '.jsonl')
    need(not out_path.exists(), 'phase output already exists')
    args = [str(work / 'native'), '--first', str(first), '--seconds', '25', '--limit', str(phase_limit)]
    started = time.monotonic()
    try:
        with out_path.open('w') as out, (work / (stem + '.stderr')).open('w') as err:
            subprocess.run(args, stdout=out, stderr=err, timeout=30, check=True)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as error:
        (work / 'operational-limit.json').write_text(json.dumps(dict(status='INCOMPLETE', first=first,
            error=str(error), deadline_seconds=30, mathematical_nonexistence=False), indent=2) + '\n')
        raise
    items = [json.loads(line) for line in out_path.read_text().splitlines()]
    footer = items.pop()
    need(footer.get('segment') is True and footer['first'] == first and
         footer['next'] - first == len(items) and footer['total'] == plan['total'], 'phase boundary')
    joins = list(combinations(range(7), 3))
    promotions = list(combinations(range(35), 4))
    need(len(joins) * len(promotions) == plan['total'], 'Python product domain')
    hist = {8: Counter(), 9: Counter()}
    minima = {}
    controls = []
    pools = Counter()
    attempted, good = [0] * 10, [0] * 10
    native = literal.geometry()
    for index, item in enumerate(items, first):
        need(item['index'] == index and tuple(item['joins']) == joins[index // 52360]
             and tuple(item['promotions']) == promotions[index % 52360], 'literal labeled product index')
        pools[len(item['pool'])] += 1
        for depth in range(10):
            attempted[depth] += item['attempted'][depth]
            good[depth] += item['good'][depth]
        for q in (8, 9):
            for target in item['targets'][str(q)]:
                D = target['D']
                need(len(D) == q and D == sorted(set(D)) and all(d in item['pool'] for d in D), 'terminal deletion domain')
                hist[q][target['red_bad']] += 1
                if q not in minima or target['red_bad'] < minima[q]['red_bad'] or target['red_bad'] == 0:
                    rows = literal.rows(native, item['joins'], item['promotions'], D)
                    summary = model.literal_summary(rows)
                    bad = sum(v[2] == 'red' for v in summary['violations'])
                    need(not any(v[2] == 'blue' for v in summary['violations']) and bad == target['red_bad'], 'literal candidate caps')
                    need(summary['edges'] == 126 - 3*q and summary['degrees'][21] == 9, 'literal candidate size')
                    control = dict(index=index, J=item['joins'], P=item['promotions'], D=D,
                        red_bad=bad, degree_valid=all(7 <= d <= 10 for d in summary['degrees']),
                        edges=summary['edges'], degrees=summary['degrees'], red_pages=summary['red_pages'],
                        blue_pages=summary['blue_pages'], rows=[sum(1 << v for v in row) for row in rows])
                    controls.append(control)
                    minima[q] = control
    report = dict(status='COMPLETED_CASE_PREFIX_ONLY', first=first, next=footer['next'], total=plan['total'],
        case_records=len(items), program_seconds=footer['seconds'], wall_seconds=time.monotonic()-started,
        peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        attempted=attempted, good=good, pool_hist=dict(sorted(pools.items())),
        terminal_red_hist={q: dict(sorted(v.items())) for q, v in hist.items()}, minima=minima,
        literal_controls=len(controls), output_sha256=digest(out_path), output_bytes=out_path.stat().st_size,
        source_hashes=sources, scope='No all-p4 exclusion or completeness claim; one exact native algorithm, minimum controls independently reconstructed.')
    (work / (stem + '.summary.json')).write_text(json.dumps(report, indent=2) + '\n')
    (work / (stem + '.controls.json')).write_text(json.dumps(controls, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
