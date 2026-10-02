"""Produce two exact shape fixtures with identical gcd signatures."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import time

from model import divisors, parent_cut, signature


def build():
    labels = divisors(315)
    fixtures = []
    for name, fibers in (
        ("shape-obstruction", [[87, 93, 142], [2, 17, 32, 47],
                               [87, 93, 142], [5, 40, 75],
                               [87, 93, 142], [2, 23, 44],
                               [87, 93, 142]]),
        ("same-signature-control", [[87, 88], [2, 17], [87, 88], [5, 40],
                                    [87, 88], [2, 23], [87, 88]]),
    ):
        maxima = [max(sum(x % d == a for x in v) for v in fibers for a in range(d))
                  for d in labels]
        fixtures.append({"name": name, "prefixes": list(range(1, 8)), "fibers": fibers,
                         "signatures": [signature(315, v) for v in fibers],
                         "physical_demands": 4 * sum(map(len, fibers)),
                         "uniform_tail_capacities": [2 * a for a in maxima] + maxima,
                         "uniform_tail_capacity": 3 * sum(maxima),
                         "single_cost_cut": parent_cut(315, fibers, labels, q=2),
                         "pair_cost_cut": parent_cut(315, fibers, labels, q=3)})
    return {"schema": "few-class-erasers-v1", "agent": "six-covering-3", "role": "researcher",
            "cofactor_period": 315, "physical_period": 10080, "binary_parent_depth": 3,
            "replication": 2, "labels": labels, "first_original_moduli": [16 * d for d in labels],
            "last_original_moduli": [32 * d for d in labels], "fixtures": fixtures,
            "scope": "Conditional tail demands, each inside the five-class root residual. No full base-stage reachability, tail feasibility of the passing fixture, root exclusion or numerical L_min(8) bound."}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    start = time.monotonic()
    result = build()
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    args.out.write_bytes(raw)
    print(json.dumps({"certificate_sha256": sha256(raw).hexdigest(),
                      "fixtures": [{"name": f["name"], "single_cost": f["single_cost_cut"]["value"],
                                    "single_threshold": f["single_cost_cut"]["threshold"],
                                    "pair_cost": f["pair_cost_cut"]["value"],
                                    "pair_threshold": f["pair_cost_cut"]["threshold"]}
                                   for f in result["fixtures"]],
                      "seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
