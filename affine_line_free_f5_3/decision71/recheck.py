"""Check an existing DRAT corpus into a new directory, preserving its evidence.

No SAT solver is run. Every selected trace is checked afresh. Ranges must
contain whole published digest blocks. A failed or interrupted invocation
leaves its new logs but never writes a successful range summary. There is
deliberately no implicit resume or reuse of earlier acceptance records.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

from evidence import (COUNT, DOMAIN_SHA256, atomic_json, audit_record, blocks,
                      case_files, digest, load_domain)

HERE = Path(__file__).resolve().parent
HASH_FIELDS = ("ordered_cnf_hashes_sha256", "ordered_proof_hashes_sha256")


def selected_blocks(manifest, start, stop):
    """Require a complete manifest and exact block-aligned range coverage."""
    if (manifest.get("complete_family") is not True
            or manifest.get("verified_records") != COUNT
            or manifest.get("domain_sha256") != DOMAIN_SHA256
            or manifest.get("start") != 0 or manifest.get("stop") != COUNT):
        raise ValueError("a complete manifest for the fixed domain is required")
    records = manifest["blocks"]
    if [(b["start"], b["stop"]) for b in records] != blocks(0, COUNT):
        raise ValueError("manifest has missing, overlapping, or unexpected blocks")
    for b in records:
        if b["count"] != b["stop"] - b["start"] or b["proof_bytes"] < 0:
            raise ValueError("incorrect manifest block count or size")
        for field in HASH_FIELDS:
            if len(bytes.fromhex(b[field])) != 32:
                raise ValueError("invalid manifest digest")
    selected = [b for b in records if start <= b["start"] and b["stop"] <= stop]
    if (not 0 <= start < stop <= COUNT or not selected
            or selected[0]["start"] != start or selected[-1]["stop"] != stop):
        raise ValueError("range endpoints must be complete manifest block boundaries")
    return selected


def new_output(proofs, out):
    """Refuse overlapping paths and any existing output, including symlinks."""
    proofs, out = Path(proofs).resolve(), Path(out).resolve()
    if proofs == out or proofs in out.parents or out in proofs.parents:
        raise ValueError("source corpus and new output must be disjoint directories")
    out.mkdir(parents=True, exist_ok=False)
    return proofs, out


def recheck_case(domain, proofs, out, index, checker, checker_hash):
    source = case_files(proofs, index)
    before = [digest(p) for p in source]
    old = audit_record(proofs, index, domain[index])
    if before[:2] != [old["cnf_sha256"], old["proof_sha256"]]:
        raise ValueError("source changed while its record was being audited")
    _, _, log, record_path = case_files(out, index)
    log.parent.mkdir(parents=True, exist_ok=True)
    if record_path.exists():
        raise FileExistsError("fresh check cannot replace an earlier record")
    begun = time.monotonic()
    with log.open("x") as stream:
        result = subprocess.run([str(checker), str(source[0]), str(source[1])],
                                stdout=stream, stderr=subprocess.STDOUT)
    if [digest(p) for p in source] != before:
        raise ValueError("original CNF, proof, checker log, or record changed")
    if result.returncode != 0 or "s VERIFIED" not in log.read_text().splitlines():
        raise ValueError(f"fresh DRAT check rejected case {index}")
    record = {
        "status": "EXISTING_PROOF_DRAT_RECHECKED", "index": index,
        "cnf_sha256": before[0], "proof_sha256": before[1],
        "proof_bytes": old["proof_bytes"], "original_log_sha256": before[2],
        "original_record_sha256": before[3],
        "original_checker_sha256": old["checker_sha256"],
        "recheck_checker_sha256": checker_hash, "recheck_log_sha256": digest(log),
        "checker_returncode": result.returncode, "source_hashes_unchanged": True,
        "seconds": time.monotonic() - begun,
    }
    atomic_json(record_path, record)
    return record


def recheck(domain, proofs, out, checker, manifest_path, start=0, stop=COUNT):
    manifest_path, checker = Path(manifest_path), Path(checker).resolve()
    manifest_bytes = manifest_path.read_bytes()
    selected = selected_blocks(json.loads(manifest_bytes), start, stop)
    checker_hash = digest(checker)
    proofs, out = new_output(proofs, out)
    begun = time.monotonic()
    results, old_checkers = [], Counter()
    for expected in selected:
        inputs, traces, records, logs = [hashlib.sha256() for _ in range(4)]
        proof_bytes = 0
        for index in range(expected["start"], expected["stop"]):
            r = recheck_case(domain, proofs, out, index, checker, checker_hash)
            for accumulator, field in ((inputs, "cnf_sha256"), (traces, "proof_sha256"),
                                       (records, "original_record_sha256"),
                                       (logs, "original_log_sha256")):
                accumulator.update(bytes.fromhex(r[field]))
            proof_bytes += r["proof_bytes"]
            old_checkers[r["original_checker_sha256"]] += 1
        block = {"start": expected["start"], "stop": expected["stop"],
                 "count": expected["stop"] - expected["start"],
                 HASH_FIELDS[0]: inputs.hexdigest(), HASH_FIELDS[1]: traces.hexdigest(),
                 "proof_bytes": proof_bytes}
        if any(block[k] != expected[k] for k in block):
            raise ValueError("checked input/proof block differs from supplied manifest")
        block["ordered_original_record_hashes_sha256"] = records.hexdigest()
        block["ordered_original_log_hashes_sha256"] = logs.hexdigest()
        results.append(block)
        print(json.dumps({"through": expected["stop"] - 1,
                          "fresh_checks": expected["stop"] - start}), flush=True)
    if digest(checker) != checker_hash or manifest_path.read_bytes() != manifest_bytes:
        raise ValueError("checker or reference manifest changed during recheck")
    complete = start == 0 and stop == COUNT
    result = {
        "status": ("COMPLETE_EXISTING_CORPUS_DRAT_RECHECKED" if complete
                   else "PARTIAL_EXISTING_CORPUS_DRAT_RECHECKED"),
        "complete_family": complete, "start": start, "stop": stop,
        "fresh_checks": stop - start, "reused_acceptances": 0,
        "domain_sha256": DOMAIN_SHA256,
        "reference_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "input_and_proof_blocks_match_reference": True,
        "original_source_hashes_unchanged": True,
        "original_checker_counts": dict(sorted(old_checkers.items())),
        "recheck_checker_sha256": checker_hash,
        "proof_bytes": sum(b["proof_bytes"] for b in results), "blocks": results,
        "python_version": platform.python_version(),
        "driver_source_hashes": {name: digest(HERE / name) for name in
                                 ("recheck.py", "evidence.py", "point_model.py")},
        "seconds": time.monotonic() - begun,
        "scope": "Fresh DRAT checks and source integrity; no new mathematical reduction or peer acceptance",
    }
    atomic_json(out / "recheck.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", type=Path, required=True)
    parser.add_argument("--proofs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="new directory, outside the source corpus")
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=HERE / "CERTIFICATES.json")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=COUNT)
    args = parser.parse_args()
    result = recheck(load_domain(args.domain), args.proofs, args.out, args.drat_trim,
                     args.manifest, args.start, args.stop)
    print(json.dumps({k: v for k, v in result.items() if k != "blocks"}, indent=2))


if __name__ == "__main__":
    main()
