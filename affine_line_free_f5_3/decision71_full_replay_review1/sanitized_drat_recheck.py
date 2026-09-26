#!/usr/bin/env python3
"""Resumably recheck a decision71 corpus with diagnostic-safe DRAT-trim.

This checker is deliberately separate from the proof generator and from the
review's structural CNF auditor.  It runs a mechanically frozen, two-call
warning-printer patch of pinned DRAT-trim under AddressSanitizer and
UndefinedBehaviorSanitizer.  All warnings and checker control flow remain
enabled.  Every successful case gets an atomic record tied to the exact CNF,
proof, source, checker binary, and captured checker output.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import time


COUNT = 109_676
DOMAIN_SHA256 = "02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2"
STOCK_SOURCE_SHA256 = "d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee"
WARNING_SAFE_SOURCE_SHA256 = (
    "12173598973df1d7d374cfedea977451c10d5a7aea7c90dc77f41c8cf2fad1b0"
)
ORIGINAL_STATUS = "UNSAT_DRAT_VERIFIED"
SAFE_STATUS = "UNSAT_DRAT_ASAN_UBSAN_DIAGNOSTIC_PATCH_VERIFIED"
BAD_DIAGNOSTICS = (
    b"AddressSanitizer",
    b"UndefinedBehaviorSanitizer",
    b"runtime error:",
    b"LeakSanitizer",
)


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def require_sanitizer_instrumentation(path: Path) -> None:
    """Reject an accidentally supplied ordinary DRAT-trim executable.

    This is an ELF-level guard, not a substitute for the documented compiler
    command or the recorded binary hash.  Sanitized GCC builds retain these
    undefined dynamic runtime symbols even when ordinary symbols are stripped.
    """
    image = path.read_bytes()
    missing = [symbol.decode("ascii") for symbol in
               (b"__asan_init", b"__ubsan_handle_") if symbol not in image]
    if missing:
        raise ValueError(
            f"checker binary lacks sanitizer runtime symbols: {missing}"
        )


def case_prefix(root: Path, index: int) -> Path:
    return root / f"{index // 1000:03d}" / f"case_{index:06d}"


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def verified_marker(output: bytes) -> bool:
    return any(line.strip() == b"s VERIFIED" for line in output.splitlines())


def expected_case(
    index: int,
    original: dict,
    checker_source_hash: str,
    checker_binary_hash: str,
) -> dict:
    return {
        "index": index,
        "status": SAFE_STATUS,
        "cnf_sha256": original["cnf_sha256"],
        "proof_sha256": original["proof_sha256"],
        "proof_bytes": original["proof_bytes"],
        "upstream_checker_source_sha256": STOCK_SOURCE_SHA256,
        "checker_source_sha256": checker_source_hash,
        "checker_binary_sha256": checker_binary_hash,
        "checker_options": [],
        "warning_printer_patch": "two raw-buffer calls; diagnostics only",
        "asan_options": "detect_leaks=0:halt_on_error=1:abort_on_error=1",
        "ubsan_options": "halt_on_error=1:print_stacktrace=1",
        "returncode": 0,
    }


def validate_original(proofs: Path, index: int) -> tuple[Path, Path, dict]:
    prefix = case_prefix(proofs, index)
    cnf = prefix.with_suffix(".cnf")
    proof = prefix.with_suffix(".drat")
    record_path = prefix.with_suffix(".json")
    record = json.loads(record_path.read_text())
    if record.get("index") != index or record.get("status") != ORIGINAL_STATUS:
        raise ValueError(f"case {index}: original record is not verified")
    cnf_hash = file_sha256(cnf)
    proof_hash = file_sha256(proof)
    if record.get("cnf_sha256") != cnf_hash:
        raise ValueError(f"case {index}: original CNF hash differs")
    if (record.get("proof_sha256") != proof_hash
            or record.get("proof_bytes") != proof.stat().st_size):
        raise ValueError(f"case {index}: original proof hash or size differs")
    return cnf, proof, record


def reusable(output_root: Path, expected: dict, index: int) -> bool:
    prefix = case_prefix(output_root, index)
    log_path = prefix.with_suffix(".sanitized.check.log")
    record_path = prefix.with_suffix(".sanitized.json")
    if not log_path.is_file() or not record_path.is_file():
        return False
    record = json.loads(record_path.read_text())
    for key, value in expected.items():
        if record.get(key) != value:
            return False
    output = log_path.read_bytes()
    checker_seconds = record.get("checker_seconds")
    return (
        record.get("checker_output_sha256") == sha256(output).hexdigest()
        and isinstance(checker_seconds, (int, float))
        and checker_seconds >= 0
        and verified_marker(output)
        and not any(marker in output for marker in BAD_DIAGNOSTICS)
    )


def recheck(args: argparse.Namespace) -> dict:
    begun = time.monotonic()
    if not 0 <= args.start < args.stop <= COUNT:
        raise ValueError("range must satisfy 0 <= start < stop <= 109676")
    if file_sha256(args.domain) != DOMAIN_SHA256:
        raise ValueError("representative domain hash differs")
    domain = json.loads(args.domain.read_text())
    if not isinstance(domain, list) or len(domain) != COUNT:
        raise ValueError("representative domain is incomplete")
    if file_sha256(args.upstream_checker_source) != STOCK_SOURCE_SHA256:
        raise ValueError("upstream source is not the pinned stock DRAT-trim source")
    checker_source_hash = file_sha256(args.checker_source)
    if checker_source_hash != WARNING_SAFE_SOURCE_SHA256:
        raise ValueError("checker source is not the frozen diagnostic-only patch")
    checker_binary_hash = file_sha256(args.checker_binary)
    if not os.access(args.checker_binary, os.X_OK):
        raise ValueError("checker binary is not executable")
    require_sanitizer_instrumentation(args.checker_binary)

    environment = os.environ.copy()
    environment["ASAN_OPTIONS"] = (
        "detect_leaks=0:halt_on_error=1:abort_on_error=1"
    )
    environment["UBSAN_OPTIONS"] = "halt_on_error=1:print_stacktrace=1"
    reused = 0
    checked = 0
    checker_seconds = 0.0
    for index in range(args.start, args.stop):
        cnf, proof, original = validate_original(args.proofs, index)
        expected = expected_case(
            index, original, checker_source_hash, checker_binary_hash
        )
        if reusable(args.out, expected, index):
            reused += 1
        else:
            started = time.monotonic()
            process = subprocess.run(
                [args.checker_binary, cnf, proof],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=environment,
                check=False,
            )
            elapsed = time.monotonic() - started
            checker_seconds += elapsed
            output = process.stdout
            if process.returncode != 0:
                raise RuntimeError(
                    f"case {index}: sanitizer checker exited {process.returncode}"
                )
            diagnostics = [
                marker.decode("ascii") for marker in BAD_DIAGNOSTICS
                if marker in output
            ]
            if diagnostics:
                raise RuntimeError(
                    f"case {index}: sanitizer diagnostic(s): {diagnostics}"
                )
            if not verified_marker(output):
                raise RuntimeError(f"case {index}: checker did not print s VERIFIED")
            prefix = case_prefix(args.out, index)
            log_path = prefix.with_suffix(".sanitized.check.log")
            record_path = prefix.with_suffix(".sanitized.json")
            atomic_write(log_path, output)
            record = dict(expected)
            record.update({
                "checker_output_sha256": sha256(output).hexdigest(),
                "checker_seconds": elapsed,
            })
            atomic_write(
                record_path,
                (json.dumps(record, indent=2, sort_keys=True) + "\n").encode(),
            )
        checked += 1
        if checked % 100 == 0:
            print(json.dumps({
                "through": index,
                "checked": checked,
                "reused": reused,
                "seconds": time.monotonic() - begun,
            }), flush=True)

    final_identities = {
        "domain": file_sha256(args.domain),
        "upstream_source": file_sha256(args.upstream_checker_source),
        "checker_source": file_sha256(args.checker_source),
        "checker_binary": file_sha256(args.checker_binary),
    }
    expected_identities = {
        "domain": DOMAIN_SHA256,
        "upstream_source": STOCK_SOURCE_SHA256,
        "checker_source": WARNING_SAFE_SOURCE_SHA256,
        "checker_binary": checker_binary_hash,
    }
    if final_identities != expected_identities:
        raise RuntimeError("domain or checker identity changed during recheck")

    result = {
        "status": "COMPLETE_RANGE_SANITIZED_DRAT_VERIFIED",
        "start": args.start,
        "stop": args.stop,
        "verified": checked,
        "reused_records": reused,
        "domain_sha256": DOMAIN_SHA256,
        "upstream_checker_source_sha256": STOCK_SOURCE_SHA256,
        "checker_source_sha256": checker_source_hash,
        "checker_binary_sha256": checker_binary_hash,
        "checker_options": [],
        "warning_printer_patch": "two raw-buffer calls; diagnostics only",
        "sanitizers": ["address", "undefined"],
        "fresh_checker_seconds": checker_seconds,
        "total_seconds": time.monotonic() - begun,
    }
    summary_path = args.out / (
        f"sanitized_recheck_{args.start}_{args.stop}.json"
    )
    atomic_write(
        summary_path,
        (json.dumps(result, indent=2, sort_keys=True) + "\n").encode(),
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", type=Path, required=True)
    parser.add_argument("--proofs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--upstream-checker-source", type=Path, required=True)
    parser.add_argument("--checker-source", type=Path, required=True)
    parser.add_argument("--checker-binary", type=Path, required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--stop", type=int, required=True)
    args = parser.parse_args()
    result = recheck(args)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
