"""Optional bounded LP rediscovery for the published, complete branch plans.

The plans are explicit mathematical inputs, not an exhaustive cut search.
Enumeration uses square residues; verification independently uses Euler's
criterion. Only the old base-screen checker is imported here. Numerical
status never certifies a leaf: verify.py must check the exported integers.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import sys
import time

for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[name] = "1"

HERE = Path(__file__).parent
PHASES = (184, 201, 205, 269)
P, N, C, B, D = 617, 3704, 1852, 196, 1_000_000


def instance(phase, base_path):
    raw = base_path.read_bytes()
    base = json.loads(raw)
    spec = importlib.util.spec_from_file_location("old_base_check", HERE / "base/verify.py")
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    result = check.check_case(base)
    if result["phase"] != phase:
        raise ValueError("Base phase mismatch")
    d0 = base["denominator"]
    delta = B*d0 - sum(row[2] for row in base["color0_APs"])
    if delta < 0:
        raise ValueError("Base already excludes budget")
    loads = [0]*N
    for a, d, w in base["color0_APs"]:
        for j in range(7):
            loads[a+j*d] += w
    squares = {r*r % P for r in range(1, P)}
    t = (1-phase) % P
    colors = []
    for x in range(N):
        r = (x-C+(phase if x < C else t)) % P
        colors.append(-1 if r == 0 else int(r not in squares) ^ int(x >= C))
    eligible = {x for x in range(N) if colors[x] == 0 and d0-loads[x] <= delta}
    aps = [(a, d) for d in range(1, (N-1)//6+1)
           for a in range(max(0, C-6*d), min(C, N-6*d))
           if all(colors[a+j*d] == 0 for j in range(7))]
    petals = [{a+j*d for j in range(7)} & eligible for a, d in aps]
    if any(not petal for petal in petals):
        raise ValueError("Empty required petal: record a separate direct proof")
    return raw, eligible, aps, petals


def solve(rows, rhs, free):
    import highspy as hs
    import numpy as np
    index = {x: i for i, x in enumerate(free)}
    columns = [[] for _ in free]
    for ri, row in enumerate(rows):
        for x in row:
            columns[index[x]].append(ri)
    starts, indices = [0], []
    for col in columns:
        indices.extend(col)
        starts.append(len(indices))
    h = hs.Highs()
    options = {"threads": 1, "parallel": "off", "output_flag": False,
               "solver": "ipm", "run_crossover": "on", "time_limit": 15.0,
               "random_seed": 0, "primal_feasibility_tolerance": 1e-9,
               "dual_feasibility_tolerance": 1e-9, "ipm_optimality_tolerance": 1e-9}
    for key, value in options.items():
        if h.setOptionValue(key, value) != hs.HighsStatus.kOk:
            raise RuntimeError("Unsupported solver option")
    lp = hs.HighsLp()
    lp.num_col_, lp.num_row_ = len(free), len(rows)
    lp.col_cost_ = np.ones(len(free))
    lp.col_lower_, lp.col_upper_ = np.zeros(len(free)), np.ones(len(free))
    lp.row_lower_, lp.row_upper_ = np.array(rhs, dtype=float), np.full(len(rows), hs.kHighsInf)
    lp.a_matrix_.format_ = hs.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.array(starts, dtype=np.int32)
    lp.a_matrix_.index_ = np.array(indices, dtype=np.int32)
    lp.a_matrix_.value_ = np.ones(len(indices))
    if h.passModel(lp) != hs.HighsStatus.kOk:
        raise RuntimeError("Model load failed")
    h.run()
    solution = h.getSolution()
    duals = list(solution.row_dual)
    if not solution.value_valid or not solution.dual_valid or not all(math.isfinite(x) for x in duals):
        raise RuntimeError("Incomplete numerical guidance; no exclusion")
    return duals, {"solver": h.version(), "numpy": np.__version__, "options": options,
                   "status": h.modelStatusToString(h.getModelStatus()),
                   "floating_objective": h.getObjectiveValue()}


def regenerate(phase, plan, output):
    raw, eligible, aps, petals = instance(phase, HERE / f"base/certificates/phase-{phase}.json")
    lookup = {ap: petal for ap, petal in zip(aps, petals)}
    triples = plan["cover2_triples"]
    unions = []
    for triple in triples:
        key = [tuple(ap) for ap in triple]
        if len(set(key)) != 3 or any(ap not in lookup for ap in key):
            raise ValueError("Invalid fixed triple")
        ps = [lookup[ap] for ap in key]
        if set.intersection(*ps):
            raise ValueError("Cover-two triple has a common vertex")
        unions.append(set.union(*ps))
    base_hash = hashlib.sha256(raw).hexdigest()
    history = []

    def visit(node, forced, forbidden):
        if set(node) == {"leaf"} and node["leaf"] is True:
            free = sorted(eligible-forced-forbidden)
            rows, rhs, labels = [], [], []
            for kind, original in (("AP", petals), ("cover2", unions)):
                for i, row in enumerate(original):
                    residual = max(0, (1 if kind == "AP" else 2)-len(row & forced))
                    if residual:
                        rows.append(row & set(free))
                        rhs.append(residual)
                        labels.append((kind, i))
            duals, meta = solve(rows, rhs, free)
            nums = [max(0, math.floor(x*D)) for x in duals]
            loads = dict.fromkeys(free, 0)
            for row, w in zip(rows, nums):
                for x in row:
                    loads[x] += w
            surcharges = [[x, max(0, loads[x]-D)] for x in free if loads[x] > D]
            weighted = sum(w*r for w, r in zip(nums, rhs))
            penalty = sum(w for x, w in surcharges)
            gap = weighted-penalty-(B-len(forced))*D
            leaf = {"format": "QR617_UNIFORM_SCREENED_COVER2_1", "phase": phase,
                    "class_cap": B, "base_certificate_sha256": base_hash, "denominator": D,
                    "color0_APs": sorted([*aps[i], w] for (kind, i), w in zip(labels, nums)
                                         if kind == "AP" and w),
                    "color0_cover2": [[triples[i], w] for (kind, i), w in zip(labels, nums)
                                      if kind == "cover2" and w],
                    "color0_surcharges": surcharges}
            history.append({"forced": sorted(forced), "forbidden": sorted(forbidden),
                            "strict_gap_numerator": gap, "denominator": D, **meta})
            if gap <= 0:
                raise RuntimeError("No positive exact repaired dual; no exclusion")
            return {"leaf": leaf}
        if set(node) != {"split", "unchanged", "edited"}:
            raise ValueError("Exactly two planned children required")
        x = node["split"]
        if type(x) is not int or x not in eligible-forced-forbidden:
            raise ValueError("Invalid split position")
        return {"split": x, "unchanged": visit(node["unchanged"], forced, forbidden | {x}),
                "edited": visit(node["edited"], forced | {x}, forbidden)}

    tree = {"format": "QR617_CLASS196_BINARY_COVER_1", "phase": phase, "class_cap": B,
            "base_certificate_sha256": base_hash, "tree": visit(plan["tree"], set(), set())}
    encoded = (json.dumps(tree, sort_keys=True, separators=(",", ":"))+"\n").encode()
    output.write_bytes(encoded)
    return {"phase": phase, "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
            "certificate_bytes": len(encoded), "leaves": history,
            "requires_independent_exact_check": True}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work", type=Path, required=True)
    p.add_argument("--phase", type=int, choices=PHASES)
    args = p.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    plans = json.loads((HERE / "plans.json").read_text())
    start, results = time.monotonic(), []
    for phase in ((args.phase,) if args.phase is not None else PHASES):
        result = regenerate(phase, plans[str(phase)], args.work / f"phase-{phase}.json")
        results.append(result)
        print(json.dumps({k: v for k, v in result.items() if k != "leaves"}), flush=True)
    summary = {"agent": "six-vdw-3", "role": "researcher", "python": sys.version.split()[0],
               "seconds": time.monotonic()-start,
               "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "phases": results, "numeric_status_is_not_proof": True}
    (args.work / "guidance.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "phases"}), flush=True)


if __name__ == "__main__":
    main()
