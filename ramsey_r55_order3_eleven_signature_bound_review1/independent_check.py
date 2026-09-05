#!/usr/bin/env python3
"""Clean-room checker for the sharp three-triangle signature reduction.

This file deliberately imports no module from the reviewed contribution.  It
checks the finite arithmetic, the three public sharpness graphs, the primary
orbit numbering, every appended SAT clause, and (unless requested otherwise)
the one claimed DRAT refutation.
"""

from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from json import dump
from pathlib import Path
import re
import subprocess


CORE_WORDS = {
    8: "100100100",
    11: "100110110",
    13: "110110101",
}
EXPECTED_HASHES = {
    "parent.cnf": "82f27b524e893d237f7a478c43bc9d49ff559faaa28e260d688d1591bdfaad20",
    "c8.cnf": "057a61e851efe4bc213dbbf17017d3c13716cc0db3b9099c28f397cfdbb301ef",
    "c11.cnf": "edcb237d03e46805495c5151f4589d44543f0450c30564108bbefb7dea2905e1",
    "c13.cnf": "3e795444d8ce43c10c52f20f382b0f981605f47223fc24204a22e8553c132236",
    "c8.drat": "fb650c6e0f945a9987b21591d2447f59a67625a15136f19995c65e75d67047b4",
    "drat-trim": "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a",
}
FIXED_SIGNATURES = (0, 1, 1, 2, 2, 3, 4, 4, 5, 6)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    h = sha256()
    size = 0
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
            size += len(block)
    return {"bytes": size, "sha256": h.hexdigest()}


def weak_compositions_ten_into_eight():
    """Stars-and-bars enumeration, unlike the submitted recursive generator."""
    for bars in combinations(range(17), 7):
        cuts = (-1,) + bars + (17,)
        yield tuple(cuts[i + 1] - cuts[i] - 1 for i in range(8))


def arithmetic_check():
    total = basic = stronger = 0
    histogram = [0] * 11
    extremizers = []
    for counts in weak_compositions_ten_into_eight():
        require(sum(counts) == 10, "bad stars-and-bars composition")
        total += 1
        incidence = tuple(sum(counts[s] for s in range(8) if s & (1 << i))
                          for i in range(3))
        singleton = (counts[1], counts[2], counts[4])
        if max(incidence) > 4 or max(singleton) > 2:
            continue
        basic += 1
        nonempty = 10 - counts[0]
        histogram[nonempty] += 1
        if nonempty == 9:
            extremizers.append(counts)
        if all(counts[1 << i] + counts[(1 << i) | (1 << j)] <= 3
               for i in range(3) for j in range(3) if i != j):
            stronger += 1

    expected_extremizer = (1, 2, 2, 1, 2, 1, 1, 0)
    require(total == 19448, "composition count")
    require(basic == 928 and stronger == 778, "admissible-profile counts")
    require(histogram == [1, 7, 28, 81, 189, 257, 226, 110, 28, 1, 0],
            "nonempty-signature histogram")
    require(extremizers == [expected_extremizer], "equality profile")

    # Check the algebraic equality conclusion directly, independently of the
    # census totals: every integer profile saturating N=9 has the stated data.
    equality_data = []
    for c in extremizers:
        x = (c[1], c[2], c[4])
        y = (c[3], c[5], c[6])
        z = c[7]
        incidence = tuple(sum(c[s] for s in range(8) if s & (1 << i))
                          for i in range(3))
        equality_data.append({"singletons": x, "pairs": y, "triple": z,
                              "incidences": incidence})
    require(equality_data == [{"singletons": (2, 2, 2), "pairs": (1, 1, 1),
                               "triple": 0, "incidences": (4, 4, 4)}],
            "equality-case multiplicities")
    return {
        "profiles": total,
        "basic_profiles": basic,
        "stronger_profiles": stronger,
        "nonempty_histogram": histogram,
        "unique_equality_profile": list(expected_extremizer),
        "equality_data": [{k: list(v) if isinstance(v, tuple) else v for k, v in row.items()}
                          for row in equality_data],
    }


def load_graph(path):
    rows = path.read_text().splitlines()
    require(rows, f"empty graph file: {path}")
    n, claimed_m = map(int, rows[0].split())
    edge_rows = [tuple(map(int, row.split())) for row in rows[1:]]
    require(n == 19, f"wrong order: {path}")
    require(len(edge_rows) == claimed_m == len(set(edge_rows)), f"bad edge count: {path}")
    require(all(0 <= a < b < n for a, b in edge_rows), f"bad edge endpoints: {path}")
    return n, set(edge_rows)


def red(edges, a, b):
    return tuple(sorted((a, b))) in edges


