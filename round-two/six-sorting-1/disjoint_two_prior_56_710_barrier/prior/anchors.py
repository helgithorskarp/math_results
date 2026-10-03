"""Huffman leaf budgets from exact semantic extreme profiles.

This module consumes profile.py's original-family-preserving data. It does
not identify conditional free-input images merely by their marker ports.
"""

import argparse
import importlib.util
import json
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "sorting_semantic_profile", Path(__file__).with_name("profile.py"))
semantic = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(semantic)


def log_ceiling(x):
    if not isinstance(x, int) or x <= 0:
        raise ValueError("positive integer mass required")
    return (x - 1).bit_length()


def aggregate(n, data, direction, use_semantic=True):
    if direction not in ("low", "high"):
        raise ValueError("direction must be low or high")
    position = 0 if direction == "low" else 1
    count = "low_count" if direction == "low" else "high_count"
    unary = "one_minimum" if direction == "low" else "one_maximum"
    exponent_column = 3 if use_semantic else 2
    chosen = {name: item for name, item in data.items() if item[count] > 0}
    sizes = {name: semantic.SIZES[n - item["low_count"] - item["high_count"]]
             for name, item in chosen.items()}
    base = min(sizes.values())
    ports = sorted(z[position].bit_length() - 1 for z in data[unary]["envelope"])
    rows = []
    for p in ports:
        masses = {name: sum(1 << z[exponent_column] for z in item["envelope"]
                            if (z[position] >> p) & 1)
                  for name, item in chosen.items()}
        label = max(sizes[name] + log_ceiling(mass)
                    for name, mass in masses.items() if mass)
        rows.append({"port": p, "anchored_masses": masses,
                     "label": label, "units": 1 << (label - base)})
    mass = sum(row["units"] for row in rows)
    return {"base": base, "normalized_mass": mass,
            "lower_bound": base + log_ceiling(mass), "rows": rows}


def both(n, data, use_semantic=True):
    return {side: aggregate(n, data, side, use_semantic) for side in ("low", "high")}


def prefix_trace(n, gates):
    """Exact simple implementation; callers with existing data use aggregate."""
    trace = []
    for cut in range(len(gates) + 1):
        data = semantic.analyze(n, gates[:cut])
        profiles = both(n, data)
        trace.append({"cut": cut,
                      "low": profiles["low"]["normalized_mass"],
                      "high": profiles["high"]["normalized_mass"],
                      "base": profiles["low"]["base"]})
    return trace


def first_rejection(trace, budget):
    for row in trace:
        for side in ("low", "high"):
            bound = row["base"] + log_ceiling(row[side])
            if bound > budget:
                return {"cut": row["cut"], "direction": side,
                        "normalized_mass": row[side], "base": row["base"],
                        "lower_bound": bound}
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", required=True)
    parser.add_argument("--field", default="gates")
    parser.add_argument("--case", help="select a named entry in a cases fixture")
    parser.add_argument("--budget", type=int, default=44)
    args = parser.parse_args()
    obj = json.load(open(args.network, encoding="utf-8"))
    if args.case:
        matches = [case for case in obj["cases"] if case["name"] == args.case]
        if len(matches) != 1:
            parser.error("case name is missing or ambiguous")
        obj = matches[0]
    n, gates = obj["n"], obj[args.field]
    data = semantic.analyze(n, gates)
    result = both(n, data)
    print(json.dumps({"n": n, "prefix_size": len(gates), "budget": args.budget,
                      "first_rejection": first_rejection(prefix_trace(n, gates), args.budget),
                      "anchors": result}, sort_keys=True))


if __name__ == "__main__":
    main()
