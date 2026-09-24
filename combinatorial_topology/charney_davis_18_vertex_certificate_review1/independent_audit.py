#!/usr/bin/env python3
"""Independent structural and LRAT audit for the 18-vertex proof.

This file imports no module from the reviewed package.  It independently
enumerates the six-vertex facet-incidence orbits, checks the complement
identities on deterministic graph samples, verifies the degree-profile
reduction exhaustively, and checks every regenerated LRAT proof using a
separate standard-library implementation of hinted reverse unit propagation.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS6)}


class AuditError(ValueError):
    pass


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def edges6(mask):
    return [pair for index, pair in enumerate(PAIRS6) if mask >> index & 1]


def admissible(mask, k):
    if mask.bit_count() != k:
        return False
    degrees = [0] * 6
    for u, v in edges6(mask):
        degrees[u] += 1
        degrees[v] += 1
    if k == 5 and min(degrees) == 0:
        return False
    if k == 6 and any(degree != 2 for degree in degrees):
        return False
    return True


def permute_mask(mask, permutation):
    result = 0
    for u, v in edges6(mask):
        pair = tuple(sorted((permutation[u], permutation[v])))
        result |= 1 << PAIR_INDEX[pair]
    return result


def independent_cases():
    permutations = tuple(itertools.permutations(range(6)))
    records = []
    labelled = {}
    for k in (3, 4, 5, 6):
        masks = [mask for mask in range(1 << 15) if admissible(mask, k)]
        labelled[str(k)] = len(masks)
        classes = {}
        for mask in masks:
            representative = min(permute_mask(mask, p) for p in permutations)
            classes.setdefault(representative, 0)
            classes[representative] += 1
        for representative in sorted(classes):
            records.append({
                "id": f"{k}_{representative:04x}",
                "k": k,
                "mask": representative,
                "edges": [list(edge) for edge in edges6(representative)],
                "orbit_size": classes[representative],
            })
    assert labelled == {"3": 455, "4": 1365, "5": 1581, "6": 70}
    assert [sum(row["k"] == k for row in records) for k in (3, 4, 5, 6)] == [5, 9, 9, 2]
    return labelled, records


def graph_from_seed(seed):
    """Produce a deterministic, non-random graph on eighteen vertices."""
    state = (seed + 1) * 0x9E3779B97F4A7C15
    edges = set()
    for pair in itertools.combinations(range(18), 2):
        state ^= state >> 12
        state ^= (state << 25) & ((1 << 64) - 1)
        state ^= state >> 27
        state = (state * 0x2545F4914F6CDD1D) & ((1 << 64) - 1)
        if state % 23 < (seed % 19) + 2:
            edges.add(pair)
    return edges


def check_complement_identities():
    checks = 0
    for seed in range(512):
        edges = graph_from_seed(seed)
        neighbors = [set() for _ in range(18)]
        for u, v in edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        degrees = [len(row) for row in neighbors]
        triangles = sum(
            all(tuple(sorted(pair)) in edges for pair in itertools.combinations(triple, 2))
            for triple in itertools.combinations(range(18), 3)
        )
        independent_triples = sum(
            all(tuple(sorted(pair)) not in edges for pair in itertools.combinations(triple, 2))
            for triple in itertools.combinations(range(18), 3)
        )
        m = len(edges)
        f1 = 153 - m
        a = f1 - 9 * 18 + 48
        b = independent_triples - 6 * f1 + 22 * 18 - 64
        assert a == 39 - m
        assert independent_triples == 816 - 16 * m + sum(q * (q - 1) // 2 for q in degrees) - triangles
        assert b == 230 + sum(q * (q - 11) // 2 for q in degrees) - triangles
        link_values = []
        for v in range(18):
            antipodes = neighbors[v]
            link_vertices = set(range(18)) - {v} - antipodes
            link_edges = sum(
                tuple(sorted(pair)) not in edges
                for pair in itertools.combinations(link_vertices, 2)
            )
            local_triangles = sum(tuple(sorted(pair)) in edges for pair in itertools.combinations(antipodes, 2))
            direct = link_edges - 7 * len(link_vertices) + 30
            formula = (
                a + 8 + degrees[v] * (degrees[v] - 19) // 2
                + sum(degrees[u] for u in antipodes) - local_triangles
            )
            assert direct == formula
            link_values.append(direct)
            checks += 1
        assert sum(link_values) == 3 * b + 4 * a
    return checks


def degree_profile_audit():
    profiles_with_nonnegative_sum = 0
    profiles_compatible_with_negative_b = 0
    for n3 in range(19):
        for n4 in range(19 - n3):
            for n5 in range(19 - n3 - n4):
                for n6 in range(19 - n3 - n4 - n5):
                    n7 = 18 - n3 - n4 - n5 - n6
                    counts = (n3, n4, n5, n6, n7)
                    if sum((q + 3) * counts[q] for q in range(5)) % 2:
                        continue
                    cost = 8 * n4 + 13 * n5 + 15 * n6 + 14 * n7
                    if cost > 90:
                        continue
                    profiles_with_nonnegative_sum += 1
                    assert n3 >= 8
                    half_quadratic = sum(
                        count * degree * (degree - 11) // 2
                        for degree, count in zip(range(3, 8), counts)
                    )
                    triangle_minimum = max(0, 231 + half_quadratic)
                    triangle_maximum = (90 - cost) // 3
                    if triangle_minimum <= triangle_maximum:
                        profiles_compatible_with_negative_b += 1
    return {
        "handshake_profiles_with_S_nonnegative": profiles_with_nonnegative_sum,
        "profiles_also_compatible_with_b_negative": profiles_compatible_with_negative_b,
        "minimum_cubic_count": 8,
    }


def threshold_tables():
    result = []
    for q in range(3, 8):
        thresholds = [int(q >= j) for j in range(4, 8)]
        b_cost = 2 * thresholds[0] + thresholds[1] - thresholds[3]
        s_cost = 8 * thresholds[0] + 5 * thresholds[1] + 2 * thresholds[2] - thresholds[3]
        local_adjustment = -6 * thresholds[0] - 4 * thresholds[1] - 2 * thresholds[2]
        assert b_cost == -12 - q * (q - 11) // 2
        assert s_cost == -42 - q * (3 * q - 37) // 2
        assert local_adjustment == q * (q - 13) + 30
        result.append({"degree": q, "b_cost": b_cost, "S_cost": s_cost,
                       "local_adjustment": local_adjustment})
    return result


def read_cnf(path):
    active = {}
    header = None
    clause = []
    with path.open() as stream:
        for line in stream:
            words = line.split()
            if not words or words[0] == "c":
                continue
            if words[0] == "p":
                if header is not None or len(words) != 4 or words[1] != "cnf":
                    raise AuditError("bad CNF header")
                header = (int(words[2]), int(words[3]))
                continue
            if header is None:
                raise AuditError("CNF data before header")
            for word in words:
                literal = int(word)
                if literal == 0:
                    active[len(active) + 1] = tuple(clause)
                    clause.clear()
                else:
                    if abs(literal) > header[0]:
                        raise AuditError("CNF literal outside header")
                    clause.append(literal)
    if header is None or clause or len(active) != header[1]:
        raise AuditError("incomplete CNF")
    return active, header


def independent_rup(clause, hints, active):
    assignment = {}
    for literal in clause:
        variable = abs(literal)
        value = literal < 0
        if variable in assignment and assignment[variable] != value:
            return 0
        assignment[variable] = value
    used = 0
    for identifier in hints:
        if identifier <= 0 or identifier not in active:
            raise AuditError("invalid or inactive hint")
        unresolved = set()
        for literal in active[identifier]:
            variable = abs(literal)
            if variable in assignment:
                if assignment[variable] == (literal > 0):
                    raise AuditError("hinted clause is satisfied")
            else:
                unresolved.add(literal)
        used += 1
        if not unresolved:
            return used
        if len(unresolved) != 1:
            raise AuditError("hinted clause is not unit")
        literal = unresolved.pop()
        assignment[abs(literal)] = literal > 0
    raise AuditError("RUP addition has no conflict")


def rup_controls():
    active = {1: (1,), 2: (-1,), 3: (1, 2)}
    assert independent_rup((), (1, 2), active) == 2
    assert independent_rup((1, -1), (), active) == 0
    rejected = 0
    for clause, hints in [
        ((), ()),                 # unsupported empty clause
        ((), (3,)),               # nonunit first hint
        ((-1,), (1,)),            # hinted clause already satisfied
        ((), (99,)),              # inactive identifier
    ]:
        try:
            independent_rup(clause, hints, active)
        except AuditError:
            rejected += 1
    assert rejected == 4
    return {"valid_conflict_accepted": 1, "sound_tautology_accepted": 1,
            "malformed_or_unjustified_rejected": rejected}


def check_lrat(cnf_path, lrat_path):
    active, (variables, input_count) = read_cnf(cnf_path)
    last_addition = input_count
    additions = deletions = hint_steps = 0
    has_empty = False
    with lrat_path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            words = line.split()
            if not words or words[0] == "c":
                continue
            if len(words) < 3:
                raise AuditError(f"short LRAT line {line_number}")
            identifier = int(words[0])
            if words[1] == "d":
                deleted = [int(word) for word in words[2:]]
                if not deleted or deleted[-1] != 0 or any(item <= 0 for item in deleted[:-1]):
                    raise AuditError("malformed deletion")
                for item in deleted[:-1]:
                    active.pop(item, None)
                    deletions += 1
                continue
            if identifier <= last_addition or identifier in active:
                raise AuditError("addition identifiers are not increasing")
            data = [int(word) for word in words[1:]]
            if data.count(0) != 2 or data[-1] != 0:
                raise AuditError("bad LRAT terminators")
            separator = data.index(0)
            clause = tuple(data[:separator])
            hints = data[separator + 1:-1]
            if any(abs(literal) > variables for literal in clause):
                raise AuditError("LRAT introduced an undeclared variable")
            hint_steps += independent_rup(clause, hints, active)
            active[identifier] = clause
            last_addition = identifier
            additions += 1
            has_empty |= not clause
    if not has_empty:
        raise AuditError("no justified empty clause")
    return {"input_clauses": input_count, "additions": additions,
            "deletion_references": deletions, "propagation_hints_checked": hint_steps}


def certificate_audit(target, proof_dir, expected):
    totals = {"input_clauses": 0, "additions": 0, "deletion_references": 0,
              "propagation_hints_checked": 0}
    for record in expected["cases"]:
        stem = proof_dir / record["id"]
        paths = {suffix: stem.with_suffix("." + suffix) for suffix in ("cnf", "drat", "lrat")}
        for suffix, path in paths.items():
            if sha256(path) != record[f"{suffix}_sha256"]:
                raise AuditError(f"{record['id']}: {suffix} hash mismatch")
        checked = check_lrat(paths["cnf"], paths["lrat"])
        published = record["strict_rup"]
        for key, value in checked.items():
            if published[key] != value:
                raise AuditError(f"{record['id']}: {key} mismatch")
            totals[key] += value
    return {"case_count": len(expected["cases"]), "all_file_hashes_match": True,
            "all_lrat_proofs_independently_verified": True, **totals}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--proof-dir", type=Path, required=True)
    args = parser.parse_args()
    expected = json.loads((args.target / "EXPECTED.json").read_text())
    labelled, records = independent_cases()
    published_cases = [
        {key: row[key] for key in ("id", "k", "mask", "edges", "orbit_size")}
        for row in expected["cases"]
    ]
    if records != published_cases:
        raise AuditError("independent incidence orbit census differs from EXPECTED.json")
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    output = {
        "target_expected_sha256": sha256(args.target / "EXPECTED.json"),
        "facet_incidence": {
            "labelled_by_k": labelled,
            "orbit_count_by_k": {str(k): sum(row["k"] == k for row in records) for k in (3, 4, 5, 6)},
            "case_count": len(records),
            "canonical_records_sha256": hashlib.sha256(canonical).hexdigest(),
        },
        "complement_identity_vertex_checks": check_complement_identities(),
        "degree_profiles": degree_profile_audit(),
        "threshold_tables": threshold_tables(),
        "independent_rup_controls": rup_controls(),
        "certificates": certificate_audit(args.target, args.proof_dir, expected),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
