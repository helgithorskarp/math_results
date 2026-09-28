"""Definition-level verifier for a local-repair obstruction at S(6)."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 536
COLORS = range(1, 7)


def require(test: bool, message: str) -> None:
    if not test:
        raise ValueError(message)


def main() -> None:
    encoded = (HERE / "baseline.txt").read_text(encoding="ascii").strip()
    require(len(encoded) == N, "baseline must have 536 entries")
    require(set(encoded) == set("123456"), "baseline must use exactly six colors")
    color = [0] + [int(digit) for digit in encoded]

    # This loop checks the definition directly, including x = y.
    triples = 0
    for x in range(1, N + 1):
        for y in range(x, N - x + 1):
            z = x + y
            require(color[x] != color[y] or color[x] != color[z],
                    f"baseline has monochromatic triple {(x, y, z)}")
            triples += 1

    pairs: dict[int, set[tuple[int, int]]] = {c: set() for c in COLORS}
    for x in range(1, 269):
        y = 537 - x
        if color[x] == color[y]:
            pairs[color[x]].add((x, y))

    certificate = json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))
    require(certificate["target"] == 537, "wrong target")
    selected_by_color = certificate["selected_by_color"]
    require(set(selected_by_color) == {str(c) for c in COLORS}, "missing color case")
    bounds = {}
    witness_count = 0

    for c in COLORS:
        selected = selected_by_color[str(c)]
        require(isinstance(selected, list), f"color {c} certificate is not a list")
        seen_pairs: set[tuple[int, int]] = set()
        used_support: set[int] = set()
        for entry in selected:
            pair = tuple(entry["pair"])
            require(pair in pairs[c] and pair not in seen_pairs,
                    f"invalid or duplicate target pair for color {c}: {pair}")
            seen_pairs.add(pair)
            witnesses = entry["witnesses"]
            require(len(witnesses) == 10, f"incomplete witnesses for pair {pair}")
            covered = set()
            support: set[int] = set()
            for witness in witnesses:
                v = witness["endpoint"]
                d = witness["new_color"]
                triple = witness["triple"]
                require(v in pair and d in COLORS and d != c,
                        f"wrong endpoint or new color for pair {pair}")
                require((v, d) not in covered, f"duplicate witness for {(v, d)}")
                covered.add((v, d))
                require(len(triple) == 3, "a witness must have three entries")
                x, y, z = triple
                require(1 <= x <= y and z == x + y and z <= N and v in triple,
                        f"invalid Schur triple {triple}")
                other = set(triple) - {v}
                require(other and all(color[u] == d for u in other),
                        f"witness support is not baseline color {d}: {triple}")
                support.update(other)
                witness_count += 1
            require(covered == {(v, d) for v in pair for d in COLORS if d != c},
                    f"missing endpoint/color witness for pair {pair}")
            require(not (support & used_support),
                    f"support overlap between selected pairs of color {c}")
            used_support.update(support)
        bounds[c] = len(pairs[c]) + len(selected)

    require(min(bounds.values()) >= certificate["claimed_min_distance"],
            "claimed distance exceeds certificate bound")
    print(f"PASS triples={triples} pair_counts=" +
          ",".join(str(len(pairs[c])) for c in COLORS) +
          " selected_counts=" + ",".join(str(len(selected_by_color[str(c)])) for c in COLORS) +
          f" witnesses={witness_count} distance_at_least={min(bounds.values())}")


if __name__ == "__main__":
    main()
