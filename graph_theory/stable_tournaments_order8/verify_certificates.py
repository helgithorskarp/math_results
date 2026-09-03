#!/usr/bin/env python3
"""Definition-level verifier for the order-eight stable-tournament certificates."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

N = 8
PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]
M0_RE = re.compile(r"^CLASS (?P<index>\d+) tournament=(?P<tournament>\d+) m=0$")
M1_RE = re.compile(
    r"^CLASS (?P<index>\d+) tournament=(?P<tournament>\d+) m=1 "
    r"relabel=(?P<relabel>[0-7,]+) y=(?P<y>[0-7,]+) z=(?P<z>[0-7,]+)$"
)
FAIL_RE = re.compile(r"^FAIL (?P<index>\d+) tournament=(?P<tournament>\d+)$")
M2_RE = re.compile(
    r"^CLASS (?P<index>\d+) tournament=(?P<tournament>\d+) "
    r"x1=(?P<x1>[0-7,]+) x2=(?P<x2>[0-7,]+) "
    r"y1=(?P<y1>[0-7,]+) y2=(?P<y2>[0-7,]+) y3=(?P<y3>[0-7,]+)$"
)
SUMMARY01_RE = re.compile(
    r"^SUMMARY classes=6880 m0=1 m1=6783 m2_candidates=96 relabelings_tested=(?P<tested>\d+)$"
)
SUMMARY2_RE = re.compile(r"^SUMMARY classes=96 m2_witnesses=96$")


@dataclass(frozen=True)
class M01Record:
    index: int
    tournament: int
    status: int
    relabel: tuple[int, ...] | None = None
    y: tuple[int, ...] | None = None
    z: tuple[int, ...] | None = None


def parse_order(text: str) -> tuple[int, ...]:
    order = tuple(map(int, text.split(",")))
    if sorted(order) != list(range(N)):
        raise ValueError(f"not an order on [8]: {text}")
    return order


def parse_representatives(path: Path) -> list[int]:
    representatives: list[int] = []
    for line in path.read_text(encoding="ascii").splitlines():
        if len(line) != len(PAIRS) or set(line) - {"0", "1"}:
            raise ValueError("bad representative line")
        representatives.append(sum((character == "1") << bit for bit, character in enumerate(line)))
    if len(representatives) != 6880:
        raise ValueError(f"expected 6880 representatives, got {len(representatives)}")
    if len(set(representatives)) != len(representatives):
        raise ValueError("duplicate representative mask")
    return representatives


def parse_m01(path: Path) -> list[M01Record]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != "CERTIFICATE stable_tournaments_n8_v1 classes=6880":
        raise ValueError("bad m01 header")
    records: list[M01Record] = []
    saw_summary = False
    for line in lines[1:]:
        match = M0_RE.fullmatch(line)
        if match:
            records.append(M01Record(int(match["index"]), int(match["tournament"]), 0))
            continue
        match = M1_RE.fullmatch(line)
        if match:
            records.append(
                M01Record(
                    int(match["index"]),
                    int(match["tournament"]),
                    1,
                    parse_order(match["relabel"]),
                    parse_order(match["y"]),
                    parse_order(match["z"]),
                )
            )
            continue
        match = FAIL_RE.fullmatch(line)
        if match:
            records.append(M01Record(int(match["index"]), int(match["tournament"]), 2))
            continue
        if SUMMARY01_RE.fullmatch(line) and not saw_summary:
            saw_summary = True
            continue
        raise ValueError(f"bad or duplicate m01 line: {line}")
    if not saw_summary:
        raise ValueError("missing m01 summary")
    return records


def parse_m2(path: Path) -> dict[int, tuple[int, list[tuple[int, ...]]]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != "CERTIFICATE stable_tournaments_n8_m2_v1 classes=96":
        raise ValueError("bad m2 header")
    records: dict[int, tuple[int, list[tuple[int, ...]]]] = {}
    saw_summary = False
    for line in lines[1:]:
        match = M2_RE.fullmatch(line)
        if match:
            index = int(match["index"])
            if index in records:
                raise ValueError(f"duplicate m2 index {index}")
            records[index] = (
                int(match["tournament"]),
                [parse_order(match[name]) for name in ("x1", "x2", "y1", "y2", "y3")],
            )
            continue
        if SUMMARY2_RE.fullmatch(line) and not saw_summary:
            saw_summary = True
            continue
        raise ValueError(f"bad or duplicate m2 line: {line}")
    if not saw_summary or len(records) != 96:
        raise ValueError("incomplete m2 certificate")
    return records


def tournament_matrix(mask: int) -> list[list[int]]:
    matrix = [[0] * N for _ in range(N)]
    for bit, (i, j) in enumerate(PAIRS):
        matrix[i][j] = (mask >> bit) & 1
        matrix[j][i] = 1 - matrix[i][j]
    return matrix


def order_matrix(order: tuple[int, ...]) -> list[list[int]]:
    rank = [0] * N
    for position, vertex in enumerate(order):
        rank[vertex] = position
    return [[int(i != j and rank[i] > rank[j]) for j in range(N)] for i in range(N)]


def relabel_matrix(matrix: list[list[int]], relabeling: tuple[int, ...]) -> list[list[int]]:
    return [[matrix[relabeling[i]][relabeling[j]] for j in range(N)] for i in range(N)]


def is_transitive(matrix: list[list[int]]) -> bool:
    return sorted(map(sum, matrix)) == list(range(N))


def check_m1(record: M01Record) -> None:
    if record.relabel is None or record.y is None or record.z is None:
        raise ValueError(f"missing m1 data in class {record.index}")
    tournament = relabel_matrix(tournament_matrix(record.tournament), record.relabel)
    identity = order_matrix(tuple(range(N)))
    y = order_matrix(record.y)
    z = order_matrix(record.z)
    for i in range(N):
        for j in range(N):
            if tournament[i][j] + identity[i][j] != y[i][j] + z[i][j]:
                raise ValueError(f"bad m1 equation in class {record.index} at ({i},{j})")


def check_m2(index: int, tournament: int, orders: list[tuple[int, ...]]) -> None:
    matrices = [order_matrix(order) for order in orders]
    t = tournament_matrix(tournament)
    for i in range(N):
        for j in range(N):
            lhs = t[i][j] + matrices[0][i][j] + matrices[1][i][j]
            rhs = matrices[2][i][j] + matrices[3][i][j] + matrices[4][i][j]
            if lhs != rhs:
                raise ValueError(f"bad m2 equation in class {index} at ({i},{j})")


def verify(representative_path: Path, m01_path: Path, m2_path: Path) -> None:
    representatives = parse_representatives(representative_path)
    m01 = parse_m01(m01_path)
    m2 = parse_m2(m2_path)
    if len(m01) != 6880 or [record.index for record in m01] != list(range(6880)):
        raise ValueError("m01 class indices are not exactly 0,...,6879")
    counts = [0, 0, 0]
    for record in m01:
        if record.tournament != representatives[record.index]:
            raise ValueError(f"representative mismatch in class {record.index}")
        transitive = is_transitive(tournament_matrix(record.tournament))
        if record.status == 0:
            if not transitive:
                raise ValueError("m0 record is not transitive")
        elif record.status == 1:
            if transitive:
                raise ValueError("m1 record is transitive")
            check_m1(record)
        else:
            if transitive or record.index not in m2:
                raise ValueError(f"invalid m2 candidate class {record.index}")
            m2_tournament, orders = m2[record.index]
            if m2_tournament != record.tournament:
                raise ValueError(f"m2 tournament mismatch in class {record.index}")
            check_m2(record.index, record.tournament, orders)
        counts[record.status] += 1
    if counts != [1, 6783, 96] or set(m2) != {record.index for record in m01 if record.status == 2}:
        raise ValueError(f"wrong class partition: {counts}")
    print(
        "verified n=8: 6880 isomorphism representatives; "
        "m=0 classes=1, m=1 classes=6783, m=2 classes=96"
    )
    for path in (representative_path, m01_path, m2_path):
        print(f"sha256 {hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("representatives", type=Path)
    parser.add_argument("m01_certificate", type=Path)
    parser.add_argument("m2_certificate", type=Path)
    args = parser.parse_args()
    try:
        verify(args.representatives, args.m01_certificate, args.m2_certificate)
    except (OSError, ValueError) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
