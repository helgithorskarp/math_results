#!/usr/bin/env python3
"""Generate exact good-Cayley(44) CNFs from four group presentations."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


GROUPS = ("c11_c4", "c11_v4", "c11_sd_c4", "c11_sd_v4")


class Group:
    def __init__(self, name):
        if name not in GROUPS:
            raise ValueError(name)
        self.name = name
        self.is_v4 = name in ("c11_v4", "c11_sd_v4")
        self.twisted = name in ("c11_sd_c4", "c11_sd_v4")
        if self.is_v4:
            self.elements = [(a, b, c) for c in range(2) for b in range(2)
                             for a in range(11)]
        else:
            self.elements = [(a, b) for b in range(4) for a in range(11)]
        self.index = {x: i for i, x in enumerate(self.elements)}
        assert self.elements[0] == ((0, 0, 0) if self.is_v4 else (0, 0))
        self.table = [[self.index[self._mul_tuple(x, y)] for y in self.elements]
                      for x in self.elements]
        self.inverse = []
        for i in range(44):
            candidates = [j for j in range(44)
                          if self.table[i][j] == 0 and self.table[j][i] == 0]
            if len(candidates) != 1:
                raise RuntimeError((name, i, candidates))
            self.inverse.append(candidates[0])

    def _mul_tuple(self, x, y):
        if self.is_v4:
            a, b, c = x
            d, e, f = y
            sign_d = -d if self.twisted and b else d
            return ((a + sign_d) % 11, b ^ e, c ^ f)
        a, b = x
        c, d = y
        sign_c = -c if self.twisted and (b & 1) else c
        return ((a + sign_c) % 11, (b + d) % 4)

    def diff(self, x, y):
        return self.table[self.inverse[x]][y]

    def inverse_orbits(self):
        unseen = set(range(1, 44))
        ans = []
        while unseen:
            x = min(unseen)
            orbit = tuple(sorted({x, self.inverse[x]}))
            ans.append(orbit)
            unseen.difference_update(orbit)
        return ans


def build(name):
    group = Group(name)
    orbits = group.inverse_orbits()
    orbit_var = {x: i + 1 for i, orbit in enumerate(orbits) for x in orbit}
    clauses = set()
    rooted_fives = 0
    for tail in combinations(range(1, 44), 4):
        rooted_fives += 1
        vertices = (0,) + tail
        used = sorted({orbit_var[group.diff(u, v)]
                       for u, v in combinations(vertices, 2)})
        clauses.add(tuple(used))
        clauses.add(tuple(-x for x in used))
    ordered = sorted(clauses, key=lambda c: (len(c), tuple(abs(x) for x in c), c))
    return group, orbits, rooted_fives, ordered


def main(outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    all_meta = []
    for name in GROUPS:
        group, orbits, rooted_fives, clauses = build(name)
        cnf = outdir / f"{name}.cnf"
        with cnf.open("w") as stream:
            stream.write(f"p cnf {len(orbits)} {len(clauses)}\n")
            for clause in clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
        raw = cnf.read_bytes()
        involutions = sum(group.inverse[x] == x for x in range(1, 44))
        meta = {
            "group": name,
            "order": 44,
            "rooted_five_sets": rooted_fives,
            "inverse_orbits": [list(x) for x in orbits],
            "variables": len(orbits),
            "nonidentity_involutions": involutions,
            "unique_clauses": len(clauses),
            "width_histogram": {str(k): v for k, v in sorted(Counter(map(len, clauses)).items())},
            "cnf_bytes": len(raw),
            "cnf_sha256": sha256(raw).hexdigest(),
        }
        (outdir / f"{name}.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
        all_meta.append(meta)
    (outdir / "FORMULAS.json").write_text(json.dumps(all_meta, indent=2, sort_keys=True) + "\n")
    print(json.dumps(all_meta, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: generate.py OUTDIR")
    main(Path(sys.argv[1]))
