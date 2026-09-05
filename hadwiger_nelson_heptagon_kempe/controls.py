"""Exhaust the component-union criterion on every graph on three vertices."""
from itertools import combinations, product
import json
from audit import groups, proper
from run import components

cases = 0
union_colourings = 0
all_edges = list(combinations(range(3), 2))
for mask in range(8):
    edges = [e for i, e in enumerate(all_edges) if mask >> i & 1]
    adj = [set() for _ in range(3)]
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    for c in product(range(4), repeat=3):
        if not proper(c, edges, 3):
            continue
        for a, b in combinations(range(4), 2):
            blocks = list(components(adj, c, a, b))
            assert blocks == groups(3, edges, c, a, b)
            block_of = {v: i for i, block in enumerate(blocks) for v in block}
            possible = set()
            for bits in range(1 << len(blocks)):
                changed = list(c)
                for i, block in enumerate(blocks):
                    if bits >> i & 1:
                        for v in block:
                            changed[v] ^= a ^ b
                assert proper(changed, edges, 3)
                union_colourings += 1
                possible.update((u, v) for u, v in all_edges if changed[u] == changed[v])
            for u, v in all_edges:
                if c[u] != c[v]:
                    predicted = ({c[u], c[v]} == {a, b} and block_of[u] != block_of[v])
                    assert predicted == ((u, v) in possible)
                    cases += 1
print(json.dumps({'graphs': 8, 'different_colour_pair_cases': cases,
                  'component_union_colourings': union_colourings,
                  'status': 'ALL SMALL CONTROLS PASSED'}, indent=2))
