#!/usr/bin/env python3
"""Independent SAT enumeration for the finite hinge in h3909.

This checker does not import the reviewed producer or its native enumerator.
It encodes the forbidden subgraphs directly.  The optional producer stream is
used only for an entry-level comparison after the independent enumeration.
"""

import argparse
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

import pysat
from pysat.solvers import Solver


REVIEWED_MANIFEST_SHA256 = (
    "a9ea0aeb000182d0f1e3ff5f8bd1763230669b29dd7587785ed77336c6d572d0"
)
REVIEWED_SUMMARY_SHA256 = (
    "f3929746501691cb853865c9bb743adf66829c4e2b7f14415556c5be7644be31"
)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def edge_index(n):
    return {edge: i for i, edge in enumerate(combinations(range(n), 2))}


def adjacency(n, word):
    need(type(word) is int and 0 <= word < 1 << (n * (n - 1) // 2),
         "invalid graph word")
    rows = [0] * n
    for i, (u, v) in enumerate(combinations(range(n), 2)):
        if word >> i & 1:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def encode(rows):
    return sum(
        ((rows[u] >> v) & 1) << i
        for i, (u, v) in enumerate(combinations(range(len(rows)), 2))
    )


def independent(rows, vertices):
    vertices = tuple(vertices)
    return all(not (rows[u] >> v & 1) for u, v in combinations(vertices, 2))


def enumerate_sat(clauses, variables, solver_name):
    """Enumerate every assignment to exactly variables 1,...,variables."""
    models = []
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        while solver.solve():
            model = {abs(lit): lit > 0 for lit in solver.get_model()}
            need(all(v in model for v in range(1, variables + 1)),
                 "solver returned a partial primary assignment")
            bits = sum(int(model[v]) << (v - 1) for v in range(1, variables + 1))
            models.append(bits)
            solver.add_clause([-v if model[v] else v for v in range(1, variables + 1)])
        need(not solver.solve(), "blocking enumeration did not terminate UNSAT")
    need(len(models) == len(set(models)), "duplicate SAT assignment")
    return set(models)


def core_cnf(n):
    index = edge_index(n)

    def var(u, v):
        return index[tuple(sorted((u, v)))] + 1

    clauses = []
    # Triangle-free in F.
    for u, v, w in combinations(range(n), 3):
        clauses.append([-var(u, v), -var(u, w), -var(v, w)])
    # No independent four-set in F.
    for vertices in combinations(range(n), 4):
        clauses.append([var(u, v) for u, v in combinations(vertices, 2)])
    return clauses, len(index)


def permuted_word(n, word, order):
    rows = adjacency(n, word)
    return sum(
        ((rows[order[u]] >> order[v]) & 1) << i
        for i, (u, v) in enumerate(combinations(range(n), 2))
    )


def check_core_orbits(summary, solver_name):
    counts = {}
    orbit_counts = {}
    labeled_digests = {}
    for n in (6, 7, 8):
        clauses, variables = core_cnf(n)
        literal = enumerate_sat(clauses, variables, solver_name)
        union = set()
        rows = summary["core_orbits"][str(n)]
        for row in rows:
            orbit = {
                permuted_word(n, row["code"], order)
                for order in permutations(range(n))
            }
            need(len(orbit) == row["orbit_size"], "incorrect reported orbit size")
            need(not (union & orbit), "reported core orbits overlap")
            union |= orbit
        need(literal == union, "SAT core family differs from reported orbit union")
        counts[n] = len(literal)
        orbit_counts[n] = len(rows)
        h = hashlib.sha256()
        width = (variables + 7) // 8
        for word in sorted(literal):
            h.update(word.to_bytes(width, "little"))
        labeled_digests[n] = h.hexdigest()
    need([counts[n] for n in (6, 7, 8)] ==
         summary["labeled_core_counts_n1_to_n8"][5:],
         "labeled core counts differ")
    return counts, orbit_counts, labeled_digests


def marked_cnf(n, h, core):
    rows = adjacency(h, core)
    q = n - h

    def var(i, u):
        return i * h + u + 1

    clauses = []
    # The q marked vertices are mutually nonadjacent.  A triangle can therefore
    # only use one marked vertex and one physical H-edge.
    for i in range(q):
        for u, v in combinations(range(h), 2):
            if rows[u] >> v & 1:
                clauses.append([-var(i, u), -var(i, v)])

    # Every physical five-set must contain an F-edge.  Existing H-edges satisfy
    # the constraint immediately; otherwise the clause lists every cross edge.
    for subset in combinations(range(n), 5):
        hs = [v for v in subset if v < h]
        tails = [v - h for v in subset if v >= h]
        if any(rows[u] >> v & 1 for u, v in combinations(hs, 2)):
            continue
        clause = [var(i, u) for i in tails for u in hs]
        need(clause, "fixed independent five-set in a marked job")
        clauses.append(clause)
    return clauses, h * q


def marked_word(n, h, core, assignment):
    rows = adjacency(h, core) + [0] * (n - h)
    for i in range(n - h):
        for u in range(h):
            var = i * h + u
            if assignment >> var & 1:
                v = h + i
                rows[u] |= 1 << v
                rows[v] |= 1 << u
    return encode(rows)


def direct_marked_audit(n, word):
    rows = adjacency(n, word)
    need(not any(
        all(rows[u] >> v & 1 for u, v in combinations(t, 2))
        for t in combinations(range(n), 3)
    ), "SAT model contains a triangle")
    need(not any(independent(rows, q) for q in combinations(range(n), 5)),
         "SAT model contains an independent five-set")

    triangles = [tuple(t) for t in combinations(range(n), 3)
                 if independent(rows, t)]
    need(triangles, "missing red triangle")
    beta_values = {}
    common = {}
    for tri in triangles:
        contacts = [sum(rows[v] >> u & 1 for u in tri)
                    for v in range(n) if v not in tri]
        beta_values[tri] = 2 * n + 1 - 2 * contacts.count(3) - contacts.count(2)
        common[tri] = sum(
            all(not (rows[v] >> u & 1) for u in tri)
            for v in range(n) if v not in tri
        )
        need(common[tri] <= 4, "component violates common-neighbor cap")
    beta = min(beta_values.values())
    need(beta <= (19 if n == 10 else 20), "marked degree bound fails")

    if n == 10 or beta < 19:
        return beta, None, 0

    specials = []
    independent_fours = [set(q) for q in combinations(range(n), 4)
                         if independent(rows, q)]
    for size in range(5):
        for q in combinations(range(n), size):
            if independent(rows, q) and all(set(q) & t for t in independent_fours):
                specials.append(((1 << n) - 1) ^ sum(1 << v for v in q))
    need(specials, "marked graph has no special attachment")

    best = None
    for length in (1, 2):
        for cover in combinations(triangles, length):
            if not all(any(all(red >> v & 1 for v in tri) for tri in cover)
                       for red in specials):
                continue
            cost = sum(4 - common[tri] for tri in cover)
            candidate = (cost, cover)
            if best is None or candidate < best:
                best = candidate
    need(best is not None and best[0] <= 6, "six-capacity cover does not exist")
    return beta, best[0], len(specials)


def load_producer_stream(path):
    if path is None:
        return None
    jobs = {}
    with Path(path).open() as stream:
        for line in stream:
            record = json.loads(line)
            key = (record["n"], record["h"], record["core"])
            jobs.setdefault(key, set()).add(record["code"])
    return jobs


def check_marked(summary, solver_name, producer_stream):
    expected_rows = {
        (row["n"], row["h"], row["core"]): row
        for row in summary["rows"]
    }
    producer = load_producer_stream(producer_stream)
    if producer is not None:
        need(set(producer) <= set(expected_rows), "producer contains an unknown job")
        producer = {key: producer.get(key, set()) for key in expected_rows}

    job_evidence = []
    totals = Counter()
    cost_histogram = Counter()
    special_sets_checked = 0
    for key, expected in expected_rows.items():
        n, h, core = key
        clauses, variables = marked_cnf(n, h, core)
        assignments = enumerate_sat(clauses, variables, solver_name)
        words = {marked_word(n, h, core, assignment) for assignment in assignments}
        need(len(words) == len(assignments), "two cross assignments encode one graph")
        need(len(words) == expected["marked_graphs"], "marked job count differs")
        if producer is not None:
            need(words == producer[key], "entry-level producer/SAT graph sets differ")

        beta_histogram = Counter()
        covers = 0
        h_words = hashlib.sha256()
        for word in sorted(words):
            beta, cost, specials = direct_marked_audit(n, word)
            beta_histogram[beta] += 1
            h_words.update(word.to_bytes(8, "little"))
            if cost is not None:
                covers += 1
                cost_histogram[cost] += 1
                special_sets_checked += specials
        expected_histogram = {int(k): v for k, v in expected["beta_histogram"].items()}
        need(dict(sorted(beta_histogram.items())) == expected_histogram,
             "marked beta histogram differs")
        need(covers == expected["cover_certificates"], "cover count differs")
        totals[n] += len(words)
        job_evidence.append({
            "n": n,
            "h": h,
            "core": core,
            "models": len(words),
            "beta_histogram": expected_histogram,
            "word_set_sha256": h_words.hexdigest(),
        })

    need(totals[10] == summary["marked10"] and totals[11] == summary["marked11"],
         "marked totals differ")
    evidence_bytes = json.dumps(job_evidence, sort_keys=True,
                                separators=(",", ":")).encode()
    return totals, cost_histogram, special_sets_checked, hashlib.sha256(evidence_bytes).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path,
                        help="reviewed ramsey_r55_maximal_vertex_connectivity directory")
    parser.add_argument("--producer-stream", type=Path,
                        help="optional regenerated witnesses.jsonl for entry comparison")
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()

    need(digest(args.source / "SHA256SUMS") == REVIEWED_MANIFEST_SHA256,
         "reviewed source manifest hash differs")
    need(digest(args.source / "SUMMARY.json") == REVIEWED_SUMMARY_SHA256,
         "reviewed summary hash differs")
    summary = json.loads((args.source / "SUMMARY.json").read_text())

    core_counts, orbit_counts, core_digests = check_core_orbits(summary, args.solver)
    marked_counts, costs, special_sets, jobs_digest = check_marked(
        summary, args.solver, args.producer_stream
    )
    result = {
        "status": "INDEPENDENT_SAT_ENUMERATION_VERIFIED_H3909_FINITE_HINGE",
        "python": sys.version.split()[0],
        "pysat": pysat.__version__,
        "solver": args.solver,
        "core_labeled_counts": {str(k): v for k, v in core_counts.items()},
        "core_orbit_counts": {str(k): v for k, v in orbit_counts.items()},
        "core_word_set_sha256": {str(k): v for k, v in core_digests.items()},
        "marked10": marked_counts[10],
        "marked11": marked_counts[11],
        "complete_marked_jobs": len(summary["rows"]),
        "triangle_cover_records": sum(costs.values()),
        "minimum_cover_cost_histogram": dict(sorted(costs.items())),
        "special_sets_checked_in_cover_records": special_sets,
        "job_evidence_sha256": jobs_digest,
        "producer_entry_sets_compared": args.producer_stream is not None,
        "solver_terminal_unsat_after_blocking": True,
        "good43_found": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
