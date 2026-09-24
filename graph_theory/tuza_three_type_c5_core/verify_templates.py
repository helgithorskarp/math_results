"""Independent exhaustive verifier: all 2^20 optional edge subsets.

No generator imports, search for graph homomorphisms, or external solver.
Failures remain active under python -O.
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(path):
    raw = Path(path).read_bytes()
    rows = json.loads(raw)
    protected = [(i, j) for i in range(7) for j in range(i + 1, 7)
                 if not ((i + 1) & (j + 1))]
    host = protected + [(i, j) for i in range(7) for j in (7, 8)] + [(7, 8)]
    certificates = {}
    for row in rows:
        require(isinstance(row, list) and len(row) == 4, "bad row")
        h, u, v, colors = row
        require(all(type(x) is int for x in (h, u, v)), "bad mask types")
        require(0 <= h < 64 and 0 <= u < 128 and 0 <= v < 128, "mask range")
        require(isinstance(colors, list) and len(colors) == 9
                and all(type(c) is int and 0 <= c < 5 for c in colors), "colors")
        require((h, u, v) not in certificates, "duplicate template")
        certificates[h, u, v] = colors
    seen, histogram = set(), Counter()
    triangle_free = 0
    for bits in range(1 << 20):
        h, u, v = bits & 63, (bits >> 6) & 127, (bits >> 13) & 127
        if u & v:  # a triangle on the distinguished edge
            continue
        edges = [e for i, e in enumerate(protected) if (h >> i) & 1]
        edges += [(i, 7) for i in range(7) if (u >> i) & 1]
        edges += [(i, 8) for i in range(7) if (v >> i) & 1]
        edges.append((7, 8))
        neighbors = [0] * 9
        for a, b in edges:
            neighbors[a] |= 1 << b
            neighbors[b] |= 1 << a
        if any(neighbors[a] & neighbors[b] for a, b in edges):
            continue
        triangle_free += 1
        if any(not ((neighbors[a] >> b) & 1) and not (neighbors[a] & neighbors[b])
               for a, b in host):
            continue
        key = (h, u, v)
        require(key in certificates, "missing maximal template")
        colors = certificates[key]
        require(all((colors[a] - colors[b]) % 5 in (1, 4) for a, b in edges),
                "invalid C5 map")
        seen.add(key)
        histogram[len(edges)] += 1
    require(seen == set(certificates), "spurious certificate row")
    require(len(seen) == 392, "unexpected maximal-template count")
    return {"optional_edge_subsets": 1 << 20, "triangle_free": triangle_free,
            "maximal_templates": len(seen), "all_map_to_C5": True,
            "edge_histogram": dict(sorted(histogram.items())),
            "certificate_sha256": sha256(raw).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(verify(Path(__file__).with_name("templates.json")), sort_keys=True))
