"""Cold complete independent audit. Artifacts stay in the requested work dir."""
from pathlib import Path
from itertools import combinations, permutations, product
from collections import Counter
from hashlib import sha256
import argparse, json, os, resource, subprocess, time
from carrier import build, points, write_native
from incidence import need
from literal import solve


def matrix_census(models):
    rows = tuple(combinations(range(5), 3))
    actual = set()
    for rr in product(rows, repeat=5):
        if all(sum(j in r for r in rr) == 3 for j in range(5)):
            actual.add(tuple((i, j) for i, r in enumerate(rr) for j in r))
    need(len(actual) == 2040, 'matrix census mismatch')
    unions = set(); masses = []
    for m in models:
        orbit = {tuple(sorted((a[i], b[j]) for i, j in m['cells']))
                 for a in permutations(range(5)) for b in permutations(range(5))}
        need(orbit <= actual and not unions & orbit, 'matrix orbit false/overlap')
        unions.update(orbit); masses.append(len(orbit))
    need(unions == actual, 'incomplete anchor matrix normalization')
    return dict(binary_degree_three_matrices=len(actual), row_column_orbit_masses=masses)


def literal_input(m, case):
    h = frozenset(points(case['high'], 15)); low = frozenset(range(15))-h
    edge = tuple(points(case['low_edge'], 15))
    need(len(h) == 5 and (len(edge) == 2 if case['extra'] else len(edge) == 0), 'bad normalized high/low mask')
    covered = set()
    for w in m['anchors']:
        pp = set(combinations(tuple(z for z in points(w) if z < 15), 2))
        need(not covered & pp, 'literal anchor pair overlap'); covered.update(pp)
    need(not edge or set(edge) <= low and edge not in covered, 'bad selected low-low leave')
    budget = 5-case['extra']-sum(set(p) <= h for p in covered)
    mandatory = set(combinations(sorted(low), 2))-covered-({edge} if edge else set())
    cols = tuple(c for c in combinations(range(15), 4)
                 if not set(combinations(c, 2)) & covered
                 and (not edge or not set(edge) <= set(c))
                 and len(set(c)&h)*(len(set(c)&h)-1)//2 <= budget)
    need(set(cols) == {points(w, 15) for w in case['columns']}, 'literal/native column input mismatch')
    pp = tuple(combinations(range(15), 2))
    decoded = {p for i, p in enumerate(pp) if case['mandatory'] >> i & 1}
    need(mandatory == decoded and budget == case['budget'], 'literal/native row/budget mismatch')
    q = tuple(2 if z in h else 3 for z in range(15))
    need(q == case['quotas'], 'literal/native quota mismatch')
    return cols, q, mandatory, h, budget


def native_results(path, cases):
    lines = path.read_text().splitlines()
    need(len(lines) == len(cases), 'incomplete native output')
    result = []
    for i, (line, c) in enumerate(zip(lines, cases)):
        rr = tuple(map(int, line.split()))
        need(len(rr) >= 4 and rr[0] == i and rr[1] in (0, 1) and 0 < rr[2] <= 200000 and len(rr) == 4+rr[3], 'malformed native result')
        need(rr[1] == 0 and rr[3] == 0, 'positive native completion: mathematical exclusion fails')
        result.append(rr[2])
    return result


def main():
    ap = argparse.ArgumentParser();ap.add_argument('--work-dir', required=True)
    ap.add_argument('--expected');args = ap.parse_args()
    source = Path(__file__).resolve().parent;work = Path(args.work_dir).resolve();work.mkdir(parents=True, exist_ok=True)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
        os.environ[name] = '1'
    started = time.monotonic()
    models, cases, carrier = build()
    print(json.dumps(dict(stage='carrier', **carrier)), flush=True)
    matrix = matrix_census(models)
    binary = work/'quota';flags = ['-std=c++17','-O2','-Wall','-Wextra','-Wconversion']
    subprocess.run(['g++',*flags,str(source/'quota.cpp'),'-o',str(binary)], check=True, timeout=60)
    nativein = work/'cases.txt';nativeout = work/'native.txt';write_native(cases, nativein)
    st = time.monotonic();subprocess.run([str(binary),str(nativein),str(nativeout)],check=True,timeout=300)
    native_seconds = time.monotonic()-st; native = native_results(nativeout, cases)
    print(json.dumps(dict(stage='native complete', cases=len(cases), nodes=sum(native), max_nodes=max(native))), flush=True)
    groups = {}
    literal_states = []
    for i, c in enumerate(cases):
        cols, q, mandatory, h, budget = literal_input(models[c['model']], c)
        result = solve(cols, q, mandatory, h, budget)
        need(not result['sat'], 'positive literal completion: mathematical exclusion fails')
        literal_states.append(result['states'])
        key = str((c['model'], c['extra']))
        g = groups.setdefault(key, dict(cases=0, native_nodes=0, native_max=0, literal_states=0, literal_max=0))
        g['cases'] += 1;g['native_nodes'] += native[i];g['native_max'] = max(g['native_max'], native[i])
        g['literal_states'] += result['states'];g['literal_max'] = max(g['literal_max'], result['states'])
        if i % 1000 == 0:
            print(json.dumps(dict(stage='literal', completed=i+1, total=len(cases))), flush=True)
    stable = dict(agent='six-reviewer-2', role='independent mathematical reviewer', verdict='COMPLETE all e=5 and e=6 normalized quota cases empty',
                  carrier=carrier, matrix_census=matrix, groups=groups,
                  native_result_sha256=sha256(nativeout.read_bytes()).hexdigest(),
                  literal_states_sha256=sha256(json.dumps(literal_states,separators=(',',':')).encode()).hexdigest())
    metrics = dict(seconds=time.monotonic()-started, native_seconds=native_seconds,
                   parent_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   child_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   python=subprocess.check_output(['python3','--version'],text=True).strip(),
                   compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0], flags=flags)
    if args.expected:
        need(stable == json.loads(Path(args.expected).read_text()), 'cold complete audit differs from expected')
    (work/'result.json').write_text(json.dumps(stable,indent=2)+'\n')
    (work/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print(json.dumps(dict(result=stable,metrics=metrics),indent=2), flush=True)


if __name__ == '__main__':
    main()
