#!/usr/bin/env python3
"""Definition-level lower-bound verification; independent of the SAT encoding."""
import itertools
import json
from pathlib import Path


def check(points):
    if len(points) != 20 or len({tuple(p) for p in points}) != 20:
        raise ValueError("need20 distinct points")
    if any(len(p)!=2 or not all(type(x) is int for x in p)
           or not (0<=p[0]<3 and 0<=p[1]<18) for p in points):
        raise ValueError("bad group coordinates")
    checked = 0
    for subset in itertools.combinations(points,18):
        checked += 1
        if sum(p[0] for p in subset)%3 == 0 and sum(p[1] for p in subset)%18 == 0:
            raise ValueError("18-element zero sum found")
    return {"distinct_points":20,"subsets_checked":checked,
            "zero_sum_18_subsets":0,"certified_lower_bound":21}


if __name__ == "__main__":
    points=json.loads(Path(__file__).with_name("witness20.json").read_text())["points"]
    print(json.dumps(check(points),sort_keys=True))
