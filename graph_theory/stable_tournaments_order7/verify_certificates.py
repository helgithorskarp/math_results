#!/usr/bin/env python3
"""Definition-level verifier for stable-tournament certificates through n=7."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CLASS_RE = re.compile(
    r"^CLASS (?P<mask>\d+) orbit=(?P<orbit>\d+) m=(?P<m>[01])"
    r"(?: x=(?P<x>[0-9,]+) y=(?P<y>[0-9,]+) z=(?P<z>[0-9,]+))?$"
)
SUMMARY_RE = re.compile(
    r"^SUMMARY n=(?P<n>\d+) tournaments=(?P<tournaments>\d+) "
    r"classes=(?P<classes>\d+) transitive_classes=(?P<transitive>\d+) "
    r"stabilized_classes=(?P<stabilized>\d+) distinct_pair_sums=(?P<sums>\d+)$"
)


@dataclass(frozen=True)
class ClassCertificate:
    mask: int
    orbit_size: int
    m: int
    x: tuple[int, ...] | None
    y: tuple[int, ...] | None
    z: tuple[int, ...] | None


def edge_pairs(n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def tournament_matrix(mask: int, n: int) -> list[list[int]]:
    matrix = [[0] * n for _ in range(n)]
    for bit, (i, j) in enumerate(edge_pairs(n)):
        matrix[i][j] = (mask >> bit) & 1
        matrix[j][i] = 1 - matrix[i][j]
    return matrix


def order_matrix(order: tuple[int, ...], n: int) -> list[list[int]]:
    if sorted(order) != list(range(n)):
        raise ValueError(f"not a permutation of 0,...,{n - 1}: {order}")
    rank = [0] * n
    for position, vertex in enumerate(order):
        rank[vertex] = position
    return [[int(i != j and rank[i] > rank[j]) for j in range(n)] for i in range(n)]


def is_transitive(matrix: list[list[int]]) -> bool:
    # A tournament is transitive exactly when its outdegrees are 0,1,...,n-1.
    return sorted(map(sum, matrix)) == list(range(len(matrix)))


def check_equation(certificate: ClassCertificate, n: int) -> None:
    tournament = tournament_matrix(certificate.mask, n)
    transitive = is_transitive(tournament)
    if certificate.m == 0:
        if not transitive or any(v is not None for v in (certificate.x, certificate.y, certificate.z)):
            raise ValueError(f"invalid m=0 class {certificate.mask}")
        return
    if transitive or any(v is None for v in (certificate.x, certificate.y, certificate.z)):
        raise ValueError(f"invalid m=1 class {certificate.mask}")
    x = order_matrix(certificate.x, n)  # type: ignore[arg-type]
    y = order_matrix(certificate.y, n)  # type: ignore[arg-type]
    z = order_matrix(certificate.z, n)  # type: ignore[arg-type]
    for i in range(n):
        for j in range(n):
            if tournament[i][j] + x[i][j] != y[i][j] + z[i][j]:
                raise ValueError(
                    f"bad decomposition in class {certificate.mask} at ({i},{j})"
                )


def relabel_mask(mask: int, relabeling: tuple[int, ...], n: int) -> int:
    # New vertex i is old vertex relabeling[i].  This implementation reads
    # the definition from a full adjacency matrix rather than using the
    # generator's bit-index transformation.
    old = tournament_matrix(mask, n)
    result = 0
    for bit, (i, j) in enumerate(edge_pairs(n)):
        result |= old[relabeling[i]][relabeling[j]] << bit
    return result


def parse_order(text: str | None) -> tuple[int, ...] | None:
    return None if text is None else tuple(map(int, text.split(",")))


def parse_certificate(path: Path) -> tuple[int, list[ClassCertificate], dict[str, int]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines:
        raise ValueError("empty certificate")
    header = re.fullmatch(r"CERTIFICATE stable_tournaments_v1 n=(\d+)", lines[0])
    if header is None:
        raise ValueError("bad certificate header")
    n = int(header.group(1))
    if not (1 <= n <= 7):
        raise ValueError("certificate n outside checked range")
    certificates: list[ClassCertificate] = []
    summary: dict[str, int] | None = None
    for line in lines[1:]:
        class_match = CLASS_RE.fullmatch(line)
        if class_match is not None:
            certificates.append(
                ClassCertificate(
                    mask=int(class_match.group("mask")),
                    orbit_size=int(class_match.group("orbit")),
                    m=int(class_match.group("m")),
                    x=parse_order(class_match.group("x")),
                    y=parse_order(class_match.group("y")),
                    z=parse_order(class_match.group("z")),
                )
            )
            continue
        summary_match = SUMMARY_RE.fullmatch(line)
        if summary_match is not None and summary is None:
            summary = {key: int(value) for key, value in summary_match.groupdict().items()}
            continue
        raise ValueError(f"unrecognized or duplicate line: {line}")
    if summary is None:
        raise ValueError("missing summary")
    return n, certificates, summary


def verify(path: Path) -> None:
    n, certificates, summary = parse_certificate(path)
    pairs = edge_pairs(n)
    tournament_count = 1 << len(pairs)
    if [item.mask for item in certificates] != sorted(item.mask for item in certificates):
        raise ValueError("class representatives are not strictly increasing")
    if len({item.mask for item in certificates}) != len(certificates):
        raise ValueError("duplicate class representative")

    seen = bytearray(tournament_count)
    seen_count = 0
    relabelings = list(itertools.permutations(range(n)))
    for item in certificates:
        if not (0 <= item.mask < tournament_count):
            raise ValueError(f"representative out of range: {item.mask}")
        check_equation(item, n)
        orbit = {relabel_mask(item.mask, p, n) for p in relabelings}
        if len(orbit) != item.orbit_size:
            raise ValueError(f"wrong orbit size for class {item.mask}")
        if item.mask != min(orbit):
            raise ValueError(f"class {item.mask} is not canonically minimal")
        for image in orbit:
            if seen[image]:
                raise ValueError(f"overlapping isomorphism orbits at tournament {image}")
            seen[image] = 1
            seen_count += 1

    transitive_classes = sum(item.m == 0 for item in certificates)
    stabilized_classes = sum(item.m == 1 for item in certificates)
    calculated = {
        "n": n,
        "tournaments": tournament_count,
        "classes": len(certificates),
        "transitive": transitive_classes,
        "stabilized": stabilized_classes,
    }
    for key, value in calculated.items():
        if summary[key] != value:
            raise ValueError(f"summary mismatch for {key}: {summary[key]} != {value}")
    if seen_count != tournament_count or 0 in seen:
        raise ValueError(f"incomplete coverage: {seen_count} of {tournament_count}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(
        f"verified n={n}: {tournament_count} labeled tournaments in "
        f"{len(certificates)} isomorphism classes; "
        f"m=0 classes={transitive_classes}, m=1 classes={stabilized_classes}; "
        f"sha256={digest}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificates", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        for path in args.certificates:
            verify(path)
    except (OSError, ValueError) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
