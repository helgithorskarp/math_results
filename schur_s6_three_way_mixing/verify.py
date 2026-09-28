"""Build and verify all path-cycle cases; Python standard library only."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
BASELINE_SHA256 = '2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def valid(word):
    return all(word[x - 1] != word[z - 1] or word[z - x - 1] != word[z - 1]
               for z in range(2, len(word) + 1) for x in range(1, z // 2 + 1))


def cases(k):
    for r in range(2, k + 1):
        for order in permutations(range(1, k + 1), r):
            for entry in range(r - 1):
                yield order, entry


def orbit(destination, root):
    order = []
    while root not in order:
        order.append(root)
        root = destination[root - 1]
    return tuple(order), order.index(root)


def build(binary, sanitize=False):
    flags = ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer'] if sanitize else ['-O3']
    subprocess.run(['g++', '-std=c++17', '-Wall', '-Wextra', '-Wpedantic',
                    '-Wconversion', '-Wshadow', *flags, str(HERE / 'verify.cpp'), '-o', str(binary)], check=True)


def run_lists(binary, domains):
    text = str(len(domains)) + '\n' + ''.join(str(len(ds)) + ' ' + ' '.join(map(str, ds)) + '\n' for ds in domains)
    output = subprocess.run([str(binary), '--lists'], input=text, text=True, capture_output=True, check=True)
    require(not output.stderr, 'unexpected list checker stderr')
    lines = output.stdout.splitlines()
    require(len(lines) == len(domains), 'missing list-case results')
    results = []
    for index, (line, ds) in enumerate(zip(lines, domains)):
        fields = line.split()
        require(len(fields) in (3, 4) and int(fields[0]) == index, 'list-case framing')
        require(int(fields[2]) >= 1, 'invalid node count')
        sat = fields[1] == 'SAT'
        require(fields[1] in ('SAT', 'UNSAT') and len(fields) == 3 + int(sat), 'list-case status')
        if sat:
            word = list(map(int, fields[3]))
            require(len(word) == len(ds) and all(1 <= d <= 6 for d in word), 'model length or colour')
            require(all(mask & (1 << (d - 1)) for mask, d in zip(ds, word)), 'model outside lists')
            require(valid(word), 'invalid literal model')
        results.append(sat)
    return results


def controls(binary, word):
    # Complete independent oracle on all nonempty 3-colour domain systems
    # of lengths 1 through 5. This includes both SAT and UNSAT cases.
    domains = [ds for n in range(1, 6) for ds in product(range(1, 8), repeat=n)]
    results = run_lists(binary, domains)
    for ds, sat in zip(domains, results):
        choices = [[d for d in range(1, 4) if mask & (1 << (d - 1))] for mask in ds]
        direct = any(valid(c) for c in product(*choices))
        require(sat == direct, 'exhaustive small list oracle disagreement')
    status_counts = dict(Counter('SAT' if x else 'UNSAT' for x in results))

    # Every arbitrary no-loop destination map and endpoint reduces to an
    # enumerated orbit; every enumerated orbit is reached. No deduplication
    # or heuristic assumption enters coverage.
    expected = set(cases(6))
    observed = set()
    map_roots = 0
    for dest in product(*[[d for d in range(1, 7) if d != i] for i in range(1, 7)]):
        for root in range(1, 7):
            reduced = orbit(dest, root)
            require(reduced in expected, 'forward orbit absent from enumeration')
            observed.add(reduced)
            map_roots += 1
    require(observed == expected and len(expected) == 7830, 'orbit coverage incomplete')

    # Positive reduction control: all valid 3-colourings through 6,
    # compared with the optimal old colouring 12312 through 5.
    base = [1, 2, 3, 1, 2]
    reduction_cases = 0
    for candidate in product(range(1, 4), repeat=6):
        if not valid(candidate):
            continue
        images = [{candidate[v] for v, old in enumerate(base) if old == i} for i in range(1, 4)]
        matching = next((p for p in permutations(range(1, 4))
                         if all(p[i - 1] in images[i - 1] for i in range(1, 4))), None)
        require(matching is not None, 'small Hall normalization failed')
        rename = {d: i for i, d in enumerate(matching, 1)}
        aligned = [rename[d] for d in candidate]
        dest = []
        for i in range(1, 4):
            other = {aligned[v] for v, old in enumerate(base) if old == i} - {i}
            require(len(other) <= 1, 'small candidate is not binary')
            dest.append(next(iter(other)) if other else next(d for d in range(1, 4) if d != i))
        order, entry = orbit(dest, aligned[-1])
        require((order, entry) in set(cases(3)), 'small orbit missing')
        reset = [aligned[v] if old in order else old for v, old in enumerate(base)] + [aligned[-1]]
        require(valid(reset), 'restoring outside an orbit broke validity')
        reduction_cases += 1
    require(reduction_cases > 0, 'no positive reduction controls')

    small_lists = []
    for order, entry in cases(3):
        dest = dict(zip(order, order[1:] + (order[entry],)))
        ds = [(1 << (d - 1)) | ((1 << (dest[d] - 1)) if d in dest else 0) for d in base]
        ds.append(1 << (order[0] - 1))
        small_lists.append(ds)
    small_answers = run_lists(binary, small_lists)
    require(any(small_answers) and not all(small_answers), 'small orbit positive/negative coverage')

    baseline_domains = [1 << (d - 1) for d in word]
    big_controls = [baseline_domains] + [baseline_domains + [1 << d] for d in range(6)]
    require(run_lists(binary, big_controls) == [True] + [False] * 6, '536/537 controls')
    return {'small_list_systems': len(domains), 'small_status_counts': status_counts,
            'map_endpoint_pairs': map_roots, 'orbits': len(observed),
            'positive_reduction_candidates': reduction_cases,
            'small_orbit_systems': len(small_lists),
            'small_orbit_sat': sum(small_answers), 'large_controls': 7}


def parse_proof(output):
    lines = output.splitlines()
    all_cases = list(cases(6))
    require(len(lines) == len(all_cases), 'incomplete proof output')
    groups, total, largest = {}, 0, 0
    for index, ((order, entry), line) in enumerate(zip(all_cases, lines)):
        fields = line.split()
        require(len(fields) == 6, 'malformed proof row')
        require(fields[:4] == [str(index), ''.join(map(str, order)), str(entry), 'UNSAT'],
                'wrong, missing or satisfiable case')
        nodes, edges = map(int, fields[4:])
        require(nodes >= 1 and 0 < edges <= 72092, 'invalid proof counts')
        g = groups.setdefault(str(len(order)), {'cases': 0, 'nodes': 0, 'max_nodes': 0})
        g['cases'] += 1
        g['nodes'] += nodes
        g['max_nodes'] = max(g['max_nodes'], nodes)
        total += nodes
        largest = max(largest, nodes)
    return {'cases': len(lines), 'total_nodes': total, 'max_nodes': largest,
            'by_length': groups, 'rows_sha256': sha256(output.encode()).hexdigest()}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--controls-only', action='store_true')
    p.add_argument('--sanitize', action='store_true')
    args = p.parse_args()
    raw = (HERE / 'baseline536.txt').read_bytes()
    require(sha256(raw).hexdigest() == BASELINE_SHA256, 'wrong baseline bytes')
    word = list(map(int, raw.decode().strip()))
    require(len(word) == 536 and set(word) == set(range(1, 7)) and valid(word), 'invalid baseline')
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='schur-mixing-') as temp:
        binary = Path(temp) / 'verify'
        build(binary, args.sanitize)
        control_summary = controls(binary, word)
        require(control_summary == json.loads((HERE / 'controls_expected.json').read_text()),
                'unexpected control results')
        print('PASS controls', json.dumps(control_summary, sort_keys=True), flush=True)
        if not args.controls_only:
            run = subprocess.run([str(binary), str(HERE / 'baseline536.txt')],
                                 text=True, capture_output=True, check=True)
            require(not run.stderr, 'unexpected proof stderr')
            result = parse_proof(run.stdout)
            require(result == json.loads((HERE / 'expected.json').read_text()), 'proof output differs')
            print('PASS cases={} nodes={} max_nodes={} rows_sha256={}'.format(
                result['cases'], result['total_nodes'], result['max_nodes'], result['rows_sha256']))
    print('seconds={:.3f}'.format(time.monotonic() - start))


if __name__ == '__main__':
    main()
