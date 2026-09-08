#!/usr/bin/env python3
"""SAT-based independent audit of the separator-18 finite hinge.

No module from the reviewed package is imported.  The claimant constructs
graphs recursively and then enumerates star tuples; this checker instead
enumerates direct edge assignments from literal triangle/independence CNFs.
The final all-model-blocked formulas have DRAT traces for external checking.
"""

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

import pysat
from pysat.solvers import Glucose3


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pairs(n):
    return list(itertools.combinations(range(n), 2))


def adjacency(n, code):
    result = [0] * n
    for bit, (u, v) in enumerate(pairs(n)):
        if code >> bit & 1:
            result[u] |= 1 << v
            result[v] |= 1 << u
    return result


def independent(adj, vertices):
    return all(not (adj[u] >> v & 1) for u, v in itertools.combinations(vertices, 2))


def direct_h_check(code):
    adj = adjacency(8, code)
    require(
        not any(
            all(adj[u] >> v & 1 for u, v in itertools.combinations(q, 2))
            for q in itertools.combinations(range(8), 3)
        ),
        "SAT core contains a triangle",
    )
    require(
        not any(independent(adj, q) for q in itertools.combinations(range(8), 4)),
        "SAT core contains an independent four",
    )


def direct_f_check(code):
    adj = adjacency(12, code)
    require(
        not any(
            all(adj[u] >> v & 1 for u, v in itertools.combinations(q, 2))
            for q in itertools.combinations(range(12), 3)
        ),
        "SAT extension contains a triangle",
    )
    require(
        not any(independent(adj, q) for q in itertools.combinations(range(12), 5)),
        "SAT extension contains an independent five",
    )
    fours = [
        set(q)
        for q in itertools.combinations(range(12), 4)
        if independent(adj, q)
    ]
    special = [sorted(q) for q in fours if all(q & other for other in fours)]
    require(special == [[8, 9, 10, 11]], "extension does not have unique marked special four")


def dimacs(variables, clauses):
    text = f"p cnf {variables} {len(clauses)}\n"
    text += "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return text.encode()


def write_proof(output, stem, variables, clauses, trace):
    cnf = dimacs(variables, clauses)
    drat = ("\n".join(trace) + "\n").encode()
    (output / f"{stem}.cnf").write_bytes(cnf)
    (output / f"{stem}.drat").write_bytes(drat)
    return {
        "cnf_bytes": len(cnf),
        "cnf_sha256": hashlib.sha256(cnf).hexdigest(),
        "drat_bytes": len(drat),
        "drat_sha256": hashlib.sha256(drat).hexdigest(),
    }


def enumerate_models(variables, base_clauses, decoder, direct_check, output, stem):
    clauses = [list(clause) for clause in base_clauses]
    decoded = []
    with Glucose3(bootstrap_with=clauses, with_proof=True) as solver:
        while solver.solve():
            positive = {lit for lit in solver.get_model() if lit > 0}
            word = tuple(variable in positive for variable in range(1, variables + 1))
            value = decoder(word)
            direct_check(value)
            decoded.append(value)
            block = [(-variable if word[variable - 1] else variable)
                     for variable in range(1, variables + 1)]
            clauses.append(block)
            solver.add_clause(block)
        trace = solver.get_proof()
        stats = solver.accum_stats()
    require(len(decoded) == len(set(decoded)), "duplicate SAT models")
    proof = write_proof(output, stem, variables, clauses, trace)
    proof.update({"models": len(decoded), "final_clauses": len(clauses),
                  "conflicts": stats["conflicts"]})
    return decoded, proof


