#!/usr/bin/env python3
"""Small arithmetic and malformed-certificate controls."""
import copy
import json

import verify as v


def rejected(fn, label):
    try:
        fn()
    except ValueError:
        return
    raise ValueError(f"control accepted: {label}")


cert = json.loads((v.HERE / "certificate.json").read_text())
result = v.run(cert)
v.need(result["status"] == "VERIFIED_FOUR_COLOUR_STOP", "baseline")
v.need(v.kmul((v.F(0), v.F(1)), (v.F(0), v.F(1))) == (v.F(33), v.F(0)),
       "K radical square")
v.need(v.lmul((v.KZERO, (v.F(1), v.F(0))),
              (v.KZERO, (v.F(1), v.F(0)))) == (v.T, v.KZERO),
       "L radical square")
base = v.base_coordinates(v.source_core())
co, sy = v.rotation(base)
p = (v.lift(base[45][0]), v.lift(base[45][1]))
q0 = v.rotate(base[65], co, sy)
v.need(v.unit(p, q0), "defining contact")
bad = copy.deepcopy(cert)
bad["schema"] = "wrong"
rejected(lambda: v.run(bad), "schema")
badword = list(cert["proper4"])
a, b = cert["cross_edges"][0]
badword[b] = badword[a]
rejected(lambda: v.proper("".join(badword), 481, [(a, b)]), "cross-edge colouring")
rejected(lambda: v.proper(cert["proper4"][:-1], 481, []), "word length")
print(json.dumps({"status": "CONTROLS_PASS", "baseline_points": 481,
                  "arithmetic_controls": 3, "malformed_controls": 3},
                 indent=2, sort_keys=True))
