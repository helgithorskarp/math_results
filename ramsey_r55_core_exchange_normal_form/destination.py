"""All-q physical destination. No owner queue or solver state is accessed."""
from itertools import combinations
from pathlib import Path
import argparse
import json
from catalog import Lookup, adjacency
from exchange import need, decode, encode, validate, descend, violations, augment, clique


def normalize(a, packing, lookup):
    red, blue, core = packing['red'], packing['blue'], packing['core']
    validate(a, red, blue, core)
    q, r = len(red)+len(blue), len(red)
    need(len(a) == 43 and 7 <= q <= 10 and 5 <= r <= q, '43-carrier shape')
    root = red[0][:]
    def signature(v):
        return sum(a[u][v] << i for i, u in enumerate(root))
    def child(B):
        return sorted(B, key=lambda v: (-signature(v), v))
    def word(B):
        return sum(a[u][v] << (4*i+j) for i, u in enumerate(root) for j, v in enumerate(B))
    blocks = [root]+sorted(map(child, red[1:]), key=word, reverse=True)+sorted(map(child, blue), key=word, reverse=True)
    index, core = lookup.find(a, core)
    p = sum(blocks, [])+core
    g = encode(a, p); transported = decode(g)
    need(all(transported[u][v] == a[p[u]][p[v]] for u, v in combinations(range(43), 2)), 'physical transport')
    nc = adjacency(lookup.lines[len(core)][index])
    need(all(transported[4*q+u][4*q+v] == nc[u][v] for u, v in combinations(range(len(core)), 2)), 'catalogue binding')
    # Literal pair and star checks establish the inherited ordered domain; no ranking trust.
    bad = None
    for i, j in combinations(range(q), 2):
        vertices = blocks[i]+blocks[j]
        for color in (0, 1):
            S = clique(a, vertices, 5, color)
            if S is not None:
                bad = dict(vertices=S, color=color); break
        if bad is not None:
            break
    if bad is None:
        for B in blocks:
            for v in core:
                for color in (0, 1):
                    S = clique(a, B+[v], 5, color)
                    if S is not None:
                        bad = dict(vertices=S, color=color); break
                if bad is not None:
                    break
            if bad is not None:
                break
    return dict(status='MONOCHROMATIC_FIVE' if bad else 'ORDERED_CARRIER_NO_RAMSEY_VERDICT',
                task=f'bo1-q{q}-r{r}-c{index:06d}', graph=g, new_to_old=p,
                physical_five_in_input_labels=bad)


def run(source, lookup):
    a = decode(source)
    final = descend(a, source['red'], source['blue'], source['core'])
    destination = normalize(a, final, lookup)
    need(next(violations(a, final['red'], final['blue'], final['core']), None) is None, 'terminal swaps')
    need(augment(a, final['red'], final['core']) is None, 'terminal augmentation')
    return dict(status='GLOBAL_REDIRECT_NOT_ORIGINAL_TASK_UNSAT', packing=final, destination=destination)

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('data'); p.add_argument('source'); p.add_argument('output')
    args = p.parse_args()
    result = run(json.loads(Path(args.source).read_text()), Lookup(args.data))
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
