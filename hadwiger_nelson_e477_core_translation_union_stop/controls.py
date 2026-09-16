#!/usr/bin/env python3
"""Independent norm and corruption controls for the translation union."""

from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path

import verify


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_overlapping_forcing_seed"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def direct_unit(left, right):
    a, b, c, d = (x - y for x, y in zip(left, right))
    return 3 * a * a + 11 * b * b + c * c + 33 * d * d == 1296 and a * b + c * d == 0


def rejected(certificate):
    try:
        verify.verify(certificate)
    except (ValueError, KeyError, TypeError):
        return True
    return False


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    baseline = verify.verify(certificate)
    equal = json.loads((SOURCE / "certificate.json").read_text())["equal"]
    mandatory = json.loads((SOURCE / "mandatory_vertices.json").read_text())
    core_labels = sorted({0, 1, *[entry["deleted"] for entry in mandatory]})
    core = [tuple(equal["points"][label]) for label in core_labels]
    delta = tuple(certificate["selected_translation"])
    rows = sorted(set(core) | {verify.row_add(row, delta) for row in core})
    generic_direct_agreements = 0
    for left, right in combinations(rows, 2):
        require(verify.unit(verify.point(list(left)), verify.point(list(right))) == direct_unit(left, right), "unit formula disagreement")
        generic_direct_agreements += 1

    corruptions = []
    wrong = deepcopy(certificate)
    wrong["selected_translation"][0] += 1
    corruptions.append(wrong)
    wrong = deepcopy(certificate)
    wrong["translation_overlap_maximum"] -= 1
    corruptions.append(wrong)
    wrong = deepcopy(certificate)
    wrong["four_colouring"] = "0" + wrong["four_colouring"][1:]
    corruptions.append(wrong)
    wrong = deepcopy(certificate)
    wrong["point_sha256"] = "0" * 64
    corruptions.append(wrong)
    wrong = deepcopy(certificate)
    wrong["moser_source_labels"][0] = 0
    corruptions.append(wrong)
    require(all(rejected(corruption) for corruption in corruptions), "accepted corruption")
    result = {
        "status": "CONTROLS_PASS",
        "baseline_status": baseline["status"],
        "generic_direct_unit_agreements": generic_direct_agreements,
        "rejected_corruptions": len(corruptions),
    }
    expected = json.loads((HERE / "CONTROLS_EXPECTED.json").read_text())
    require(result == expected, "expected controls")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
