"""Generic residual geometry, with credited SHA-pinned mask algorithms.

No pilot interval or private corpus is imported. The literal candidate
decoder and triple-resource graph are compared with the mask graph.
"""
from itertools import combinations

from bindings import load, v
from verify import joint

residual = load('published_residual_algorithms', 'residual.py',
                '783baef7f3a9df7dcfe3b353d89c8140538169b488b39475866166127a75fec2')


def literal_graph(core):
    words = [v.points(mask) for mask in core['blocks']]
    joint(words)
    v.check(v.sha(sorted(core['blocks'])) == core['core_sha256'], 'literal residual core binding')
    candidates = [q for q in combinations(range(15), 5)
                  if all(len(frozenset(q) & w) <= 2 for w in words)]
    triples = [{frozenset(t) for t in combinations(q, 3)} for q in candidates]
    adjacent = [{j for j, b in enumerate(triples) if i != j and a.isdisjoint(b)}
                for i, a in enumerate(triples)]
    return words, candidates, adjacent
