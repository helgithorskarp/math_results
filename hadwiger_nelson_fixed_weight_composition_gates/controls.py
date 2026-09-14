#!/usr/bin/env python3
"""Small corruption controls for the positive-colouring checker."""

import json
from pathlib import Path
import verify


ROOT = Path(__file__).resolve().parent
certificate = json.loads((ROOT / "certificate.json").read_text())
built = {
    "regular12_weight5": verify.regular12(),
    "regular18_weight4": verify.regular18(),
    "mixed_weight5": verify.mixed_weight5(),
}
rejected = 0

for name in sorted(certificate):
    points, addresses, edges, adjacency = built[name]
    try:
        verify.check_word(name, "0" * len(points), certificate[name]["colours"], points, edges, adjacency)
    except ValueError:
        rejected += 1
    else:
        raise AssertionError("monochromatic word accepted: " + name)

points, addresses, edges, adjacency = built["mixed_weight5"]
try:
    verify.check_word("mixed_weight5", certificate["mixed_weight5"]["word"][:-1], 4, points, edges, adjacency)
except ValueError:
    rejected += 1
else:
    raise AssertionError("truncated word accepted")

result = {"rejected_corruptions": rejected, "status": "PASS"}
if result != json.loads((ROOT / "CONTROLS_EXPECTED.json").read_text()):
    raise AssertionError("control result mismatch")
print(json.dumps(result, sort_keys=True))
