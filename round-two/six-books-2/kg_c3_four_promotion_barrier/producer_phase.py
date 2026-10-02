"""Run one bounded pair-clique phase, literally checking every blue positive."""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE
sys.path.insert(0, str(PREVIOUS))
import literal
import model as m


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    work = Path(sys.argv[1]).resolve()
    phase_limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    m.need(0 < phase_limit <= 50000, 'phase limit')
    for name in ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json'):
        m.need(not (Path('/scratch/research-team-sol61-six-20260929/state')/name).exists(), 'pause/handover barrier')
    m.need(not (work/'operational-limit.json').exists(), 'existing operational limit')
    manifest = json.loads((work/'cases.json').read_text())
    m.need(manifest['status'] == 'COMPLETE_EXPLICIT_CASE_QUOTIENT'
           and digest(work/'cases.txt') == manifest['manifest_sha256'], 'complete case inventory')
    sources = {p.name:digest(p) for p in (HERE/'produce.cpp', Path(__file__),
                                         PREVIOUS/'model.py', PREVIOUS/'literal.py')}
    plan_path = work/'producer-plan.json'
    env = dict(os.environ)
    env.update({k:'1' for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')})
    if plan_path.exists():
        plan = json.loads(plan_path.read_text())
        m.need(plan['sources'] == sources and plan['manifest_sha256'] == manifest['manifest_sha256'], 'resume input/source drift')
    else:
        result = subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow',
            str(HERE/'produce.cpp'),'-o',str(work/'produce')], capture_output=True,text=True,env=env,timeout=30)
        (work/'compile.stdout').write_text(result.stdout);(work/'compile.stderr').write_text(result.stderr)
        result.check_returncode();m.need(not result.stderr, 'strict compiler warning')
        plan = dict(sources=sources,manifest_sha256=manifest['manifest_sha256'],total=manifest['representatives'],
                    binary_sha256=digest(work/'produce'),phase_seconds=25,child_deadline_seconds=30,threads=1)
        plan_path.write_text(json.dumps(plan,indent=2)+'\n')
    m.need(digest(work/'produce') == plan['binary_sha256'], 'binary drift')
    first = 0
    for path in sorted(work.glob('producer-*.jsonl')):
        items = [json.loads(line) for line in path.read_text().splitlines()]
        footer = items.pop()
        m.need(footer.get('segment') is True and footer['first'] == first and
               len(items) == footer['next']-first and footer['total'] == plan['total'], 'previous phase boundary')
        m.need([x['index'] for x in items] == list(range(first,footer['next'])), 'previous phase index coverage')
        m.need(path.with_suffix('.summary.json').exists(), 'previous phase literal checking unfinished')
        first = footer['next']
    m.need(first < plan['total'], 'producer already complete')
    stem = f'producer-{first:06d}'
    output = work/(stem+'.jsonl')
    critical = work/(f'critical-{first:06d}.txt')
    m.need(not output.exists() and not critical.exists(), 'refuse overwrite')
    started = time.monotonic()
    try:
        with output.open('w') as out,(work/(stem+'.stderr')).open('w') as err:
            subprocess.run([str(work/'produce'),'--manifest',str(work/'cases.txt'),'--critical',str(critical),
                '--first',str(first),'--limit',str(phase_limit),'--seconds','25'],env=env,stdout=out,stderr=err,check=True,timeout=30)
    except (subprocess.TimeoutExpired,subprocess.CalledProcessError) as error:
        (work/'operational-limit.json').write_text(json.dumps(dict(status='INCOMPLETE_PRODUCER',first=first,
            error=str(error),deadline_seconds=30,mathematical_nonexistence=False),indent=2)+'\n')
        raise
    records = [json.loads(line) for line in output.read_text().splitlines()]
    boundary = records.pop()
    m.need(boundary.get('segment') is True and boundary['first'] == first and
           boundary['next']-first == len(records) and boundary['total'] == plan['total'], 'new phase boundary')
    cases = [tuple(map(int,line.split())) for line in (work/'cases.txt').read_text().splitlines()]
    m.need(len(cases) == plan['total'], 'manifest count')
    counts = {q:Counter() for q in (8,9)}
    hist = {q:Counter() for q in (8,9)}
    weighted_hist = {q:Counter() for q in (8,9)}
    degree_hist = {q:Counter() for q in (8,9)}
    critical_counts = Counter()
    positive_counts = Counter()
    positive_degree = Counter()
    native = literal.geometry()
    minima = {}
    positive_path = work/(f'positive-{first:06d}.jsonl')
    with critical.open() as stream,positive_path.open('w') as good_out:
        for line in stream:
            fields = tuple(map(int,line.split()))
            index,q,blue = fields[:3]
            m.need(first <= index < boundary['next'] and q in (8,9) and len(fields) == 3+q
                   and blue == 1, 'positive-only domain')
            critical_counts[index,q] += 1
            if not blue:
                continue
            D = fields[3:]
            m.need(tuple(sorted(set(D))) == D, 'ordered deletion subset')
            case = cases[index]
            m.need(case[0] == index and len(case) == 9, 'case identity')
            J,P,weight = case[1:4],case[4:8],case[8]
            ground_rows = literal.rows(native,J,P,D)
            result = m.literal_summary(ground_rows)
            m.need(not any(v[2] == 'blue' for v in result['violations']), 'literal blue cap')
            bad = sum(v[2] == 'red' for v in result['violations'])
            degrees = all(7 <= d <= 10 for d in result['degrees'])
            m.need(result['edges'] == 126-3*q and result['degrees'][21] == 9, 'literal edge/root')
            positive_counts[index,q] += 1
            positive_degree[index,q] += degrees
            hist[q][bad] += 1
            weighted_hist[q][bad] += weight
            shape = tuple(sorted(Counter(result['degrees']).items()))
            degree_hist[q][str(shape)] += 1
            entry = dict(index=index,J=J,P=P,D=D,weight=weight,red_bad=bad,degrees=degrees,
                         degree_sequence=result['degrees'],red_pages=result['red_pages'],blue_pages=result['blue_pages'])
            good_out.write(json.dumps(entry,separators=(',',':'))+'\n')
            if q not in minima or bad < minima[q]['red_bad']:
                minima[q] = entry
    for index,item in enumerate(records,first):
        m.need(item['index'] == index and item['weight'] == cases[index][8], 'consecutive producer case/weight')
        for q in (8,9):
            target = item['targets'][str(q)]
            m.need(target['blue_valid'] == critical_counts[index,q] and target['blue_valid'] == positive_counts[index,q]
                   and target['degree_valid'] == positive_degree[index,q], 'critical/literal aggregate agreement')
            for key in ('cliques','blue_valid','degree_valid','two_color_valid'):
                counts[q][key] += target[key]
                counts[q]['weighted_'+key] += item['weight']*target[key]
    report = dict(status='COMPLETE_PRODUCER' if boundary['next'] == plan['total'] else 'CHECKED_PRODUCER_PREFIX',
        first=first,next=boundary['next'],total=plan['total'],boundary=boundary,
        counts={q:dict(v) for q,v in counts.items()},red_hist={q:dict(sorted(v.items())) for q,v in hist.items()},
        weighted_red_hist={q:dict(sorted(v.items())) for q,v in weighted_hist.items()},
        degree_hist={q:dict(v) for q,v in degree_hist.items()},minima=minima,
        seconds=time.monotonic()-started,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        peak_parent_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        output_sha256=digest(output),critical_sha256=digest(critical),positive_sha256=digest(positive_path),
        critical_bytes=critical.stat().st_size,positive_records=sum(positive_counts.values()),
        scope='Case quotient/pair-clique algorithm plus literal every-positive checks; independent full native census still required.')
    output.with_suffix('.summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
