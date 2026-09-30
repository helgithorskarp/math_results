"""One bounded LP proposal on APs avoiding the entire base zero-load set.

Only the old base-screen checker is imported. This generator uses square
residues; the new independent checker uses Euler's criterion.
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

for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"
HERE = Path(__file__).parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--summary", type=Path)
    args = p.parse_args()
    start = time.monotonic()
    raw = (HERE / "base/phase-269.json").read_bytes()
    base = json.loads(raw)
    spec = importlib.util.spec_from_file_location("old_base", HERE / "base/verify.py")
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    old.check_case(base)
    squares = {r*r % 617 for r in range(1, 617)}
    colors = []
    for x in range(3704):
        r = (x-1852+(269 if x < 1852 else 349)) % 617
        colors.append(-1 if r == 0 else int(r not in squares) ^ int(x >= 1852))
    load = [0]*3704
    for a, d, w in base["color0_APs"]:
        for j in range(7):
            load[a+j*d] += w
    D0 = base["denominator"]
    delta = 196*D0-sum(w for a, d, w in base["color0_APs"])
    vertices = [x for x in range(3704) if colors[x] == 0 and D0-load[x] <= delta]
    index = {x: i for i, x in enumerate(vertices)}
    aps = [(a, d) for d in range(1, 618)
           for a in range(max(0, 1852-6*d), min(1852, 3704-6*d))
           if all(colors[a+j*d] == 0 and load[a+j*d] > 0 for j in range(7))]
    petals = [{index[x] for x in (a+j*d for j in range(7)) if x in index} for a, d in aps]
    if any(not petal for petal in petals):
        raise ValueError("Empty required petal needs a separate direct certificate")
    lookup = {ap: p for ap, p in zip(aps, petals)}
    plans = json.loads((HERE / "plans.json").read_text())
    if plans["phase"] != 269:
        raise ValueError("Wrong plan phase")
    triples = plans["cover2_triples"]
    cuts = []
    for triple in triples:
        keys = [tuple(ap) for ap in triple]
        if len(set(keys)) != 3 or any(ap not in lookup for ap in keys):
            raise ValueError("Invalid actual AP triple")
        ps = [lookup[ap] for ap in keys]
        if set.intersection(*ps):
            raise ValueError("Common point in triple petals")
        cuts.append(set.union(*ps))
    rows = petals+cuts
    columns = [[] for x in vertices]
    for ri, row in enumerate(rows):
        for ci in row:
            columns[ci].append(ri)
    starts, indices = [0], []
    for col in columns:
        indices.extend(col)
        starts.append(len(indices))
    import highspy as hs
    import numpy as np
    h = hs.Highs()
    options = {"threads": 1, "parallel": "off", "output_flag": False,
               "solver": "ipm", "run_crossover": "on", "time_limit": 15.0,
               "random_seed": 0, "primal_feasibility_tolerance": 1e-9,
               "dual_feasibility_tolerance": 1e-9, "ipm_optimality_tolerance": 1e-9}
    for key, value in options.items():
        if h.setOptionValue(key, value) != hs.HighsStatus.kOk:
            raise RuntimeError("Unsupported solver option")
    lp = hs.HighsLp()
    lp.num_col_, lp.num_row_ = len(vertices), len(rows)
    lp.col_cost_, lp.col_lower_, lp.col_upper_ = np.ones(len(vertices)), np.zeros(len(vertices)), np.ones(len(vertices))
    lp.row_lower_ = np.array([1]*len(petals)+[2]*len(cuts), dtype=float)
    lp.row_upper_ = np.full(len(rows), hs.kHighsInf)
    lp.a_matrix_.format_ = hs.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.array(starts, dtype=np.int32)
    lp.a_matrix_.index_ = np.array(indices, dtype=np.int32)
    lp.a_matrix_.value_ = np.ones(len(indices))
    if h.passModel(lp) != hs.HighsStatus.kOk:
        raise RuntimeError("Model load failed")
    h.run()
    solution = h.getSolution()
    duals = list(solution.row_dual)
    if not solution.value_valid or not solution.dual_valid or not all(math.isfinite(w) for w in duals):
        raise RuntimeError("Incomplete numerical guidance; no mathematical exclusion")
    D = 1_000_000
    nums = [max(0, math.floor(w*D)) for w in duals]
    final_load = [0]*len(vertices)
    for row, w in zip(rows, nums):
        for i in row:
            final_load[i] += w
    nu = [[x, w-D] for x, w in zip(vertices, final_load) if w > D]
    W = sum(nums[:len(aps)])+2*sum(nums[len(aps):])
    gap = W-sum(w for x, w in nu)-196*D
    certificate = {"format": "QR617_UNIFORM_ZERO_AVOIDANCE_1", "phase": 269, "class_cap": 197,
                   "base_sha256": hashlib.sha256(raw).hexdigest(), "denominator": D,
                   "AP_weights": sorted([a, d, w] for (a, d), w in zip(aps, nums[:len(aps)]) if w),
                   "cover2_weights": [[triple, w] for triple, w in zip(triples, nums[len(aps):]) if w],
                   "surcharges": nu}
    encoded = (json.dumps(certificate, sort_keys=True, separators=(",", ":"))+"\n").encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded)
    summary = {"agent": "six-vdw-3", "role": "researcher", "python": sys.version.split()[0],
               "solver": h.version(), "numpy": np.__version__, "options": options,
               "numerical_status": h.modelStatusToString(h.getModelStatus()),
               "safe_original_APs": len(aps), "fixed_cover_two_rows": len(cuts),
               "strict_gap_numerator": gap, "denominator": D,
               "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
               "seconds": time.monotonic()-start,
               "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "requires_independent_exact_check": True}
    if args.summary:
        args.summary.write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary))
    if gap <= 0:
        raise RuntimeError("Nonpositive repaired proposal; no exclusion")


if __name__ == "__main__":
    main()
