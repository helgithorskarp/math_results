#!/usr/bin/env python3
"""Sanitizer and adversarial controls for the narrowly repaired DRAT checker."""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess


SAFE_SOURCE_SHA256 = "6658bb2543bbf9c556171795f735a2c4418c9dd42c4aaea8281c16c6388afffb"
SAFE_RELEASE_SHA256 = "e2076223bbd2a2bd2b60f90eaabb359b9d020fd6c5869bb40fe23c743060b34d"
SAFE_SANITIZED_SHA256 = "66b10b6e6b7da8ce4d9bee51d77199c90679ab326f1127f67c1dc45bc6cf771b"


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def case_paths(root, index):
    prefix = Path(root) / f"{index // 1000:03d}" / f"case_{index:06d}"
    return prefix.with_suffix(".cnf"), prefix.with_suffix(".drat")


def checked_run(checker, cnf, proof, expected_acceptance, env):
    run = subprocess.run([str(checker), str(cnf), str(proof)], env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, timeout=120)
    lines = run.stdout.splitlines()
    diagnostics = [line for line in lines
                   if "runtime error:" in line or "AddressSanitizer:" in line]
    accepted = run.returncode == 0 and "s VERIFIED" in lines
    rejected = run.returncode >= 0 and "s NOT VERIFIED" in lines and not accepted
    if diagnostics or (accepted if not expected_acceptance else not accepted):
        raise ValueError(f"unexpected sanitized-checker outcome for {cnf}")
    if not expected_acceptance and not rejected:
        raise ValueError(f"wrong input did not reject normally: {cnf}")
    return {"cnf_sha256": digest(cnf), "proof_sha256": digest(proof),
            "accepted": accepted, "normal_rejection": rejected}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--sanitized", type=Path, required=True)
    parser.add_argument("--proofs", type=Path, required=True)
    parser.add_argument("--adversarial", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    expected_hashes = ((args.source, SAFE_SOURCE_SHA256),
                       (args.release, SAFE_RELEASE_SHA256),
                       (args.sanitized, SAFE_SANITIZED_SHA256))
    for path, wanted in expected_hashes:
        if digest(path) != wanted:
            raise ValueError(f"unexpected file identity: {path}")
    symbols = subprocess.check_output(["nm", "-D", str(args.sanitized)], text=True)
    if "__asan_init" not in symbols or "__ubsan_handle_shift_out_of_bounds" not in symbols:
        raise ValueError("sanitized checker lacks ASan/UBSan instrumentation")
    env = dict(os.environ, ASAN_OPTIONS="detect_leaks=0:halt_on_error=1",
               UBSAN_OPTIONS="halt_on_error=1:print_stacktrace=1")

    production = []
    for index in (0, 20750, 109675):
        cnf, proof = case_paths(args.proofs, index)
        production.append({"index": index,
                           **checked_run(args.sanitized, cnf, proof, True, env)})

    summary = json.loads((args.adversarial / "summary.json").read_text())
    if summary.get("status") != "FOUR_MINIMAL_TWO_CLAUSE_WEAKENINGS_VERIFIED":
        raise ValueError("missing adversarial-control corpus")
    adversarial = []
    for record in summary["records"]:
        index, omission = record["index"], record["omitted_clause"]
        prefix = args.adversarial / f"case_{index}_omit_{omission}"
        proof = prefix.with_suffix(".drat")
        valid = checked_run(args.sanitized, prefix.with_suffix(".cnf"), proof, True, env)
        wrong = checked_run(args.sanitized,
                            args.adversarial / f"case_{index}_omit_both.cnf",
                            proof, False, env)
        adversarial.append({"index": index, "omission": omission,
                            "valid": valid, "wrong_input": wrong})

    result = {
        "status": "SAFE_CHECKER_SANITIZER_AND_ADVERSARIAL_CONTROLS_PASSED",
        "safe_source_sha256": SAFE_SOURCE_SHA256,
        "safe_release_sha256": SAFE_RELEASE_SHA256,
        "safe_sanitized_sha256": SAFE_SANITIZED_SHA256,
        "environment": {k: env[k] for k in ("ASAN_OPTIONS", "UBSAN_OPTIONS")},
        "production_proofs_cleanly_verified": len(production),
        "adversarial_valid_proofs_cleanly_verified": len(adversarial),
        "adversarial_wrong_inputs_normally_rejected": len(adversarial),
        "production": production,
        "adversarial": adversarial,
    }
    temporary = args.out.with_name(args.out.name + ".tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n")
    temporary.replace(args.out)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("production", "adversarial")}, indent=2))


if __name__ == "__main__":
    main()
