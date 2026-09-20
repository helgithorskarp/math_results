#!/usr/bin/env python3
"""Exhaustively check the local Hall-witness reduction for sizes 1, 2, 3."""

from __future__ import annotations

import hashlib
import json


def tournament_scores(order: int, bits: int) -> list[int]:
    scores = [0] * order
    shift = 0
    for first in range(order):
        for second in range(first + 1, order):
            winner = first if bits & (1 << shift) else second
            scores[winner] += 1
            shift += 1
    return scores


def check_size(size: int) -> dict[str, int]:
    hall_size = size - 1
    outside_hall_size = 8 - size
    patterns = 0
    locally_feasible = 0
    degree_six_patterns = 0
    rigid_patterns = 0
    record = hashlib.sha256()

    tournament_count = 1 << (size * (size - 1) // 2)
    hall_arc_count = size * hall_size
    for tournament_bits in range(tournament_count):
        internal = tournament_scores(size, tournament_bits)
        for hall_bits in range(1 << hall_arc_count):
            patterns += 1
            hall_out = [0] * size
            hall_indegree = [0] * hall_size
            shift = 0
            for tail in range(size):
                for head in range(hall_size):
                    if hall_bits & (1 << shift):
                        hall_out[tail] += 1
                        hall_indegree[head] += 1
                    shift += 1

            # Inclusion-minimality: every Hall neighbor has at least two
            # preimages in S.
            if any(indegree < 2 for indegree in hall_indegree):
                continue

            local = [internal[v] + hall_out[v] for v in range(size)]
            # A witness vertex has no arc to B\Gamma(S), and at most 7-size
            # arcs to C=A\S.  Global minimum out-degree six therefore forces
            # internal+Hall out-degree at least size-1.
            if any(value < size - 1 for value in local):
                continue
            locally_feasible += 1

            equality = [v for v, value in enumerate(local) if value == size - 1]
            if equality:
                degree_six_patterns += 1
                for vertex in equality:
                    # Equality forces the vertex to dominate all of C, hence
                    # all D=B\Gamma(S) are exact second out-neighbors because
                    # the chosen root is ordinary.  One more second neighbor
                    # is forced either through Gamma(S), or (only for size 3
                    # with q=0) both Hall vertices are reached through S.
                    if size == 1:
                        lower_bound = outside_hall_size
                    elif hall_out[vertex] > 0:
                        lower_bound = outside_hall_size + 1  # plus the root
                    else:
                        assert size == 3
                        assert internal[vertex] == 2
                        assert all(indegree == 2 for indegree in hall_indegree)
                        lower_bound = outside_hall_size + hall_size
                    assert lower_bound >= 6
            else:
                # This alternative occurs only at size three.  Summing the
                # three internal scores gives 3 and Hall out-scores at most 6;
                # local[v]>=3 for all v forces equality everywhere.
                assert size == 3
                assert internal == [1, 1, 1]
                assert hall_out == [2, 2, 2]
                rigid_patterns += 1

            record.update(
                json.dumps(
                    [size, tournament_bits, hall_bits, internal, hall_out, equality],
                    separators=(",", ":"),
                ).encode()
            )

    if size < 3:
        assert degree_six_patterns == locally_feasible and rigid_patterns == 0
    else:
        assert rigid_patterns == 2
    return {
        "degree_six_patterns": degree_six_patterns,
        "locally_feasible": locally_feasible,
        "patterns": patterns,
        "record_sha256": record.hexdigest(),
        "rigid_patterns": rigid_patterns,
    }


def main() -> None:
    report = {f"size_{size}": check_size(size) for size in range(1, 4)}
    report["status"] = "VERIFIED"
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
