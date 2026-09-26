"""Exact inputs for the two orthocentric flap templates; no Gaussian sign test.

Python 3.11+, standard library. All public coordinates and weights are strings
of integers or fractions. Bits on (01,02,03,12,13,23) select low -> high.
"""
from argparse import ArgumentParser
from fractions import Fraction as F
from itertools import combinations, permutations
import json

EDGES = tuple(combinations(range(4), 2))
TEMPLATES = {"source_cycle": 2, "strong": 4}


def rational(text):
    """Reject floating syntax instead of silently rationalizing it."""
    if not isinstance(text, str):
        raise ValueError("rational input must be an integer/fraction string")
    parts = text.split("/")
    if len(parts) not in (1, 2) or any(not p.lstrip("+-").isdigit() for p in parts):
        raise ValueError("use an integer or numerator/denominator")
    return F(text)


def exact(value):
    if isinstance(value, F) or type(value) is int:
        return F(value)
    return rational(value)


def arcs(mask):
    if type(mask) is not int or not 0 <= mask < 64:
        raise ValueError("mask must be an integer from 0 to 63")
    return tuple((i, j) if mask & (1 << e) else (j, i)
                 for e, (i, j) in enumerate(EDGES))


def encoded(arclist):
    return sum(1 << EDGES.index((i, j)) for i, j in arclist if i < j)


def orbit_record(mask):
    candidates = [(encoded([(p[i], p[j]) for i, j in arcs(mask)]), p)
                  for p in permutations(range(4))]
    canonical, p = min(candidates)
    return [mask, canonical, list(p)]


def vertices(a, b, d):
    a, b, d = map(exact, (a, b, d))
    if min(a, b, d) <= 0:
        raise ValueError("shape parameters must be positive")
    z = -1/a
    x = -(1+1/a**2)/b
    y = -(1+1/a**2+x**2)/d
    return ((F(0), F(0), a), (b, F(0), z), (x, d, z), (x, y, z))


def instance(template, a, b, d, units, variance=F(1), threshold=None):
    a, b, d = map(exact, (a, b, d))
    units = tuple(map(exact, units))
    variance = exact(variance)
    threshold = None if threshold is None else exact(threshold)
    if template not in TEMPLATES:
        raise ValueError("unknown template")
    if len(units) != 10 or min(units) < 0 or sum(units) <= 0:
        raise ValueError("need ten nonnegative rational units with positive sum")
    if variance <= 0 or (threshold is not None and threshold <= 0):
        raise ValueError("variance and optional threshold must be positive")
    v = vertices(a, b, d)
    x, y = list(v), list(v)
    labels = ["anchor_"+str(i) for i in range(4)]
    for i, j in arcs(TEMPLATES[template]):
        x.append(tuple(v[j][k]-v[i][k] for k in range(3)))
        y.append(tuple(v[j][k]+v[i][k] for k in range(3)))
        labels.append(f"flap_{i}_{j}")
    out = {"status": "INPUT_ONLY_NO_GAUSSIAN_SIGN", "template": template,
           "mask": TEMPLATES[template], "shape_parameters": list(map(str, (a, b, d))),
           "labels": labels, "input": [list(map(str, p)) for p in x],
           "output": [list(map(str, p)) for p in y],
           "weights": [str(w/sum(units)) for w in units],
           "variance": str(variance)}
    if threshold is not None:
        out["physical_threshold"] = str(threshold)
    return out


def certificate():
    return {"schema": "orthocentric_flap_selectors_v1",
            "bit_edges": [list(e) for e in EDGES],
            "bit_one": "smaller_to_larger",
            "relabelling_direction": "old_vertex_to_new_vertex",
            "records": [orbit_record(mask) for mask in range(64)],
            "fixtures": [instance(t, F(1), F(2), F(3), tuple(map(F, range(1, 11))))
                         for t in TEMPLATES]}


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument("--certificate", action="store_true")
    p.add_argument("--template", choices=tuple(TEMPLATES), default="strong")
    p.add_argument("--a", default="1")
    p.add_argument("--b", default="2")
    p.add_argument("--d", default="3")
    p.add_argument("--units", default="1,2,3,4,5,6,7,8,9,10")
    p.add_argument("--variance", default="1")
    p.add_argument("--threshold")
    args = p.parse_args()
    try:
        if args.certificate:
            data = certificate()
        else:
            data = instance(args.template, rational(args.a), rational(args.b),
                            rational(args.d), tuple(map(rational, args.units.split(","))),
                            rational(args.variance),
                            None if args.threshold is None else rational(args.threshold))
    except (ValueError, ZeroDivisionError) as e:
        p.error(str(e))
    print(json.dumps(data, indent=2)+"\n", end="")


if __name__ == "__main__":
    main()
