#!/usr/bin/env python3
"""Definition-level verifier for the three safe BHR a=2 mantles."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

SUPPORT = (1, 2, 11)
MODES = (2, 11)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ValueError(str(message))


def cyclic_length(u: int, v: int, n: int) -> int:
    difference = abs(u - v)
    return min(difference, n - difference)


def embedded(vertex: int, mode: int, cut: int) -> int:
    return vertex if vertex <= cut else vertex + mode


def changed_edges(path: list[int], mode: int, cut: int) -> list[tuple[int, int]]:
    n = len(path)
    return [
        (u, v)
        for u, v in zip(path, path[1:])
        if cyclic_length(embedded(u, mode, cut), embedded(v, mode, cut), n + mode)
        > cyclic_length(u, v, n)
    ]


def verify_realization(path: list[int], counts: tuple[int, int, int]) -> None:
    n = sum(counts) + 1
    require(sorted(path) == list(range(n)), ("permutation", counts))
    actual = Counter(cyclic_length(u, v, n) for u, v in zip(path, path[1:]))
    require(actual == Counter(dict(zip(SUPPORT, counts))), ("lengths", counts, actual))


def verify_growth(path: list[int], mode: int, cut: int) -> None:
    n = len(path)
    require(mode - 1 <= cut <= n - 1 - mode, ("cut range", n, mode, cut))
    critical = set(range(cut - mode + 1, cut + 1))
    incidence: Counter[int] = Counter()
    for u, v in changed_edges(path, mode, cut):
        require(u in critical or v in critical, ("outside edge", mode, cut, u, v))
        if u in critical:
            incidence[u] += 1
        if v in critical:
            incidence[v] += 1
    require(all(incidence[x] == 1 for x in critical), ("incidence", mode, cut, incidence))


def grow_once(path: list[int], mode: int, cut: int) -> list[int]:
    verify_growth(path, mode, cut)
    n = len(path)
    critical = set(range(cut - mode + 1, cut + 1))
    output = [embedded(path[0], mode, cut)]
    for u, v in zip(path, path[1:]):
        old = cyclic_length(u, v, n)
        uu, vv = embedded(u, mode, cut), embedded(v, mode, cut)
        if cyclic_length(uu, vv, n + mode) > old:
            inside = [x for x in (u, v) if x in critical]
            require(len(inside) == 1, ("ambiguous split", mode, cut, u, v))
            output.append(inside[0] + mode)
        output.append(vv)
    return output


def transport(old_cut: int, inserted_cut: int, mode: int) -> int:
    return old_cut if old_cut <= inserted_cut else old_cut + mode


def derive(
    seed_path: list[int], seed_cuts: dict[int, int], q: int, r: int
) -> tuple[list[int], dict[int, int]]:
    path = list(seed_path)
    cuts = dict(seed_cuts)
    for mode, repetitions in ((2, q), (11, r)):
        for _ in range(repetitions):
            cut = cuts[mode]
            path = grow_once(path, mode, cut)
            cuts = {
                other: transport(value, cut, mode)
                for other, value in cuts.items()
            }
    return path, cuts


def verify_certificate(path: Path, grid: int) -> dict[str, object]:
    raw = path.read_bytes()
    data = json.loads(raw)
    require(data["schema"] == "bhr-1-2-11-a2-completion-v1", "schema")
    require(tuple(data["support"]) == SUPPORT, "support")
    require(len(data["seeds"]) == 3, "seed count")
    require(
        [tuple(seed["counts"]) for seed in data["seeds"]]
        == [(2, 8, 28), (2, 8, 29), (2, 8, 30)],
        "seed corners",
    )
    records = []
    for seed in data["seeds"]:
        counts = tuple(seed["counts"])
        seed_path = seed["path"]
        cuts = {int(mode): cut for mode, cut in seed["growth"].items()}
        require(counts[0] == 2 and set(cuts) == set(MODES), counts)
        verify_realization(seed_path, counts)
        for mode in MODES:
            verify_growth(seed_path, mode, cuts[mode])
        intervals = {
            mode: set(range(cuts[mode] - mode + 1, cuts[mode] + 1))
            for mode in MODES
        }
        require(intervals[2].isdisjoint(intervals[11]), ("overlap", counts, cuts))
        require(2 * 11 + 2 + 11 <= len(seed_path), ("safe margin", counts))

        family = {}
        for q in range(grid + 2):
            for r in range(grid + 2):
                state_path, state_cuts = derive(seed_path, cuts, q, r)
                target = (2, counts[1] + 2 * q, counts[2] + 11 * r)
                verify_realization(state_path, target)
                for mode in MODES:
                    verify_growth(state_path, mode, state_cuts[mode])
                family[q, r] = (state_path, state_cuts)
        for q in range(grid + 1):
            for r in range(grid + 1):
                state_path, state_cuts = family[q, r]
                for mode, target_index in ((2, (q + 1, r)), (11, (q, r + 1))):
                    grown = grow_once(state_path, mode, state_cuts[mode])
                    require(
                        grown == family[target_index][0],
                        ("noncommuting", counts, q, r, mode),
                    )
                records.append([list(counts), q, r, state_path])
    digest = hashlib.sha256(
        json.dumps(records, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "seeds": len(data["seeds"]),
        "family_paths_checked": len(data["seeds"]) * (grid + 2) ** 2,
        "commuting_squares_checked": len(data["seeds"]) * (grid + 1) ** 2,
        "record_sha256": digest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=5)
    args = parser.parse_args()
    require(args.grid >= 1, "grid")
    for key, value in verify_certificate(args.certificate, args.grid).items():
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
