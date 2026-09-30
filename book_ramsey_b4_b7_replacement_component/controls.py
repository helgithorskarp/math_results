"""Literal full-pattern sweep and rejection controls for component certificates."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import tempfile
import time
import verify


def literal_domain(edges, labels):
    """Sweep all masks; evaluate old saturated spines and every new spine."""
    n = len(labels)
    full = (1 << n) - 1
    rows = [sum(1 << j for j, v in enumerate(labels)
                if tuple(sorted((u, v))) in edges) for u in labels]
    constraints = []
    for u, v in itertools.combinations(range(n), 2):
        color = (rows[u] >> v) & 1
        pages = rows[u] & rows[v] if color else full & ~(rows[u] | rows[v] | (1 << u) | (1 << v))
        if pages.bit_count() == (3 if color else 6):
            constraints.append(((1 << u) | (1 << v), color))
    blue_rows = [full & ~(row | (1 << u)) for u, row in enumerate(rows)]
    domain = []
    for mask in range(1 << n):
        if any((mask & endpoints) == (endpoints if color else 0)
               for endpoints, color in constraints):
            continue
        blue = full ^ mask
        if all(((rows[u] & mask).bit_count() <= 3 if (mask >> u) & 1 else
                (blue_rows[u] & blue).bit_count() <= 6) for u in range(n)):
            domain.append(mask)
    return domain


def rejected(cert, directory, parent, label, mutate):
    bad = copy.deepcopy(cert)
    mutate(bad)
    with tempfile.TemporaryDirectory(prefix='component-control-', dir=parent) as temp:
        path = Path(temp) / 'bad-proof.json'
        path.write_text(json.dumps(bad, separators=(',', ':')))
        try:
            verify.check(path, directory)
        except (AssertionError, KeyError, TypeError, ValueError, IndexError):
            print('rejected:', label)
            return
    raise AssertionError('Corrupted certificate accepted: ' + label)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    start = time.perf_counter()
    directory = Path(__file__).parent
    cert = json.loads(args.certificate.read_text())
    data = json.loads((directory / 'h21.json').read_text())
    manifest = json.loads((directory / 'templates.json').read_text())
    base = set(map(tuple, data['red_edges']))
    by_name = {t['name']: base ^ set(map(tuple, t['toggles'])) for t in manifest}
    # The largest domain across all five representatives is used as the control.
    name, case = max(((r['name'], c) for r in cert['representatives'] for c in r['cases']),
                     key=lambda p: len(p[1]['domain']))
    labels = [u for u in range(21) if u not in case['deleted']]
    swept = literal_domain(by_name[name], labels)
    assert swept == case['domain'], 'Literal domain mismatch'
    print('literal sweep:', name, 'deleted', case['deleted'], 'masks', 1 << len(labels),
          'valid_patterns', len(swept), 'entrywise agreement')

    def first_case(x):
        return x['representatives'][0]['cases'][0]

    def false_bijection(x):
        image = first_case(x)['isomorphisms'][0]['image']
        image[0], image[1] = image[1], image[0]

    def wrong_target(x):
        witness = first_case(x)['isomorphisms'][0]
        witness['target'] = 'A' if witness['target'] != 'A' else 'B'

    def omitted_pair(x):
        first_case(x)['pair_colors'].pop()

    rejected(cert, directory, args.certificate.parent, 'missing representative',
             lambda x: x['representatives'].pop())
    rejected(cert, directory, args.certificate.parent, 'false root conflict',
             lambda x: first_case(x).__setitem__('tree', 'C'))
    rejected(cert, directory, args.certificate.parent, 'omitted valid pair', omitted_pair)
    rejected(cert, directory, args.certificate.parent, 'bijective false isomorphism', false_bijection)
    rejected(cert, directory, args.certificate.parent, 'wrong isomorphism target', wrong_target)
    rejected(cert, directory, args.certificate.parent, 'incomplete status',
             lambda x: x.__setitem__('complete', False))
    print('seconds=', time.perf_counter() - start)


if __name__ == '__main__':
    main()
