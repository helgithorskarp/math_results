"""Independent full enlarged P7 row domain; no researcher-code imports."""
from itertools import combinations, product
import json
from pathlib import Path
from star_primitives import canonical, positive_compositions, flags, unit_types, require, digest

HERE = Path(__file__).resolve().parent


def domain():
    graphs, units = unit_types(json.loads((HERE/'fixtures.json').read_text())['stars'])
    refined = set()
    for h in (3, 4, 5):
        for edges in combinations(tuple(combinations(range(h), 2)), h-1):
            if h == 5 and canonical(5, edges) not in graphs:
                continue
            for deficit in positive_compositions(5, h):
                for hubs in product(range(-1, h), repeat=3):
                    high = tuple(v for v in hubs if v >= 0)
                    if len(set(high)) != len(high):
                        continue
                    d = tuple(deficit[v] if v >= 0 else 0 for v in hubs)
                    q = sum(bool(set(edge)&set(high)) for edge in edges)
                    refined.add(d+(5-h, q, h-len(high))+flags(deficit, edges, hubs))
    refined = tuple(sorted(refined))
    coarse = tuple(sorted({r[:6] for r in refined}))
    return coarse, refined, units
