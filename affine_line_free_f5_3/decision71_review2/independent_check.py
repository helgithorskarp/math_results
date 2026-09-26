#!/usr/bin/env python3
"""Independent source-to-CNF and complete DRAT-corpus checker.

This file intentionally imports no module from decision71.  It reconstructs
the affine lines and direct cardinality clauses from the definitions, checks
every saved record and byte-for-byte CNF, and can invoke a selected DRAT
checker on every trace.  Raw traces stay outside the repository.
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import time


COUNT = 109676
DOMAIN_SHA256 = "02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2"
STOCK_DRAT_SHA256 = "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a"
EXPECTED_TYPE_COUNTS = [
    252, 2496, 2765, 2950, 1345, 2254, 2517, 2242, 2009, 1978,
    6555, 13621, 14022, 6556, 7543, 15200, 7038, 8481, 7841, 2011,
]


def file_sha256(path):
    h = sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def affine_lines(dimension):
    """Build lines from unordered pairs, independently of normal vectors."""
    points = tuple(product(range(5), repeat=dimension))
    index = {p: i + 1 for i, p in enumerate(points)}
    lines = set()
    for a, p in enumerate(points):
        for q in points[a + 1:]:
            step = tuple((y - x) % 5 for x, y in zip(p, q))
            line = tuple(sorted(index[tuple((x + t * d) % 5
                                            for x, d in zip(p, step))]
                                for t in range(5)))
            lines.add(line)
    expected = 30 if dimension == 2 else 775
    if len(lines) != expected:
        raise ValueError(f"expected {expected} affine lines, found {len(lines)}")
    return tuple(sorted(lines))


SPATIAL_LINES = affine_lines(3)
QUOTIENT_LINES = affine_lines(2)


def direct_cnf(word):
    if len(word) != 25 or any(c not in "01234" for c in word):
        raise ValueError("invalid weight word")
    weights = tuple(map(int, word))
    if sum(weights) != 71:
        raise ValueError("weight word does not have cardinality 71")
    if any(sum(weights[v - 1] for v in line) > 16 for line in QUOTIENT_LINES):
        raise ValueError("weight word violates a quotient-plane bound")

    clauses = [tuple(-v for v in line) for line in SPATIAL_LINES]
    for i, n in enumerate(weights):
        fiber = tuple(range(5 * i + 1, 5 * i + 6))
        clauses.extend(tuple(-v for v in chosen)
                       for chosen in combinations(fiber, n + 1))
        clauses.extend(tuple(chosen)
                       for chosen in combinations(fiber, 6 - n))

    full = [i for i, n in enumerate(weights) if n == 4]
    gauge = None
    for a, b, c in combinations(full, 3):
        ax, ay = divmod(a, 5)
        bx, by = divmod(b, 5)
        cx, cy = divmod(c, 5)
        if ((bx - ax) * (cy - ay) - (cx - ax) * (by - ay)) % 5:
            gauge = (a, b, c)
            break
    if gauge is None:
        raise ValueError("no noncollinear triple of four-point fibers")
    clauses.extend((-(5 * i + 1),) for i in gauge)
    header = f"p cnf 125 {len(clauses)}\n"
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return (header + body).encode("ascii"), gauge, len(clauses)


def case_paths(proofs, index):
    prefix = proofs / f"{index // 1000:03d}" / f"case_{index:06d}"
    return tuple(prefix.with_suffix(s) for s in
                 (".cnf", ".drat", ".check.log", ".json"))


def inspect_case(proofs, checker, recheck, index, representative):
    cnf_path, proof_path, log_path, record_path = case_paths(proofs, index)
    cnf, gauge, clauses = direct_cnf(representative["weights"])
    stored_cnf = cnf_path.read_bytes()
    if stored_cnf != cnf:
        raise ValueError(f"CNF bytes disagree with definition at {index}")
    cnf_hash = sha256(cnf).hexdigest()
    proof_hash = file_sha256(proof_path)
    proof_bytes = proof_path.stat().st_size
    record = json.loads(record_path.read_text())
    expected = {
        "index": index,
        "type": representative["type"],
        "weights": representative["weights"],
        "gauge": list(gauge),
        "variables": 125,
        "clauses": clauses,
        "input_catalogue_sha256": DOMAIN_SHA256,
        "cnf_sha256": cnf_hash,
        "proof_sha256": proof_hash,
        "proof_bytes": proof_bytes,
        "status": "UNSAT_DRAT_VERIFIED",
        "checker_sha256": STOCK_DRAT_SHA256,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise ValueError(f"record field {key} disagrees at {index}")
    if "s VERIFIED" not in log_path.read_text():
        raise ValueError(f"saved checker log is not accepting at {index}")
    if recheck:
        run = subprocess.run(
            [str(checker), str(cnf_path), str(proof_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if run.returncode or b"s VERIFIED" not in run.stdout:
            raise ValueError(f"fresh stock DRAT check failed at {index}")
    return {
        "index": index,
        "type": representative["type"],
        "clauses": clauses,
        "cnf_hash": cnf_hash,
        "proof_hash": proof_hash,
        "proof_bytes": proof_bytes,
        "conflicts": int(record["stats"]["conflicts"]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--domain", type=Path, required=True)
    parser.add_argument("--proofs", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    recheck = args.drat_trim is not None
    checker = args.drat_trim.resolve() if recheck else None
    expected = json.loads((Path(__file__).with_name("EXPECTED.json")).read_text())
    if (expected["domain_sha256"] != DOMAIN_SHA256
            or expected["cases"] != COUNT
            or expected["counts_by_type"] != EXPECTED_TYPE_COUNTS
            or expected["spatial_lines"] != len(SPATIAL_LINES)
            or expected["quotient_lines"] != len(QUOTIENT_LINES)):
        raise ValueError("review expectation constants disagree with checker")
    for name, wanted in expected["reviewed_source_sha256"].items():
        if file_sha256(args.source / name) != wanted:
            raise ValueError(f"reviewed source file changed: {name}")
    if recheck and file_sha256(checker) != STOCK_DRAT_SHA256:
        raise ValueError("selected checker is not the pinned stock DRAT-trim binary")
    if file_sha256(args.domain) != DOMAIN_SHA256:
        raise ValueError("representative domain hash mismatch")
    domain = json.loads(args.domain.read_text())
    if len(domain) != COUNT:
        raise ValueError("representative domain is incomplete")
    if Counter(r.get("type") for r in domain) != Counter(
            {i: n for i, n in enumerate(EXPECTED_TYPE_COUNTS)}):
        raise ValueError("representative type counts disagree")

    begun = time.monotonic()
    all_cnf, all_proofs = sha256(), sha256()
    total_bytes = 0
    minimum_clauses, maximum_clauses = 10**9, 0
    hardest = (-1, -1)
    batch_size = max(64, args.jobs * 8)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for first in range(0, COUNT, batch_size):
            last = min(COUNT, first + batch_size)
            futures = [pool.submit(inspect_case, args.proofs, checker, recheck,
                                   i, domain[i]) for i in range(first, last)]
            for future in futures:
                item = future.result()
                all_cnf.update(bytes.fromhex(item["cnf_hash"]))
                all_proofs.update(bytes.fromhex(item["proof_hash"]))
                total_bytes += item["proof_bytes"]
                minimum_clauses = min(minimum_clauses, item["clauses"])
                maximum_clauses = max(maximum_clauses, item["clauses"])
                hardest = max(hardest, (item["conflicts"], item["index"]))
            if last % 1000 < batch_size or last == COUNT:
                print(json.dumps({"through": last, "seconds": time.monotonic() - begun}),
                      flush=True)

    result = {
        "status": ("COMPLETE_INDEPENDENT_STOCK_DRAT_RECHECK_PASSED"
                   if recheck else "COMPLETE_INDEPENDENT_CORPUS_AUDIT_PASSED"),
        "cases": COUNT,
        "proofs_rechecked": COUNT if recheck else 0,
        "reviewed_source_commit": expected["reviewed_source_commit"],
        "domain_sha256": DOMAIN_SHA256,
        "spatial_lines": len(SPATIAL_LINES),
        "quotient_lines": len(QUOTIENT_LINES),
        "counts_by_type": EXPECTED_TYPE_COUNTS,
        "clause_range": [minimum_clauses, maximum_clauses],
        "proof_bytes": total_bytes,
        "maximum_conflicts": hardest[0],
        "hardest_index": hardest[1],
        "ordered_cnf_hashes_sha256": all_cnf.hexdigest(),
        "ordered_proof_hashes_sha256": all_proofs.hexdigest(),
        "checker_sha256": STOCK_DRAT_SHA256 if recheck else None,
        "seconds": time.monotonic() - begun,
    }
    temporary = args.out.with_name(args.out.name + ".tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n")
    temporary.replace(args.out)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
