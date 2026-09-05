#!/usr/bin/env python3
"""Exhaustive small-graph controls for motif census and forest recognition."""
from itertools import combinations, permutations
import json
from motifs import adjacency, opposite_pairs, closed_walks, components, forest_union


def main():
    graphs = motifs = 0
    canonical = {'C4': [(0,1),(1,2),(2,3),(0,3)],
                 'diamond': [(0,1),(0,2),(0,3),(1,2),(1,3)]}
    labelled_patterns = {
        name: {frozenset(tuple(sorted((p[a],p[b]))) for a,b in pattern)
               for p in permutations(range(4))}
        for name, pattern in canonical.items()}
    for n in (4,5):
        vertices = [10+7*i for i in range(n)]
        pairs = list(combinations(vertices,2))
        for mask in range(1<<len(pairs)):
            edges = [e for i,e in enumerate(pairs) if mask>>i&1]
            adj = adjacency(vertices,edges)
            expected = []
            for block in combinations(vertices,4):
                induced = frozenset((i,j) for i,j in combinations(range(4),2)
                                    if block[j] in adj[block[i]])
                expected += [(name,block) for name,patterns in labelled_patterns.items() if induced in patterns]
            expected.sort()
            assert opposite_pairs(vertices,edges) == expected
            assert closed_walks(vertices,edges) == expected
            # A graph is a forest iff every nonempty induced subgraph has a vertex of degree <=1.
            direct = all(any(len(adj[v]&set(subset)) <= 1 for v in subset)
                         for size in range(1,n+1) for subset in combinations(vertices,size))
            assert forest_union(vertices,edges) == direct
            assert all(c['tree'] for c in components(vertices,edges)) == direct
            graphs += 1; motifs += len(expected)
    assert components([],[]) == [] and forest_union([],[])
    print(json.dumps(dict(labelled_graphs=graphs,induced_motif_occurrences=motifs,
                          empty_forest_checked=True,
                          status='BOTH MOTIF ENUMERATORS AND FOREST TESTS MATCH BRUTE FORCE'),indent=2))


if __name__ == '__main__':
    main()
