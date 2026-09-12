"""Independent definition-level receiver; imports no producer module.

Reconstructs an entire chain using explicit rectangle traversal, checks actual
physical witness vertices, and produces/rechecks the short RUP closure.
The small positive controls are exhaustive literal five/four-set checks.
"""
import argparse
from functools import cache
from itertools import combinations
import json
from pathlib import Path


def require(test, reason):
    if not test:
        raise ValueError(reason)


def local_chains(red):
    parts = [[0]]
    for dimension in range(4):
        updated = []
        for seq in parts:
            for offset in range(min(2, len(seq))):
                items = [(i, offset) for i in range(len(seq)-offset)]
                items += [(len(seq)-1-offset, j) for j in range(offset+1, 2)]
                updated.append([seq[i]+(j << dimension) for i, j in items])
        parts = updated
    return [[x for x in seq if x != (15 if red else 0)] for seq in parts]


@cache
def completions(remaining, length):
    if remaining == 0:
        return 1
    # Enumerate actual local chains, without the producer's length distribution.
    return sum(completions(remaining-1, length+len(c)-1-2*t)
               for c in local_chains(True) for t in range(min(length, len(c))))


def expand(packet):
    f = packet['frame']
    n, q, r = f['n'], f['q'], f['r']
    require(all(type(x) is int for x in (n, q, r)) and 1 <= r <= q and n >= 4*q,
            'frame dimensions')
    pairs = list(combinations(range(n), 2))
    ids = {e: k for k, e in enumerate(pairs)}
    fixed = int(f['fixed_hex'], 16)
    require(0 <= fixed < 1 << len(pairs), 'physical word range')
    stars = [(b, v) for b in range(q) for v in range(4*q, n)]
    require(len(packet['path']) == len(stars), 'path dimensions')
    free = {ids[u, v] for b, v in stars for u in range(4*b, 4*b+4)}
    require(not any(fixed >> k & 1 for k in free), 'canonical fixed frame')
    for b in range(q):
        require(all((fixed >> ids[e] & 1) == int(b < r)
                    for e in combinations(range(4*b, 4*b+4), 2)), 'block colors')
    root = []
    for a, b in combinations(range(q), 2):
        vs = list(range(4*a, 4*a+4))+list(range(4*b, 4*b+4))
        for s in combinations(vs, 5):
            require(len({fixed >> ids[e] & 1 for e in combinations(s, 2)}) == 2,
                    'pair domain')
        if a == 0:
            values = [sum((fixed >> ids[u, 4*b+j] & 1) << u for u in range(4))
                      for j in range(4)]
            require(all(values[j] >= values[j+1] for j in range(3)), 'column order')
            root.append(sum((fixed >> ids[u, 4*b+j] & 1) << (4*u+j)
                            for u in range(4) for j in range(4)))
    for seq in (root[:r-1], root[r-1:]):
        require(all(x >= y for x, y in zip(seq, seq[1:])), 'block order')
    states, rank = [fixed], 0
    for i, ((b, v), choice) in enumerate(zip(stars, packet['path'])):
        j, t = choice
        parts = local_chains(b < r)
        require(type(j) is int and 0 <= j < len(parts), 'local chain ID')
        seq = parts[j]
        a = len(states)
        require(type(t) is int and 0 <= t < min(a, len(seq)), 'hook ID')
        for jj, part in enumerate(parts):
            for tt in range(min(a, len(part))):
                if (jj, tt) < (j, t):
                    rank += completions(len(stars)-i-1, a+len(part)-1-2*tt)
        coords = [(x, t) for x in range(a-t)]
        coords += [(a-t-1, y) for y in range(t+1, len(seq))]
        states = [states[x] | sum((seq[y] >> u & 1) << ids[4*b+u, v] for u in range(4))
                  for x, y in coords]
    require(rank == packet['chain_index'], 'chain index mismatch')
    require(len(states) == packet['length'], 'chain length')
    mobile = []
    for x, y in zip(states, states[1:]):
        delta = x ^ y
        require(x & ~y == 0 and delta.bit_count() == 1, 'nonsaturated physical chain')
        mobile.append(delta.bit_length()-1)
    require(len(set(mobile)) == len(mobile), 'repeated chain edge')
    return n, r, pairs, ids, states, mobile


