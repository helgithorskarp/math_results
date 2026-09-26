"""Validate archive preservation and fail-closed proof rechecking.

This consumes two real cases from an existing corpus and damages only
private copies. It does not run the complete family or claim peer review.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil

from evidence import atomic_json, case_files, digest, load_domain
from recheck import HERE, new_output, recheck_case, selected_blocks


def reject(action, exception):
    try:
        action()
    except exception:
        return
    raise ValueError("a deliberately invalid control was accepted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", type=Path, required=True)
    parser.add_argument("--proofs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    args = parser.parse_args()
    domain = load_domain(args.domain)
    checker = args.drat_trim.resolve()
    checker_hash = digest(checker)
    proofs, out = new_output(args.proofs, args.out)
    indices = [0, 109675]
    original_hashes = {i: [digest(p) for p in case_files(proofs, i)] for i in indices}
    old_checkers = {}
    for index in indices:
        case = recheck_case(domain, proofs, out / "positive", index, checker, checker_hash)
        if case["checker_returncode"] != 0 or not case["source_hashes_unchanged"]:
            raise ValueError("positive source-preserving control failed")
        old_checkers[str(index)] = case["original_checker_sha256"]
    original = case_files(proofs, 0)
    reject(lambda: recheck_case(domain, proofs, out / "positive", 0, checker, checker_hash),
           FileExistsError)
    for bad in (proofs, proofs / "nested", proofs.parent):
        reject(lambda: new_output(proofs, bad), ValueError)
    reject(lambda: new_output(proofs, out), FileExistsError)

    for fault in ("missing", "cnf", "unknown", "proof", "old_log"):
        source = out / f"copy_{fault}"
        paths = case_files(source, 0)
        paths[0].parent.mkdir(parents=True)
        for before, after in zip(original, paths):
            shutil.copyfile(before, after)
        if fault == "missing":
            paths[1].unlink()
        elif fault == "cnf":
            paths[0].write_bytes(b"p cnf 125 1\n1 0\n")
        elif fault == "old_log":
            paths[2].write_text("s NOT VERIFIED\n")
        else:
            record = json.loads(paths[3].read_text())
            if fault == "unknown":
                record["status"] = "UNKNOWN"
            else:
                # The damaged proof has a consistent new hash and still has
                # the historical success log: only a fresh checker rejects it.
                paths[1].write_bytes(b"0\n")
                record["proof_sha256"] = digest(paths[1])
                record["proof_bytes"] = paths[1].stat().st_size
            atomic_json(paths[3], record)
        fresh = out / f"rejected_{fault}"
        reject(lambda: recheck_case(domain, source, fresh, 0, checker, checker_hash),
               (ValueError, FileNotFoundError))
        if case_files(fresh, 0)[3].exists():
            raise ValueError("rejected case obtained a successful record")

    manifest = json.loads((HERE / "CERTIFICATES.json").read_text())
    selected = selected_blocks(manifest, 0, 1000)
    if len(selected) != 1 or selected[0]["count"] != 1000:
        raise ValueError("incorrect bounded manifest coverage")
    for start, stop in ((0, 999), (1, 1000), (1000, 1000), (0, 109677)):
        reject(lambda: selected_blocks(manifest, start, stop), ValueError)
    for fault in ("missing", "overlap", "incomplete", "domain"):
        broken = deepcopy(manifest)
        if fault == "missing":
            broken["blocks"].pop()
        elif fault == "overlap":
            broken["blocks"][1]["start"] = 999
        elif fault == "incomplete":
            broken["complete_family"] = False
        else:
            broken["domain_sha256"] = "0" * 64
        reject(lambda: selected_blocks(broken, 0, 1000), ValueError)
    for index in indices:
        if [digest(p) for p in case_files(proofs, index)] != original_hashes[index]:
            raise ValueError("controls changed the original corpus")
    result = {
        "status": "SOURCE_PRESERVING_RECHECK_CONTROLS_PASSED",
        "fresh_valid_cases": indices, "original_four_files_per_case_unchanged": True,
        "original_checkers_by_case": old_checkers,
        "damaged_case_rejections": ["missing", "cnf", "unknown", "proof", "old_log"],
        "invalid_range_rejections": 4, "invalid_manifest_rejections": 4,
        "source_output_overlap_rejections": 3,
        "existing_output_and_record_rejected": True,
        "recheck_checker_sha256": checker_hash,
        "scope": "Author pipeline controls, not complete proof replay or peer acceptance",
    }
    atomic_json(out / "validation.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
