#!/usr/bin/env python3
"""Run or audit the native radius-seven catalog census deterministically.

With ``--native``, this driver runs every selected eligible orientation and
prints a progress-free transcript in catalog order.  With one or more
``--input-log`` arguments, it instead consolidates existing native logs.  In
both modes it reruns the Python reference self-tests, pins the catalog hash,
requires every eligible orientation exactly once, checks every native PASS
record against Python-derived metadata, and reconciles positive-event counts.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import search_known_r42_radius7_extension as reference
from verify_known_r42_bridge import (
    CATALOG_PATH,
    CATALOG_SHA256,
    decode_short_graph6,
)


def fields(line: str) -> dict[str, str]:
    answer = {}
    for token in line.split()[1:]:
        if "=" in token:
            key, value = token.split("=", 1)
            answer[key] = value
    return answer


def event_key(line: str) -> tuple[int, str]:
    parsed = fields(line)
    return int(parsed["parent"]), parsed["orientation"]


def parse_output(text: str, source: str):
    records = {}
    events = defaultdict(list)
    shard_markers = 0
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("PROGRESS "):
            continue
        if line.startswith("RAMSEY42 ") or line.startswith("CERTIFIED "):
            try:
                events[event_key(line)].append(line)
            except (KeyError, ValueError) as error:
                raise AssertionError(
                    f"malformed positive event {source}:{line_number}: {line}"
                ) from error
            continue
        if line.startswith("SHARD_PASS ") or line.startswith("TAIL_PASS "):
            shard_markers += 1
            continue
        if not line.startswith("PASS parent="):
            raise AssertionError(
                f"unexpected line {source}:{line_number}: {line}"
            )
        parsed = fields(line)
        try:
            key = int(parsed["parent"]), parsed["orientation"]
            record = {
                "line": line,
                "parent": key[0],
                "orientation": key[1],
                "edges": int(parsed["edges"]),
                "lower_bound": int(parsed["degree_lower_bound"]),
                "candidates": int(parsed["candidates"]),
                "ramsey42": int(parsed["Ramsey42"]),
                "extensions": int(parsed["extensions"]),
            }
        except (KeyError, ValueError) as error:
            raise AssertionError(
                f"malformed PASS record {source}:{line_number}: {line}"
            ) from error
        if key in records:
            raise AssertionError(f"duplicate PASS record for {key} in {source}")
        records[key] = record
    return records, events, shard_markers


def run_one(native: Path, catalog: Path, row):
    index, orientation, _, _, _ = row
    completed = subprocess.run(
        (str(native), str(catalog), str(index), orientation),
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(
            f"native search failed for {(index, orientation)} with status "
            f"{completed.returncode}: {completed.stderr.strip()}"
        )
    if completed.stderr.strip():
        raise RuntimeError(
            f"native search wrote stderr for {(index, orientation)}: "
            f"{completed.stderr.strip()}"
        )
    records, events, markers = parse_output(
        completed.stdout, f"native:{index}:{orientation}"
    )
    if markers:
        raise AssertionError("single native run emitted a shard marker")
    return records, events


def merge_outputs(outputs):
    records = {}
    events = defaultdict(list)
    markers = 0
    for new_records, new_events, new_markers in outputs:
        for key, record in new_records.items():
            if key in records:
                raise AssertionError(f"duplicate PASS record across inputs: {key}")
            records[key] = record
        for key, lines in new_events.items():
            events[key].extend(lines)
        markers += new_markers
    return records, events, markers


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--native", type=Path, help="compiled native executable")
    mode.add_argument(
        "--input-log", type=Path, action="append", help="native log to audit"
    )
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--only-parent", type=int, action="append")
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error("--workers must lie in 1,...,16")
    if args.input_log and args.workers != 1:
        parser.error("--workers applies only with --native")

    reference.run_self_tests()
    raw_catalog = args.catalog.read_bytes()
    if hashlib.sha256(raw_catalog).hexdigest() != CATALOG_SHA256:
        raise AssertionError("known R(5,5;42) catalog digest changed")
    catalog = [
        decode_short_graph6(line)
        for line in raw_catalog.decode("ascii").splitlines()
    ]
    if len(catalog) != 328:
        raise AssertionError("wrong catalog record count")
    # The changed-edge clique criterion assumes the parent is Ramsey.
    for index, matrix in enumerate(catalog):
        adjacency = reference.bit_adjacency(matrix)
        if reference.contains_clique(adjacency) or reference.contains_clique(
            reference.complement_bits(adjacency)
        ):
            raise AssertionError(f"catalog parent {index} is not Ramsey")
    selected = None if args.only_parent is None else set(args.only_parent)
    eligible = reference.eligible_orientations(catalog, selected, None)
    if not eligible:
        raise AssertionError("selection contains no radius-seven orientation")
    expected = {
        (index, orientation): (edges, lower_bound)
        for index, orientation, edges, lower_bound, _ in eligible
    }

    if args.native:
        native = args.native.resolve()
        if not native.is_file():
            raise AssertionError(f"native executable does not exist: {native}")
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=args.workers
        ) as executor:
            futures = [
                executor.submit(run_one, native, args.catalog.resolve(), row)
                for row in eligible
            ]
            raw_outputs = []
            for future in futures:
                records, events = future.result()
                raw_outputs.append((records, events, 0))
        records, events, _shard_markers = merge_outputs(raw_outputs)
    else:
        raw_outputs = []
        for path in args.input_log:
            raw_outputs.append(parse_output(path.read_text(), str(path)))
        records, events, _shard_markers = merge_outputs(raw_outputs)

    missing = expected.keys() - records.keys()
    extra = records.keys() - expected.keys()
    if missing or extra:
        raise AssertionError(
            f"coverage mismatch missing={sorted(missing)} extra={sorted(extra)}"
        )
    if events.keys() - expected.keys():
        raise AssertionError(
            f"positive event outside eligible set: {sorted(events.keys()-expected.keys())}"
        )

    lower_counts = Counter()
    edge_counts = Counter()
    total_candidates = total_ramsey = total_extensions = 0
    event_ramsey = event_extensions = 0
    orientation_counts = Counter()
    for index, orientation, edges, lower_bound, _ in eligible:
        key = index, orientation
        record = records[key]
        if (record["edges"], record["lower_bound"]) != expected[key]:
            raise AssertionError(f"metadata mismatch for {key}: {record}")
        key_events = events[key]
        observed_ramsey = sum(line.startswith("RAMSEY42 ") for line in key_events)
        observed_extensions = sum(
            line.startswith("CERTIFIED ") for line in key_events
        )
        if (observed_ramsey, observed_extensions) != (
            record["ramsey42"], record["extensions"]
        ):
            raise AssertionError(f"positive-event mismatch for {key}")
        for line in key_events:
            print(line)
        print(record["line"])
        total_candidates += record["candidates"]
        total_ramsey += record["ramsey42"]
        total_extensions += record["extensions"]
        event_ramsey += observed_ramsey
        event_extensions += observed_extensions
        lower_counts[lower_bound] += record["candidates"]
        edge_counts[edges] += record["candidates"]
        orientation_counts[orientation] += 1

    if (event_ramsey, event_extensions) != (total_ramsey, total_extensions):
        raise AssertionError("global positive-event mismatch")
    for lower_bound in sorted(lower_counts):
        orientation_count = sum(
            row[3] == lower_bound for row in eligible
        )
        print(
            f"SUMMARY degree_lower_bound={lower_bound} "
            f"orientations={orientation_count} "
            f"candidates={lower_counts[lower_bound]}"
        )
    for edges in sorted(edge_counts):
        orientation_count = sum(row[2] == edges for row in eligible)
        print(
            f"SUMMARY edges={edges} orientations={orientation_count} "
            f"candidates={edge_counts[edges]}"
        )
    print(
        f"PASS radius-seven orientations={len(eligible)} "
        f"base={orientation_counts['base']} "
        f"complement={orientation_counts['complement']} "
        f"degree-compatible-candidates={total_candidates} "
        f"Ramsey42={total_ramsey} extensions={total_extensions}"
    )


if __name__ == "__main__":
    main()
