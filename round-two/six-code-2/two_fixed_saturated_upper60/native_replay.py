"""P/X pivot replay of every residual maximum family, distinct from coloring."""
from pathlib import Path
from itertools import combinations
import argparse
import json
import resource
import subprocess
import time
import model as M
import completions as C


def compile_pivot(work, sanitized):
    source = Path(__file__).resolve().parent.parent / 'free_involution_upper68' / 'pivot.cpp'
    executable = work / 'pivot'
    flags = ['g++', '-std=c++20', '-Wall', '-Wextra', '-Werror', '-O1' if sanitized else '-O2']
    if sanitized:
        flags += ['-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-fno-pie', '-no-pie']
    run = subprocess.run(flags + [str(source), '-o', str(executable)], capture_output=True, text=True, timeout=60)
    work.joinpath('compiler.log').write_text(run.stdout + run.stderr)
    M.require(run.returncode == 0, 'native build failed')
    return executable


def pivot(executable, work, case, adjacency, target, cap=30000000, expected='COMPLETE'):
    path = work / (case + '.graph')
    lines = [str(len(adjacency))]
    for row in adjacency:
        neighbors = tuple(j for j in range(len(adjacency)) if row >> j & 1)
        lines.append(' '.join(str(v) for v in (len(neighbors),) + neighbors))
    path.write_text('\n'.join(lines) + '\n')
    output = work / (case + '.maxima')
    run = subprocess.run([str(executable), str(path), str(output), str(cap), '30', str(target)],
                         capture_output=True, text=True, timeout=40)
    work.joinpath(case + '.native.log').write_text(run.stdout + run.stderr)
    M.require(run.stdout.startswith(expected + ' ') and run.returncode == (0 if expected == 'COMPLETE' else 2),
              'native incomplete or unexpected status: ' + run.stdout + run.stderr)
    if expected != 'COMPLETE':
        return (), 0
    maxima = tuple(sorted(tuple(int(v) for v in line.split()) for line in output.read_text().splitlines()))
    M.require(len(maxima) == len(set(maxima)) and all(len(q) == len(set(q)) == target and
              all(0 <= v < len(adjacency) for v in q) and
              all(adjacency[a] >> b & 1 for a,b in combinations(q, 2)) for q in maxima), 'native bad maximum family')
    return maxima, int(run.stdout.split()[2])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stars', type=Path, required=True)
    parser.add_argument('--color', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--sanitized', action='store_true')
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    executable = compile_pivot(args.work, args.sanitized)
    stars = json.loads(args.stars.read_text())['anchors']
    resources, rows = M.orbit_carrier()
    records = []
    start = time.monotonic()
    for i, record in enumerate(stars):
        _, adjacency = C.residual_graph(tuple(record['words']), resources, rows)
        saved = json.loads((args.color / f'case-{i:02}.json').read_text())
        expected = tuple(tuple(q) for q in json.loads((args.color / f'case-{i:02}.maxima.json').read_text()))
        native, nodes = pivot(executable, args.work, f'case-{i:02}', adjacency, saved['alpha'])
        M.require(native == expected, 'native maximum families differ entrywise')
        summary = dict(case=i, vertices=len(adjacency), alpha=saved['alpha'], families=len(native), pivot_nodes=nodes)
        records.append(summary)
        print(json.dumps(summary, sort_keys=True), flush=True)
    result = dict(status='COMPLETE native entrywise maximum-family validation', sanitized=args.sanitized,
                  cases=len(records), records=records, seconds=time.monotonic() - start,
                  peak_child_RSS_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    args.work.joinpath('summary.json').write_bytes(M.encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
