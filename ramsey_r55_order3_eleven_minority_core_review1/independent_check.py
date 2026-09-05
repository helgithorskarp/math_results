#!/usr/bin/env python3
"""Clean-room review of the eleven-cycle three-versus-eight core cover.

The script imports no submitted module.  It reconstructs the literal
nine-vertex action and its fourteen orbits, derives the cube literals from the
43-vertex pair action, compares every cube with the previously reviewed parent
formula, and replays all claimed DRAT refutations serially.
"""

from argparse import ArgumentParser
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import re
import subprocess


PAIR_CYCLES = ((0, 1), (0, 2), (1, 2))
CANONICAL_WORDS = ("000", "100", "110")
REPRESENTATIVES = (
    "000000000", "000000001", "000000011", "000100001",
    "000100011", "000110011", "100100001", "100100011",
    "100100100", "100100101", "100110011", "100110110",
    "110110011", "110110101",
)
EXCLUDED = (0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12)
OPEN = (8, 11, 13)
PARENT = {
    "bytes": 24_811_001,
    "clauses": 615_572,
    "sha256": "82f27b524e893d237f7a478c43bc9d49ff559faaa28e260d688d1591bdfaad20",
    "variables": 34_268,
}
COVER_SHA256 = "ed47db1eb0d18e8829fe903ded99c5bb2bc9e305891297396f7b94fdc17a8b62"
RESULT_SHA256 = "409948deda8e061ff9730f7e432cc9c1c01a216dd73f11c0b2f1897800176c01"
DRAT_TRIM_SHA256 = "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a"


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def file_info(path: Path) -> dict[str, object]:
    digest = sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            size += len(block)
            digest.update(block)
    return {"bytes": size, "sha256": digest.hexdigest()}


def core_graph(code: str) -> tuple[tuple[bool, ...], ...]:
    require(len(code) == 9 and set(code) <= {"0", "1"}, "core bit string")
    adjacency = [[False] * 9 for _ in range(9)]
    for left, right in combinations(range(9), 2):
        ci, si = divmod(left, 3)
        cj, sj = divmod(right, 3)
        if ci == cj:
            red = True
        else:
            index = 3 * PAIR_CYCLES.index((ci, cj)) + (sj - si) % 3
            red = code[index] == "1"
        adjacency[left][right] = adjacency[right][left] = red
    return tuple(tuple(row) for row in adjacency)


def monochromatic_five(adjacency) -> bool:
    for vertices in combinations(range(len(adjacency)), 5):
        colors = {adjacency[left][right] for left, right in combinations(vertices, 2)}
        if len(colors) == 1:
            return True
    return False


def small_maps():
    """Maps send a new labeled vertex to its old labeled vertex."""
    rows = []
    for cycle_permutation in permutations(range(3)):
        for shifts in product(range(3), repeat=3):
            for sign in (1, -1):
                mapping = tuple(
                    3 * cycle_permutation[cycle] + (sign * phase + shifts[cycle]) % 3
                    for cycle in range(3) for phase in range(3)
                )
                rows.append((cycle_permutation, shifts, sign, mapping))
    require(len(rows) == len({row[3] for row in rows}) == 324, "normalizer map count")
    return tuple(rows)


def encode_transported(adjacency, mapping) -> str:
    return "".join(
        "1" if adjacency[mapping[3 * ci]][mapping[3 * cj + offset]] else "0"
        for ci, cj in PAIR_CYCLES for offset in range(3)
    )


def invariant(code: str):
    words = (code[:3], code[3:6], code[6:])
    weights = tuple(sorted(word.count("1") for word in words))
    if 0 in weights:
        return [list(weights), None]
    phase = []
    for word in words:
        phase.append(word.index("1" if word.count("1") == 1 else "0"))
    holonomy_nonzero = int((phase[0] + phase[2] - phase[1]) % 3 != 0)
    return [list(weights), holonomy_nonzero]


def is_normalized(code: str) -> bool:
    return (code[:3] in CANONICAL_WORDS and code[3:6] in CANONICAL_WORDS
            and code[:3].count("1") <= code[3:6].count("1"))


