"""Exact physical chain receiver. Forbidden-set witnesses, never solver status."""
import argparse
from functools import cache
from itertools import combinations
import json
from pathlib import Path
from chains import Product


@cache
def edges(n):
    return tuple(combinations(range(n), 2))


def clique(word, n, size, color, vertices=None):
    """Deterministic bitset clique finder; independent checker is literal."""
    adj = [0]*n
    for k, (u, v) in enumerate(edges(n)):
        if (word >> k & 1) == color:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    def visit(candidates, need, chosen):
        if need == 0:
            return chosen
        while candidates.bit_count() >= need:
            bit = candidates & -candidates
            v = bit.bit_length()-1
            candidates ^= bit
            found = visit(candidates & adj[v], need-1, chosen+[v])
            if found is not None:
                return found
        return None
    mask = sum(1 << v for v in (range(n) if vertices is None else vertices))
    return visit(mask, size, [])


class Frame:
    """All non-star physical edges fixed, including the entire arbitrary core.

    Production scope is n=43, q=7..10, r=5..q (original), or q=8, r=5..8
    (physical). Smaller parameters are accepted solely for exact controls.
    A core-catalog index/guard is external metadata, validated at its bridge.
    """
    def __init__(self, n, q, r, fixed_hex):
        if not all(type(x) is int for x in (n, q, r)) or not (1 <= r <= q and n >= 4*q):
            raise ValueError('frame parameters')
        self.n, self.q, self.r = n, q, r
        self.fixed = int(fixed_hex, 16)
        if not 0 <= self.fixed < 1 << len(edges(n)):
            raise ValueError('frame bit range')
        self.pairs = {e: k for k, e in enumerate(edges(n))}
        self.stars = [(b, v) for b in range(q) for v in range(4*q, n)]
        self.star_edges = [[self.pairs[4*b+j, v] for j in range(4)] for b, v in self.stars]
        self.mobile_domain = sum(1 << k for e in self.star_edges for k in e)
        if self.fixed & self.mobile_domain:
            raise ValueError('canonical frame requires all star bits zero')
        for b in range(q):
            for e in combinations(range(4*b, 4*b+4), 2):
                if (self.fixed >> self.pairs[e] & 1) != int(b < r):
                    raise ValueError('fixed block color')
        # Literal two-block domains and root/block orders; core is arbitrary.
        root_words = []
        for a, b in combinations(range(q), 2):
            vs = list(range(4*a, 4*a+4))+list(range(4*b, 4*b+4))
            for xs in combinations(vs, 5):
                colors = {self.fixed >> self.pairs[e] & 1 for e in combinations(xs, 2)}
                if len(colors) == 1:
                    raise ValueError('block-pair forbidden five')
            if a == 0:
                cols = [sum((self.fixed >> self.pairs[u, 4*b+v] & 1) << u
                            for u in range(4)) for v in range(4)]
                if cols != sorted(cols, reverse=True):
                    raise ValueError('root column order')
                root_words.append(sum((self.fixed >> self.pairs[u, 4*b+v] & 1) << (4*u+v)
                                      for u in range(4) for v in range(4)))
        for part in (root_words[:r-1], root_words[r-1:]):
            if part != sorted(part, reverse=True):
                raise ValueError('same-color whole-block order')
        self.product = Product([int(b < r) for b, _ in self.stars])

    def data(self):
        return dict(n=self.n, q=self.q, r=self.r, fixed_hex=format(self.fixed, 'x'))

    def graph(self, index, position):
        word = self.fixed
        for mask, star in zip(self.product.state(index, position), self.star_edges):
            for j, k in enumerate(star):
                word |= (mask >> j & 1) << k
        return word

    def decide(self, index):
        path, length = self.product.path(index)
        packet = dict(format='mc1', frame=self.data(), chain_index=index,
                      path=[[j, t] for _, _, j, t in path], length=length)
        top = self.graph(index, length-1)
        blue = clique(top, self.n, 5, 0)
        if blue is not None:
            return dict(packet, status='CLOSED_CHAIN', cut=length, blue=blue, red=None)
        lo, hi = 0, length-1
        while lo < hi:
            mid = (lo+hi)//2
            if clique(self.graph(index, mid), self.n, 5, 0) is None:
                hi = mid
            else:
                lo = mid+1
        k, word = lo, self.graph(index, lo)
        blue = clique(self.graph(index, k-1), self.n, 5, 0) if k else None
        red = clique(word, self.n, 5, 1)
        if red is None:
            red = clique(word, self.n, 4, 1, range(4*self.r, self.n))
        if red is not None:
            return dict(packet, status='CLOSED_CHAIN', cut=k, blue=blue, red=red)
        return dict(packet, status='GOOD_GRAPH', cut=k, blue=blue, red=None,
                    red_hex=format(word, 'x'))


def from_graph(n, q, r, word):
    pairs = {e: k for k, e in enumerate(edges(n))}
    for b in range(q):
        for v in range(4*q, n):
            for u in range(4*b, 4*b+4):
                word &= ~(1 << pairs[u, v])
    return Frame(n, q, r, format(word, 'x'))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('frame', help='JSON with n,q,r,fixed_hex')
    p.add_argument('chain', type=int)
    a = p.parse_args()
    print(json.dumps(Frame(**json.loads(Path(a.frame).read_text())).decide(a.chain),
                     indent=2, sort_keys=True))
