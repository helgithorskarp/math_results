#!/usr/bin/env python3
"""Independent finite-matroid check; no imports from the symbolic producer."""
import argparse
from collections import Counter
from itertools import combinations
import json
from math import isqrt
from pathlib import Path

PRIME = 65537


def require(ok, message):
    if not ok:
        raise ValueError(message)


def nullvector(rows):
    """RREF mod PRIME. Return the normal if the six rows are independent."""
    m = [[x % PRIME for x in row] for row in rows]
    pivots = []
    for col in range(7):
        k = len(pivots)
        pick = next((i for i in range(k, 6) if m[i][col]), None)
        if pick is None:
            continue
        m[k], m[pick] = m[pick], m[k]
        inv = pow(m[k][col], -1, PRIME)
        m[k] = [x*inv % PRIME for x in m[k]]
        for i in range(6):
            if i != k:
                factor = m[i][col]
                m[i] = [(x-factor*y) % PRIME for x, y in zip(m[i], m[k])]
        pivots.append(col)
        if len(pivots) == 6:
            break
    if len(pivots) != 6:
        return None
    free = next(i for i in range(7) if i not in pivots)
    out = [0]*7
    out[free] = 1
    for i, col in enumerate(pivots):
        out[col] = -m[i][free] % PRIME
    return out


def check(path):
    cert = json.loads(path.read_text())
    require(cert["schema"] == "two-scale-rank-five-faces-v1", "schema")
    A = [(1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1)]
    B = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)]
    require(cert["A_rays"] == list(map(list, A)) and cert["B_rays"] == list(map(list, B)), "rays")
    rows = [(1, *(r*x for x in v), 0, 0, 0) for r in (1, 2) for v in A]
    rows += [(1, 0, 0, 0, *(r*x for x in v)) for r in (1, 2) for v in B]
    require(all(sum(x*x for x in row) <= 13 for row in rows), "Hadamard hypothesis")
    require(13**4 < PRIME and all(PRIME % d for d in range(2, isqrt(PRIME)+1)), "prime or determinant bound")
    found = set()
    independent = 0
    tried = 0
    for indices in combinations(range(16), 6):
        tried += 1
        n = nullvector([rows[i] for i in indices])
        if n is None:
            continue
        independent += 1
        mask = sum(1 << i for i, row in enumerate(rows) if sum(x*y for x, y in zip(row, n)) % PRIME == 0)
        require(mask != 65535, "configuration does not have affine rank six")
        found.add(mask)
    masks = cert["maximal_face_masks"]
    require(masks == sorted(set(masks)), "mask ordering or duplicates")
    require(found == set(masks), "face certificate is not the full finite matroid")
    counts = dict(sorted(Counter(m.bit_count() for m in found).items()))
    require({str(k): v for k, v in counts.items()} == cert["face_size_counts"], "size counts")
    require(tried == 8008 and len(found) == 208, "enumeration totals")
    return {"six_subsets": tried, "independent_six_subsets": independent,
            "faces": len(found), "sizes": counts, "prime": PRIME,
            "scope": "exact r0=1,r1=2 matroid; universal parameters use written proof"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path, default=Path(__file__).with_name("CERTIFICATE.json"))
    print(json.dumps(check(parser.parse_args().certificate), sort_keys=True))