def enumerate_cores(output):
    edge_pairs = pairs(8)
    edge_var = {pair: i + 1 for i, pair in enumerate(edge_pairs)}
    clauses = []
    for q in itertools.combinations(range(8), 3):
        clauses.append([-edge_var[pair] for pair in itertools.combinations(q, 2)])
    for q in itertools.combinations(range(8), 4):
        clauses.append([edge_var[pair] for pair in itertools.combinations(q, 2)])

    def decode(word):
        return sum(value << bit for bit, value in enumerate(word))

    codes, proof = enumerate_models(28, clauses, decode, direct_h_check,
                                    output, "cores_all_blocked")
    ordered = sorted(codes)
    digest = hashlib.sha256(("\n".join(map(str, ordered)) + "\n").encode()).hexdigest()
    unseen = set(ordered)
    orbits = []
    while unseen:
        representative = min(unseen)
        adj = adjacency(8, representative)
        orbit = set()
        for permutation in itertools.permutations(range(8)):
            code = 0
            for bit, (u, v) in enumerate(edge_pairs):
                code |= ((adj[permutation[u]] >> permutation[v]) & 1) << bit
            orbit.add(code)
        require(orbit <= unseen, "core orbit overlap or missing labeled model")
        unseen -= orbit
        orbits.append((representative, len(orbit)))
    return ordered, digest, orbits, proof


def extension_clauses(core_code):
    core = adjacency(8, core_code)

    def edge_term(u, v):
        if v < 8:
            return bool(core[u] >> v & 1)
        if u >= 8:
            return False
        return (v - 8) * 8 + u + 1

    clauses = []
    for vertices in itertools.combinations(range(12), 3):
        terms = [edge_term(u, v) for u, v in itertools.combinations(vertices, 2)]
        if any(term is False for term in terms):
            continue
        clause = [-term for term in terms if type(term) is int]
        require(clause, "fixed core triangle")
        clauses.append(clause)
    for vertices in itertools.combinations(range(12), 5):
        terms = [edge_term(u, v) for u, v in itertools.combinations(vertices, 2)]
        if any(term is True for term in terms):
            continue
        clause = [term for term in terms if type(term) is int]
        require(clause, "fixed independent five")
        clauses.append(clause)
    return clauses


def enumerate_extensions(core_code, output):
    base = extension_clauses(core_code)
    full_pairs = pairs(12)
    core = adjacency(8, core_code)

    def decode(word):
        code = 0
        for bit, (u, v) in enumerate(full_pairs):
            if v < 8:
                value = bool(core[u] >> v & 1)
            elif u < 8:
                value = word[(v - 8) * 8 + u]
            else:
                value = False
            code |= value << bit
        return code

    return enumerate_models(32, base, decode, direct_f_check, output,
                            f"extensions_{core_code}_all_blocked")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-package", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    require(not output.exists(), "proof output directory already exists")
    output.mkdir(parents=True, exist_ok=True)

    expected = json.loads((args.claim_package / "INDEPENDENT.json").read_text())
    cores, digest, orbits, core_proof = enumerate_cores(output)
    require(len(cores) == 17640, "labeled core count")
    require(digest == expected["labeled_R34_8_codes_sha256"], "labeled core stream")
    expected_records = expected["complete_marked_extension_classes"]
    require(
        orbits == [(row["core_code"], row["labeled_orbit_size"])
                   for row in expected_records],
        "core orbit classification",
    )

    extension_counts = []
    extension_proofs = []
    for row in expected_records:
        models, proof = enumerate_extensions(row["core_code"], output)
        require(sorted(models) == row["extension_codes"], "extension code set")
        extension_counts.append(len(models))
        extension_proofs.append({"core_code": row["core_code"], **proof})

    result = {
        "status": "INDEPENDENT_SAT_ENUMERATION_VERIFIED",
        "claimant_modules_imported": False,
        "core_encoding": "56 triangle clauses and 70 independent-four clauses on 28 edge variables",
        "labeled_R34_8_models": len(cores),
        "labeled_R34_8_codes_sha256": digest,
        "orbit_representatives_and_sizes": [list(item) for item in orbits],
        "extension_encoding": "literal triangle and independent-five clauses on 32 cross-edge variables",
        "marked_extension_counts": extension_counts,
        "all_emitted_graphs_literal_checked": True,
        "all_extension_code_sets_match": True,
        "python": sys.version.split()[0],
        "python_sat": pysat.__version__,
        "solver": "PySAT Glucose3",
        "core_exhaustion_proof": core_proof,
        "extension_exhaustion_proofs": extension_proofs,
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
