"""Audit every saved record and regenerated CNF; produce compact block hashes.

This verifies complete coverage, source correspondence and unchanged evidence.
It does not check DRAT inferences again. replay.py does that separately.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

from evidence import (COUNT, DOMAIN_SHA256, atomic_json, audit_record,
                      blocks as digest_blocks, case_files, load_domain)


def audit(domain, proofs, start=0, stop=COUNT, wait_for_records=False):
    if not 0 <= start < stop <= COUNT:
        raise ValueError("invalid audit interval")
    begun = time.monotonic()
    blocks = []
    checker_counts = Counter()
    type_counts = Counter()
    total_bytes = 0
    total_solver = total_run = 0.0
    hardest = (-1, -1)
    minimum_clauses, maximum_clauses = 10**9, 0
    for first, last in digest_blocks(start, stop):
        inputs, traces = hashlib.sha256(), hashlib.sha256()
        proof_bytes = 0
        for index in range(first, last):
            while wait_for_records and not case_files(proofs, index)[3].exists():
                if (Path(proofs) / "STOP.json").exists():
                    raise RuntimeError("proof producer stopped; inspect STOP.json")
                time.sleep(1)
            r = audit_record(proofs, index, domain[index])
            inputs.update(bytes.fromhex(r["cnf_sha256"]))
            traces.update(bytes.fromhex(r["proof_sha256"]))
            proof_bytes += r["proof_bytes"]
            checker_counts[r["checker_sha256"]] += 1
            type_counts[r["type"]] += 1
            total_solver += r["solver_seconds"]
            total_run += r["total_seconds"]
            hardest = max(hardest, (r["stats"]["conflicts"], index))
            minimum_clauses = min(minimum_clauses, r["clauses"])
            maximum_clauses = max(maximum_clauses, r["clauses"])
        total_bytes += proof_bytes
        blocks.append({"start": first, "stop": last, "count": last - first,
                       "ordered_cnf_hashes_sha256": inputs.hexdigest(),
                       "ordered_proof_hashes_sha256": traces.hexdigest(),
                       "proof_bytes": proof_bytes})
    complete = start == 0 and stop == COUNT
    if complete and dict(type_counts) != dict(Counter(r["type"] for r in domain)):
        raise ValueError("typed coverage mismatch")
    return {
        "status": "COMPLETE_CERTIFICATE_CORPUS_AUDITED" if complete else "PARTIAL_CORPUS_AUDITED",
        "complete_family": complete, "start": start, "stop": stop,
        "verified_records": stop - start, "domain_sha256": DOMAIN_SHA256,
        "proof_format": "binary DRAT", "proofs_rechecked_by_this_audit": False,
        "hash_rule": "SHA256 of the concatenated ordered 32-byte SHA256 digests within each half-open block",
        "blocks": blocks, "proof_bytes": total_bytes,
        "checker_counts": dict(sorted(checker_counts.items())),
        "counts_by_type": [type_counts[t] for t in range(20)],
        "maximum_conflicts": hardest[0], "hardest_index": hardest[1],
        "clause_range": [minimum_clauses, maximum_clauses],
        "summed_solver_seconds": total_solver, "summed_solver_checker_seconds": total_run,
        "audit_seconds": time.monotonic() - begun,
        "waited_for_records": wait_for_records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=Path, required=True)
    parser.add_argument("--proofs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=COUNT)
    parser.add_argument("--wait-for-records", action="store_true",
                        help="follow a running proof producer; never infer a missing record")
    parser.add_argument("--compare-inputs", type=Path,
                        help="compare a complete audit's input block digests with a published manifest")
    args = parser.parse_args()
    result = audit(load_domain(args.domain), args.proofs, args.start, args.stop, args.wait_for_records)
    if args.compare_inputs:
        expected=json.loads(args.compare_inputs.read_text())
        if not result['complete_family'] or not expected['complete_family']:
            raise ValueError('input-manifest comparison requires complete coverage')
        fields=('start','stop','count','ordered_cnf_hashes_sha256')
        if ([[b[k] for k in fields] for b in result['blocks']]
            != [[b[k] for k in fields] for b in expected['blocks']]):
            raise ValueError('regenerated input blocks differ from published proof inputs')
        result['published_input_blocks_matched']=True
    atomic_json(args.out, result)
    print(json.dumps({k: v for k, v in result.items() if k != "blocks"}, indent=2))


if __name__ == "__main__":
    main()
