"""Independent semantic and witness audit of the paired-prefix lemma."""

import hashlib
import itertools
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "additive_combinatorics/schur6_paired_prefix_obstruction"


def schur(word, modulus=None):
    n = len(word)
    ordinary = doubling = 0
    for z in range(2, n + 1):
        for x in range(1, z // 2 + 1):
            y = z - x
            assert len({word[x - 1], word[y - 1], word[z - 1]}) > 1, (x, y, z)
            ordinary += 1
            doubling += x == y
    modular = 0
    if modulus is not None:
        for x in range(1, modulus):
            for y in range(x, modulus):
                z = (x + y) % modulus
                if z:
                    assert len({word[x - 1], word[y - 1], word[z - 1]}) > 1
                    modular += 1
    return ordinary, doubling, modular


def paired(word):
    for q in range(len(word) // 5 + 1):
        for start, special in ((5*q + 1, (0, 1)), (5*q + 3, (1, 0))):
            values = word[start - 1:min(start + 1, len(word))]
            if values:
                assert values == list(special[:len(values)]) or (
                    len(set(values)) == 1 and values[0] in (2, 3, 4))


def witnesses():
    data = json.loads((SOURCE / "witnesses.json").read_text())
    prefix = data["prefix109"]["word"]
    assert len(prefix) == 109 and set(prefix) == set(range(5))
    paired(prefix)
    assert schur(prefix) == (2970, 54, 0)
    full = data["full334"]["word"]
    assert len(full) == 334 and set(full) == set(range(6))
    assert schur(full, 335) == (27889, 167, 55778)
    assert all(full[x - 1] == full[335 - x - 1] for x in range(1, 335))
    for q in range(67):
        low = full[5*q:5*q + 2]
        assert low == [0, 1] or low[0] == low[1] and low[0] in (2, 3, 4, 5)
    assert [full.count(c) for c in range(6)] == [44, 44, 110, 52, 44, 40]
    assert full.index(2) + 1 == 110
    assert {q for q in range(67) if full[5*q] == 2} == set(range(23, 45))
    t = {22} | set(range(24, 34))
    assert {q for q in range(1, 67) if full[5*q - 1] == 2} == t | {67 - q for q in t}
    return len(prefix), len(full)


def canonical_cnf():
    with tempfile.TemporaryDirectory(prefix="paired-review-") as tmp:
        cnf = Path(tmp) / "instance.cnf"
        cmd = [sys.executable, "-B", "-c",
               "from pathlib import Path; from prove import instance; "
               "Path(__import__('sys').argv[1]).write_bytes(instance()[2])", str(cnf)]
        subprocess.run(cmd, cwd=SOURCE, check=True, capture_output=True, text=True)
        raw = cnf.read_bytes()
    assert len(raw) == 131765
    assert hashlib.sha256(raw).hexdigest() == "627bb81fd23127c3f4276f536b892b93dd7eb52b8e440c3781882a75472db71c"
    lines = raw.decode("ascii").splitlines()
    assert lines.pop(0).split() == ["p", "cnf", "286", "7827"]
    clauses = []
    for line in lines:
        values = [int(x) for x in line.split()]
        assert values and values[-1] == 0 and 0 not in values[:-1]
        clause = tuple(sorted(values[:-1]))
        assert clause and len(clause) == len(set(clause))
        assert all(1 <= abs(x) <= 286 for x in clause)
        clauses.append(clause)
    assert len(clauses) == len(set(clauses)) == 7827
    return set(clauses)


def semantic_cnf():
    rows = []
    point = {}
    group = {}
    next_var = 0
    for x in range(1, 111):
        q, b = divmod(x, 5)
        key = ("axis" if b == 0 else "lower" if b < 3 else "upper", q)
        if key not in group:
            labels = range(5) if b == 0 else (0, 2, 3, 4)
            row = {}
            for state in labels:
                next_var += 1
                row[state] = next_var
            group[key] = row
            rows.append(row)
        row = group[key]
        if b == 0:
            for c in range(5): point[x, c] = row[c]
        else:
            special = 0 if b in (1, 4) else 1
            point[x, special] = row[0]
            for c in (2, 3, 4): point[x, c] = row[c]
    assert next_var == 286
    clauses = set()
    for row in rows:
        clauses.add(tuple(sorted(row.values())))
        for a, b in itertools.combinations(row.values(), 2):
            clauses.add(tuple(sorted((-a, -b))))
    schur_clauses = set()
    for z in range(2, 111):
        for x in range(1, z // 2 + 1):
            y = z - x
            for c in range(5):
                if all((v, c) in point for v in (x, y, z)):
                    schur_clauses.add(tuple(sorted({-point[v, c] for v in (x, y, z)})))
    clauses.update(schur_clauses)
    for i, row in enumerate(rows):
        for c in (3, 4):
            clauses.add(tuple(sorted([-row[c]] + [earlier[c - 1] for earlier in rows[:i]])))
    assert len(clauses) == 7827
    return clauses, len(schur_clauses)


def boundary_and_split():
    interval = set(range(37, 73))
    caps = []
    for d in range(1, 23):
        seen = set()
        cap = 0
        for v in interval:
            if v in seen: continue
            path = []
            cur = v
            while cur - d in interval: cur -= d
            while cur in interval:
                path.append(cur)
                seen.add(cur)
                cur += d
            cap += (len(path) + 1) // 2
        assert seen == interval
        caps.append(cap)
    assert caps == [18, 18, 18, 20, 20, 18, 21, 20, 18, 20, 22, 24,
                    23, 22, 21, 20, 19, 18, 19, 20, 21, 22]
    C = set(range(37, 49)) | set(range(61, 73))
    assert len(C) == 24
    assert all((x + y) % 109 not in C and (-1 - x - y) % 109 not in C
               for x in C for y in C)
    diff = {(x - y) % 109 for x in C for y in C}
    assert diff == {0} | {sign*d % 109 for d in list(range(1, 12)) + list(range(13, 36))
                          for sign in (-1, 1)}
    allowed = {min(q, 109 - q) for q in range(1, 109) if q not in diff}
    assert allowed == {12} | set(range(36, 55))
    candidates = list(range(36, 55))

    def axis_free(reps):
        E = {q for r in reps for q in (r, 109 - r)}
        return all((x + y) % 109 not in E for x in E for y in E)

    assert axis_free((12,))
    assert all(axis_free((12, q)) for q in candidates)
    bad_pairs = {frozenset((u, v)) for u, v in itertools.combinations(candidates, 2)
                 if not axis_free((12, u, v))}
    for u, v, w in itertools.combinations(candidates, 3):
        if not any(pair <= {u, v, w} for pair in bad_pairs):
            assert axis_free((12, u, v, w))
    edges = [sum(1 << candidates.index(v) for v in pair) for pair in bad_pairs]
    valid = maximal = 0
    maximal_reps = []
    sizes = {}
    for mask in range(1 << len(candidates)):
        if any(mask & edge == edge for edge in edges): continue
        valid += 1
        if all(any((mask | 1 << bit) & edge == edge for edge in edges)
               for bit in range(len(candidates)) if not mask >> bit & 1):
            maximal += 1
            maximal_reps.append([12] + [q for bit, q in enumerate(candidates)
                                        if mask >> bit & 1])
            size = 2 * (1 + mask.bit_count())
            sizes[size] = sizes.get(size, 0) + 1
    assert (valid, maximal, sizes) == (21875, 64, {16: 2, 18: 10, 20: 20,
                                                   22: 20, 24: 10, 26: 2})
    for reps in maximal_reps:
        E = {q for r in reps for q in (r, 109 - r)}
        points = {5*q for q in E}
        for q in C:
            points.update((5*q + 1, 5*q + 2, 545 - 5*q - 1, 545 - 5*q - 2))
        assert all((x + y) % 545 not in points for x in points for y in points)
    axis = set(range(41, 69))
    A = set(range(39, 73)) - {63}
    B = set(range(37, 68)) | {77}
    pts = {5*q for q in axis}
    pts.update(5*q + 1 for q in A)
    pts.update(545 - 5*q - 1 for q in A)
    pts.update(5*q + 2 for q in B)
    pts.update(545 - 5*q - 2 for q in B)
    assert len(pts) == 158 and min(pts) == 158
    assert all((x + y) % 545 not in pts for x in pts for y in pts)
    D = A ^ B
    U = set(range(22)) | set(range(87, 109))
    lower = {q for q in range(109) if 5*q + 2 <= 110}
    reflected = {108 - r for r in range(109) if 5*r + 4 <= 110}
    assert lower | reflected == U
    assert D == {37, 38, 63, 68, 69, 70, 71, 72, 77} and not D & U
    assert len(U) == 44
    return max(caps), len(allowed), len(pts), maximal


def main():
    witness_lengths = witnesses()
    generated = canonical_cnf()
    semantic, forbidden = semantic_cnf()
    assert generated == semantic
    bound = boundary_and_split()
    print(f"PASS prefix={witness_lengths[0]} full={witness_lengths[1]} "
          f"cnf_clauses={len(generated)} schur_clause_patterns={forbidden} "
          f"capacity={bound[0]} axis_orbit_options={bound[1]} "
          f"split_class_points={bound[2]} maximal_axis_sets={bound[3]} "
          f"exact_semantics=yes")


if __name__ == "__main__":
    main()
