"""Bounded packing with an exact worst-case removed-edit loss charge.

Unlike whole-mask avoidance, a weighted AP may contain a possible removed
edit. All such losses are explicitly bounded, then independently checked.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time

import os

for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"

HERE = Path(__file__).parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--threshold", type=int, default=65000)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--summary", type=Path)
    p.add_argument("--plans", type=Path, default=HERE / "plans.json")
    args = p.parse_args()
    # This package reproduces one checked coordinate restriction. Other
    # thresholds are exploration and require a fresh exact replay.
    start = time.monotonic()
    raw = (HERE / "base/phase-269.json").read_bytes()
    base = json.loads(raw)
    spec = importlib.util.spec_from_file_location("base_replay", HERE / "base/verify.py")
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    old.check_case(base)
    if base["s"] != 269:
        raise ValueError("Wrong base phase")
    load = [0]*3704
    for a, d, w in base["color0_APs"]:
        for j in range(7):
            load[a+j*d] += w
    total = sum(w for a, d, w in base["color0_APs"])
    slack = 196*base["denominator"]-total+args.threshold
    if args.threshold < 0 or not 0 <= slack < base["denominator"]:
        raise ValueError("Threshold outside chosen screened frontier")
    sq = {r*r % 617 for r in range(1, 617)}
    def color(x):
        r = (x-1852+(269 if x < 1852 else 349)) % 617
        return -1 if r == 0 else int(r not in sq) ^ int(x >= 1852)
    vertices = [x for x in range(3704) if color(x) == 0 and base["denominator"]-load[x] <= slack]
    mask = {x for x in range(3704) if color(x) == 0 and load[x] <= args.threshold}
    if set(vertices) & mask:
        raise ValueError("Chosen low-load mask must be outside the remaining-edit screen")
    aps = [(a, d) for d in range(1, 618)
           for a in range(max(0, 1852-6*d), min(1852, 3704-6*d))
           if all(color(a+j*d) == 0 for j in range(7))]
    actual = [set(a+j*d for j in range(7)) for a, d in aps]
    index = {x: i for i, x in enumerate(vertices)}
    petals = [{index[x] for x in row if x in index} for row in actual]
    # A zero petal is allowed here: if not hit by the removed edit the
    # corresponding row is itself a contradiction. AP loss is still charged.
    lookup = {ap: i for i, ap in enumerate(aps)}
    triples, cuts, cut_actual = [], [], []
    plans = json.loads(args.plans.read_text())
    if plans["phase"] != 269:
        raise ValueError("Wrong triple-plan phase")
    for triple in plans["cover2_triples"]:
        keys = [tuple(ap) for ap in triple]
        if len(set(keys)) != 3 or any(ap not in lookup for ap in keys):
            continue
        ids = [lookup[ap] for ap in keys]
        ps = [petals[i] for i in ids]
        if not all(ps) or set.intersection(*ps):
            continue
        triples.append(triple)
        cuts.append(set.union(*ps))
        cut_actual.append([actual[i] for i in ids])
    masks = sorted(mask)
    z_index = {x: i for i, x in enumerate(masks)}
    rows = petals+cuts
    # Direct packing LP: maximize weighted RHS - worst loss - surcharges.
    # Columns are AP/triple weights, then worst-loss t, then one surcharge
    # per screened point. All variables are nonnegative, no symmetry of f.
    starts, indices, values = [0], [], []
    for i, row in enumerate(rows):
        indices.extend(sorted(row)); values.extend([1.0]*len(row))
        if i < len(aps):
            losses = {x: 1 for x in actual[i] & mask}
        else:
            ps = cut_actual[i-len(aps)]
            losses = {x: (2 if all(x in a for a in ps) else 1) for x in set.union(*ps) & mask}
        for x in sorted(losses):
            indices.append(len(vertices)+z_index[x]); values.append(float(losses[x]))
        starts.append(len(indices))
    indices.extend(range(len(vertices), len(vertices)+len(masks)))
    values.extend([-1.0]*len(masks)); starts.append(len(indices))
    for i in range(len(vertices)):
        indices.append(i); values.append(-1.0); starts.append(len(indices))
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
    lp.num_col_, lp.num_row_ = len(rows)+1+len(vertices), len(vertices)+len(masks)
    lp.col_cost_ = np.array([-1.0]*len(aps)+[-2.0]*len(cuts)+[1.0]*(1+len(vertices)))
    lp.col_lower_ = np.zeros(lp.num_col_)
    lp.col_upper_ = np.full(lp.num_col_, hs.kHighsInf)
    lp.row_lower_ = np.full(lp.num_row_, -hs.kHighsInf)
    lp.row_upper_ = np.array([1.0]*len(vertices)+[0.0]*len(masks))
    lp.a_matrix_.format_ = hs.MatrixFormat.kColwise
    lp.a_matrix_.start_, lp.a_matrix_.index_ = np.array(starts, dtype=np.int32), np.array(indices, dtype=np.int32)
    lp.a_matrix_.value_ = np.array(values)
    if h.passModel(lp) != hs.HighsStatus.kOk:
        raise RuntimeError("Model load failed")
    h.run()
    sol = h.getSolution()
    if not sol.value_valid or not all(math.isfinite(w) for w in sol.col_value):
        raise RuntimeError("Incomplete numerical guidance; no mathematical exclusion")
    D = 1_000_000
    nums = [max(0, math.floor(w*D)) for w in sol.col_value[:len(rows)]]
    packed = [0]*len(vertices)
    loss = {z: 0 for z in masks}
    for i, (row, w) in enumerate(zip(rows, nums)):
        for x in row:
            packed[x] += w
        if i < len(aps):
            for z in actual[i] & mask:
                loss[z] += w
        else:
            ps = cut_actual[i-len(aps)]
            for z in set.union(*ps) & mask:
                loss[z] += w*(2 if all(z in a for a in ps) else 1)
    nu = [[x, w-D] for x, w in zip(vertices, packed) if w > D]
    worst = max(loss.values())
    W = sum(nums[:len(aps)])+2*sum(nums[len(aps):])
    gap = W-worst-sum(w for x, w in nu)-196*D
    cert = {"format": "QR617_ROBUST_LOW_LOAD_REMOVAL_1", "phase": 269, "class_cap": 197,
            "threshold": args.threshold, "base_sha256": hashlib.sha256(raw).hexdigest(), "denominator": D,
            "AP_weights": sorted([a, d, w] for (a, d), w in zip(aps, nums[:len(aps)]) if w),
            "cover2_weights": [[triple, w] for triple, w in zip(triples, nums[len(aps):]) if w],
            "surcharges": nu, "worst_loss_numerator": worst}
    encoded = (json.dumps(cert, sort_keys=True, separators=(",", ":"))+"\n").encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded)
    out = {"agent": "six-vdw-3", "role": "researcher", "threshold": args.threshold,
           "mask": len(mask), "screen": len(vertices), "original_APs": len(aps), "valid_cut_rows": len(cuts),
           "weighted_numerator": W, "worst_removed_edit_loss_numerator": worst,
           "positive_APs": len(cert["AP_weights"]), "positive_cuts": len(cert["cover2_weights"]),
           "gap_numerator": gap, "denominator": D, "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           "numerical_status": h.modelStatusToString(h.getModelStatus()), "seconds": time.monotonic()-start,
           "solver": h.version(), "numpy": np.__version__, "options": options,
           "certificate_sha256": hashlib.sha256(encoded).hexdigest(), "exact_check_required": True,
           "failed_guidance_proves_no_exclusion": True}
    if args.summary:
        args.summary.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out))


if __name__ == "__main__":
    main()
