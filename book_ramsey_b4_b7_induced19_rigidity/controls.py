"""Direct exhaustive pattern sweep and rejection controls for the certificate."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import tempfile
import time
from verify import check

if not __debug__:
    raise SystemExit('Python assertions must be enabled')


def direct_sweep(base, deleted):
    labels = [u for u in range(21) if u not in deleted]
    n = len(labels)
    matrix = [[int(tuple(sorted((u, v))) in base) for v in labels] for u in labels]
    spines = []
    for u, v in itertools.combinations(range(n), 2):
        color = matrix[u][v]
        count = sum(matrix[u][w] == color and matrix[v][w] == color
                    for w in range(n) if w not in (u, v))
        spines.append((u, v, color, count, 3 if color else 6))
    domain = []
    for mask in range(1 << n):
        bits = [(mask >> u) & 1 for u in range(n)]
        # Literal page count at every old spine, with the new vertex included.
        if any(count + int(bits[u] == color and bits[v] == color) > limit
               for u, v, color, count, limit in spines):
            continue
        # Literal page count at every new spine.
        if any(sum(matrix[u][w] == bits[u] and bits[w] == bits[u]
                   for w in range(n) if w != u) > (3 if bits[u] else 6)
               for u in range(n)):
            continue
        domain.append(mask)
    return domain


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    start = time.perf_counter()
    directory = Path(__file__).parent
    graph_path = directory / 'h21.json'
    cert = json.loads(args.certificate.read_text())
    base = set(map(tuple, json.loads(graph_path.read_text())['red_edges']))
    case = next(c for c in cert['cases'] if c['deleted'] == [6, 18])
    assert direct_sweep(base, [6, 18]) == case['domain']
    assert len(case['domain']) == 24
    print('Direct sweep: all 524288 patterns, 24 survivors, entry-level agreement')
    with tempfile.TemporaryDirectory(dir=args.certificate.parent) as temporary:
        path = Path(temporary) / 'control-proof.json'

        def reject(data, label):
            path.write_text(json.dumps(data))
            try:
                check(path, graph_path)
            except AssertionError:
                print('Rejected:', label)
            else:
                raise AssertionError('Accepted invalid certificate: ' + label)

        altered = copy.deepcopy(cert)
        altered['cases'][0]['tree'] = 'C'
        reject(altered, 'false conflict at an unassigned root')
        altered = copy.deepcopy(cert)
        altered['cases'].pop()
        reject(altered, 'omitted core')
        altered = copy.deepcopy(cert)
        altered['cases'][0]['pair_colors'].append([0, 0, 0])
        reject(altered, 'fabricated compatible loop')
        altered = copy.deepcopy(cert)

        def corrupt_valid(node):
            if type(node) is not list:
                return False
            if len(node) == 2 and node[0] == 'V':
                node[1] ^= 1
                return True
            return corrupt_valid(node[1]) or corrupt_valid(node[2])

        assert corrupt_valid(altered['cases'][0]['tree'])
        reject(altered, 'wrong valid-leaf assignment')
    print('seconds=', time.perf_counter() - start)


if __name__ == '__main__':
    main()
