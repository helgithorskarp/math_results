"""Count packing automorphisms from literal blocks, without leave-group code.

An exact, complete partial point-bijection search. Each mapped block subset
must be contained in a target block, and covered/leave pair status is
preserved. These necessary conditions never remove an automorphism. The
full point image is checked literally at every leaf. Any guard gives
INCOMPLETE, not an automorphism-group verdict.
"""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import math
import resource
import time

BASE = Path(__file__).resolve().parent


def audit(words, max_nodes=200000, max_seconds=10):
    if (type(max_nodes) is not int or not 1 <= max_nodes <= 200000
            or type(max_seconds) not in (int, float) or not math.isfinite(max_seconds)
            or not 0 < max_seconds <= 10):
        raise RuntimeError('invalid audit guard; maximum is 200000 nodes and ten seconds')
    if (len(words) != 20 or len(set(words)) != 20
            or any(type(w) is not int or not 0 <= w < 131072 or w.bit_count() != 4 for w in words)):
        raise RuntimeError('malformed twenty-quadruple packing')
    blocks = [frozenset(i for i in range(17) if word >> i & 1) for word in words]
    family = set(blocks)
    through = [[b for b in blocks if u in b] for u in range(17)]
    rho = [len(b) for b in through]
    if rho != [3, 4, 4, 4] + [5] * 13:
        raise RuntimeError('replication profile differs')
    covered = set()
    for block in blocks:
        for pair in combinations(sorted(block), 2):
            if pair in covered:
                raise RuntimeError('pair repeated in input packing')
            covered.add(pair)
    pair = [[tuple(sorted((u, v))) in covered for v in range(17)] for u in range(17)]
    image = {0: 0}
    unused = set(range(1, 17))
    output = []
    started = time.monotonic()
    nodes = 0

    def candidates(u):
        answer = []
        for v in sorted(unused):
            if rho[u] != rho[v] or any(pair[u][a] != pair[v][b] for a, b in image.items()):
                continue
            if any(not any({v} | {image[a] for a in block if a in image} <= target
                           for target in through[v]) for block in through[u]):
                continue
            answer.append(v)
        return answer

    def search():
        nonlocal nodes
        nodes += 1
        if nodes > max_nodes or time.monotonic() - started > max_seconds:
            raise RuntimeError('INCOMPLETE literal automorphism audit node/time guard')
        if not unused:
            point = tuple(image[u] for u in range(17))
            if len(set(point)) != 17 or {frozenset(point[u] for u in b) for b in blocks} != family:
                raise RuntimeError('non-automorphism at audit leaf')
            output.append(point)
            return
        domain = [(candidates(u), u) for u in range(17) if u not in image]
        choices, u = min(domain, key=lambda x: (len(x[0]), x[1]))
        for v in choices:
            image[u] = v
            unused.remove(v)
            search()
            unused.add(v)
            del image[u]

    search()
    if len(set(output)) != len(output) or tuple(range(17)) not in output:
        raise RuntimeError('automorphism output repeated or identity absent')
    return {'automorphisms': sorted(output), 'order': len(output), 'nodes': nodes,
            'seconds': round(time.monotonic() - started, 6)}


def run(expected_path, output_path):
    raw = expected_path.read_bytes()
    expected = json.loads(raw)
    result = {'agent': 'six-code-3', 'role': 'researcher', 'status': 'INCOMPLETE',
              'expected_sha256': hashlib.sha256(raw).hexdigest(), 'cases': []}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + '\n')
    for family in expected['packing_families']:
        for orbit in family['orbits']:
            entry = audit(orbit['representative'])
            if entry['order'] != orbit['packing_automorphism_order']:
                raise RuntimeError('literal count disagrees with expected orbit-stabilizer order')
            entry.update(class_index=len(result['cases']), leave_index=family['index'],
                         hub_index=family['prefix_index'], orbit_index=orbit['index'])
            result['cases'].append(entry)
            output_path.write_text(json.dumps(result, indent=2) + '\n')
            print({k: entry[k] for k in ('class_index', 'order', 'nodes', 'seconds')}, flush=True)
    if len(result['cases']) != 8:
        raise RuntimeError('expected eight complete audit cases')
    result.update(status='COMPLETE literal block-incidence automorphism census',
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  orders=[c['order'] for c in result['cases']])
    output_path.write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], result['orders'])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=BASE / 'expected.json')
    parser.add_argument('--output', type=Path, default=BASE / '.work' / 'automorphisms.json')
    args = parser.parse_args()
    run(args.expected, args.output)
