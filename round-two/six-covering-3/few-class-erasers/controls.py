"""Semantic damages, stage input guards, and a literal positive tail."""

from copy import deepcopy
import json
from pathlib import Path
import resource
import time

from check import audit, require
from model import divisors, parent_cut
from stage import BASE, evaluate


def run():
    certificate = json.loads(Path(__file__).with_name("certificate.json").read_text())
    damages = []
    d = deepcopy(certificate); d["first_original_moduli"][1] = 16; damages.append(d)
    d = deepcopy(certificate); d["fixtures"].pop(); damages.append(d)
    d = deepcopy(certificate); d["labels"].pop(); damages.append(d)
    d = deepcopy(certificate); d["fixtures"][0]["fibers"][0][-1] += 1; damages.append(d)
    d = deepcopy(certificate); d["fixtures"][0]["signatures"][0] = 3; damages.append(d)
    d = deepcopy(certificate); d["fixtures"][0]["pair_cost_cut"]["supports"][0].pop(); damages.append(d)
    d = deepcopy(certificate); d["fixtures"][0]["pair_cost_cut"]["supports"][0].append((1 << 4) | (1 << 11)); damages.append(d)
    d = deepcopy(certificate); d["fixtures"][0]["pair_cost_cut"]["right_labels"].remove(1); damages.append(d)
    d = deepcopy(certificate); d["fixtures"][0]["pair_cost_cut"]["value"] += 1; damages.append(d)
    d = deepcopy(certificate); d["fixtures"][0]["pair_cost_cut"]["threshold"] = 70; damages.append(d)
    d = deepcopy(certificate); d["fixtures"][0]["pair_cost_cut"]["excluded"] = False; damages.append(d)
    d = deepcopy(certificate); d["fixtures"][0]["uniform_tail_capacities"][0] += 1; damages.append(d)
    rejected = 0
    for damaged in damages:
        try:
            audit(damaged)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("damaged certificate was accepted")
    phases = [[n, 0] for n in BASE]
    bad = [phases[:-1], phases + [[16, 0]], deepcopy(phases), deepcopy(phases), deepcopy(phases)]
    bad[2][0] = [8, 0]
    bad[3][0][1] = bad[3][0][0]
    bad[4][0][1] = True
    malformed_rejected = 0
    for rows in bad:
        try:
            evaluate(rows)
        except ValueError:
            malformed_rejected += 1
        else:
            raise ValueError("malformed base inventory accepted")

    # A real completing tail on seven singleton parents; no base reachability.
    demand = {x for x in range(10080) if x % 8 != 0 and x % 315 == 2}
    labels = divisors(315)
    first_targets = [r + 8 * e for r in range(1, 8) for e in range(2)]
    tail = []
    for d, prefix in zip(labels, first_targets[:12]):
        n = 16 * d
        phase = next(a for a in range(n) if a % 16 == prefix and a % d == 2 % d)
        tail.append((n, phase))
    final_targets = [c + 16 * e for c in first_targets[12:] for e in range(2)]
    for d, prefix in zip(labels, final_targets):
        n = 32 * d
        phase = next(a for a in range(n) if a % 32 == prefix and a % d == 2 % d)
        tail.append((n, phase))
    require(len(demand) == 28 and len({n for n, a in tail}) == len(tail) == 16, "bad positive dimensions")
    require(all(any(x % n == a for n, a in tail) for x in demand), "positive tail misses demand")
    require(all(not parent_cut(315, [[2]] * 7, labels, q=q)["excluded"] for q in (2, 3)), "positive tail cut incorrectly excludes")
    return {"agent": "six-covering-3", "role": "researcher", "status": "CONTROLS PASSED",
            "damaged_certificates_rejected": rejected, "malformed_base_inputs_rejected": malformed_rejected,
            "positive_tail": {"physical_demands": len(demand), "original_phases": tail},
            "scope": "Semantic guards and one literal conditional positive tail; no base-stage witness."}


if __name__ == "__main__":
    start = time.monotonic()
    result = run()
    print(json.dumps({"evidence": result, "seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
