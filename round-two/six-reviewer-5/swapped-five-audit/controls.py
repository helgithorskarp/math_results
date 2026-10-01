"""Exhaustive graph/weight controls and consequential semantic damages."""
from copy import deepcopy
from itertools import combinations, product
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from core import HERE, G, pin_inputs, require
from clique import maximum, twins
from construction import check_witness, matchings, plane, transfer

def brute(adjacency, weights):
    n = len(adjacency)
    return max(sum(weights[i] for i in range(n) if subset >> i & 1)
               for subset in range(1 << n) if all(adjacency[a] >> b & 1
               for a, b in combinations(range(n), 2) if subset >> a & 1 and subset >> b & 1))

def audit():
    pin_inputs()
    graphs, weighted = 0, 0
    for n in range(6):
        edges = list(combinations(range(n), 2))
        for flags in range(1 << len(edges)):
            rows = [0] * n
            for k, (a, b) in enumerate(edges):
                if flags >> k & 1:
                    rows[a] |= 1 << b
                    rows[b] |= 1 << a
            chosen, nodes = maximum(rows)
            require(len(chosen) == brute(rows, [1] * n), 'ordinary maximum versus brute force')
            graphs += 1
            if n <= 4:
                for weights in product((1, 2), repeat=n):
                    expanded, carriers = twins(rows, weights)
                    chosen, nodes = maximum(expanded)
                    require(len(chosen) == brute(rows, weights), 'true-twin equivalence versus brute force')
                    weighted += 1
    # A completely separate ordinary product confirms all 3^10 omissions.
    triples, perfect = matchings(tuple(range(5)))
    observed = set()
    for omissions in product(*(tuple(t) for t in triples)):
        pairs = {tuple(v for v in t if v != a) for t, a in zip(triples, omissions)}
        if len(pairs) == 10:
            observed.add(omissions)
    require(observed == set(perfect), 'inclusion matching coverage')
    blocks = plane()
    good = json.loads((HERE / 'WITNESS69.json').read_text())
    check_witness(good, blocks)
    rejected = []
    def reject(name, function):
        try:
            function()
        except (ValueError, RuntimeError):
            rejected.append(name)
        else:
            raise ValueError('semantic damage accepted: ' + name)
    reject('clique-node-guard', lambda: maximum((0,), node_cap=0))
    reject('asymmetric-clique-graph', lambda: maximum((2, 0)))
    reject('twin-zero-weight', lambda: twins((0,), (0,)))
    for name, damage in [
        ('duplicate-word', lambda d: d['words'].__setitem__(0, d['words'][1])),
        ('wrong-word-weight', lambda d: d['words'].__setitem__(0, 3)),
        ('involution-wrong-cycle-type', lambda d: d.__setitem__('involution', list(range(18)))),
        ('unexchanged-centers', lambda d: d.__setitem__('centers', [2, 4])),
        ('false-degree-readout', lambda d: d['replications'].__setitem__(2, 19)),
        ('wrong-parent-omission', lambda d: d['construction']['omissions'][0].__setitem__(1, 17)),
        ('duplicate-parent', lambda d: d['construction']['omissions'].__setitem__(0, d['construction']['omissions'][1])),
    ]:
        bad = deepcopy(good)
        damage(bad)
        reject(name, lambda: check_witness(bad, blocks))
    reject('false-cap', lambda: transfer(blocks, (0, 1, 2, 3, 16), {}))
    with TemporaryDirectory(prefix='swapped-five-controls-') as name:
        base = Path(name)
        manifest = (HERE / 'INPUTS.json').read_bytes()
        (base / 'INPUTS.json').write_bytes(manifest)
        pins = json.loads(manifest)
        for row in pins:
            target = base / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((HERE / row['path']).read_bytes())
        pin_inputs(base)
        for row in pins:
            target = base / row['path']
            original = target.read_bytes()
            target.write_bytes(original + b'changed')
            reject('changed-pin-' + row['path'], lambda: pin_inputs(base))
            target.write_bytes(original)
    return {'status': 'PASS_EXHAUSTIVE_AND_SEMANTIC_CONTROLS', 'ordinary_graphs': graphs,
            'weighted_graph_cases': weighted, 'ordinary_omission_products': 59049,
            'inclusion_perfect_matchings': len(perfect), 'damage_rejections': rejected}

if __name__ == '__main__':
    print(json.dumps(audit(), sort_keys=True))
