#!/usr/bin/env python3
"""Literal induced-embedding controls and switching-parity controls."""
import argparse
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess

from compare import histogram, normalize
from verify import need


def rows(n, code):
    out = [0]*n
    for j, (u, v) in enumerate(combinations(range(n), 2)):
        if code & (1 << j):
            out[u] |= 1 << v
            out[v] |= 1 << u
    return out


def run(binary, work):
    work.mkdir(parents=True, exist_ok=False)
    cases, expected = [], []
    for host_code in range(64):
        host = rows(4, host_code)
        for m in range(1, 5):
            for code in range(1 << (m*(m-1)//2)):
                pattern = rows(m, code)
                ok = any(all(((pattern[u] >> v) & 1) == ((host[f[u]] >> f[v]) & 1)
                             for u, v in combinations(range(m), 2)) for f in permutations(range(4), m))
                i = len(cases)
                cases.append(f'{i} 4 {m}\n'+' '.join(map(str, host))+'\n'+' '.join(map(str, pattern))+'\n')
                expected.append(ok)
    # Highest permitted shift, a full-size successful map, and early UNKNOWN.
    large = [0]*63
    large[0] = 1 << 62
    large[62] = 1
    cases.append(f'{len(cases)} 63 63\n'+' '.join(map(str, large))+'\n'+' '.join(map(str, large))+'\n')
    expected.append(True)
    input_file, output = work/'cases.txt', work/'decisions.txt'
    input_file.write_text(''.join(cases))
    subprocess.run([str(binary.resolve()), str(input_file), str(output), '2000000'], check=True)
    results = [list(map(int, line.split())) for line in output.read_text().splitlines()]
    need(len(results) == len(expected), 'small case coverage')
    for i, (result, truth) in enumerate(zip(results, expected)):
        need(result[0] == i and result[1] == int(truth), 'induced search vs literal injections')
    tiny = work/'tiny.txt'
    tiny.write_text('0 2 2\n0 0\n0 0\n')
    subprocess.run([str(binary.resolve()), str(tiny), str(work/'capped.txt'), '1'], check=True)
    need((work/'capped.txt').read_text().split()[1] == '2', 'node cap is UNKNOWN')
    rejected = 0
    for text in ('0 64 1\n', '0 3 4\n', '0 2 2\n1 0\n0 0\n',
                 '0 2 2\n2 0\n0 0\n', '0 2 2\n0 0\n0\n'):
        tiny.write_text(text)
        r = subprocess.run([str(binary.resolve()), str(tiny), str(work/'bad.txt'), '100'], capture_output=True)
        need(r.returncode != 0, 'malformed embedding case accepted')
        rejected += 1
    parity_checks = switch_checks = 0
    for code in range(64):
        graph = rows(4, code)
        for vertices in [list(range(4))]+[list(q) for q in combinations(range(4), 3)]:
            counts = [0]*(len(vertices)-1)
            for u, v in combinations(vertices, 2):
                odd = sum(((graph[u] >> v) ^ (graph[u] >> w) ^ (graph[v] >> w)) & 1
                          for w in vertices if w not in (u, v))
                counts[odd] += 1
            need(tuple(counts) == histogram(graph, vertices), 'literal parity histogram')
            parity_checks += 1
        for spins in range(16):
            switched = [0]*4
            for u, v in combinations(range(4), 2):
                if ((graph[u] >> v) ^ (spins >> u) ^ (spins >> v)) & 1:
                    switched[u] |= 1 << v
                    switched[v] |= 1 << u
            for anchor in range(4):
                need(normalize(graph, anchor) == normalize(switched, anchor), 'anchored switching invariant')
                switch_checks += 1
    return {'status': 'PASS', 'literal_induced_cases': 4800,
            'word_size_boundary_case': 1, 'unknown_cap_control': 1,
            'malformed_cases_rejected': rejected,
            'literal_parity_histograms': parity_checks, 'normalized_switch_cases': switch_checks}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('binary', type=Path)
    p.add_argument('work', type=Path)
    a = p.parse_args()
    result = run(a.binary, a.work)
    (a.work/'controls.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
