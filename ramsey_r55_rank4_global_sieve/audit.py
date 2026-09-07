"""Exact cross-checks: independent counts, exhaustive matrices and graph controls."""
from collections import Counter
from itertools import product, combinations
from math import comb
from copy import deepcopy
import json
import random
import counts
import independent_counts as independent
import model
from extract import extract, clique
from verify import decode, verify


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def dense_rank(rows):
    a = [list(x) for x in rows]
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for i in range(len(a)):
            if i != r and a[i][j]:
                a[i] = [x ^ y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def count_audit():
    checks = 0
    for r in range(5):
        for m in range(25):
            for cap in (1, 2, 4, 5, 24):
                require(counts.nonzero_span(m, r, cap) == independent.spanning(m, r, cap), "span mismatch")
                checks += 1
                if r and m:
                    require(counts.affine_span(m, r, cap) == independent.affine(m, r-1, cap), "affine mismatch")
                    checks += 1
    result = counts.compute()
    for row, params in zip(result["stages"], [(20, 23, 20, 23), (20, 23, 1, 2), (4, 23, 1, 2), (4, 5, 1, 2)]):
        raw, low = independent.stage(20, 23, 4, *params)
        require(raw == row["raw_zero_filtered"] and low == row["complement_rank_three_overlap"], "stage mismatch")
        checks += 2
    total_a = sum(comb(20, z)*independent.spanning(20-z, 4, 20) for z in range(21))
    total_b = sum(comb(23, z)*independent.spanning(23-z, 4, 23) for z in range(24))
    require(total_a*total_b//20160 == result["rank4_total"], "total mismatch")
    return {"exact_count_comparisons": checks+1, "counts": result}


def matrices():
    number = queries = complement_cases = 0
    for m, n in [(2, 3), (3, 3), (3, 4), (4, 3)]:
        hist = Counter()
        for bits in range(2**(m*n)):
            a = [[(bits >> (i*n+j)) & 1 for j in range(n)] for i in range(m)]
            r = dense_rank(a)
            number += 1
            if not r:
                continue
            b = [[1-x for x in row] for row in a]
            br = dense_rank(b)
            ra = [tuple(row) for row in a]
            co = list(zip(*a))
            z1, z2 = ra.count((0,)*n), co.count((0,)*m)
            if z1 and z2:
                continue
            ca = max(v for k, v in Counter(ra).items() if any(k))
            cb = max(v for k, v in Counter(co).items() if any(k))
            hist[r, ca, cb, z1, z2, br] += 1
            if br == r-1:
                require(z1 == z2 == 0, "rank drop with a zero")
                complement_cases += 1
        for r in range(1, min(m, n)+1):
            for ac, bc, az, bz in product(range(1, m+1), range(1, n+1), range(m+1), range(n+1)):
                selected = [(key, value) for key, value in hist.items()
                            if key[0] == r and key[1] <= ac and key[2] <= bc and key[3] <= az and key[4] <= bz]
                raw = sum(value for key, value in selected)
                low = sum(value for key, value in selected if key[-1] == r-1)
                require(raw == counts.pair_count(m, n, r, ac, bc, az, bz), "physical matrix count mismatch")
                require(low == counts.lower_complement(m, n, r, ac, bc), "physical rank-drop count mismatch")
                queries += 2
    # Complete fibers of the 3x4 rank-two factor map: exactly |GL(2,2)|=6.
    fiber = Counter()
    for a in product(range(4), repeat=3):
        if dense_rank([[(x >> j) & 1 for j in range(2)] for x in a]) != 2:
            continue
        for b in product(range(4), repeat=4):
            if dense_rank([[(x >> j) & 1 for j in range(2)] for x in b]) != 2:
                continue
            physical = sum(model.dot(x, y) << (i*4+j) for i, x in enumerate(a) for j, y in enumerate(b))
            fiber[physical] += 1
    require(set(fiber.values()) == {6}, "wrong factor fiber size")
    require(len(fiber) == counts.total_span(3, 2)*counts.total_span(4, 2)//6, "missing fibers")
    return {"exhaustive_matrices": number, "matrix_count_comparisons": queries,
            "physical_complement_rank_drop_cases": complement_cases,
            "complete_rank_two_fibers": len(fiber), "factor_pairs": sum(fiber.values())}


def rejected(call):
    try:
        call()
    except (ValueError, ArithmeticError):
        return
    raise ArithmeticError("corruption accepted")


def physical_controls():
    a = list(range(1, 16))+list(range(1, 6))
    b = list(range(1, 16))+list(range(1, 9))
    base = {"rows": a, "columns": b, "internal_hex": "0"*111}
    require(model.classify(base) == {"baseline": True, "keep": True, "reason": "survives_necessary_filter"}, "keeper lost")
    cases = [
        ([0, 0]+list(range(1, 16))+[1, 2, 3], b, "zero_multiplicity"),
        (a, [0]*3+list(range(1, 16))+[1, 2, 3, 4, 5], "zero_multiplicity"),
        ([1]*5+list(range(2, 16))+[2], b, "row_class"),
        (a, [1]*6+list(range(2, 16))+[2, 3, 4], "column_class"),
    ]
    rng = random.Random(43112023)
    certificates = basis_checks = negative = 0
    fixture = None
    for av, bv, reason in cases:
        for _ in range(16):
            data = {"rows": av[:], "columns": bv[:], "internal_hex": format(rng.getrandbits(443), "0111x")}
            rng.shuffle(data["rows"])
            rng.shuffle(data["columns"])
            require(model.classify(data) == {"baseline": True, "keep": False, "reason": reason}, "wrong rejection branch")
            graph, cert = extract(data)
            require(verify(graph, cert) == "VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE", "certificate failed")
            certificates += 1
            if fixture is None:
                fixture = {"parameters": data, "graph": graph, "certificate": cert}
            # Basis change represented by a bijective linear map f; construct dual map by its defining identity.
            while True:
                basis = [rng.randrange(16) for _ in range(4)]
                if model.rank(basis) == 4:
                    break
            def f(x):
                z = 0
                for j in range(4):
                    if (x >> j) & 1:
                        z ^= basis[j]
                return z
            dual = {y: next(z for z in range(16) if all(model.dot(f(1 << j), z) == ((y >> j) & 1) for j in range(4))) for y in range(16)}
            changed = {"rows": [f(x) for x in data["rows"]], "columns": [dual[y] for y in data["columns"]], "internal_hex": data["internal_hex"]}
            require(model.physical(changed) == graph and model.classify(changed) == model.classify(data), "basis dependence")
            basis_checks += 1
            bad = deepcopy(cert)
            bad["color"] = "blue" if cert["color"] == "red" else "red"
            rejected(lambda: verify(graph, bad))
            negative += 1
    # Every within-side coordinate has one and only one physical pair.
    base_bits = int(model.physical(base)["red_hex"], 16)
    for k, pair in enumerate(model.INTERNAL):
        data = dict(base, internal_hex=format(1 << k, "0111x"))
        delta = base_bits ^ int(model.physical(data)["red_hex"], 16)
        require(delta == 1 << model.PAIRS.index(pair), "internal coordinate not physical")
    # Dense, independently decoded verification of all 460 cross contacts.
    adj = decode(model.physical(base))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            expected = sum(((x >> k) & 1)*((y >> k) & 1) for k in range(4)) % 2
            require(adj[i][20+j] == bool(expected), "wrong cross contact")
    # Previously excluded families, including the exact affine omission.
    prior = deepcopy(base)
    prior["rows"][0] = prior["columns"][0] = 0
    require(model.classify(prior)["reason"] == "previous_zero_pair", "old zero branch missing")
    prior = deepcopy(base)
    h = [x for x in range(16) if x & 1]
    prior["rows"] = (h*3)[:20]
    prior["columns"] = (h*3)[:23]
    require(model.classify(prior)["reason"] == "previous_complement_rank", "old rank branch missing")
    prior = deepcopy(base)
    prior["columns"] = list(range(1, 16))+h
    require(model.classify(prior)["reason"] == "previous_affine_family", "old affine branch missing")
    malformed = []
    for key, value in [("rows", [1]*20), ("columns", b[:-1]), ("internal_hex", "0"*110), ("internal_hex", "f"*111)]:
        malformed.append(dict(base, **{key: value}))
    bad = deepcopy(base)
    bad["rows"][0] = True
    malformed.append(bad)
    malformed.append(dict(base, extra=1))
    for data in malformed:
        rejected(lambda: model.physical(data))
        negative += 1
    g, c = fixture["graph"], fixture["certificate"]
    for bad in [{}, dict(c, extra=1), dict(c, vertices=[0]*5), dict(c, vertices=[0, 1, 2, 3, 43])]:
        rejected(lambda: verify(g, bad))
        negative += 1
    rejected(lambda: extract(base))
    negative += 1
    return {"physical_certificates": certificates, "basis_changes": basis_checks,
            "internal_coordinates": 443, "cross_coordinates": 460,
            "rejected_corruptions_or_out_of_scope": negative, "fixture": fixture}


def elementary():
    signatures = 0
    for x, y, z in product((0, 1), repeat=3):
        require(x*y+x*z+(1-y)*(1-z) == int(x == y == z)+x, "triple identity")
        signatures += 1
    # At each contact pattern to five vertices, at most nine triples are distinguished.
    max_dist = 0
    for bits in product((0, 1), repeat=5):
        d = sum(len({bits[i] for i in t}) == 2 for t in combinations(range(5), 3))
        max_dist = max(max_dist, d)
    require(max_dist == 9 and 20+9*(20-5) < 170, "five-class inequality")
    require(34 > (20-2)+13 and 54 > 2*23+4, "zero class inequalities")
    # Exhaustively compare the certificate extractor's clique primitive with literal subsets.
    comparisons = 0
    pairs = list(combinations(range(5), 2))
    for bits in range(2**10):
        for color in (0, 1):
            rows = [0]*5
            for k, (u, v) in enumerate(pairs):
                if ((bits >> k) & 1) == color:
                    rows[u] |= 1 << v
                    rows[v] |= 1 << u
            for size in range(1, 6):
                found = clique(rows, 31, size)
                literal = any(all((rows[u] >> v) & 1 for u, v in combinations(vs, 2)) for vs in combinations(range(5), size))
                require((found is not None) == literal, "clique primitive mismatch")
                if found is not None:
                    require(len(found) == size and all((rows[u] >> v) & 1 for u, v in combinations(found, 2)), "wrong clique")
                comparisons += 1
    return {"mixed_triple_signatures": signatures, "five_contact_signatures": 32,
            "literal_clique_comparisons": comparisons}


def run():
    return {"status": "VERIFIED_RANK4_GLOBAL_SIEVE", "arithmetic": count_audit(),
            "matrices": matrices(), "physical": physical_controls(), "elementary": elementary()}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