def unit_conflict(clauses, assumptions=()):
    assignment = {}
    def put(lit):
        v, b = abs(lit), lit > 0
        if v in assignment:
            return assignment[v] != b
        assignment[v] = b
        return False
    for x in assumptions:
        if put(x):
            return True
    while True:
        changed = False
        for clause in clauses:
            if any(assignment.get(abs(x)) == (x > 0) for x in clause if abs(x) in assignment):
                continue
            todo = [x for x in clause if abs(x) not in assignment]
            if not todo:
                return True
            if len(todo) == 1:
                if put(todo[0]):
                    return True
                changed = True
        if not changed:
            return False


def check(packet):
    require(packet['format'] == 'mc1', 'packet version')
    n, r, pairs, ids, states, mobile = expand(packet)
    k, length = packet['cut'], len(states)
    require(type(k) is int and 0 <= k <= length, 'cut range')
    clauses = [(-(j+1), j) for j in range(1, length-1)]
    sources = []
    def witness(vs, color, position):
        require(isinstance(vs, list) and vs == sorted(set(vs)) and
                all(type(v) is int and 0 <= v < n for v in vs), 'witness vertices')
        require(len(vs) == 5 or (color == 1 and len(vs) == 4 and min(vs) >= 4*r),
                'not an actual parent forbidden set')
        es = [ids[e] for e in combinations(vs, 2)]
        require(all((states[position] >> e & 1) == color for e in es), 'false witness')
        # Restrict actual monochromatic-forbidding clause to this chain.
        restricted = tuple((-1 if color else 1)*(mobile.index(e)+1)
                           for e in es if e in mobile)
        require(all((states[0] >> e & 1) == color for e in es if e not in mobile),
                'fixed colors contradict parent-clause origin')
        clauses.append(restricted)
        sources.append(dict(vertices=vs, forbidden_color=color, restricted=list(restricted)))
    if k:
        witness(packet['blue'], 0, k-1)
    else:
        require(packet['blue'] is None, 'unexpected lower witness')
    if packet['status'] == 'GOOD_GRAPH':
        require(k < length and packet['red'] is None, 'positive packet cut')
        require(int(packet['red_hex'], 16) == states[k], 'positive graph mismatch')
        word = states[k]
        for size, vs, colors in ((5, range(n), (0, 1)), (4, range(4*r, n), (1,))):
            for s in combinations(vs, size):
                values = {word >> ids[e] & 1 for e in combinations(s, 2)}
                require(not any(values == {c} for c in colors), 'positive forbidden set')
        return dict(status='VERIFIED_GOOD_GRAPH', n=n, length=length, cut=k), None, None
    require(packet['status'] == 'CLOSED_CHAIN', 'unknown packet status')
    if k < length:
        witness(packet['red'], 1, k)
    else:
        require(packet['red'] is None, 'unexpected upper witness')
    proof = [(k,)] if 0 < k < length else []
    proof.append(())
    database = list(clauses)
    for clause in proof:
        require(unit_conflict(database, [-x for x in clause]), 'RUP rejection')
        database.append(clause)
    cnf = 'p cnf %d %d\n' % (max(1, length-1), len(clauses))
    cnf += ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)
    drat = ''.join(' '.join(map(str, c))+' 0\n' for c in proof)
    return dict(status='VERIFIED_CLOSED_CHAIN', n=n, length=length, cut=k,
                parent_witness_clauses=sources, proof_lines=len(proof)), cnf, drat


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('packet')
    p.add_argument('--proof-prefix', help='Write restricted CNF and RUP proof')
    a = p.parse_args()
    result, cnf, drat = check(json.loads(Path(a.packet).read_text()))
    if a.proof_prefix and cnf is not None:
        Path(a.proof_prefix+'.cnf').write_text(cnf)
        Path(a.proof_prefix+'.drat').write_text(drat)
    print(json.dumps(result, indent=2, sort_keys=True))
