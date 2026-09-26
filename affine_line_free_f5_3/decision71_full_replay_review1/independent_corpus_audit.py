#!/usr/bin/env python3
"""Independently audit a complete fresh decision71 DRAT replay.

This checker imports no decision71 module.  It reconstructs the spatial
lines from point pairs, writes the direct cardinality clauses from their
Boolean semantics, and checks every generated CNF and replay record.  The
DRAT inferences themselves are checked by the separately invoked stock
DRAT-trim processes during replay.py; this program audits their complete
input/evidence correspondence rather than implementing DRAT again.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import re
import time


COUNT = 109_676
DOMAIN_SHA256 = "02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2"
STOCK_SOURCE_SHA256 = "d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee"
WARNING_SAFE_SOURCE_SHA256 = (
    "12173598973df1d7d374cfedea977451c10d5a7aea7c90dc77f41c8cf2fad1b0"
)
MANIFEST_SHA256 = "ec7fabe454c7a0e6297f3347de038028602a1aae81efd377ff4d938883af31c4"
VERIFIED = "UNSAT_DRAT_VERIFIED"
SANITIZED_VERIFIED = "UNSAT_DRAT_ASAN_UBSAN_DIAGNOSTIC_PATCH_VERIFIED"
RANGE_NAME = re.compile(r"replay_(\d+)_(\d+)\.json\Z")
SANITIZED_RANGE_NAME = re.compile(
    r"sanitized_recheck_(\d+)_(\d+)\.json\Z"
)
BAD_SANITIZER_DIAGNOSTICS = (
    "AddressSanitizer",
    "UndefinedBehaviorSanitizer",
    "runtime error:",
    "LeakSanitizer",
)


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def require_sanitizer_instrumentation(path: Path) -> None:
    image = path.read_bytes()
    missing = [symbol.decode("ascii") for symbol in
               (b"__asan_init", b"__ubsan_handle_") if symbol not in image]
    if missing:
        raise ValueError(
            f"sanitized checker lacks runtime symbols: {missing}"
        )


def variable(point: tuple[int, int, int]) -> int:
    x, y, z = point
    return 1 + 25 * x + 5 * y + z


def spatial_lines() -> tuple[tuple[int, ...], ...]:
    """Construct all affine lines from unordered point pairs."""
    points = tuple(product(range(5), repeat=3))
    lines: set[tuple[int, ...]] = set()
    for first, second in combinations(points, 2):
        direction = tuple((b - a) % 5 for a, b in zip(first, second))
        line = tuple(sorted(variable(tuple((a + t * d) % 5
                                           for a, d in zip(first, direction)))
                            for t in range(5)))
        lines.add(line)
    result = tuple(sorted(lines))
    if len(result) != 775 or any(len(line) != 5 for line in result):
        raise ValueError("point-pair geometry did not give 775 five-point lines")
    pair_counts = Counter(pair for line in result for pair in combinations(line, 2))
    if len(pair_counts) != 7_750 or set(pair_counts.values()) != {1}:
        raise ValueError("the reconstructed lines do not partition point pairs")
    return result


def clause_bytes(clause: tuple[int, ...] | list[int]) -> bytes:
    return (" ".join(map(str, clause)) + " 0\n").encode("ascii")


LINES = spatial_lines()
BASE_BODY = b"".join(clause_bytes(tuple(-value for value in line))
                     for line in LINES)


def direct_formula(word: str) -> tuple[bytes, tuple[int, int, int], int]:
    """Return the exact direct DIMACS bytes, gauge triple, and clause count."""
    if len(word) != 25 or any(symbol not in "01234" for symbol in word):
        raise ValueError("invalid weight word")
    weights = tuple(map(int, word))
    if sum(weights) != 71:
        raise ValueError("weight word does not have total 71")
    body = bytearray(BASE_BODY)
    clauses = len(LINES)
    for index, weight in enumerate(weights):
        fiber = tuple(range(5 * index + 1, 5 * index + 6))
        for chosen in combinations(fiber, weight + 1):
            body.extend(clause_bytes(tuple(-value for value in chosen)))
            clauses += 1
        for absent in combinations(fiber, 6 - weight):
            body.extend(clause_bytes(absent))
            clauses += 1
    full = tuple(index for index, weight in enumerate(weights) if weight == 4)
    gauge = next(
        (triple for triple in combinations(full, 3)
         if ((triple[1] // 5 - triple[0] // 5)
             * (triple[2] % 5 - triple[0] % 5)
             - (triple[2] // 5 - triple[0] // 5)
             * (triple[1] % 5 - triple[0] % 5)) % 5),
        None,
    )
    if gauge is None:
        raise ValueError("no noncollinear full-fiber gauge")
    for index in gauge:
        body.extend(clause_bytes((-(5 * index + 1),)))
        clauses += 1
    header = f"p cnf 125 {clauses}\n".encode("ascii")
    return header + body, gauge, clauses


def case_paths(root: Path, index: int) -> tuple[Path, Path, Path, Path]:
    prefix = root / f"{index // 1000:03d}" / f"case_{index:06d}"
    return tuple(prefix.with_suffix(suffix)
                 for suffix in (".cnf", ".drat", ".check.log", ".json"))


def load_complete_ranges(root: Path, checker_hash: str) -> list[dict]:
    ranges = []
    for path in sorted(root.glob("replay_*_*.json")):
        match = RANGE_NAME.fullmatch(path.name)
        if match is None:
            raise ValueError(f"malformed range result name: {path.name}")
        start, stop = map(int, match.groups())
        if not 0 <= start < stop <= COUNT:
            raise ValueError(f"range {start}:{stop} is empty or out of bounds")
        record = json.loads(path.read_text())
        expected = {
            "status": "COMPLETE_RANGE_DRAT_VERIFIED",
            "start": start,
            "stop": stop,
            "verified": stop - start,
            "complete_family": start == 0 and stop == COUNT,
            "input_catalogue_sha256": DOMAIN_SHA256,
            "checker_sha256": checker_hash,
        }
        for key, value in expected.items():
            if record.get(key) != value:
                raise ValueError(f"range {start}:{stop} has wrong {key}")
        reused = record.get("reused_records")
        if (type(reused) is not int or not 0 <= reused <= record["verified"]):
            raise ValueError(f"range {start}:{stop} has invalid resume count")
        ranges.append(record)
    ranges.sort(key=lambda item: item["start"])
    if not ranges or ranges[0]["start"] != 0 or ranges[-1]["stop"] != COUNT:
        raise ValueError("range summaries do not span the full domain")
    if any(first["stop"] != second["start"]
           for first, second in zip(ranges, ranges[1:])):
        raise ValueError("range summaries have a gap or overlap")
    if sum(item["verified"] for item in ranges) != COUNT:
        raise ValueError("range summaries have the wrong total")
    return ranges


def load_sanitized_ranges(
    root: Path, checker_binary_hash: str
) -> list[dict]:
    ranges = []
    for path in sorted(root.glob("sanitized_recheck_*_*.json")):
        match = SANITIZED_RANGE_NAME.fullmatch(path.name)
        if match is None:
            raise ValueError(f"malformed sanitized range name: {path.name}")
        start, stop = map(int, match.groups())
        if not 0 <= start < stop <= COUNT:
            raise ValueError(
                f"sanitized range {start}:{stop} is empty or out of bounds"
            )
        record = json.loads(path.read_text())
        expected = {
            "status": "COMPLETE_RANGE_SANITIZED_DRAT_VERIFIED",
            "start": start,
            "stop": stop,
            "verified": stop - start,
            "domain_sha256": DOMAIN_SHA256,
            "upstream_checker_source_sha256": STOCK_SOURCE_SHA256,
            "checker_source_sha256": WARNING_SAFE_SOURCE_SHA256,
            "checker_binary_sha256": checker_binary_hash,
            "checker_options": [],
            "warning_printer_patch": "two raw-buffer calls; diagnostics only",
            "sanitizers": ["address", "undefined"],
        }
        for key, value in expected.items():
            if record.get(key) != value:
                raise ValueError(
                    f"sanitized range {start}:{stop} has wrong {key}"
                )
        reused = record.get("reused_records")
        if type(reused) is not int or not 0 <= reused <= record["verified"]:
            raise ValueError(
                f"sanitized range {start}:{stop} has invalid resume count"
            )
        ranges.append(record)
    ranges.sort(key=lambda item: item["start"])
    if not ranges or ranges[0]["start"] != 0 or ranges[-1]["stop"] != COUNT:
        raise ValueError("sanitized ranges do not span the full domain")
    if any(first["stop"] != second["start"]
           for first, second in zip(ranges, ranges[1:])):
        raise ValueError("sanitized ranges have a gap or overlap")
    if sum(item["verified"] for item in ranges) != COUNT:
        raise ValueError("sanitized ranges have the wrong total")
    return ranges


def validate_manifest(manifest: dict) -> list[dict]:
    if (manifest.get("complete_family") is not True
            or manifest.get("start") != 0
            or manifest.get("stop") != COUNT
            or manifest.get("verified_records") != COUNT
            or manifest.get("domain_sha256") != DOMAIN_SHA256):
        raise ValueError("published manifest does not describe the complete domain")
    blocks = manifest.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("published manifest has no digest blocks")
    if blocks[0]["start"] != 0 or blocks[-1]["stop"] != COUNT:
        raise ValueError("published blocks do not span the domain")
    if any(first["stop"] != second["start"]
           for first, second in zip(blocks, blocks[1:])):
        raise ValueError("published blocks have a gap or overlap")
    if any(block["count"] != block["stop"] - block["start"]
           for block in blocks):
        raise ValueError("published block count is inconsistent")
    return blocks


def audit(args: argparse.Namespace) -> dict:
    begun = time.monotonic()
    if file_sha256(args.domain) != DOMAIN_SHA256:
        raise ValueError("representative domain hash differs")
    if file_sha256(args.checker_source) != STOCK_SOURCE_SHA256:
        raise ValueError("DRAT-trim source is not the pinned stock source")
    if file_sha256(args.manifest) != MANIFEST_SHA256:
        raise ValueError("published certificate manifest hash differs")
    known70_hash = file_sha256(args.known70)
    checker_hash = file_sha256(args.checker_binary)
    sanitized_checker_source_hash = file_sha256(args.sanitized_checker_source)
    if sanitized_checker_source_hash != WARNING_SAFE_SOURCE_SHA256:
        raise ValueError("sanitized checker source is not the frozen patch")
    sanitized_checker_hash = file_sha256(args.sanitized_checker_binary)
    require_sanitizer_instrumentation(args.sanitized_checker_binary)
    domain = json.loads(args.domain.read_text())
    if len(domain) != COUNT:
        raise ValueError("representative domain is incomplete")
    manifest = json.loads(args.manifest.read_text())
    published_blocks = validate_manifest(manifest)
    ranges = load_complete_ranges(args.proofs, checker_hash)
    sanitized_ranges = load_sanitized_ranges(
        args.sanitized_recheck, sanitized_checker_hash
    )

    known = json.loads(args.known70.read_text()).get("points")
    if (not isinstance(known, list) or len(known) != 70
            or any(type(value) is not int or not 0 <= value < 125 for value in known)
            or len(set(known)) != 70):
        raise ValueError("known lower-bound fixture is not a 70-point set")
    selected = {value + 1 for value in known}
    if any(set(line) <= selected for line in LINES):
        raise ValueError("known lower-bound fixture contains a complete affine line")

    records = list(args.proofs.glob("[0-9][0-9][0-9]/case_*.json"))
    if len(records) != COUNT:
        raise ValueError(f"found {len(records)} case records, expected {COUNT}")
    sanitized_records = list(args.sanitized_recheck.glob(
        "[0-9][0-9][0-9]/case_*.sanitized.json"
    ))
    if len(sanitized_records) != COUNT:
        raise ValueError(
            f"found {len(sanitized_records)} sanitized records, expected {COUNT}"
        )
    if (list(args.proofs.rglob("WITNESS71_*.json"))
            or list(args.proofs.rglob("UNKNOWN_*.json"))):
        raise ValueError("SAT or UNKNOWN marker exists in the alleged exclusion")

    type_counts: Counter[int] = Counter()
    checker_counts: Counter[str] = Counter()
    proof_bytes = 0
    clause_minimum, clause_maximum = 10**9, 0
    maximum_conflicts = (-1, -1)
    solver_seconds = 0.0
    total_seconds = 0.0
    sanitized_checker_seconds = 0.0
    fresh_blocks = []
    block_index = 0
    input_digest = sha256()
    proof_digest = sha256()
    block_bytes = 0

    for index, representative in enumerate(domain):
        current = published_blocks[block_index]
        if not isinstance(representative, dict):
            raise ValueError(f"domain entry {index} is not an object")
        kind = representative.get("type")
        word = representative.get("weights")
        orbit_size = representative.get("orbit_size")
        if (type(kind) is not int or not 0 <= kind < 20
                or type(word) is not str or len(word) != 25
                or any(symbol not in "01234" for symbol in word)
                or sum(map(int, word)) != 71
                or type(orbit_size) is not int or orbit_size <= 0):
            raise ValueError(f"invalid domain entry {index}")

        cnf, proof, log, record_path = case_paths(args.proofs, index)
        record = json.loads(record_path.read_text())
        generated, gauge, clauses = direct_formula(word)
        generated_hash = sha256(generated).hexdigest()
        expected_record = {
            "index": index,
            "type": kind,
            "weights": word,
            "gauge": list(gauge),
            "variables": 125,
            "clauses": clauses,
            "input_catalogue_sha256": DOMAIN_SHA256,
            "cnf_sha256": generated_hash,
            "status": VERIFIED,
            "checker_sha256": checker_hash,
            "conflict_limit": 500_000,
        }
        for key, value in expected_record.items():
            if record.get(key) != value:
                raise ValueError(f"case {index} has wrong {key}")
        stored_cnf = cnf.read_bytes()
        if stored_cnf != generated:
            raise ValueError(f"stored CNF differs from independent encoding at {index}")
        proof_hash = file_sha256(proof)
        if (record.get("proof_sha256") != proof_hash
                or record.get("proof_bytes") != proof.stat().st_size):
            raise ValueError(f"proof hash or size differs at {index}")
        log_lines = log.read_text().splitlines()
        if not any(line.strip() == "s VERIFIED" for line in log_lines):
            raise ValueError(f"fresh stock-checker log rejects case {index}")

        sanitized_prefix = (
            args.sanitized_recheck / f"{index // 1000:03d}"
            / f"case_{index:06d}"
        )
        sanitized_log = sanitized_prefix.with_suffix(
            ".sanitized.check.log"
        )
        sanitized_record_path = sanitized_prefix.with_suffix(
            ".sanitized.json"
        )
        sanitized_record = json.loads(sanitized_record_path.read_text())
        expected_sanitized = {
            "index": index,
            "status": SANITIZED_VERIFIED,
            "cnf_sha256": generated_hash,
            "proof_sha256": proof_hash,
            "proof_bytes": record["proof_bytes"],
            "upstream_checker_source_sha256": STOCK_SOURCE_SHA256,
            "checker_source_sha256": WARNING_SAFE_SOURCE_SHA256,
            "checker_binary_sha256": sanitized_checker_hash,
            "checker_options": [],
            "warning_printer_patch": (
                "two raw-buffer calls; diagnostics only"
            ),
            "asan_options": (
                "detect_leaks=0:halt_on_error=1:abort_on_error=1"
            ),
            "ubsan_options": "halt_on_error=1:print_stacktrace=1",
            "returncode": 0,
        }
        for key, value in expected_sanitized.items():
            if sanitized_record.get(key) != value:
                raise ValueError(f"sanitized case {index} has wrong {key}")
        sanitized_output = sanitized_log.read_bytes()
        if (sanitized_record.get("checker_output_sha256")
                != sha256(sanitized_output).hexdigest()):
            raise ValueError(f"sanitized log hash differs at {index}")
        decoded_output = sanitized_output.decode("utf-8", errors="replace")
        if not any(line.strip() == "s VERIFIED"
                   for line in decoded_output.splitlines()):
            raise ValueError(f"sanitized checker log rejects case {index}")
        if any(marker in decoded_output for marker in BAD_SANITIZER_DIAGNOSTICS):
            raise ValueError(f"sanitizer diagnostic exists at case {index}")
        safe_seconds = sanitized_record.get("checker_seconds")
        if not isinstance(safe_seconds, (int, float)) or safe_seconds < 0:
            raise ValueError(f"invalid sanitized checker timing at {index}")
        sanitized_checker_seconds += float(safe_seconds)
        stats = record.get("stats")
        if (not isinstance(stats, dict) or type(stats.get("conflicts")) is not int
                or not 0 <= stats["conflicts"] <= record["conflict_limit"]):
            raise ValueError(f"invalid solver statistics at {index}")
        if (not isinstance(record.get("solver_seconds"), (int, float))
                or not isinstance(record.get("total_seconds"), (int, float))
                or not 0 <= record["solver_seconds"] <= record["total_seconds"]):
            raise ValueError(f"invalid timings at {index}")

        input_digest.update(bytes.fromhex(generated_hash))
        proof_digest.update(bytes.fromhex(proof_hash))
        block_bytes += record["proof_bytes"]
        proof_bytes += record["proof_bytes"]
        type_counts[kind] += 1
        checker_counts[checker_hash] += 1
        clause_minimum = min(clause_minimum, clauses)
        clause_maximum = max(clause_maximum, clauses)
        maximum_conflicts = max(maximum_conflicts, (stats["conflicts"], index))
        solver_seconds += float(record["solver_seconds"])
        total_seconds += float(record["total_seconds"])

        if index + 1 == current["stop"]:
            new_block = {
                "start": current["start"],
                "stop": current["stop"],
                "count": current["count"],
                "ordered_cnf_hashes_sha256": input_digest.hexdigest(),
                "ordered_proof_hashes_sha256": proof_digest.hexdigest(),
                "proof_bytes": block_bytes,
            }
            if new_block["ordered_cnf_hashes_sha256"] != current["ordered_cnf_hashes_sha256"]:
                raise ValueError(f"published input block differs at {current['start']}")
            fresh_blocks.append(new_block)
            block_index += 1
            input_digest, proof_digest = sha256(), sha256()
            block_bytes = 0
        if (index + 1) % 1000 == 0:
            print(json.dumps({"through": index, "audited": index + 1,
                              "seconds": time.monotonic() - begun}), flush=True)

    if block_index != len(published_blocks):
        raise ValueError("not every published input block was checked")
    if [type_counts[kind] for kind in range(20)] != manifest["counts_by_type"]:
        raise ValueError("domain type counts differ from the published manifest")
    published_proofs_match = all(
        fresh["ordered_proof_hashes_sha256"] == old["ordered_proof_hashes_sha256"]
        and fresh["proof_bytes"] == old["proof_bytes"]
        for fresh, old in zip(fresh_blocks, published_blocks)
    )
    final_identities = {
        "domain": file_sha256(args.domain),
        "manifest": file_sha256(args.manifest),
        "known70": file_sha256(args.known70),
        "stock_source": file_sha256(args.checker_source),
        "stock_binary": file_sha256(args.checker_binary),
        "sanitized_source": file_sha256(args.sanitized_checker_source),
        "sanitized_binary": file_sha256(args.sanitized_checker_binary),
    }
    expected_identities = {
        "domain": DOMAIN_SHA256,
        "manifest": MANIFEST_SHA256,
        "known70": known70_hash,
        "stock_source": STOCK_SOURCE_SHA256,
        "stock_binary": checker_hash,
        "sanitized_source": WARNING_SAFE_SOURCE_SHA256,
        "sanitized_binary": sanitized_checker_hash,
    }
    if final_identities != expected_identities:
        raise RuntimeError("an audit input or checker changed during the audit")
    return {
        "status": "INDEPENDENT_COMPLETE_DIAGNOSTIC_SAFE_REPLAY_AUDITED",
        "scope": (
            "All direct CNFs and replay records are independently reconstructed; "
            "DRAT inference validity is supplied by fresh stock DRAT-trim processes "
            "and a complete diagnostic-patched ASan/UBSan recheck."
        ),
        "complete_family": True,
        "verified_records": COUNT,
        "domain_sha256": DOMAIN_SHA256,
        "geometry": {"points": 125, "lines": len(LINES)},
        "lower_bound": {
            "fixture_sha256": known70_hash,
            "selected_points": len(selected),
            "complete_lines_contained": 0,
        },
        "typed_classes": [type_counts[kind] for kind in range(20)],
        "range_count": len(ranges),
        "ranges": [{"start": item["start"], "stop": item["stop"]}
                   for item in ranges],
        "records_revalidated_on_final_resumes": sum(
            item["reused_records"] for item in ranges
        ),
        "sanitized_range_count": len(sanitized_ranges),
        "sanitized_ranges": [
            {"start": item["start"], "stop": item["stop"]}
            for item in sanitized_ranges
        ],
        "sanitized_records_revalidated_on_final_resumes": sum(
            item["reused_records"] for item in sanitized_ranges
        ),
        "stock_checker_source_sha256": STOCK_SOURCE_SHA256,
        "stock_checker_binary_sha256": checker_hash,
        "sanitized_checker_source_sha256": sanitized_checker_source_hash,
        "sanitized_checker_binary_sha256": sanitized_checker_hash,
        "published_manifest_sha256": MANIFEST_SHA256,
        "checker_counts": dict(checker_counts),
        "clause_range": [clause_minimum, clause_maximum],
        "proof_bytes": proof_bytes,
        "maximum_conflicts": maximum_conflicts[0],
        "hardest_index": maximum_conflicts[1],
        "summed_solver_seconds": solver_seconds,
        "summed_solver_checker_seconds": total_seconds,
        "summed_sanitized_checker_seconds": sanitized_checker_seconds,
        "published_input_blocks_matched": True,
        "published_proof_blocks_matched": published_proofs_match,
        "blocks": fresh_blocks,
        "audit_seconds": time.monotonic() - begun,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", type=Path, required=True)
    parser.add_argument("--proofs", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--known70", type=Path, required=True)
    parser.add_argument("--checker-source", type=Path, required=True)
    parser.add_argument("--checker-binary", type=Path, required=True)
    parser.add_argument("--sanitized-recheck", type=Path, required=True)
    parser.add_argument("--sanitized-checker-source", type=Path, required=True)
    parser.add_argument("--sanitized-checker-binary", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.out.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
