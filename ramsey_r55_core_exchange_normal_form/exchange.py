"""Physical packing descent and an exact 903-variable receiver specification.

A normal-form violation is a REDIRECT, never an old-task UNSAT certificate.
"""
from itertools import combinations
from pathlib import Path
import argparse
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def decode(obj):
    n = obj['n']; bits = int(obj['red_hex'], 16)
    need(isinstance(n, int) and 1 <= n <= 43, 'graph order')
    need(0 <= bits < (1 << (n*(n-1)//2)), 'graph bits')
    a = [[0]*n for _ in range(n)]
    for k, (u, v) in enumerate(combinations(range(n), 2)):
        a[u][v] = a[v][u] = (bits >> k) & 1
    return a


def encode(a, permutation=None):
    p = list(range(len(a))) if permutation is None else permutation
    need(sorted(p) == list(range(len(a))), 'permutation')
    return dict(n=len(a), red_hex=format(sum(a[p[u]][p[v]] << k
                for k, (u, v) in enumerate(combinations(range(len(a)), 2))), f'0{(len(a)*(len(a)-1)//2+3)//4}x'))


def clique(a, vertices, size, color):
    for S in combinations(sorted(vertices), size):
        if all(a[u][v] == color for u, v in combinations(S, 2)):
            return list(S)
    return None


def validate(a, red, blue, core):
    need(sorted(sum(red+blue, [])+core) == list(range(len(a))), 'partition')
    for blocks, color in ((red, 1), (blue, 0)):
        for B in blocks:
            need(len(B) == 4 and all(a[u][v] == color for u, v in combinations(B, 2)), 'block')
    need(clique(a, sum(blue, [])+core, 4, 1) is None, 'red maximality')
    need(clique(a, core, 4, 0) is None, 'blue maximality')


def potential(a, red, blue, core):
    return (len(red), len(red)+len(blue), sum(a[u][v] for u, v in combinations(core, 2)))


def violations(a, red, blue, core):
    d = {v: sum(a[v][u] for u in core if u != v) for v in core}
    for color, blocks in ((1, red), (0, blue)):
        for index, B in enumerate(blocks):
            for v in sorted(core):
                missing = [w for w in B if a[v][w] != color]
                if len(missing) == 1:
                    w = missing[0]
                    gain = sum(a[w][u] for u in core if u != v)-d[v]
                    if gain > 0:
                        yield dict(color=color, block_index=index, vertex=v, displaced=w, gain=gain)


def augment(a, red, core):
    edges = [e for e in combinations(sorted(core), 2) if a[e[0]][e[1]]]
    for index, B in enumerate(red):
        for e, f in combinations(edges, 2):
            if set(e) & set(f):
                continue
            for S in combinations(B, 2):
                T = sorted(set(B)-set(S))
                if all(a[u][v] for u in S for v in e) and all(a[u][v] for u in T for v in f):
                    return index, list(S)+list(e), T+list(f), set(e+f)
    return None


def repair(a, red, blue, core):
    residual = sorted(sum(blue, [])+core)
    K = clique(a, residual, 4, 1)
    if K is not None:
        blue = []
        while K is not None:
            red.append(K); residual = sorted(set(residual)-set(K))
            K = clique(a, residual, 4, 1)
        core = residual
    K = clique(a, core, 4, 0)
    while K is not None:
        blue.append(K); core = sorted(set(core)-set(K))
        K = clique(a, core, 4, 0)
    return red, blue, core


def descend(a, red, blue, core):
    red, blue, core = [list(B) for B in red], [list(B) for B in blue], list(core)
    validate(a, red, blue, core)
    steps = []
    while True:
        before = potential(a, red, blue, core)
        move = augment(a, red, core)
        if move is not None:
            index, B1, B2, used = move
            old = red.pop(index); red.extend([B1, B2]); core = sorted(set(core)-used)
            event = dict(kind='TWO_EDGE_AUGMENTATION', old_block=old, new_blocks=[B1, B2])
        else:
            violation = next(violations(a, red, blue, core), None)
            if violation is None:
                break
            blocks = red if violation['color'] else blue
            B = blocks[violation['block_index']]
            v, w = violation['vertex'], violation['displaced']
            B[B.index(w)] = v; core[core.index(v)] = w
            red, blue, core = repair(a, red, blue, core)
            event = dict(kind='CORE_EDGE_EXCHANGE', **violation)
        validate(a, red, blue, core)
        after = potential(a, red, blue, core)
        need(after > before, 'non-increasing potential')
        steps.append(dict(event, before=list(before), after=list(after), red=[B[:] for B in red],
                          blue=[B[:] for B in blue], core=core[:]))
        if len(a) == 43 and len(red) >= 5:
            need(len(steps) <= 675, '43-vertex potential bound')
    return dict(status='NORMAL_PACKING_NO_RAMSEY_VERDICT', red=red, blue=blue, core=core, steps=steps)


def receiver_clauses(q, r, core_adjacency):
    """Exact clauses for ALL rows. Fixed core edges are a caller precondition.

    Positive variable means red, variables 1..903 enumerate u<v lexicographically.
    These clauses define a new global representative family, not learned clauses.
    """
    n = len(core_adjacency)
    need(7 <= q <= 10 and 5 <= r <= q and n == 43-4*q, 'task shape')
    variable = {e: i+1 for i, e in enumerate(combinations(range(43), 2))}
    def edge(u, v):
        return variable[tuple(sorted((u, v)))]
    C = list(range(4*q, 43))
    for b in range(q):
        color = int(b < r); B = list(range(4*b, 4*b+4))
        for v0, v in enumerate(C):
            d = sum(core_adjacency[v0])
            for w in B:
                # Guard: three block-color contacts, and one opposite contact.
                guard = [(edge(v, u) if color else -edge(v, u)) for u in B if u != w]
                guard.append(-edge(v, w) if color else edge(v, w))
                for S in combinations([u for u in C if u != v], d+1):
                    yield [-x for x in guard]+[-edge(w, u) for u in S]


def main():
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest='mode', required=True)
    d = sub.add_parser('descend'); d.add_argument('input'); d.add_argument('output')
    c = sub.add_parser('clauses'); c.add_argument('q', type=int); c.add_argument('r', type=int)
    c.add_argument('core_graph6'); c.add_argument('output')
    args = p.parse_args()
    if args.mode == 'descend':
        obj = json.loads(Path(args.input).read_text()); a = decode(obj)
        result = dict(descend(a, obj['red'], obj['blue'], obj['core']), graph=encode(a))
        Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    else:
        from catalog import adjacency
        a = adjacency(args.core_graph6.encode())
        count = 0
        with Path(args.output).open('w') as f:
            # Header count known without materializing clauses.
            from math import comb
            size = 4*args.q*sum(comb(len(a)-1, sum(row)+1) for row in a if sum(row)+1 <= len(a)-1)
            f.write('c GLOBAL NORMAL FORM ONLY: not an original-task Ramsey implicate\n')
            f.write(f'p cnf 903 {size}\n')
            for clause in receiver_clauses(args.q, args.r, a):
                f.write(' '.join(map(str, clause))+' 0\n'); count += 1
        need(count == size, 'clause count')

if __name__ == '__main__':
    main()
