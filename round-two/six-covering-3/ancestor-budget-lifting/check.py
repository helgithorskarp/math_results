"""Literal checks for an ancestor-budget lifting lemma.

Author: six-covering-3, researcher. Standard library only. The all-weight
implication is the written proof; this checker replays the pinned descendant
certificate and checks the concrete ancestors and simultaneous phase orbit.
"""
import argparse
import hashlib
import importlib.util
from itertools import permutations, product
import json
from math import gcd
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / "node622-budget-obstruction"
PINS = {
    "check.py": "82aa8f53e20d851711bbcba8cfecc3bf754b36cbc967748cfcd7f683298d800a",
    "certificate.json": "c08fcc3754c69296f8ef79e88e849f7439e23875fd4bb1781306c53b189abd25",
    "expected.json": "960cbfaef13e70a5b7b4a43eaed3b1a479bce34ca47fab3568e014ab06c1ccc9",
    "proof.md": "34deed446bbd1beaaa92a71f6d1d80fa746721399c98c1af82f96324c92bb67b",
}


def need(test, message):
    if not test:
        raise ValueError(message)


def check(data, prior_dir=PRIOR):
    for name, digest in PINS.items():
        need(hashlib.sha256((prior_dir / name).read_bytes()).hexdigest() == digest,
             "prior source pin mismatch: " + name)
    cert = json.loads((prior_dir / "certificate.json").read_text())
    Pprime = [tuple(pair) for pair in cert["fixture"]["anchors"]]
    need(data["descendant_anchors"] == [list(pair) for pair in Pprime],
         "wrong descendant anchors")
    need(data["beta"] == cert["beta"] == [107, 100], "wrong descendant beta")
    need(data["period_geometry"] == [10080, 288, 35, 48, 1680], "wrong geometry")
    root = [tuple(pair) for pair in data["root_anchors"]]
    need(root == Pprime[:5], "wrong ancestor root")
    ns = tuple(data["absorbed_resources"])
    need(ns == tuple(n for n, a in Pprime[5:]) == (16, 15, 32),
         "wrong absorbed resource identities or order")
    need(data["top_resources"] == cert["fixture"]["four_top_resources"],
         "wrong TOP resource identities")
    need(data["exact_eight_ancestor_count"] == 127, "wrong ancestor count")
    factors = data["orbit_factors"]
    need(len(factors) == len(ns) and all(len(set(f)) == len(f) for f in factors)
         and all(type(a) is int and 0 <= a < n for n, f in zip(ns, factors) for a in f),
         "invalid orbit factors")

    # Verify every imported executable byte before import. Its rational phase
    # certificate is then replayed, not merely authenticated by the hash.
    spec = importlib.util.spec_from_file_location("prior8857", prior_dir / "check.py")
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)
    prior = p.check(cert)
    need(prior == json.loads((prior_dir / "expected.json").read_text()),
         "prior certificate replay differs from its published expected record")

    N, B, C, T, Q = data["period_geometry"]
    mass = [p.balanced_mass(mask) for mask in range(64)]
    telescoping = 0
    for U, F, H in product(range(64), repeat=3):
        left = mass[U] - mass[U & ~(F | H)]
        right = mass[U] - mass[U & ~F] + mass[U & ~F] - mass[U & ~F & ~H]
        need(left == right, "deletion increments fail telescoping")
        need(left <= mass[U] - mass[U & ~H] + mass[F],
             "joint deletion exceeds separate restoration bound")
        telescoping += 1
    for U, F in product(range(64), repeat=2):
        need(mass[U] - mass[U & ~F] >= 0, "negative restoration cost")
    proper_patterns = 0
    for period in (1, 2, 3):
        for mask in range(64):
            if all(bool(mask & (1 << j)) == bool(mask & (1 << ((j + period) % 6)))
                   for j in range(6)):
                for h in permutations((-1, 0, 1)):
                    m = sum(1 + (-1) ** j * h[j % 3]
                            for j in range(6) if mask & (1 << j))
                    need(m == mask.bit_count(), "proper-period balanced mass changed")
                proper_patterns += 1

    Uprime = [[0] * C for _ in range(T)]
    for x in range(N):
        if all(x % n != a for n, a in Pprime):
            Uprime[x % T][x % C] |= 1 << ((x % B) // T)
    Rprime = cert["fixture"]["available_moduli"]
    ancestor_records = []
    for code in range(1, 1 << 7):
        A = [pair for i, pair in enumerate(Pprime[1:]) if code & (1 << i)]
        P = [pair for pair in Pprime if pair not in A]
        need(min(n for n, a in P) == 8 and (8, 0) in P, "exact-eight anchor changed")
        U = [[0] * C for _ in range(T)]
        F = [[0] * C for _ in range(T)]
        r = [all(x % n != a for n, a in P) for x in range(N)]
        hits = [any(x % n == a for n, a in A) for x in range(N)]
        for x in range(N):
            if r[x]:
                U[x % T][x % C] |= 1 << ((x % B) // T)
            if hits[x]:
                F[x % T][x % C] |= 1 << ((x % B) // T)
        need(all(U[q][z] & ~F[q][z] == Uprime[q][z]
                 for q in range(T) for z in range(C)), "ancestor deletion changed descendant")
        resources = [n for n in range(8, N + 1) if N % n == 0 and n not in dict(P)]
        need(set(resources) == set(Rprime) | {n for n, a in A},
             "ancestor resource family incomplete")
        need(all(gcd(n, B) < B for n, a in A), "absorbed resource is not outside")
        # Diagnostic arbitrary, non-stabilizer-invariant weights. These checks
        # do not replace the universal telescoping proof or prior all-weight lemma.
        u = [(x * 7 + code) % 13 if r[x] else 0 for x in range(N)]
        v = [(y * 11 + code) % 7 for y in range(Q)]
        off = [w if not hits[x] else 0 for x, w in enumerate(u)]
        dp = sum(u) + sum(mass[U[y % T][y % C]] * v[y] for y in range(Q))
        dc = sum(off) + sum(mass[Uprime[y % T][y % C]] * v[y] for y in range(Q))
        cost = sum(u) - sum(off) + sum(
            (mass[U[y % T][y % C]] - mass[Uprime[y % T][y % C]]) * v[y]
            for y in range(Q))
        need(dp == dc + cost and cost >= 0, "literal demand restoration identity fails")
        ancestor_records.append({"removed_moduli": [n for n, a in A], "residual": sum(r)})
    need(len(ancestor_records) == data["exact_eight_ancestor_count"], "incomplete ancestors")

    # Complete simultaneous tuple action of the explicitly generated root
    # subgroup. No product of independent one-resource orbits is assumed.
    tuples = list(product(*(range(n) for n in ns)))
    index = {t: i for i, t in enumerate(tuples)}
    dsu = p.DSU(len(tuples))
    generators = p.swaps(N, root)
    divisors = [n for n in range(1, N + 1) if N % n == 0]
    for gen in generators:
        permutation = [p.image(x, N, gen) for x in range(N)]
        need(len(set(permutation)) == N, "root generator is not bijective")
        maps = {n: [permutation[a] % n for a in range(n)] for n in set(divisors) | {Q}}
        for n, mapping in maps.items():
            need(all(permutation[x] % n == mapping[x % n] for x in range(N)),
                 "root generator changes a divisor class family")
        block_maps = {}
        for x, y in enumerate(permutation):
            need(all((x % n == a) == (y % n == a) for n, a in root),
                 "root prescribed class moved")
            key, target = (x % T, x % C), (y % T, y % C)
            j, jj = (x % B) // T, (y % B) // T
            if key not in block_maps:
                block_maps[key] = (target, {}, {})
            to, row, col = block_maps[key]
            need(to == target, "primitive block split")
            need(j % 2 not in row or row[j % 2] == jj % 2,
                 "root row action is not independent")
            need(j % 3 not in col or col[j % 3] == jj % 3,
                 "root column action is not independent")
            row[j % 2], col[j % 3] = jj % 2, jj % 3
        need(len({value[0] for value in block_maps.values()}) == Q,
             "root block permutation not bijective")
        for to, row, col in block_maps.values():
            need(set(row.values()) == {0, 1} and set(col.values()) == {0, 1, 2},
                 "invalid root grid action")
        for i, t in enumerate(tuples):
            dsu.join(i, index[tuple(maps[n][a] for n, a in zip(ns, t))])
    seed = tuple(a for n, a in Pprime[5:])
    orbit = [t for i, t in enumerate(tuples) if dsu.root(i) == dsu.root(index[seed])]
    need(set(orbit) == set(product(*factors)) and len(orbit) == 256,
         "wrong complete simultaneous no-separation orbit")
    raw = ("\n".join(",".join(map(str, t)) for t in orbit) + "\n").encode()
    return {
        "agent": "six-covering-3", "role": "researcher",
        "status": "EXACT LIFTING HYPOTHESES CHECK PASSED",
        "prior_graph": 8857, "prior_certificate_verified": prior,
        "all_mask_telescoping_and_subadditive_bounds": telescoping,
        "all_mask_nonnegative_restoration_costs": 4096,
        "proper_period_pattern_vertex_checks": proper_patterns * 6,
        "exact_eight_ancestors": len(ancestor_records),
        "root_anchors": [list(pair) for pair in root], "absorbed_resources": list(ns),
        "root_actual_phase_family": len(tuples), "root_generators": len(generators),
        "all_divisor_class_families_literally_preserved": len(divisors),
        "root_phase_orbits": len(dsu.orbits()),
        "distinguished_orbit": {"size": len(orbit), "factors_in_resource_order": factors,
                                "ordered_sha256": hashlib.sha256(raw).hexdigest()},
        "scope": "Ancestor no-separation for specified mixed budgets; no nonextendibility or permission to prune covering branches",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("application", type=Path, nargs="?", default=HERE / "application.json")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    result = check(json.loads(args.application.read_text()))
    expected = json.loads((HERE / "expected.json").read_text())
    need(result == expected, "computed record differs from published expected record")
    if args.out:
        args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    print(json.dumps({"seconds": round(time.monotonic() - start, 3),
                      "peak_self_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
