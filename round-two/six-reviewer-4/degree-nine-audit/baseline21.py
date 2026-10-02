"""Known primary construction; baseline only, not a new22-point witness."""
import hashlib
import json
from pathlib import Path

data = Path(__file__).with_name("primary21.txt").read_bytes()
expected = "3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55"
if hashlib.sha256(data).hexdigest() != expected:
    raise RuntimeError("primary fixture hash")
g, _ = json.JSONDecoder().raw_decode(data.decode())
if len(g) != 21 or any(len(row) != 21 for row in g):
    raise RuntimeError("primary fixture dimensions")
if any(g[i][i] != 0 for i in range(21)) or any(g[i][j] not in (0, 1) or g[i][j] != g[j][i]
                                               for i in range(21) for j in range(21)):
    raise RuntimeError("primary fixture simple graph")
# The primary file's zero off-diagonal entries encode the B4-avoiding color;
# its ones encode the B7-avoiding color. Normalize to our red=True convention.
g = [[int(i != j and not g[i][j]) for j in range(21)] for i in range(21)]
values = {"red_edges": 0, "blue_edges": 0, "red_page_max": 0, "blue_page_max": 0}
for i in range(21):
    for j in range(i + 1, 21):
        color = g[i][j]
        count = sum(g[i][k] == color and g[j][k] == color for k in range(21) if k not in (i, j))
        name = "red" if color else "blue"
        values[name + "_edges"] += 1
        values[name + "_page_max"] = max(values[name + "_page_max"], count)
if values != {"red_edges": 93, "blue_edges": 117, "red_page_max": 3, "blue_page_max": 6}:
    raise RuntimeError("primary fixture book counts")
print(json.dumps({**values, "points": 21, "raw_sha256": expected}, sort_keys=True))
