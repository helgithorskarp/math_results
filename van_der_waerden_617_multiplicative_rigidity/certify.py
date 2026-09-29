"""Independent exhaustive Boolean checker for the p=617 orbit frontier.

No SAT library is used. Orbit sets are constructed as multiplicative cosets,
and every finite-field progression is enumerated directly. The search uses
exact bit masks, unit propagation, and exhaustive binary branching.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import time

P = 617


def direct_edges(m):
    assert 616 % m == 0
    h = {pow(3, m*j, P) for j in range(616//m)}
    assert len(h) == 616//m
    ids = [-1] * P
    ids[0] = m
    for v in range(m):
        coset = {pow(3,v,P)*x % P for x in h}
        assert len(coset) == len(h)
        for x in coset:
            assert ids[x] == -1
            ids[x] = v
    assert all(x >= 0 for x in ids)
    edges = set()
    for d in range(1,P):
        for a in range(P):
            mask = 0
            for j in range(7):
                mask |= 1 << ids[(a+j*d) % P]
            edges.add(mask)
    return sorted(edges), ids


class Exhaustive:
    def __init__(self, limit):
        self.limit = limit
        self.nodes = 0
        self.conflicts = 0
        self.propagations = 0

    def run(self, edges, assigned, ones):
        assert ones & ~assigned == 0
        self.nodes += 1
        if self.nodes > self.limit:
            raise RuntimeError('INCOMPLETE: exhausted explicit node budget')
        active = edges
        while True:
            todo = []
            unit_zero = 0
            unit_one = 0
            zeros = assigned ^ ones
            for mask in active:
                has_one = mask & ones
                has_zero = mask & zeros
                if has_one and has_zero:
                    continue
                free = mask & ~assigned
                if free == 0:
                    self.conflicts += 1
                    return None
                if free & (free-1) == 0:
                    if not (has_one or has_zero):
                        self.conflicts += 1
                        return None  # A singleton cannot be non-monochromatic.
                    if has_one:
                        unit_zero |= free
                    else:
                        unit_one |= free
                else:
                    todo.append(mask)
            if unit_zero & unit_one:
                self.conflicts += 1
                return None
            if not (unit_one | unit_zero):
                active = todo
                break
            assigned |= unit_one | unit_zero
            ones |= unit_one
            self.propagations += (unit_one | unit_zero).bit_count()
            active = todo
        if not active:
            return (assigned,ones)
        # Choose a variable in a shortest unsatisfied edge, preferring frequency.
        smallest = min((mask & ~assigned).bit_count() for mask in active)
        freq = {}
        for mask in active:
            free = mask & ~assigned
            if free.bit_count() != smallest:
                continue
            while free:
                bit = free & -free
                freq[bit] = freq.get(bit,0) + 1
                free ^= bit
        var = max(freq, key=lambda x: (freq[x], -x))
        hit = self.run(active, assigned | var, ones)
        if hit is not None:
            return hit
        return self.run(active, assigned | var, ones | var)


def certify(m, limit):
    assert m in (8,28,44), 'This artifact certifies exactly indices 8, 28, 44.'
    start = time.monotonic()
    edges, ids = direct_edges(m)
    digest = hashlib.sha256('\n'.join(map(str,edges)).encode()).hexdigest()
    # Removing all progressions through zero weakens the constraints. Proving
    # rigidity of this weaker system proves rigidity for either color of zero.
    nz_edges = [S for S in edges if not S & (1 << m)]
    search = Exhaustive(limit)
    cases = []
    for first_deviation in range(1,m):
        assigned = (1 << (first_deviation+1))-1
        ones = sum(1 << v for v in range(first_deviation) if v % 2)
        if first_deviation % 2 == 0:
            ones |= 1 << first_deviation
        previous = search.nodes
        witness = search.run(nz_edges, assigned, ones)
        cases.append({'first_deviation': first_deviation, 'nodes':search.nodes-previous, 'unsat':witness is None})
        if witness:
            result = {'m':m,'status':'COUNTEREXAMPLE_TO_RIGIDITY','partial_assignment':witness,'case':first_deviation}
            print(json.dumps(result),flush=True)
            return result
    qr = sum(1 << v for v in range(m) if v%2)
    assert all(S & qr and S & ~qr for S in nz_edges)
    result = {'p': P,'m':m,'full_edges':len(edges),'nonzero_edges':len(nz_edges),
              'direct_edge_masks_sha256':digest,'nodes':search.nodes,
              'conflicts':search.conflicts,'propagations':search.propagations,
              'first_deviation_cases':cases,'status':'RIGIDITY_CERTIFIED',
              'seconds':round(time.monotonic()-start,4)}
    print(json.dumps({k:v for k,v in result.items() if k != 'first_deviation_cases'},sort_keys=True),flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m',type=int,nargs='+',default=[8,28,44])
    ap.add_argument('--nodes',type=int,default=100000)
    ap.add_argument('--output')
    args = ap.parse_args()
    results = [certify(m,args.nodes) for m in args.m]
    if args.output:
        with open(args.output,'w') as f:
            json.dump(results,f,sort_keys=True,indent=2)
            f.write('\n')


if __name__ == '__main__':
    main()
