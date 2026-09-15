#!/usr/bin/env python3
"""Negative controls for the exact EI21 contact/self-sum verifier."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from verify import verify


HERE = Path(__file__).resolve().parent


def write(path, obj):
    path.write_text(json.dumps(obj, separators=(",", ":"))+"\n")


def main():
    geometry = json.loads((HERE/"geometry_certificate.json").read_text())
    selfsum = json.loads((HERE/"selfsum_certificate.json").read_text())
    cases = []

    bad = copy.deepcopy(geometry); bad["target_contact"] = [0, 13]
    cases.append(("wrong target", bad, selfsum))
    bad = copy.deepcopy(geometry); bad["source_blocked_word"] = bad["surviving_complete_word"]
    cases.append(("nonblocked word", bad, selfsum))
    bad = copy.deepcopy(geometry); bad["midpoint_numerators"][1][1] += 1
    cases.append(("fixed midpoint corruption", bad, selfsum))
    bad = copy.deepcopy(geometry); bad["inverse_numerators"] = [[0]*38 for _ in range(38)]
    cases.append(("singular inverse witness", bad, selfsum))
    bad_sum = copy.deepcopy(selfsum); bad_sum["four_colour_word"] = bad_sum["four_colour_word"][:-1]
    cases.append(("truncated four-word", geometry, bad_sum))
    bad_sum = copy.deepcopy(selfsum); bad_sum["possible_unit_cluster_edge_count"] -= 1
    cases.append(("wrong edge count", geometry, bad_sum))
    bad_sum = copy.deepcopy(selfsum); bad_sum["conservative_graph_sha256"] = "0"*64
    cases.append(("wrong graph hash", geometry, bad_sum))

    rejected = []
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for index, (name, geom, summation) in enumerate(cases):
            gp = root/f"g{index}.json"; sp = root/f"s{index}.json"
            write(gp, geom); write(sp, summation)
            try:
                verify(gp, sp, check_expected=False)
            except (ValueError, KeyError, IndexError, ZeroDivisionError):
                rejected.append(name)
            else:
                raise AssertionError(f"control accepted: {name}")
    print(json.dumps({"status": "ALL NEGATIVE CONTROLS REJECTED",
                      "count": len(rejected), "controls": rejected}, indent=2))


if __name__ == "__main__":
    main()
