#!/usr/bin/env python3
"""Independent exact checker: direct set intersections, no generator import."""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED_HASH = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"
SATURATED = [0, 1, 2, 5, 7, 8, 9, 10, 12, 14, 15, 16]
EXCEPTIONS = [[0, 5], [7, 15], [12, 14]]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bits(mask):
    while mask:
        bit = mask & -mask
        mask -= bit
        yield bit.bit_length() - 1


def check_tree(tree, words, statistics):
    """Return every compatible 16-subset, checking exhaustive branch coverage."""
    witnessed = []

    def visit(node, active, chosen):
        statistics["tree_nodes"] += 1
        require(type(node) is dict, "malformed tree node")
        if set(node) == {"c"}:
            parts = node["c"]
            require(type(parts) is list and len(parts) < 16 - len(chosen),
                    "cover does not exclude a 16-subset")
            covered = 0
            for part in parts:
                require(type(part) is int and part > 0 and not (part & ~active)
                        and not (covered & part), "cover is not a disjoint subpartition")
                group = list(bits(part))
                for u, v in itertools.combinations(group, 2):
                    require(len(words[u] & words[v]) >= 3, "cover class is not conflicting")
                    statistics["cover_pair_checks"] += 1
                covered |= part
            require(covered == active, "cover omits an active word")
            statistics["cover_leaves"] += 1
            return
        if set(node) == {"w"}:
            witness = node["w"]
            require(type(witness) is list and all(type(v) is int for v in witness)
                    and witness == sorted(chosen) and len(chosen) == 16,
                    "wrong terminal witness")
            require(all(len(words[u] & words[v]) <= 2
                        for u, v in itertools.combinations(chosen, 2)),
                    "terminal witness is incompatible")
            witnessed.append(tuple(witness))
            statistics["witness_leaves"] += 1
            return
        require(set(node) == {"v", "i", "o"}, "unknown tree node")
        vertex = node["v"]
        require(type(vertex) is int and 0 <= vertex < len(words)
                and active >> vertex & 1 and len(chosen) < 16,
                "invalid branch vertex")
        next_active = sum(1 << v for v in bits(active)
                          if v != vertex and len(words[v] & words[vertex]) <= 2)
        visit(node["i"], next_active, chosen + [vertex])
        visit(node["o"], active & ~(1 << vertex), chosen)

    visit(tree, (1 << len(words)) - 1, [])
    require(len(witnessed) == len(set(witnessed)), "duplicate terminal witness")
    return witnessed


def verify(seed_path, certificate_path):
    raw = seed_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SEED_HASH, "wrong seed hash")
    rows = raw.decode("ascii").splitlines()
    require(len(rows) == 69 and all(len(s) == 18 and set(s) <= set("01")
                                  and s.count("1") == 5 for s in rows), "invalid seed rows")
    seed = [frozenset(p for p, c in enumerate(s) if c == "1") for s in rows]
    require(len(set(seed)) == 69, "duplicate seed")
    distances = Counter(2 * (5 - len(a & b)) for a, b in itertools.combinations(seed, 2))
    require(min(distances) == 6, "seed minimum distance is not six")
    degrees = [sum(p in w for w in seed) for p in range(18)]
    require([p for p, d in enumerate(degrees) if d == 20] == SATURATED,
            "unexpected saturated coordinates")
    universe = [frozenset(t) for t in itertools.combinations(range(18), 5)]
    require(len(universe) == 8568, "wrong complete universe size")
    certificate = json.loads(certificate_path.read_text())
    require(type(certificate) is dict
            and set(certificate) == {"schema", "seed_sha256", "cases"}
            and certificate["schema"] == "acl69-saturated-pair-classification-v1"
            and certificate["seed_sha256"] == SEED_HASH, "wrong certificate header")
    cases = certificate["cases"]
    expected_pairs = [list(p) for p in itertools.combinations(SATURATED, 2)]
    require(type(cases) is list and len(cases) == 66
            and all(type(c) is dict for c in cases)
            and [c.get("coordinates") for c in cases] == expected_pairs,
            "incomplete or reordered pair coverage")
    statistics = Counter()
    profiles = Counter()
    exceptions = []
    obstructions = []
    for case in cases:
        require(set(case) == {"coordinates", "mode", "proofs"}, "wrong case fields")
        p, q = case["coordinates"]
        core = [word for word in seed if p not in word and q not in word]
        require(len(core) == 34, "wrong retained-core size")
        residual = [word for word in universe if word not in core
                    and all(len(word & fixed) <= 2 for fixed in core)]
        residual.sort(key=lambda word: sum(1 << v for v in word))
        profiles[(len(residual), sum(p not in w and q not in w for w in residual))] += 1
        statistics["residual_word_occurrences"] += len(residual)
        proofs = case["proofs"]
        mode = case["mode"]
        require(mode in {"one-side", "coupled"} and type(proofs) is list,
                "unknown proof mode")
        avoids = [q] if mode == "one-side" else [q, p]
        require(len(proofs) == len(avoids), "wrong number of side proofs")
        classified = []
        sides = []
        for proof, avoid in zip(proofs, avoids):
            require(type(proof) is dict and set(proof) == {"avoid", "tree"}
                    and type(proof["avoid"]) is int and proof["avoid"] == avoid,
                    "wrong side orientation")
            words = [word for word in residual if avoid not in word]
            statistics["side_word_occurrences"] += len(words)
            classified.append(check_tree(proof["tree"], words, statistics))
            sides.append(words)
        if mode == "one-side":
            require(classified == [[]], "one-side classification has a 16-subset")
            statistics["one_side_pairs"] += 1
        else:
            require(not any(p not in w and q not in w for w in residual),
                    "coupled proof has a residual word avoiding both points")
            require(all(len(w) == 1 for w in classified), "side 16-subset is not unique")
            left = [sides[0][v] for v in classified[0][0]]
            right = [sides[1][v] for v in classified[1][0]]
            conflicts = [(a, b) for a in left for b in right if len(a & b) >= 3]
            require(conflicts, "unique side families have no cross-conflict")
            a, b = conflicts[0]
            obstructions.append({"coordinates": [p, q], "left": sorted(a),
                                 "right": sorted(b), "intersection": sorted(a & b),
                                 "cross_conflicts": len(conflicts)})
            exceptions.append([p, q])
            statistics["coupled_pairs"] += 1
    require(exceptions == EXCEPTIONS, "unexpected exceptional-pair classification")
    return {"claim": "Every code containing an ACL69 core avoiding two saturated coordinates has maximum size 69.",
            "external_dependency": "Brouwer (1975): A(17,6,4)=20; hence every point degree is at most 20.",
            "seed_sha256": SEED_HASH, "seed_size": 69, "seed_minimum_distance": min(distances),
            "seed_distance_histogram": {str(d): distances[d] for d in sorted(distances)},
            "saturated_coordinates": SATURATED, "pair_count": len(cases), "core_size": 34,
            "complete_universe_size": len(universe), "statistics": dict(sorted(statistics.items())),
            "residual_profiles": [{"words": n, "avoiding_both": z, "pairs": count}
                                  for (n, z), count in sorted(profiles.items())],
            "coupled_obstructions": obstructions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=Path, default=ROOT / "acl69.txt")
    parser.add_argument("--certificate", type=Path, default=ROOT / "certificates.json")
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    result = verify(args.seed, args.certificate)
    if args.expect:
        require(result == json.loads(args.expect.read_text()), "verification differs from expected output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