def normalizer_and_later_steps(maps) -> dict[str, int]:
    def sigma(vertex: int, exponent: int = 1) -> int:
        if vertex >= 33:
            return vertex
        cycle, phase = divmod(vertex, 3)
        return 3 * cycle + (phase + exponent) % 3

    checked = 0
    for _, _, sign, small in maps:
        full = small + tuple(
            3 * cycle + (sign * phase) % 3
            for cycle in range(3, 11) for phase in range(3)
        ) + tuple(range(33, 43))
        require(sorted(full) == list(range(43)), "full map is not a permutation")
        require(all(full[sigma(vertex)] == sigma(full[vertex], sign)
                    for vertex in range(43)), "full normalizer identity")
        checked += 1

    later = []
    # Blue-cycle rotations and adjacent blue-cycle permutations generate the
    # phase normalization and weight sorting used after the core is fixed.
    for cycle in range(3, 11):
        mapping = list(range(43))
        for phase in range(3):
            mapping[3 * cycle + phase] = 3 * cycle + (phase + 1) % 3
        later.append(tuple(mapping))
    for cycle in range(3, 10):
        mapping = list(range(43))
        for phase in range(3):
            mapping[3 * cycle + phase] = 3 * (cycle + 1) + phase
            mapping[3 * (cycle + 1) + phase] = 3 * cycle + phase
        later.append(tuple(mapping))
    # Adjacent fixed-vertex swaps generate lexicographic signature sorting.
    for vertex in range(33, 42):
        mapping = list(range(43))
        mapping[vertex], mapping[vertex + 1] = mapping[vertex + 1], mapping[vertex]
        later.append(tuple(mapping))
    for mapping in later:
        require(mapping[:9] == tuple(range(9)), "later normalization changes the core")
        require(all(mapping[sigma(vertex)] == sigma(mapping[vertex])
                    for vertex in range(43)), "later map fails to centralize action")
    rotation_representatives = {
        min(word[offset:] + word[:offset] for offset in range(3))
        for word in ("".join(bits) for bits in product("01", repeat=3))
    }
    # Lexicographic minima are 000,001,011,111; the parent uses the reversed
    # phase convention 000,100,110,111.  Both sets are one representative per
    # rotation orbit, and the latter is a componentwise chain.
    require(rotation_representatives == {"000", "001", "011", "111"},
            "three-bit rotation orbits")
    require(all(all(int(left[i]) <= int(right[i]) for i in range(3))
                for left, right in zip(("000", "100", "110"), ("100", "110", "111"))),
            "canonical anchor words are not a chain")
    return {"full_normalizer_maps": checked, "later_centralizer_generators": len(later)}


