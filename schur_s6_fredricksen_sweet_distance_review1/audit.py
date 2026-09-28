"""Independent set-based audit of the published S(6) distance certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parent.parent / "schur_s6_fredricksen_sweet_distance"


def audit(source: Path = SOURCE) -> None:
    baseline_bytes = (source / "baseline.txt").read_bytes()
    certificate_bytes = (source / "certificate.json").read_bytes()
    digits = baseline_bytes.decode("ascii").strip()
    assert len(digits) == 536 and set(digits) == set("123456")
    classes = {c: {i for i, digit in enumerate(digits, 1) if digit == str(c)}
               for c in range(1, 7)}
    assert sum(map(len, classes.values())) == 536
    for c, elements in classes.items():
        # This checks the x=y boundary as well as distinct summands.
        assert not elements.intersection({a + b for a in elements for b in elements}), c

    data = json.loads(certificate_bytes)
    assert data["target"] == 537 and data["claimed_min_distance"] == 51
    selected_by_color = data["selected_by_color"]
    assert set(selected_by_color) == {str(c) for c in range(1, 7)}
    pair_counts = []
    selected_counts = []
    witness_total = 0
    bounds = []
    for c in range(1, 7):
        target_pairs = {(a, 537 - a) for a in range(1, 269)
                        if a in classes[c] and 537 - a in classes[c]}
        assert all(a < b for a, b in target_pairs)
        pair_counts.append(len(target_pairs))
        entries = selected_by_color[str(c)]
        chosen = set()
        used_support = set()
        for entry in entries:
            pair = tuple(entry["pair"])
            assert pair in target_pairs and pair not in chosen
            chosen.add(pair)
            witness_map = {}
            support = set()
            for w in entry["witnesses"]:
                v, d = w["endpoint"], w["new_color"]
                t = tuple(w["triple"])
                assert v in pair and d in classes and d != c
                assert (v, d) not in witness_map
                assert len(t) == 3 and 1 <= t[0] <= t[1] and t[0] + t[1] == t[2] <= 536
                assert v in t
                other = set(t) - {v}
                assert other and other <= classes[d]
                witness_map[v, d] = t
                support |= other
                witness_total += 1
            assert set(witness_map) == {(v, d) for v in pair
                                        for d in range(1, 7) if d != c}
            assert not support & used_support
            assert not support & classes[c]
            used_support |= support
        selected_counts.append(len(chosen))
        bounds.append(len(target_pairs) + len(chosen))
    assert pair_counts == [64, 43, 55, 38, 32, 35]
    assert selected_counts == [0, 8, 0, 13, 19, 16]
    assert witness_total == 560
    assert bounds == [64, 51, 55, 51, 51, 51]
    assert min(bounds) == 51
    print("PASS independent_audit", "pair_counts=" + ",".join(map(str, pair_counts)),
          "selected_counts=" + ",".join(map(str, selected_counts)),
          "bounds=" + ",".join(map(str, bounds)), "witnesses=" + str(witness_total))
    print("baseline_sha256=" + hashlib.sha256(baseline_bytes).hexdigest())
    print("certificate_sha256=" + hashlib.sha256(certificate_bytes).hexdigest())


if __name__ == "__main__":
    audit()
