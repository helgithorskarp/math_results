#!/usr/bin/env python3
"""Definition-level finite controls and explicit rejection checks."""
import argparse
import importlib.util
import itertools as it
import json
import subprocess
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main(args):
    started = time.monotonic()
    gen = load('single_20_19_generation', 'generate.py')
    check = load('single_20_19_verification', 'verify.py')
    accepted, total = Counter(), 0
    for values in it.combinations_with_replacement(range(16), 5):
        total += 1
        deficit = Counter(values)
        active = set([1, 2, 3]) | set(deficit)
        outside = active - {1, 2, 3}
        degrees = {p: (1 if p in [1, 2, 3] else 0) + 3*deficit[p] for p in active}
        if any(r >= len(active) for r in degrees.values()) or any(degrees[p] > len(outside) for p in [1, 2, 3]):
            continue
        if sorted(deficit.values()) == [1, 1, 1, 2] and not (set(deficit) & {1, 2, 3}):
            accepted[0] += 1
        elif sorted(deficit.values()) == [1]*5 and not (set(deficit) & {1, 2, 3}):
            accepted[1] += 1
        elif sorted(deficit.values()) == [1]*5 and len(set(deficit) & {1, 2, 3}) == 1:
            accepted[2] += 1
        else:
            raise ValueError('additional feasible degree profile')
    require(total == 15504 and accepted == {0: 2860, 1: 1287, 2: 2145}, 'profile coverage failure')

    args.scratch.mkdir(parents=True, exist_ok=True)
    source = args.scratch / 'audit_input.txt'
    result = args.scratch / 'audit_output.jsonl'
    graphs, hypergraphs = 0, 0

    def native(data, valid=True, cap=None):
        source.write_text(data)
        command = [str(args.cover.resolve()), str(source), str(result)]
        if cap is not None:
            command.append(str(cap))
        p = subprocess.run(command, capture_output=True, text=True, timeout=20)
        if valid:
            require(p.returncode == 0, p.stderr)
            require(json.loads(p.stdout)['status'] == 'COMPLETE', 'missing native completion')
            return json.loads(result.read_text())
        require(p.returncode != 0, 'invalid/incomplete native input accepted')
        return p.stderr

    def check_matrix(n, width, rows):
        text = f'{n} {len(rows)} {width}\n'
        text += ''.join(' '.join(map(str, [i + 1] + list(row))) + '\n' for i, row in enumerate(rows))
        text += '1\n0 0\n'
        record = native(text)
        expected = set()
        for count in range(len(rows) + 1):
            if count*width != n:
                continue
            for selected in it.combinations(range(len(rows)), count):
                covered = [p for i in selected for p in rows[i]]
                if len(covered) == len(set(covered)) == n and set(covered) == set(range(n)):
                    expected.add(tuple(i + 1 for i in selected))
        require(record['index'] == 0 and {tuple(c) for c in record['covers']} == expected,
                'native exact cover disagrees with direct subsets')

    for n in range(6):
        universe = list(it.combinations(range(n), 2))
        for mask in range(1 << len(universe)):
            rows = [e for i, e in enumerate(universe) if mask & (1 << i)]
            check_matrix(n, 2, rows)
            graphs += 1
    for n in range(4):
        for width in [1, 3]:
            universe = list(it.combinations(range(n), width))
            for mask in range(1 << len(universe)):
                check_matrix(n, width, [e for i, e in enumerate(universe) if mask & (1 << i)])
                hypergraphs += 1

    failures = [
        '121 0 2\n0\n', '4 1 2\n1 0 0\n1\n0 0\n',
        '4 1 2\n1 0 4\n1\n0 0\n', '4 2 2\n1 0 1\n1 2 3\n1\n0 0\n',
        '4 0 2\n1\n1 0\n', '4 0 2\n1\n0 2 0 0\n',
        '4 0 2\n1\n0 0\ntrailing\n', '4 0 2\n1\n0\n',
    ]
    for text in failures:
        native(text, False)
    capped = '4 2 2\n1 0 1\n2 2 3\n1\n0 0\n'
    require('INCOMPLETE' in native(capped, False, 1), 'missing cap failure marker')

    def rejects(function):
        try:
            function()
        except (ValueError, RuntimeError):
            return
        raise ValueError('malformed/incomplete input accepted')

    rejects(lambda: gen.orbit_cover({1}, [[1, 0]], lambda v, g: g[v]))
    rejects(lambda: check.decode(-1))
    rejects(lambda: check.decode(65536))
    rejects(lambda: check.decode(True))

    with args.replay.open() as replay:
        header = json.loads(replay.readline())
        case = None
        for line in replay:
            record = json.loads(line)
            if record['covers']:
                case = record['covers'][0]
                break
    require(case is not None, 'missing control star fixture')
    valid_leave = header['leaves'][0][3]
    rejects(lambda: gen.PairCover(header['allowed']).run(valid_leave, node_cap=0))
    rejects(lambda: check.AlgorithmX(list(map(check.decode, header['allowed']))).run(
        {e for j, e in enumerate(check.PAIR_LIST) if valid_leave & (1 << j)}, node_cap=0))
    pool = list(map(check.decode, header['pool']))
    plane = check.field_plane()
    first = [b | {17} for b in sorted(plane, key=check.encode) if b != check.L] + [check.T | {16, 17}]
    check.check_case(case, pool, first)
    mutated = json.loads(json.dumps(case))
    mutated[1] = mutated[1][1:]
    mutated[2] = mutated[2][1:]
    rejects(lambda: check.check_case(mutated, pool, first))
    mutated = json.loads(json.dumps(case)); mutated[2] = [0] * len(mutated[2])
    rejects(lambda: check.check_case(mutated, pool, first))
    mutated = json.loads(json.dumps(case)); mutated[0][1] = mutated[0][0]
    rejects(lambda: check.check_case(mutated, pool, first))
    print(json.dumps({'status': 'PASS', 'deficit_compositions': total,
                      'deficit_support_counts': dict(accepted), 'simple_graphs': graphs,
                      'small_hypergraphs': hypergraphs, 'native_rejections': len(failures),
                      'native_incomplete_rejections': 1, 'python_rejections': 7,
                      'python_incomplete_rejections': 2,
                      'seconds': round(time.monotonic() - started, 4)}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover', required=True, type=Path)
    p.add_argument('--scratch', required=True, type=Path)
    p.add_argument('--replay', required=True, type=Path)
    main(p.parse_args())
