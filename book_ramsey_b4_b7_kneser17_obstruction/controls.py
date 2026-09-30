"""Literal unpruned sweeps, full-graph pair checks, and rejection controls."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import tempfile
import resource
import time
import verify

if not __debug__:
    raise SystemExit('Python assertions must be enabled')


def literal_domain(core):
    """Every mask is tested; no saturated-spine clauses or branch pruning."""
    n = 17; full = (1 << (n + 1)) - 1
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
    parser.add_argument('scratch', type=Path)
    args = parser.parse_args(); start = time.perf_counter()
    roots = [frozenset(p) for p in itertools.combinations(range(7), 2)]
    base = {(u, v) for u, v in itertools.combinations(range(21), 2) if roots[u].isdisjoint(roots[v])}
    for name, deleted, multiplicity in verify.CASES:
        cert = json.loads((args.scratch / ('case-' + name + '.json')).read_text())
        labels = [u for u in range(21) if u not in deleted]
        core = {(u, v) for u, v in itertools.combinations(range(17), 2) if (labels[u], labels[v]) in base}
        literal = literal_domain(core)
        assert literal == cert['domain'], 'Literal domain differs entrywise'
        print(name, 'literal_masks', 1 << 17, 'patterns', len(literal), flush=True)
    name, deleted, multiplicity = verify.CASES[-1]
    cert = json.loads((args.scratch / ('case-' + name + '.json')).read_text())
    labels = [u for u in range(21) if u not in deleted]
    core = {(u, v) for u, v in itertools.combinations(range(17), 2) if (labels[u], labels[v]) in base}
    domain = cert['domain']
    pairs = [[i, j, c] for i in range(len(domain)) for j in range(i, len(domain)) for c in (0, 1)
             if verify.valid(19, verify.augment(core, 17, [domain[i], domain[j]], [c]))]
    assert pairs == cert['pair_colors'], 'Full-graph pairs differ entrywise'
    print('full19_pair_color_tests', len(domain) * (len(domain) + 1), 'valid', len(pairs), flush=True)
    mutations = [
        ('wrong core identity', lambda p: p.update(name='incorrect_core')),
        ('partial completion', lambda p: p.update(complete_through_outside_vertices=4)),
        ('unjustified conflict', lambda p: p.update(tree='C')),
        ('omitted colored pair', lambda p: p['pair_colors'].pop()),
        ('wrong joining mask', lambda p: p['levels'][0][0].__setitem__(1, 1024)),
        ('omitted valid20 prefix', lambda p: p['levels'][1].pop())]
    with tempfile.TemporaryDirectory(prefix='kneser17-controls-') as temporary:
        path = Path(temporary) / 'damaged.json'
        for label, mutate in mutations:
            damaged = copy.deepcopy(cert); mutate(damaged)
            path.write_text(json.dumps(damaged, separators=(',', ':')))
            try:
                verify.check_case(path, name, deleted)
            except AssertionError as error:
                print('rejected', label, str(error), flush=True)
            else:
                raise AssertionError('Malformed certificate accepted: ' + label)
    print('controls_seconds', time.perf_counter()-start,
          'maxrss_kib', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == '__main__':
    main()
