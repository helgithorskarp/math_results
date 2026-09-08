#!/usr/bin/env python3
"""Independent catalog, result, and control-formula audit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

N = 43
L = 21
RECORD_BITS = N * (N - 1) // 2
PAIR_VARS = L * (L - 1) // 2


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def audit_package_files(package: Path) -> None:
    checksum_file = package / "SHA256SUMS"
    declared: dict[str, str] = {}
    for line in checksum_file.read_text().splitlines():
        digest, name = line.split("  ", 1)
        require(name not in declared, f"duplicate checksum entry: {name}")
        require("/" not in name and name not in {".gitignore", "SHA256SUMS"}, "bad checksum path")
        declared[name] = digest
    actual = {
        path.name
        for path in package.iterdir()
        if path.is_file() and path.name not in {".gitignore", "SHA256SUMS"}
    }
    require(set(declared) == actual, "SHA256SUMS file set mismatch")
    for name, digest in declared.items():
        require(sha256((package / name).read_bytes()) == digest, f"checksum mismatch: {name}")


def read_catalog(path: Path) -> list[str]:
    raw = path.read_bytes()
    expected = json.loads((Path(__file__).parent / "EXPECTED.json").read_text())
    require(sha256(raw) == expected["catalog_sha256"], "catalog SHA-256 mismatch")
    lines = raw.decode("ascii").splitlines()
    require(len(lines) == expected["catalog_records"], "wrong catalog record count")
    require(len(set(lines)) == len(lines), "duplicate catalog record")
    return lines


def decode(line: str) -> list[list[bool]]:
    require(len(line) == RECORD_BITS and set(line) <= {"0", "1"}, "malformed record")
    tournament = [[False] * N for _ in range(N)]
    offset = 0
    for i in range(N):
        for j in range(i + 1, N):
            tournament[i][j] = line[offset] == "1"
            tournament[j][i] = not tournament[i][j]
            offset += 1
    return tournament


def audit_drt(tournament: list[list[bool]]) -> None:
    for i in range(N):
        require(not tournament[i][i], "tournament loop")
        require(sum(tournament[i]) == 21, "wrong tournament outdegree")
        for j in range(i + 1, N):
            require(tournament[i][j] != tournament[j][i], "pair is not oriented once")
            common = sum(
                tournament[i][k] and tournament[j][k] for k in range(N)
            )
            require(common == 10, "wrong common-outneighbor count")


def pair_variables() -> dict[tuple[int, int], int]:
    return {
        edge: variable
        for variable, edge in enumerate(itertools.combinations(range(L), 2), 1)
    }


def control_cnf(line: str, root: int) -> bytes:
    """A separate Python construction of the C++ local-order CNF."""
    tournament = decode(line)
    outneighbors = [v for v in range(N) if tournament[root][v]]
    require(len(outneighbors) == L, "wrong root outneighborhood size")
    variables = pair_variables()

    def before(a: int, b: int) -> int:
        return variables[a, b] if a < b else -variables[b, a]

    clauses: list[list[int]] = []
    for a, b, c in itertools.combinations(range(L), 3):
        clauses.append([-before(a, b), -before(b, c), before(a, c)])
        clauses.append([before(a, b), before(b, c), -before(a, c)])

    for size in (4, 5):
        for subset in itertools.combinations(range(L), size):
            degrees = [
                sum(
                    tournament[outneighbors[subset[i]]][outneighbors[subset[j]]]
                    for j in range(size)
                    if i != j
                )
                for i in range(size)
            ]
            if sorted(degrees) != list(range(size)):
                continue
            order = sorted(range(size), key=lambda i: -degrees[i])
            vertices = [subset[i] for i in order]
            if size == 4:
                chain = [before(vertices[i], vertices[i + 1]) for i in range(3)]
            else:
                chain = [before(vertices[i + 1], vertices[i]) for i in range(4)]
            clauses.append([-literal for literal in chain])

    selectors = list(range(PAIR_VARS + 1, PAIR_VARS + L + 1))
    clauses.append(selectors)
    for first in range(L):
        for other in range(L):
            if other != first:
                clauses.append([-selectors[first], before(first, other)])

    text = [f"p cnf {PAIR_VARS + L} {len(clauses)}\n"]
    text.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(text).encode("ascii")


def audit_result(path: Path, expected: dict[str, object]) -> None:
    lines = path.read_text().splitlines()
    require(bool(lines), "empty result")
    require(lines[0] == "record\troots\tunsat\tclauses\tproof_bytes", "bad result header")
    records: list[tuple[int, int, int, int, int]] = []
    for line in lines[1:-1]:
        fields = tuple(map(int, line.split("\t")))
        require(len(fields) == 5, "bad result row")
        records.append(fields)
    require(
        [row[0] for row in records] == list(range(expected["catalog_records"])),
        "result does not cover records exactly",
    )
    require(all(row[1] == N and row[2] == N for row in records), "non-UNSAT result row")
    totals = (
        sum(row[1] for row in records),
        sum(row[2] for row in records),
        sum(row[3] for row in records),
        sum(row[4] for row in records),
    )
    total_fields = lines[-1].split("\t")
    require(total_fields[0] == "TOTAL", "missing result total")
    require(tuple(map(int, total_fields[1:])) == totals, "incorrect result total")
    require(totals == tuple(expected["totals"]), "unexpected result total")
    require(sha256(path.read_bytes()) == expected["result_sha256"], "result SHA-256 mismatch")


def audit_direct_screen(path: Path, expected: dict[str, object]) -> None:
    require(sha256(path.read_bytes()) == expected["direct_screen_sha256"], "screen SHA-256 mismatch")
    lines = path.read_text().splitlines()
    require(
        lines[0] == "first\trecords\troot_formulas\tsat\tunsat\tunknown\tstderr_sha256",
        "bad screen header",
    )
    rows = [line.split("\t") for line in lines[1:-1]]
    require(len(rows) == 8, "wrong screen shard count")
    require(sum(int(row[1]) for row in rows) == 2178, "wrong screened record count")
    require(sum(int(row[2]) for row in rows) == 93654, "wrong screened formula count")
    require(
        all(row[3] == "0" and row[4] == row[2] and row[5] == "0" for row in rows),
        "screen contains survivor or unknown",
    )
    require(lines[-1] == "TOTAL\t2178\t93654\t0\t93654\t0\t-", "bad screen total")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--show-control-hashes", action="store_true")
    args = parser.parse_args()
    package = Path(__file__).parent
    audit_package_files(package)
    expected = json.loads((package / "EXPECTED.json").read_text())
    lines = read_catalog(args.catalog)
    for line in lines:
        audit_drt(decode(line))
    control_hashes = {
        key: sha256(control_cnf(lines[int(key.split(":")[0])], int(key.split(":")[1])))
        for key in expected["control_cnf_sha256"]
    }
    if args.show_control_hashes:
        print(json.dumps(control_hashes, indent=2, sort_keys=True))
    require(control_hashes == expected["control_cnf_sha256"], "control CNF mismatch")
    audit_direct_screen(package / "DIRECT_SCREEN.tsv", expected)
    if args.result is not None:
        audit_result(args.result, expected)
    print("AUDITED_DRT43_CATALOG_LOCAL_EXCLUSION")


if __name__ == "__main__":
    main()
