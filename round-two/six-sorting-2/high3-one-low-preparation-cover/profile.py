"""Exact extreme profiles with deletion of conditionally redundant gates.

An oriented pair (a, b) writes min to a and max to b. Middle truth-table
assignment x puts bit j of x on the j-th unmarked original input.
No solver, external data, floating point, or enumeration cutoff is used.
"""

import argparse
from functools import lru_cache
from itertools import combinations
import json

LOW, HIGH = "L", "H"
SIZES = (0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39)
FAMILIES = (("one_minimum", 1, 0), ("one_maximum", 0, 1),
            ("two_minima", 2, 0), ("two_maxima", 0, 2),
            ("mixed_pair", 1, 1))


def require(test, message):
    if not test:
        raise ValueError(message)


def validate(n, gates):
    require(isinstance(n, int) and 2 <= n <= 13, "supported order is 2..13")
    for gate in gates:
        require(isinstance(gate, (list, tuple)) and len(gate) == 2,
                "a gate must be an oriented pair")
        a, b = gate
        require(isinstance(a, int) and isinstance(b, int) and
                0 <= a < n and 0 <= b < n and a != b, "invalid gate")


@lru_cache(None)
def truth_columns(m):
    return tuple(sum(1 << x for x in range(1 << m) if (x >> j) & 1)
                 for j in range(m))


def mask(indices):
    return sum(1 << i for i in indices)


def marked_ports(values):
    return (mask(i for i, x in enumerate(values) if x == LOW),
            mask(i for i, x in enumerate(values) if x == HIGH))


def transition(values, a, b):
    x, y = values[a], values[b]
    if isinstance(x, str) or isinstance(y, str):
        def order(z):
            return -1 if z == LOW else 1 if z == HIGH else 0
        if order(x) > order(y):
            values[a], values[b] = y, x
        return 1, 0
    redundant = int((x & ~y) == 0)
    values[a], values[b] = x & y, x | y
    return 0, redundant


def summarize(records):
    profiles = {}
    for _, _, lo, hi, d, r, _ in records:
        old_d, old_c = profiles.get((lo, hi), (0, 0))
        profiles[lo, hi] = max(old_d, d), max(old_c, d + r)
    envelope = [[lo, hi, d, c] for (lo, hi), (d, c)
                in sorted(profiles.items())]
    return {
        "ordinary_mass": sum(1 << p[2] for p in envelope),
        "semantic_mass": sum(1 << p[3] for p in envelope),
        "maximum_deletions": max(p[4] for p in records),
        "maximum_semantic_deletions": max(p[4] + p[5] for p in records),
        "maximum_redundancies": max(p[5] for p in records),
        "port_classes": len(envelope),
    }, envelope


def analyze_family(n, gates, low_count, high_count):
    validate(n, gates)
    require(0 < low_count + high_count <= n, "invalid marked counts")
    histories = [[] for _ in range(len(gates) + 1)]
    for lows in combinations(range(n), low_count):
        other = [i for i in range(n) if i not in lows]
        for highs in combinations(other, high_count):
            columns = iter(truth_columns(n - low_count - high_count))
            values = [LOW if i in lows else HIGH if i in highs else next(columns)
                      for i in range(n)]
            input_low, input_high = mask(lows), mask(highs)
            d = r = redundant_mask = 0
            for cut in range(len(gates) + 1):
                lo, hi = marked_ports(values)
                histories[cut].append([input_low, input_high, lo, hi,
                                       d, r, redundant_mask])
                if cut != len(gates):
                    deletion, redundancy = transition(values, *gates[cut])
                    d += deletion
                    r += redundancy
                    if redundancy:
                        redundant_mask |= 1 << cut
    for rows in histories:
        rows.sort()
    trace = [summarize(rows)[0] for rows in histories]
    for left, right in zip(trace, trace[1:]):
        require(left["ordinary_mass"] <= right["ordinary_mass"],
                "ordinary mass decreased")
        require(left["semantic_mass"] <= right["semantic_mass"],
                "semantic mass decreased")
    summary, envelope = summarize(histories[-1])
    return {"low_count": low_count, "high_count": high_count,
            "records": histories[-1], "envelope": envelope,
            "summary": summary, "trace": trace}


def analyze(n, gates):
    return {name: analyze_family(n, gates, lo, hi)
            for name, lo, hi in FAMILIES if lo + hi <= n}


def lower_bound(n, data):
    k = n - data["low_count"] - data["high_count"]
    require(k < len(SIZES), "unknown imported middle-size lower bound")
    return SIZES[k] + (data["summary"]["semantic_mass"] - 1).bit_length()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", required=True)
    parser.add_argument("--field", default="gates")
    parser.add_argument("--budget", type=int, default=44)
    args = parser.parse_args()
    obj = json.load(open(args.network, encoding="utf-8"))
    n, gates = obj["n"], obj[args.field]
    data = analyze(n, gates)
    first = None
    for cut in range(len(gates) + 1):
        for name, lo, hi in FAMILIES:
            if name not in data:
                continue
            mass = data[name]["trace"][cut]["semantic_mass"]
            if SIZES[n - lo - hi] + (mass - 1).bit_length() > args.budget:
                if first is None:
                    first = {"cut": cut, "family": name, "mass": mass}
    print(json.dumps({"n": n, "prefix_size": len(gates), "budget": args.budget,
                      "lower_bounds": {k: lower_bound(n, v) for k, v in data.items()},
                      "first_rejection": first}, sort_keys=True))


if __name__ == "__main__":
    main()
