"""Complete small literal two-layer models for the general counting proof.

M=2,p=3 and M=3,p=2; one/two labeled initial targets; all nonempty
cofactor sets; every pair of subpools of {1,M}; all first phase tuples;
all terminal coverage unions. No optimizer or large certificate.
"""

from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
import resource
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run():
    counts = {"models": 0, "feasible_models": 0, "first_phase_assignments": 0,
              "completing_first_assignments": 0, "complete_with_changed_survivor": 0,
              "complete_with_omitted_resource": 0, "legal_hypergraph_covers": 0,
              "feasible_cover_inequalities": 0, "first_accounting_checks": 0}
    records = []
    for m, p in ((2, 3), (3, 2)):
        nonempty = [tuple(x for x in range(m) if bits & (1 << x))
                    for bits in range(1, 1 << m)]
        pools = [(), (1,), (m,), (1, m)]
        family = {d: tuple(frozenset(x for x in range(m) if x % d == a)
                           for a in range(d)) for d in (1, m)}

        @lru_cache(None)
        def terminal(residual, d2):
            demand = 0
            for i, v in enumerate(residual):
                for child in range(p):
                    for x in v:
                        demand |= 1 << ((p * i + child) * m + x)
            unions = {0}
            for d in d2:
                actions = {0}
                for i, v in enumerate(residual):
                    for child in range(p):
                        for a in range(d):
                            actions.add(sum(1 << ((p * i + child) * m + x)
                                            for x in v if x % d == a))
                unions = {left | right for left in unions for right in actions}
            return demand in unions

        for t in (1, 2):
            for target_tuple in product(nonempty, repeat=t):
                targets = tuple(frozenset(v) for v in target_tuple)
                for d1, d2 in product(pools, repeat=2):
                    counts["models"] += 1
                    union_labels = sorted(set(d1) | set(d2))
                    covers = []
                    for q in (2, 3, 4):
                        edges = []
                        for i, v in enumerate(targets):
                            for size in range(1, min(q - 1, len(union_labels)) + 1):
                                for s in combinations(union_labels, size):
                                    if not (set(s) <= set(d1) or set(s) <= set(d2)):
                                        continue
                                    if any(v <= frozenset().union(*classes)
                                           for classes in product(*(family[d] for d in s))):
                                        edges.append((i, frozenset(s)))
                        for cmask in range(1 << t):
                            for bmask in range(1 << len(union_labels)):
                                bset = frozenset(d for j, d in enumerate(union_labels) if bmask & (1 << j))
                                if all(cmask & (1 << i) or s & bset for i, s in edges):
                                    c, b1, b2 = cmask.bit_count(), len(bset & set(d1)), len(bset & set(d2))
                                    lhs = p * q * (q - 1) * c + p * (q - 1) ** 2 * b1 + (q - 1) * b2
                                    lower_e = max(0, t - len(d2) // p)
                                    rhs = p * q * t + p * q * (q - 2) * lower_e - p * (q - 1) * len(d1) - len(d2)
                                    covers.append((q, c, b1, lhs, rhs))
                    counts["legal_hypergraph_covers"] += len(covers)
                    completions = 0
                    choices = [tuple([None] + list(product(range(t), range(d)))) for d in d1]
                    for actions in product(*choices):
                        counts["first_phase_assignments"] += 1
                        residual = [set(v) for v in targets]
                        used_at = [0] * t
                        for d, action in zip(d1, actions):
                            if action is not None:
                                i, a = action
                                residual[i].difference_update(family[d][a])
                                used_at[i] += 1
                        key = tuple(tuple(sorted(v)) for v in residual)
                        if not terminal(key, d2):
                            continue
                        completions += 1
                        counts["completing_first_assignments"] += 1
                        erased = sum(not v for v in residual)
                        changed = sum(bool(v) and v != set(targets[i]) for i, v in enumerate(residual))
                        spending = sum(used_at[i] for i, v in enumerate(residual) if not v)
                        require(erased >= max(0, t - len(d2) // p), "horizon erasure bound fails")
                        counts["complete_with_changed_survivor"] += int(changed > 0)
                        counts["complete_with_omitted_resource"] += int(any(a is None for a in actions))
                        for q, c, b1, lhs, rhs in covers:
                            counts["first_accounting_checks"] += 1
                            require(spending >= q * erased - (q - 1) * (c + b1), "first erasure accounting fails")
                            require(changed <= len(d1) - q * erased + (q - 1) * (c + b1), "changed survivor accounting fails")
                            require(lhs >= rhs, "a necessary hypergraph inequality excludes an actual completion")
                    if completions:
                        counts["feasible_models"] += 1
                        counts["feasible_cover_inequalities"] += len(covers)
                    records.append([m, p, t, target_tuple, d1, d2, completions, len(covers)])
    require(counts["complete_with_changed_survivor"] > 0, "missing change controls")
    require(counts["complete_with_omitted_resource"] > 0, "missing omission controls")
    raw = json.dumps(records, separators=(",", ":")).encode()
    return {"agent": "six-covering-3", "role": "researcher", "status": "COMPLETE SMALL MODELS PASSED",
            "cofactor_and_replication": [[2, 3], [3, 2]], "cutoffs": [2, 3, 4],
            "counts": counts, "records_sha256": sha256(raw).hexdigest(),
            "scope": "Complete stated finite models validate the counting argument; the general theorem is proved in prose."}


if __name__ == "__main__":
    start = time.monotonic()
    evidence = run()
    print(json.dumps({"evidence": evidence, "seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