def audit_cover(source: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    cover_path = source / "cover.json"
    require(file_info(cover_path)["sha256"] == COVER_SHA256, "published cover changed")
    published = json.loads(cover_path.read_text())
    maps = small_maps()

    valid = set()
    all_inputs = 0
    for value in range(512):
        code = format(value, "09b")
        no_complete_block = all(code[offset:offset + 3] != "111" for offset in (0, 3, 6))
        bad = monochromatic_five(core_graph(code))
        require(bad == (not no_complete_block), "literal nine-vertex equivalence")
        if no_complete_block:
            valid.add(code)
        all_inputs += 1
    require(len(valid) == 343, "valid labeled core count")

    reconstructed = []
    transports = 0
    left = set(valid)
    while left:
        seed = min(left)
        graph = core_graph(seed)
        orbit = {encode_transported(graph, row[3]) for row in maps}
        require(orbit <= valid, "normalizer left the valid domain")
        require(not (set(valid) - left) & orbit, "overlapping core orbits")
        normalized = sorted(code for code in orbit if is_normalized(code))
        require(normalized, "orbit lacks normalized representative")
        rep = normalized[0]
        require({json.dumps(invariant(code)) for code in orbit} == {json.dumps(invariant(rep))},
                "invariant varies within orbit")
        reconstructed.append({
            "bits": rep,
            "invariant": invariant(rep),
            "labeled": len(orbit),
            "members": sorted(orbit),
            "normalized": len(normalized),
        })
        for code in orbit:
            adjacency = core_graph(code)
            for _, _, _, mapping in maps:
                transported = encode_transported(adjacency, mapping)
                require(transported in orbit, "transport escaped orbit")
                target = core_graph(transported)
                require(all(target[a][b] == adjacency[mapping[a]][mapping[b]]
                            for a, b in combinations(range(9), 2)),
                        "literal transport mismatch")
                transports += 1
        left -= orbit
    reconstructed.sort(key=lambda row: row["bits"])
    require(tuple(row["bits"] for row in reconstructed) == REPRESENTATIVES,
            "canonical representative list")
    require(len(reconstructed) == 14 and sum(row["normalized"] for row in reconstructed) == 42,
            "orbit/normalization count")
    require(len({json.dumps(row["invariant"]) for row in reconstructed}) == 14,
            "weight/holonomy invariant is not complete")

    for index, (actual, expected) in enumerate(zip(reconstructed, published["cases"], strict=True)):
        require(expected["index"] == index, "published class index")
        comparable = {key: expected[key] for key in actual}
        require(actual == comparable, "published cover differs from reconstruction")
    require(published["labeled_cores"] == 343 and published["normalizer_maps"] == 324
            and published["normalized_cores"] == 42, "published cover totals")
    require(transports == 343 * 324, "literal transport count")

    allowed_signatures = []
    for row in reconstructed:
        adjacency = core_graph(row["bits"])
        allowed = []
        for bits in product((0, 1), repeat=3):
            extension = [list(graph_row) + [bool(bits[v // 3])] for v, graph_row in enumerate(adjacency)]
            extension.append([bool(bits[v // 3]) for v in range(9)] + [False])
            if not monochromatic_five(tuple(tuple(graph_row) for graph_row in extension)):
                allowed.append("".join(map(str, bits)))
        allowed_signatures.append({"index": len(allowed_signatures), "allowed": allowed})
    require(allowed_signatures[8]["allowed"] == [format(value, "03b") for value in range(8)],
            "class 8 fixed signature claim")
    for index in (11, 13):
        require(allowed_signatures[index]["allowed"] == [format(value, "03b") for value in range(7)],
                f"class {index} fixed signature claim")

    summary = {
        "binary_core_inputs": all_inputs,
        "valid_labeled_cores": len(valid),
        "classes": len(reconstructed),
        "normalized_cores": sum(row["normalized"] for row in reconstructed),
        "raw_normalizer_maps": len(maps),
        "literal_transports": transports,
        **normalizer_and_later_steps(maps),
        "surviving_fixed_signature_counts": {
            str(index): len(allowed_signatures[index]["allowed"]) for index in (8, 11, 13)
        },
    }
    return summary, reconstructed


def primary_core_variables() -> tuple[int, ...]:
    def sigma(vertex: int) -> int:
        cycle, phase = divmod(vertex, 3)
        return 3 * cycle + (phase + 1) % 3

    variable_of = {}
    next_variable = 0
    for left, right in combinations(range(33), 2):
        if left // 3 == right // 3 or (left, right) in variable_of:
            continue
        next_variable += 1
        pair = (left, right)
        while pair not in variable_of:
            variable_of[pair] = next_variable
            pair = tuple(sorted((sigma(pair[0]), sigma(pair[1]))))
    require(next_variable == 165, "moving cross-orbit count")
    result = tuple(
        variable_of[(3 * ci, 3 * cj + offset)]
        for ci, cj in PAIR_CYCLES for offset in range(3)
    )
    require(result == (1, 2, 3, 4, 5, 6, 31, 32, 33), "core primary variables")
    return result


def audit_cube(parent: Path, cube: Path, code: str, manifest: dict[str, object]) -> dict[str, object]:
    actual = file_info(cube)
    require(actual == manifest, "cube digest differs from manifest")
    variables = primary_core_variables()
    with parent.open("rb") as base, cube.open("rb") as candidate:
        parent_header = base.readline().split()
        require(parent_header == [b"p", b"cnf", b"34268", b"615572"], "parent DIMACS header")
        require(candidate.readline() == b"p cnf 34268 615581\n", "cube DIMACS header")
        for _ in range(PARENT["clauses"]):
            line = base.readline()
            require(line and candidate.readline() == line, "cube differs in parent prefix")
        require(base.read() == b"", "parent has trailing bytes")
        expected_units = tuple(
            variable if bit == "1" else -variable
            for variable, bit in zip(variables, code, strict=True)
        )
        for literal in expected_units:
            require(candidate.readline() == f"{literal} 0\n".encode(), "incorrect cube unit")
        require(candidate.read() == b"", "cube has trailing bytes")
    return {**actual, "variables": 34_268, "clauses": 615_581,
            "parent_prefix_exact": True, "units": list(expected_units)}


def replay(checker: Path, cube: Path, proof: Path, log: Path, expected_rat: int) -> dict[str, object]:
    with log.open("w") as output:
        process = subprocess.run(
            [str(checker), str(cube), str(proof), "-t", "300"],
            stdout=output, stderr=subprocess.STDOUT, timeout=360,
        )
    text = log.read_text(errors="replace")
    require(process.returncode == 0 and "s VERIFIED" in text, "DRAT replay failed")
    match = re.search(r"(\d+) RAT lemmas in core", text)
    require(match and int(match.group(1)) == expected_rat, "RAT core count differs")
    return {"verified": True, "rat_core_lemmas": expected_rat}


def audit_formulas_and_proofs(parent: Path, proof_work: Path, source: Path,
                              checker: Path, replay_work: Path,
                              representatives) -> tuple[list[dict[str, object]], dict[str, object]]:
    require(file_info(parent) == {"bytes": PARENT["bytes"], "sha256": PARENT["sha256"]},
            "reviewed parent formula changed")
    result_path = source / "result.json"
    require(file_info(result_path)["sha256"] == RESULT_SHA256, "published result changed")
    result = json.loads(result_path.read_text())
    require((proof_work / "result.json").read_bytes() == result_path.read_bytes(),
            "proof workspace manifest differs")
    require(result["complete"] and not result["all_excluded"], "source sweep completeness flags")
    require(tuple(result["excluded"]) == EXCLUDED and tuple(result["open"]) == OPEN,
            "source case partition")
    require(tuple(row["index"] for row in result["cases"]) == tuple(range(14)),
            "source case index cover")
    require(file_info(checker) == {"bytes": 51_352, "sha256": DRAT_TRIM_SHA256},
            "unexpected drat-trim binary")
    replay_work.mkdir(parents=True, exist_ok=True)

    rows = []
    proof_bytes = 0
    for index, (cover_row, row) in enumerate(zip(representatives, result["cases"], strict=True)):
        require(row["bits"] == cover_row["bits"], "formula representative mismatch")
        require(row["audit"] == {"appended_units": 9, "clauses": 615_581,
                                 "complete_prefix": True, "variables": 34_268},
                "source cube audit record")
        cube = proof_work / f"c{index:02}.cnf"
        formula = audit_cube(parent, cube, row["bits"], row["formula"])
        record = {
            "index": index,
            "bits": row["bits"],
            "status": row["status"],
            "formula_sha256": formula["sha256"],
            "parent_prefix_exact": formula["parent_prefix_exact"],
        }
        proof = proof_work / f"c{index:02}.drat"
        if index in EXCLUDED:
            require(row["status"] == "excluded" and row["solver_code"] == 20,
                    "claimed exclusion status")
            require(file_info(proof) == row["proof"], "proof digest differs")
            expected_rat = row["replay"]["rat_core_lemmas"]
            checked = replay(checker, cube, proof,
                             replay_work / f"replay_c{index:02}.log", expected_rat)
            record["proof_sha256"] = row["proof"]["sha256"]
            record["drat_verified"] = checked["verified"]
            record["rat_core_lemmas"] = checked["rat_core_lemmas"]
            proof_bytes += row["proof"]["bytes"]
            print(f"PROOF class {index} general DRAT verified", flush=True)
        else:
            require(index in OPEN and row["status"] == "open" and row["solver_code"] == 0,
                    "open case status")
            solve_log = proof_work / f"c{index:02}.solve.log"
            require("s UNKNOWN" in solve_log.read_text(errors="replace"), "open case lacks UNKNOWN")
            record["solver_outcome"] = "UNKNOWN (not a certificate)"
        rows.append(record)
    require(proof_bytes == 399_325_866, "successful proof-byte total")
    return rows, {"successful_proof_bytes": proof_bytes,
                  "proof_replays": len(EXCLUDED),
                  "all_claimed_exclusions_verified": True}


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--parent-formula", required=True, type=Path)
    parser.add_argument("--proof-work", required=True, type=Path)
    parser.add_argument("--drat-trim", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()

    source = args.source.resolve()
    parent = args.parent_formula.resolve()
    proof_work = args.proof_work.resolve()
    checker = args.drat_trim.resolve()
    work = args.work.resolve()
    cover, representatives = audit_cover(source)
    print("COVER 343 labeled cores in 14 normalizer classes", flush=True)
    cases, certificate = audit_formulas_and_proofs(
        parent, proof_work, source, checker, work, representatives,
    )
    report = {
        "verdict": "ACCEPTED",
        "reviewed_source_commit": "e5b88c054f96354007df003068c369ed273c65a5",
        "imported_parent_review": "bafkreidkjevnpnqbwqiewmrbf7ksnxgtlad3tc54jyqppytjcykr4b36n4",
        "parent_formula": PARENT,
        "cover": cover,
        "excluded": list(EXCLUDED),
        "open": list(OPEN),
        "certificate": certificate,
        "cases": cases,
        "scope": (
            "Only the three-versus-eight branch: classes 8,11,13 remain; "
            "this neither constructs a Ramsey(5,5;43) graph nor settles four-versus-seven."
        ),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS classes 0-7,9,10,12 excluded; classes 8,11,13 open", flush=True)


if __name__ == "__main__":
    main()
