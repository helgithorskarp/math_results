"""Literal unpruned sweeps, full-graph pair checks, and rejection controls."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import tempfile
import time
import verify

if not __debug__:
    raise SystemExit('Python assertions must be enabled')


def literal_domain(core):
    """Every mask is tested; no saturated-spine clauses or branch pruning."""
    n = 18; full = (1 << (n + 1)) - 1
    rows = [sum(1 << v for v in range(n) if tuple(sorted((u, v))) in core) for u in range(n)]
    survivors = []
    for p in range(1 << n):
        g = [row | (((p >> u) & 1) << n) for u, row in enumerate(rows)] + [p]
        good = True
        for u, v in itertools.combinations(range(n + 1), 2):
            red = (g[u] >> v) & 1
            pages = g[u] & g[v] if red else (
                full & ~(g[u] | g[v] | (1 << u) | (1 << v)))
            if pages.bit_count() > (3 if red else 6):
                good = False; break
        if good:
            survivors.append(p)
    return survivors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args(); start = time.perf_counter()
    cert = json.loads(args.certificate.read_text()); directory = Path(__file__).parent
    roots = [frozenset((a, b)) for a in range(7) for b in range(a + 1, 7)]
    base = {(i, j) for i, j in itertools.combinations(range(21), 2) if roots[i].isdisjoint(roots[j])}
    assert verify.valid(21, base)
    for case in cert['cases']:
        labels = [u for u in range(21) if u not in case['deleted']]
        core = {(i, j) for i, j in itertools.combinations(range(18), 2) if (labels[i], labels[j]) in base}
        literal = literal_domain(core)
        assert literal == case['domain'], 'Literal mask sweep differs entrywise'
        print(case['name'], 'literal_masks=', 1 << 18, 'domain=', len(literal), flush=True)
    case = cert['cases'][-1]
    labels = [u for u in range(21) if u not in case['deleted']]
    core = {(i, j) for i, j in itertools.combinations(range(18), 2) if (labels[i], labels[j]) in base}
    D = case['domain']
    pairs = [[i, j, c] for i in range(len(D)) for j in range(i, len(D)) for c in (0, 1)
             if verify.valid(20, verify.augment(core, 18, [D[i], D[j]], [c]))]
    assert pairs == case['pair_colors'], 'Full-graph matching-case pairs differ entrywise'
    print('matching_full_graph_pair_tests=', len(D) * (len(D) + 1), 'valid=', len(pairs), flush=True)
    mutations = [
        ('incomplete status', lambda p: p.update(complete=False)),
        ('missing core', lambda p: p['cases'].pop()),
        ('false root conflict', lambda p: p['cases'][0].update(tree='C')),
        ('omitted colored pair', lambda p: p['cases'][0]['pair_colors'].pop()),
        ('false book page', lambda p: p['cases'][0]['obstructions'][0]['pages'].__setitem__(
            0, p['cases'][0]['obstructions'][0]['spine'][0])),
        ('wrong orbit size', lambda p: p['cases'][0]['obstructions'][0].update(orbit_size=1)),
        ('uncovered orbit', lambda p: p['cases'][0]['obstructions'].pop())]
    with tempfile.TemporaryDirectory(prefix='kneser18-controls-') as temporary:
        path = Path(temporary) / 'damaged.json'
        for label, mutate in mutations:
            damaged = copy.deepcopy(cert); mutate(damaged)
            path.write_text(json.dumps(damaged, separators=(',', ':')))
            try:
                verify.check(path, directory, compare_compact=False)
            except AssertionError as error:
                print('rejected:', label, '|', str(error), flush=True)
            else:
                raise AssertionError('Malformed certificate accepted: ' + label)
    print('controls_seconds=', time.perf_counter() - start)


if __name__ == '__main__':
    main()
