"""Exact upper cap for every block-disjoint pair of STS(9).

Regenerates the complete finite cohort and checks two fixed rational matrices
by both Schur elimination and an independent integer polynomial computation.
No external census, solver, floating-point package, or tolerance is used.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from math import lcm
from pathlib import Path
import argparse
import copy
import json

from certificates import affine_sts9, check_sts, downset, mask
from verify import check_definition, exact_psd_rank, matrix_hash, rejects


def moved(a, p):
    return sum(1 << p[i] for i in range(9) if a >> i & 1)


def all_sts9():
    pairs = list(combinations(range(9), 2))
    index = {p: i for i, p in enumerate(pairs)}
    choices = [[] for _ in pairs]
    for t in combinations(range(9), 3):
        cover = sum(1 << index[p] for p in combinations(t, 2))
        for p in combinations(t, 2):
            choices[index[p]].append((mask(t), cover))
    systems = set()

    def recurse(uncovered, chosen):
        if not uncovered:
            key = tuple(sorted(chosen))
            assert key not in systems
            systems.add(key)
            return
        k = (uncovered & -uncovered).bit_length() - 1
        for triple, cover in choices[k]:
            if cover & uncovered == cover:
                recurse(uncovered ^ cover, chosen + (triple,))

    recurse((1 << len(pairs)) - 1, ())
    return systems


def relabelling_orbit(first):
    # Adjacent transpositions generate the entire symmetric group.
    perms = {first: tuple(range(9))}
    frontier = [first]
    while frontier:
        system = frontier.pop()
        for k in range(8):
            def swap(a):
                if bool(a >> k & 1) != bool(a >> (k + 1) & 1):
                    return a ^ ((1 << k) | (1 << (k + 1)))
                return a
            image = tuple(sorted(swap(a) for a in system))
            if image not in perms:
                perms[image] = tuple(k + 1 if x == k else k if x == k + 1 else x
                                     for x in perms[system])
                frontier.append(image)
    return perms


def affine_group():
    pts = list(product(range(3), repeat=2))
    index = {p: i for i, p in enumerate(pts)}
    group = []
    for a, b, c, d in product(range(3), repeat=4):
        if (a * d - b * c) % 3 == 0:
            continue
        for t, u in pts:
            group.append(tuple(index[((a*x+b*y+t) % 3, (c*x+d*y+u) % 3)]
                               for x, y in pts))
    assert len(set(group)) == 432
    return group


def complete_cohort(first):
    systems = all_sts9()
    perms = relabelling_orbit(first)
    assert set(perms) == systems and len(systems) == 840
    group = affine_group()
    assert 362880 // len(perms) == len(group)
    for p in group:
        assert tuple(sorted(moved(a, p) for a in first)) == first
    triple_masks = [mask(t) for t in combinations(range(9), 3)]
    maps = [{a: moved(a, p) for a in triple_masks} for p in group]
    disjoint = {t for t in systems if not set(t) & set(first)}
    remaining = set(disjoint)
    representatives = []
    while remaining:
        rep = min(remaining)
        images = {tuple(sorted(mp[a] for a in rep)) for mp in maps}
        assert images <= remaining
        representatives.append((rep, len(images), perms[rep]))
        remaining -= images
    assert len(disjoint) == 192
    assert [size for rep, size, p in representatives] == [144, 48]
    serial = json.dumps(sorted(systems), separators=(",", ":")).encode()
    return representatives, {"labelled_STS9": len(systems),
        "STS9_enumeration_sha256": sha256(serial).hexdigest(),
        "disjoint_second_systems": len(disjoint),
        "ordered_pair_orbit_sizes": [size for rep, size, p in representatives]}


def decode(first, case):
    second = case["second_blocks"]
    check_sts(9, first); check_sts(9, second)
    assert not set(first) & set(second)
    D = downset(9, [first, second]); n = len(D)
    assert n == 70
    group = [tuple(p) for p in case["automorphism_subgroup"]]
    assert group and len(set(group)) == len(group)
    assert all(sorted(p) == list(range(9)) for p in group)
    assert all(tuple(p[q[i]] for i in range(9)) in group for p in group for q in group)
    assert all({moved(a, p) for a in D} == set(D) for p in group)
    table = {}
    for a, b, w in case["orbit_entries"]:
        assert a in D and b in D and a <= b and not a & b
        assert (a, b) not in table
        table[a, b] = F(w)
    Q = [[F(17 if i == j and i else 0) for j in range(n)] for i in range(n)]
    used = set()
    for i, a in enumerate(D):
        for j in range(i, n):
            b = D[j]
            if a & b:
                continue
            rep = min(tuple(sorted((moved(a, p), moved(b, p)))) for p in group)
            assert rep in table
            used.add(rep)
            Q[i][j] = Q[j][i] = table[rep]
    assert used == set(table)
    return D, Q


def polynomial_psd(Q):
    """PSD via coefficients of det(tI+A), A an integer multiple of Q.

    Faddeev-LeVerrier/Newton recurrence, independent of Schur pivots.
    Symmetry makes all eigenvalues real. Nonnegative coefficients exclude a
    positive polynomial root, hence exclude a negative eigenvalue of A.
    """
    n = len(Q)
    assert all(len(row) == n for row in Q)
    assert all(Q[i][j] == Q[j][i] for i in range(n) for j in range(n))
    scale = lcm(*(F(x).denominator for row in Q for x in row))
    A = [[int(F(x) * scale) for x in row] for row in Q]
    sparse = [[(k, a) for k, a in enumerate(row) if a] for row in A]
    B = [[int(i == j) for j in range(n)] for i in range(n)]
    coeff = [1]
    for k in range(1, n + 1):
        columns = list(zip(*B))
        AB = [[sum(a * col[h] for h, a in row) for col in columns] for row in sparse]
        numerator = -sum(AB[i][i] for i in range(n))
        c, rem = divmod(numerator, k)
        assert rem == 0, "Newton coefficient is not integral"
        for i in range(n):
            AB[i][i] += c
        B = AB
        plus = c if k % 2 == 0 else -c
        if plus < 0:
            raise ValueError("negative det(tI+A) coefficient")
        coeff.append(plus)
        if not any(x for row in B for x in row):
            coeff.extend([0] * (n - k))
            break
    rank = max(k for k, c in enumerate(coeff) if c)
    digest = sha256(json.dumps(coeff, separators=(",", ":")).encode()).hexdigest()
    return {"rank": rank, "integer_scale": scale, "polynomial_sha256": digest}


def ordinary_partition(first, second, first_to_second):
    pts = list(product(range(3), repeat=2))
    index = {p: i for i, p in enumerate(pts)}
    classes = []
    for dx, dy in [(0, 1), (1, 0), (1, 1), (1, 2)]:
        lines = sorted({mask(index[((x+t*dx) % 3, (y+t*dy) % 3)] for t in range(3))
                        for x, y in pts})
        assert len(lines) == 3
        classes.append(lines)
    assert sorted(a for c in classes for a in c) == list(first)
    classes += [[moved(a, first_to_second) for a in c] for c in classes[:4]]
    assert sorted(a for c in classes[4:] for a in c) == list(second)
    for c in range(9):
        classes.append([1 << c] + [mask(((c+i) % 9, (c-i) % 9)) for i in range(1, 5)])
    D = downset(9, [first, second])
    assert len(classes) == 17 and sorted(a for c in classes for a in c) == sorted(D[1:])
    assert all(not a & b for c in classes for a, b in combinations(c, 2))
    assert [len(c) for c in classes] == [3] * 8 + [5] * 9
    empty_Q = 17 * sum(len(c)**2 for c in classes) - 69**2 + 1
    assert empty_Q == 289 > 70
    return {"classes": 17, "class_sizes": [3] * 8 + [5] * 9,
            "uncapped_empty_Q": empty_Q}


def run():
    data = json.loads(Path(__file__).with_name("two9_certificates.json").read_text())
    first = tuple(data["first_blocks"])
    assert first == tuple(affine_sts9()) and (data["N"], data["s"]) == (70, 17)
    reps, result = complete_cohort(first)
    assert [list(rep) for rep, size, p in reps] == [c["second_blocks"] for c in data["cases"]]
    result["matrices"] = []
    for case, (rep, size, p) in zip(data["cases"], reps):
        D, Q = decode(first, case)
        rank = check_definition(D, 17, Q)
        assert rank == case["expected_rank_Q"] == 60
        assert all(x == 1 for x in Q[0])
        upper = [[F(70 if i == j else 0) - Q[i][j] for j in range(70)] for i in range(70)]
        upper_rank = exact_psd_rank(upper)
        assert upper_rank == case["expected_rank_upper"] == 69
        lower_poly = polynomial_psd(Q)
        upper_poly = polynomial_psd(upper)
        assert lower_poly["rank"] == rank and upper_poly["rank"] == upper_rank
        result["matrices"].append({"N": 70, "s": 17, "rank_Q": rank,
            "rank_upper": upper_rank, "matrix_sha256": matrix_hash(Q),
            "subgroup_order": len(case["automorphism_subgroup"]),
            "orbit_entry_count": len(case["orbit_entries"]),
            "lower_polynomial": lower_poly, "upper_polynomial": upper_poly,
            "ordinary_partition_baseline": ordinary_partition(first, rep, p)})
    bad = copy.deepcopy(data["cases"][0])
    bad["orbit_entries"][0][2] = str(F(bad["orbit_entries"][0][2]) + 1)
    def check_damaged_weight():
        damaged_D, damaged_Q = decode(first, bad)
        return check_definition(damaged_D, 17, damaged_Q)
    rejects(check_damaged_weight)
    bad = copy.deepcopy(data["cases"][0])
    bad["second_blocks"] = bad["second_blocks"][:-1]
    rejects(lambda: decode(first, bad))
    rejects(lambda: polynomial_psd([[F(0), F(1)], [F(1), F(0)]]))
    rejects(lambda: polynomial_psd([[F(-1)]]))
    assert polynomial_psd([[F(1), F(0)], [F(0), F(0)]])["rank"] == 1
    result["new_rejection_controls"] = 4
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = run()
    if args.check:
        assert output == json.loads(Path(__file__).with_name("two9_expected.json").read_text())
    print(json.dumps(output, indent=2, sort_keys=True))
