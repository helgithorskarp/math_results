"""Complete destination-task transport for h4035; never a good43 certificate."""
from itertools import combinations
from pathlib import Path
import argparse
import json
from lookup import Lookup
from support import binding, graph, matrix, need, parents, bad_five

def partition(q, r, g):
    return dict(g, blocks=[list(range(4*i, 4*i+4)) for i in range(q)],
                core=list(range(4*q, 43)), r=r)

def normalize_partition(obj, cache, lookup):
    """Root/column/block/core order; a failed new domain returns a physical K5."""
    ordered, family, exchange = parents()
    exchange.validate(obj)
    a = matrix(obj)
    q, r = len(obj['blocks']), obj['r']
    need(q in (9, 10) and 5 <= r <= q, 'destination class')
    root = obj['blocks'][0][:]
    def signature(v): return sum(a[u][v] << i for i, u in enumerate(root))
    blocks = [root] + [sorted(b, key=lambda v: (-signature(v), v)) for b in obj['blocks'][1:]]
    def word(b): return sum(a[u][v] << (4*i+j) for i,u in enumerate(root) for j,v in enumerate(b))
    blocks = [root] + sorted(blocks[1:r], key=word, reverse=True) + sorted(blocks[r:], key=word, reverse=True)
    c, core = lookup.find(a, obj['core'])
    permutation = sum(blocks, []) + core
    out = graph(a, permutation)
    task = f'bo1-q{q}-r{r}-c{c:06d}'
    carrier = ordered.carrier.Carrier(task, cache)
    try:
        carrier.rank(out)
    except ValueError:
        # Sorting and core membership have already been constructed. Every other
        # pair/star carrier failure is a literal monochromatic five-set.
        for i, j in combinations(range(q), 2):
            witness = bad_five(a, blocks[i] + blocks[j])
            if witness is not None: return dict(status='MONOCHROMATIC_FIVE', source_sha256=binding(obj), **witness)
        for b in blocks:
            for v in core:
                witness = bad_five(a, b + [v])
                if witness is not None: return dict(status='MONOCHROMATIC_FIVE', source_sha256=binding(obj), **witness)
        raise ValueError('unexplained destination carrier failure') from None
    need(carrier.old.closure(out), 'red maximality was not preserved')
    return {'status': 'ORDERED_CARRIER_NO_RAMSEY_VERDICT', 'task': task,
            'graph': out, 'new_to_old': permutation}

def reduce(source, cache, lookup):
    """Input is an ordered q8/q9 carrier assignment satisfying red maximality.

    The two alternative output certificates are a normalized destination in the
    h4035 global family, or a monochromatic five-set in the original graph.
    This does not operate on a fixed-prefix UNKNOWN task or on a partial model.
    """
    ordered, family, exchange = parents()
    name = source['task']
    carrier = ordered.carrier.Carrier(name, cache)
    q, r = carrier.q, carrier.r
    need(q in (8, 9), 'source is not a q8/q9 task')
    original = {'n': source['n'], 'red_hex': source['red_hex']}
    carrier.rank(original)
    need(carrier.old.closure(original), 'source violates upstream red-maximality clauses')
    current = partition(q, r, original)
    permutation = list(range(43)); steps = []
    while len(current['blocks']) in (8, 9):
        ex = exchange.step(current)
        if ex['status'] == 'NO_SELECTED_AUGMENTATION_NO_RAMSEY_VERDICT': break
        need(ex['status'] == 'PACKING_TRANSPORT_NEEDS_CATALOG_AND_ROOT_ORDER', 'exchange status')
        normalized = normalize_partition(ex['output'], cache, lookup)
        mid_to_source = [permutation[v] for v in ex['new_to_old']]
        if normalized['status'] == 'MONOCHROMATIC_FIVE':
            return {'status': 'MONOCHROMATIC_FIVE', 'source_sha256': binding(source),
                    'vertices': [mid_to_source[v] for v in normalized['vertices']],
                    'color': normalized['color']}
        permutation = [mid_to_source[v] for v in normalized['new_to_old']]
        steps.append({'exchange': ex, 'normalization': normalized})
        name = normalized['task']; q += 1; r += 1
        current = partition(q, r, normalized['graph'])
    need(len(steps) <= 2, 'termination')
    return {'status': 'REDUCED_FAMILY_CARRIER_NO_RAMSEY_VERDICT',
            'source_sha256': binding(source), 'source_task': source['task'],
            'destination_task': name, 'graph': graph(matrix(original), permutation),
            'new_to_old': permutation, 'steps': steps}

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('cache'); p.add_argument('tables'); p.add_argument('input')
    p.add_argument('--normalize-partition', action='store_true'); args = p.parse_args()
    lookup = Lookup(args.cache, args.tables)
    src = json.loads(Path(args.input).read_text())
    result = (normalize_partition(src, args.cache, lookup) if args.normalize_partition else
              reduce(src, args.cache, lookup))
    print(json.dumps(result, indent=2, sort_keys=True))
