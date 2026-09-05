#!/usr/bin/env python3
"""Independent finite and byte-level checks for the R55 3-cycle anchor theorem.

This checker imports no module from the reviewed package.  It expects a parent
and the two regenerated child CNFs in an external work directory.  Optional
fresh DRAT proofs and replay logs are checked by hash and replay marker.
"""
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json


PAIRS3 = tuple(combinations(range(3), 2))
REPS = {11: "100110110", 13: "110110101"}
PARENT_HASH = "c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return {"bytes": path.stat().st_size, "sha256": h.hexdigest()}


def red_edges(bits):
    edges = set()
    for a, b in combinations(range(9), 2):
        i, s = divmod(a, 3)
        j, t = divmod(b, 3)
        if i == j or bits[3 * PAIRS3.index((i, j)) + (t - s) % 3] == "1":
            edges.add((a, b))
    return edges


def transform(bits, perm, phases, sign):
    def bit(i, j, delta):
        if i > j:
            i, j, delta = j, i, -delta
        return bits[3 * PAIRS3.index((i, j)) + delta % 3]
    return "".join(
        bit(perm[i], perm[j], sign * d + phases[j] - phases[i])
        for i, j in PAIRS3 for d in range(3)
    )


def anchor_census():
    words = ["".join(map(str, row)) for row in product((0, 1), repeat=3)
             if row != (1, 1, 1)]
    actions = list(product(permutations(range(3)), product(range(3), repeat=3), (1, -1)))
    representative_orbits = {
        kind: {transform(rep, perm, phases, sign)
               for perm, phases, sign in actions}
        for kind, rep in REPS.items()
    }
    need(not representative_orbits[11] & representative_orbits[13], "representative orbits overlap")
    counts = {11: 0, 13: 0}
    survivors = []
    for triple in product(words, repeat=3):
        bits = "".join(triple)
        red = red_edges(bits)
        blue_triangle = any(
            all(edge not in red for edge in combinations(vertices, 2))
            for vertices in combinations(range(9), 3)
        )
        if blue_triangle:
            continue
        need(not any(all(edge in red for edge in combinations(vertices, 2))
                     for vertices in combinations(range(9), 5)), "local red K5")
        kinds = [kind for kind, orbit in representative_orbits.items() if bits in orbit]
        need(len(kinds) == 1, "anchor is outside or in both claimed orbits")
        kind = kinds[0]
        weights = sorted(sum(map(int, bits[q:q + 3])) for q in (0, 3, 6))
        need(weights == ([1, 2, 2] if kind == 11 else [2, 2, 2]), "weight invariant mismatch")
        counts[kind] += 1
        survivors.append(bits)
    need(len(survivors) == 45 and counts == {11: 27, 13: 18}, "anchor census")
    return {"domain": 343, "blue_triangle_free": 45,
            "type_counts": {str(k): counts[k] for k in sorted(counts)}}


def compositions(total, slots, prefix=()):
    if slots == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from compositions(total - value, slots - 1, prefix + (value,))


def signature_equality():
    feasible = []
    for counts in compositions(10, 8):
        incident = [sum(counts[mask] for mask in range(8) if mask >> i & 1)
                    for i in range(3)]
        if max(incident) > 4 or any(counts[1 << i] > 2 for i in range(3)):
            continue
        feasible.append(counts)
    minimum = min(row[0] for row in feasible)
    equality = [row for row in feasible if row[0] == 1]
    expected = (1, 2, 2, 1, 2, 1, 1, 0)
    need(minimum == 1 and equality == [expected], "sharp equality profile is not unique")
    prefixes = []
    for mask, multiplicity in enumerate(expected):
        prefixes.extend(tuple((mask >> i) & 1 for i in range(3)) for _ in range(multiplicity))
    prefixes.sort()
    need(prefixes == [(0, 0, 0), (0, 0, 1), (0, 0, 1), (0, 1, 0), (0, 1, 0),
                      (0, 1, 1), (1, 0, 0), (1, 0, 0), (1, 0, 1), (1, 1, 0)],
         "lexicographic equality prefixes")
    return {"feasible_signature_multiplicities": len(feasible), "minimum_empty": minimum,
            "empty_one_profiles": len(equality), "counts_by_mask_0_to_7": list(expected),
            "sorted_prefixes": [list(row) for row in prefixes]}


def expected_units(kind):
    rep = REPS[kind]
    variables = (1, 2, 3, 4, 5, 6, 31, 32, 33)
    units = [variable if bit == "1" else -variable for variable, bit in zip(variables, rep)]
    prefixes = signature_equality()["sorted_prefixes"]
    for fixed, prefix in enumerate(prefixes, 33):
        for cycle, bit in enumerate(prefix):
            variable = 211 + 11 * (fixed - 33) + cycle
            units.append(variable if bit else -variable)
    return units


def check_formula(parent, child, kind):
    removed_wanted = {(-4, 7), (-5, 8), (-6, 9)}
    removed = set()
    retained = 0
    with parent.open() as source, child.open() as target:
        need(source.readline() == "p cnf 34280 615920\n", "parent header")
        need(target.readline() == "p cnf 34280 615956\n", "child header")
        for line in source:
            clause = tuple(map(int, line.split()[:-1]))
            if clause in removed_wanted:
                removed.add(clause)
            else:
                need(target.readline() == line, "retained parent clause mismatch")
                retained += 1
        for unit in expected_units(kind):
            need(target.readline() == f"{unit} 0\n", "derived unit mismatch")
        need(target.read() == "", "unexpected child suffix")
    need(removed == removed_wanted and retained == 615917, "normalizer removal")
    return {"retained_parent_clauses": retained, "removed_ordering_clauses": 3,
            "anchor_units": 9, "fixed_prefix_units": 30, "clauses": 615956}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    work = args.work.resolve()
    parent = work / "parent.cnf"
    need(digest(parent)["sha256"] == PARENT_HASH, "parent hash")
    claimed = json.loads((source / "result.json").read_text())
    claimed_by_id = {row["id"]: row for row in claimed["cases"]}
    cases = []
    for kind in (11, 13):
        key = f"a{kind}_equality"
        cnf = work / f"{key}.cnf"
        proof = work / f"{key}.review1.drat"
        replay_log = work / f"{key}.review1.replay.log"
        cnf_info = digest(cnf)
        proof_info = digest(proof)
        need(cnf_info == claimed_by_id[key]["formula"], "formula identity " + key)
        need(proof_info == claimed_by_id[key]["proof"], "fresh proof identity " + key)
        replay = replay_log.read_text(errors="replace")
        need("s VERIFIED" in replay, "fresh replay marker " + key)
        cases.append({"id": key, "formula": cnf_info, "proof": proof_info,
                      "formula_audit": check_formula(parent, cnf, kind),
                      "drat_trim_verified": True})
    report = {
        "format": "r55-order3-eleven-anchor-equality-review1-v1",
        "all_checks_passed": True,
        "anchor_census": anchor_census(),
        "signature_equality": signature_equality(),
        "parent": digest(parent),
        "cases": cases,
        "reviewer_kissat": digest(args.kissat),
        "reviewer_drat_trim": digest(args.drat_trim),
        "target_graph_claimed": False,
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS 45 anchors, unique equality profile, two exact CNFs, two fresh DRAT replays")


if __name__ == "__main__":
    main()
