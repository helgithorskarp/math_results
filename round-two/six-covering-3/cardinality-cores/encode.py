"""Complete finite CNF for shared base phases and necessary support predicates.

Generated CNF/model maps belong in scratch. Satisfiability is not a covering.
"""

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import resource
import time

from model import PREFIX, BASE, frontier


class Formula:
    def __init__(self):
        self.names = []
        self.lookup = {}
        self.clauses = []

    def variable(self, name):
        name = tuple(name)
        if name in self.lookup:
            return self.lookup[name]
        self.names.append(name)
        v = len(self.names)
        self.lookup[name] = v
        return v

    def clause(self, literals):
        self.clauses.append(tuple(literals))

    def at_most_one(self, variables, name):
        if len(variables) < 2:
            return
        s = [self.variable(("counter",) + tuple(name) + (i,))
             for i in range(len(variables) - 1)]
        for i, v in enumerate(variables):
            if i < len(s):
                self.clause((-v, s[i]))
            if i > 0:
                self.clause((-v, -s[i - 1]))
            if 0 < i < len(s):
                self.clause((-s[i - 1], s[i]))


def build(only_B13=False):
    f = Formula()
    for d in BASE:
        vs = [f.variable(("base", d, a)) for a in range(d)]
        f.clause(vs)
        f.at_most_one(vs, ("base", d))
    initial = [x for x in range(2520) if all(x % d != a for d, a in PREFIX)]
    rows = [r for r in frontier() if not only_B13 or r["B"] == (1, 3)]
    for j, row in enumerate(rows):
        allowed = sorted({d for p in row["pairs"] for d in p})
        zs = []
        for r in range(1, 8):
            z = f.variable(("qualified", j, r))
            zs.append(z)
            cs = []
            for d in allowed:
                c = f.variable(("resource", j, r, d))
                cs.append(c)
                ws = [f.variable(("witness", j, r, d, a)) for a in range(d)]
                f.clause((-c, z))
                f.clause((-c, *ws))
                for w in ws:
                    f.clause((-w, c))
                f.at_most_one(ws, ("witness", j, r, d))
            for triple in combinations(cs, 3):
                f.clause(-c for c in triple)
            for x in initial:
                if x % 8 != r:
                    continue
                f.clause((-z,
                          *(f.lookup[("base", d, x % d)] for d in BASE),
                          *(f.lookup[("witness", j, r, d, x % d)] for d in allowed)))
        # At least k of seven: no set of8-k positions can be all false.
        for subset in combinations(zs, 8 - row["required"]):
            f.clause(subset)
    return f, rows


def assignment_for(phases, rows, f, predicate_witnesses):
    """Create a checkable Boolean model from literal containment witnesses."""
    values = [False] * (len(f.names) + 1)
    for d, a in phases:
        values[f.lookup[("base", d, a)]] = True
    for j, row in enumerate(rows):
        for r, witness in predicate_witnesses[j]:
            values[f.lookup[("qualified", j, r)]] = True
            for d, a in witness:
                values[f.lookup[("resource", j, r, d)]] = True
                values[f.lookup[("witness", j, r, d, a)]] = True
    first = {}
    for i, name in enumerate(f.names, 1):
        if values[i] and name[0] in ("base", "witness"):
            first[name[:-1]] = min(first.get(name[:-1], name[-1]), name[-1])
    for i, name in enumerate(f.names, 1):
        if name[0] != "counter":
            continue
        key, end = name[1:-1], name[-1]
        values[i] = key in first and first[key] <= end
    return values


def failed_clauses(f, values):
    return [i for i, clause in enumerate(f.clauses)
            if not any(values[abs(v)] == (v > 0) for v in clause)]


def write(f, rows, out):
    digest = sha256()
    with out.open("w") as stream:
        stream.write(f"p cnf {len(f.names)} {len(f.clauses)}\n")
        for clause in f.clauses:
            line = " ".join(map(str, clause)) + " 0\n"
            stream.write(line)
            digest.update(line.encode())
    metadata = {"agent": "six-covering-3", "role": "researcher",
                "variables": len(f.names), "clauses": len(f.clauses),
                "literal_occurrences": sum(map(len, f.clauses)),
                "base_moduli": list(BASE), "rows": rows,
                "names": f.names, "clause_body_sha256": digest.hexdigest(),
                "scope": "Necessary shared-base predicates only. SAT supplies no full covering; UNKNOWN is not exclusion."}
    out.with_suffix(out.suffix + ".json").write_text(json.dumps(metadata, separators=(",", ":"), sort_keys=True) + "\n")
    return {k: v for k, v in metadata.items() if k not in ("names", "rows", "base_moduli")}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only-B13", action="store_true")
    args = ap.parse_args()
    start = time.monotonic()
    f, rows = build(args.only_B13)
    evidence = write(f, rows, args.out)
    print(json.dumps({"evidence": evidence, "seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