def inspect_fixture(path, core_index):
    n, edges = load_graph(path)
    red_fives = blue_fives = 0
    for vertices in combinations(range(n), 5):
        colors = [red(edges, a, b) for a, b in combinations(vertices, 2)]
        red_fives += all(colors)
        blue_fives += not any(colors)
    require(red_fives == blue_fives == 0, f"monochromatic K5: {path}")

    for i in range(3):
        require(all(red(edges, a, b) for a, b in combinations(range(3 * i, 3 * i + 3), 2)),
                f"minority triangle is not red: {path}")

    signatures = []
    for v in range(9, 19):
        mask = 0
        for i in range(3):
            colors = {red(edges, v, 3 * i + t) for t in range(3)}
            require(len(colors) == 1, f"nonuniform fixed attachment: {path}")
            if colors.pop():
                mask |= 1 << i
        signatures.append(mask)
    require(tuple(signatures) == FIXED_SIGNATURES, f"signature list: {path}")
    require(all(red(edges, a, b) == ((signatures[a - 9] & signatures[b - 9]) == 0)
                for a, b in combinations(range(9, 19), 2)), f"fixed graph rule: {path}")

    pairs = ((0, 1), (0, 2), (1, 2))
    words = "".join(str(int(red(edges, 3 * i, 3 * j + d)))
                    for i, j in pairs for d in range(3))
    require(words == CORE_WORDS[core_index], f"core word: {path}")

    def rho(v):
        return 3 * (v // 3) + (v + 1) % 3 if v < 9 else v

    require(all(red(edges, a, b) == red(edges, rho(a), rho(b))
                for a, b in combinations(range(n), 2)), f"order-three action: {path}")
    incidences = [sum(bool(s & (1 << i)) for s in signatures) for i in range(3)]
    require(incidences == [4, 4, 4], f"incidences: {path}")
    return {
        "index": core_index,
        "vertices": n,
        "red_edges": len(edges),
        "five_sets": 11628,
        "red_K5": red_fives,
        "blue_K5": blue_fives,
        "core_words": words,
        "signatures": signatures,
        "nonempty_signatures": sum(bool(s) for s in signatures),
        "incidences": incidences,
        "action_pairs": 171,
    }


def primary_variables():
    """Reconstruct primary edge-orbit IDs from the full 43-vertex action."""
    def rho(v):
        return 3 * (v // 3) + (v + 1) % 3 if v < 33 else v

    orbit_rep = {}
    representatives = set()
    for pair in combinations(range(43), 2):
        if pair[1] < 33 and pair[0] // 3 == pair[1] // 3:
            continue  # internal moving-cycle edges are the fixed red triangles
        orbit = []
        moved = pair
        while moved not in orbit:
            orbit.append(moved)
            moved = tuple(sorted((rho(moved[0]), rho(moved[1]))))
        representative = min(orbit)
        require(len(orbit) in (1, 3), "bad action-orbit length")
        representatives.add(representative)
        for member in orbit:
            orbit_rep[member] = representative

    def block(rep):
        a, b = rep
        if b < 33:
            return (0, a, b)       # moving--moving first
        if a >= 33:
            return (1, a, b)       # fixed--fixed second
        return (2, b, a)           # then fixed vertex, moving representative

    ordered = sorted(representatives, key=block)
    ids = {rep: i + 1 for i, rep in enumerate(ordered)}
    pair_id = {pair: ids[rep] for pair, rep in orbit_rep.items()}
    require(len(ordered) == 320, "primary-orbit count")
    require(len([x for x in ordered if x[1] < 33]) == 165, "moving-pair orbits")
    require(len([x for x in ordered if x[0] >= 33]) == 45, "fixed-pair orbits")
    return pair_id


def expected_appendix(core_index, pair_id):
    core_vars = [pair_id[tuple(sorted((3 * i, 3 * j + d)))]
                 for i, j in ((0, 1), (0, 2), (1, 2)) for d in range(3)]
    require(core_vars == [1, 2, 3, 4, 5, 6, 31, 32, 33], "core variable order")
    clauses = [(v if bit == "1" else -v,) for v, bit in zip(core_vars, CORE_WORDS[core_index])]

    def attachment(v, i):
        return pair_id[tuple(sorted((v, 3 * i)))]

    consequences = {(-attachment(33, i),) for i in range(3)}
    for fixed_set in combinations(range(33, 43), 3):
        for i in range(3):
            consequences.add(tuple(sorted(
                (-attachment(v, j) if j == i else attachment(v, j))
                for v in fixed_set for j in range(3))))
    for fixed_set in combinations(range(33, 43), 4):
        for i in range(3):
            for k in range(3):
                if i != k:
                    consequences.add(tuple(sorted(
                        literal for v in fixed_set
                        for literal in (-attachment(v, i), attachment(v, k)))))
    require(len(consequences) == 1623, "signature-consequence count")
    clauses += sorted(consequences, key=lambda row: (len(row), row))
    require(Counter(map(len, clauses)) == Counter({1: 12, 8: 1260, 9: 360}),
            "appendix width census")
    return clauses


def parse_header(line, path):
    fields = line.decode("ascii").split()
    require(len(fields) == 4 and fields[:2] == ["p", "cnf"], f"DIMACS header: {path}")
    return int(fields[2]), int(fields[3])


def parse_clause(line, path):
    fields = tuple(map(int, line.split()))
    require(fields and fields[-1] == 0 and 0 not in fields[:-1], f"DIMACS clause: {path}")
    return fields[:-1]


def audit_formula(parent_path, full_path, core_index, pair_id):
    expected = expected_appendix(core_index, pair_id)
    with parent_path.open("rb") as parent, full_path.open("rb") as full:
        parent_vars, parent_clauses = parse_header(parent.readline(), parent_path)
        full_vars, full_clauses = parse_header(full.readline(), full_path)
        require((parent_vars, parent_clauses) == (34268, 615572), "parent dimensions")
        require((full_vars, full_clauses) == (34268, 617204), "full dimensions")
        for number in range(parent_clauses):
            require(parent.readline() == full.readline(),
                    f"parent-prefix mismatch in core {core_index}, clause {number + 1}")
        require(parent.read() == b"", "data after parent clause count")
        actual = [parse_clause(full.readline(), full_path) for _ in expected]
        require(actual == expected, f"wrong appendix for core {core_index}")
        require(full.read() == b"", f"data after full clause count: {full_path}")
    return {
        "index": core_index,
        "variables": full_vars,
        "clauses": full_clauses,
        "parent_prefix_clauses": parent_clauses,
        "core_units": 9,
        "signature_units": 3,
        "singleton_cuts": 360,
        "four_vertex_cuts": 1260,
        "formula": digest(full_path),
    }


def cut_truth_tables():
    singleton_tests = four_tests = 0
    for signatures in product(range(8), repeat=3):
        for i in range(3):
            clause = any(not bool(s & (1 << i)) or
                         any(bool(s & (1 << j)) for j in range(3) if j != i)
                         for s in signatures)
            require(clause == (sum(s == (1 << i) for s in signatures) <= 2),
                    "singleton-clause semantics")
            singleton_tests += 1
    for signatures in product(range(8), repeat=4):
        for i in range(3):
            for k in range(3):
                if i == k:
                    continue
                clause = any(not bool(s & (1 << i)) or bool(s & (1 << k))
                             for s in signatures)
                forbidden = sum(bool(s & (1 << i)) and not bool(s & (1 << k))
                                for s in signatures)
                require(clause == (forbidden <= 3), "four-vertex-clause semantics")
                four_tests += 1
    return {"singleton_assignments": singleton_tests, "four_vertex_assignments": four_tests}


def verify_hash(path, label):
    info = digest(path)
    require(info["sha256"] == EXPECTED_HASHES[label], f"SHA-256 mismatch: {label}")
    return info


def replay(drat_trim, formula, proof, log_path):
    with log_path.open("wb") as output:
        result = subprocess.run([str(drat_trim), str(formula), str(proof)],
                                stdout=output, stderr=subprocess.STDOUT)
    text = log_path.read_text(errors="replace").replace("\r", "")
    require(result.returncode == 0 and "s VERIFIED" in text, "DRAT replay failed")
    match = re.search(r"(\d+) RAT lemmas in core", text)
    require(match and int(match.group(1)) == 821, "unexpected RAT-core count")
    return {"exit_code": result.returncode, "verified": True,
            "rat_core_lemmas": int(match.group(1))}


def main():
    parser = ArgumentParser()
    parser.add_argument("--source", type=Path, required=True,
                        help="published ramsey_r55_order3_eleven_signature_bound directory")
    parser.add_argument("--proof-work", type=Path, required=True,
                        help="external source workspace containing parent/case CNFs and c8.drat")
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--skip-proof", action="store_true", help="run structural checks only")
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)

    report = {
        "format": "r55-order3-k11-signature-review1-v1",
        "accepted_scope": "sharp lemma, exact propagation, and class-8 exclusion",
        "arithmetic": arithmetic_check(),
        "cut_truth_tables": cut_truth_tables(),
        "fixtures": [inspect_fixture(args.source / f"core{i}.edges", i) for i in CORE_WORDS],
    }
    pair_id = primary_variables()
    report["primary_orbits"] = 320
    report["parent"] = verify_hash(args.proof_work / "parent.cnf", "parent.cnf")
    report["formulas"] = []
    for i in CORE_WORDS:
        label = f"c{i}.cnf"
        verify_hash(args.proof_work / label, label)
        report["formulas"].append(
            audit_formula(args.proof_work / "parent.cnf", args.proof_work / label, i, pair_id))

    report["proof"] = verify_hash(args.proof_work / "c8.drat", "c8.drat")
    report["drat_trim"] = verify_hash(args.drat_trim, "drat-trim")
    if not args.skip_proof:
        report["proof_replay"] = replay(args.drat_trim, args.proof_work / "c8.cnf",
                                         args.proof_work / "c8.drat", args.work / "c8.replay.log")
    report["excluded"] = [8] if report.get("proof_replay", {}).get("verified") else []
    report["open_not_certified"] = [11, 13]
    report["target_graph_claimed"] = False
    report["all_checks_passed"] = not args.skip_proof

    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("w") as stream:
        dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print("PASS sharp lemma census, fixtures, formula bridge" +
          (", and class-8 DRAT replay" if not args.skip_proof else " (proof replay skipped)"))


if __name__ == "__main__":
    main()
