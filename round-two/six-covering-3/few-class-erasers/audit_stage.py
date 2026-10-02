"""Literal10080-point stage audit on three complete original base choices."""

from hashlib import sha256
import json
import resource
import time

from check import local_supports, minimum_cover, require
from stage import BASE, PREFIX, evaluate


def run():
    evidence = []
    for name, phases in (
        ("zero", [[n, 0] for n in BASE]),
        ("one", [[n, 1] for n in BASE]),
        ("varying", [[n, (n // 3 + 17) % n] for n in BASE]),
    ):
        got = evaluate(phases)
        selected = list(PREFIX) + [tuple(row) for row in phases]
        physical = {x for x in range(10080) if all(x % n != a for n, a in selected)}
        holes = [sorted({x % 315 for x in physical if x % 8 == r}) for r in range(8)]
        prefixes = [r for r in range(8) if holes[r]]
        fibers = [holes[r] for r in prefixes]
        require(len(physical) == 4 * sum(map(len, fibers)), "a base class differs across high copies")
        require(got["prefixes"] == prefixes and got["holes"] == fibers, "stage fiber extraction differs")
        supports, singles, pairs = local_supports(fibers)
        m = len(fibers)
        costs = []
        for q, field in ((2, "single_cost_cut"), (3, "pair_cost_cut")):
            options = [[s for s in row if s.bit_count() < q] for row in supports]
            minimum, _ = minimum_cover(options, q)
            threshold = 8 * m - 36 if q == 2 else 12 * m + 6 * max(0, 2 * m - 6) - 60
            require(got[field]["supports"] == options and got[field]["value"] == minimum, "stage support/optimizer mismatch")
            require(got[field]["threshold"] == threshold and got[field]["excluded"] == (minimum < threshold), "stage count/exclusion mismatch")
            costs.append([q, minimum, threshold])
        evidence.append({"name": name, "base_phases": len(phases), "physical_holes": len(physical),
                         "prefixes": prefixes, "cofactor_holes": list(map(len, fibers)),
                         "cost_thresholds": costs, "literal_single_phases": singles,
                         "literal_pair_phase_combinations": pairs,
                         "physical_holes_sha256": sha256(json.dumps(sorted(physical), separators=(",", ":")).encode()).hexdigest()})
    return {"agent": "six-covering-3", "role": "researcher", "status": "LITERAL STAGE AUDIT PASSED",
            "assignments": evidence,
            "scope": "Only three explicit all36-base-phase choices, not a complete base-phase search."}


if __name__ == "__main__":
    start = time.monotonic()
    result = run()
    print(json.dumps({"evidence": result, "seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
