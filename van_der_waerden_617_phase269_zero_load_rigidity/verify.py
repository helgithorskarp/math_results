"""Definition-level uniform zero-load rigidity proof, without case splitting.

Euler colors, actual APs avoiding the entire base zero-load set, integer
loads and a strict weighted contradiction. No generator/solver imports.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

P, N, C, B = 617, 3704, 1852, 197


def need(ok, message):
    if not ok:
        raise ValueError(message)


def check(data, base_path, base_checker):
    need(type(data) is dict and set(data) == {"format", "phase", "class_cap", "base_sha256", "denominator", "AP_weights", "cover2_weights", "surcharges"}, "Certificate schema")
    need(data["format"] == "QR617_UNIFORM_ZERO_AVOIDANCE_1", "Certificate format")
    need(type(data["phase"]) is int and data["phase"] == 269 and type(data["class_cap"]) is int and data["class_cap"] == B, "Phase269 class197 frontier")
    D = data["denominator"]
    need(type(D) is int and D > 0, "Positive integer denominator")
    raw = base_path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == data["base_sha256"], "Base bytes")
    base = json.loads(raw)
    spec = importlib.util.spec_from_file_location("old_exact_base", base_checker)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    old.check_case(base)
    need(base["s"] == 269, "Base phase")
    D0 = base["denominator"]
    S = sum(w for a, d, w in base["color0_APs"])
    delta = (B-1)*D0-S
    need(0 <= delta < D0, "Screen after deleting one zero edit")
    colors, loads = [], [0]*N
    for x in range(N):
        r = (x-C+(base["s"] if x < C else base["t"])) % P
        colors.append(-1 if r == 0 else old.Q[r] ^ int(x >= C))
    for a, d, w in base["color0_APs"]:
        for aa in (a, N-1-a-6*d):
            for j in range(7):
                loads[aa+j*d] += w
    zero = [{x for x in range(N) if colors[x] == c and loads[x] == 0} for c in (0, 1)]
    free = [{x for x in range(N) if colors[x] == c and D0-loads[x] <= delta} for c in (0, 1)]
    need(zero[0] and zero[1] == {N-1-x for x in zero[0]}, "Reflected nonempty zero sets")
    need(free[1] == {N-1-x for x in free[0]}, "Reflected screens")
    need(not zero[0] & free[0], "Zero points outside other-edit screen")
    need(all(type(data[k]) is list for k in ("AP_weights", "cover2_weights", "surcharges")), "Weight lists")
    new_load, totals, checks = [0]*N, [0, 0], 0

    def petal(a, d, c):
        nonlocal checks
        need(type(a) is int and type(d) is int and d > 0, "Actual AP integers")
        need(0 <= a < C <= a+6*d < N, "Actual crossing coordinates")
        points = {a+j*d for j in range(7)}
        need(all(colors[x] == c for x in points), "Actual monochromatic nonpole AP")
        need(not points & zero[c], "AP must avoid ALL base zero-load points")
        checks += 1
        return points & free[c]

    seen = set()
    for row in data["AP_weights"]:
        need(type(row) is list and len(row) == 3 and all(type(x) is int for x in row), "AP row")
        a, d, w = row
        need(w > 0 and (a, d) not in seen, "Positive unique AP")
        seen.add((a, d))
        for c, aa in ((0, a), (1, N-1-a-6*d)):
            p = petal(aa, d, c)
            totals[c] += w
            for x in p:
                new_load[x] += w
    cut_details, seen = [], set()
    for row in data["cover2_weights"]:
        need(type(row) is list and len(row) == 2, "Cut row")
        triple, w = row
        need(type(triple) is list and len(triple) == 3 and type(w) is int and w > 0, "Positive triple weight")
        need(all(type(ap) is list and len(ap) == 2 and all(type(x) is int for x in ap) for ap in triple), "Triple AP integers")
        key = tuple(sorted(tuple(ap) for ap in triple))
        need(len(set(key)) == 3 and key not in seen, "Three distinct unique APs")
        seen.add(key)
        sizes = []
        for c in (0, 1):
            ps = [petal(a if c == 0 else N-1-a-6*d, d, c) for a, d in triple]
            need(all(ps) and not set.intersection(*ps), "Nonempty petals and empty common intersection")
            union = set.union(*ps)
            totals[c] += 2*w
            sizes.append(len(union))
            for x in union:
                new_load[x] += w
        need(sizes[0] == sizes[1], "Reflected union sizes")
        cut_details.append({"APs": triple, "union_size": sizes[0], "weight": w})
    surcharge, penalties, seen = [0]*N, [0, 0], set()
    for row in data["surcharges"]:
        need(type(row) is list and len(row) == 2 and all(type(x) is int for x in row), "Surcharge row")
        x, num = row
        need(x in free[0] and x not in seen and num > 0, "Eligible unique positive surcharge")
        seen.add(x)
        for c, xx in ((0, x), (1, N-1-x)):
            surcharge[xx] = num
            penalties[c] += num
    for c in (0, 1):
        need(all(new_load[x] <= D+surcharge[x] for x in free[c]), "Exact screened point capacity")
    need(totals[0] == totals[1] > 0 and penalties[0] == penalties[1], "Reflected positive totals")
    gap = totals[0]-penalties[0]-(B-1)*D
    need(gap > 0, "No strict uniform zero-edit contradiction")
    return {"agent": "six-vdw-3", "role": "researcher", "status": "EXACT_UNIFORM_ZERO_LOAD_RIGIDITY",
            "phase": 269, "key": [269, 349, 1], "conditional_class_cap": B,
            "forbidden_zero_load_edit_positions_color0": sorted(zero[0]),
            "forbidden_zero_load_edit_positions_color1": sorted(zero[1]),
            "forbidden_positions_per_class": len(zero[0]),
            "other_edit_screen_positions_per_class": len(free[0]),
            "remaining_edit_cap_if_zero_edited": B-1,
            "base_weight_numerator": S, "base_denominator": D0,
            "other_edit_defect_slack_numerator": delta,
            "new_weighted_numerator": totals[0], "vertex_penalty_numerator": penalties[0],
            "denominator": D, "strict_gap_numerator": gap,
            "strict_gap": str(Fraction(gap, D)),
            "positive_AP_weights": len(data["AP_weights"]),
            "positive_cover2_weights": len(cut_details),
            "positive_vertex_surcharges": len(data["surcharges"]),
            "checked_new_AP_instances": checks, "checked_new_incidences": 7*checks,
            "case_enumeration_required": False, "other_class_budget_required": False,
            "candidate_symmetry_assumed": False, "pole_colors_free": True,
            "solver_trusted": False, "new_W_bound": False, "attainability_claim": False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("certificate", type=Path)
    p.add_argument("--base", type=Path, required=True)
    p.add_argument("--base-checker", type=Path, required=True)
    p.add_argument("--expected", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    raw = args.certificate.read_bytes()
    out = check(json.loads(raw), args.base, args.base_checker)
    out["certificate_sha256"] = hashlib.sha256(raw).hexdigest()
    if args.expected:
        need(out == json.loads(args.expected.read_text()), "Expected checked result differs")
    if args.output:
        args.output.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out))


if __name__ == "__main__":
    main()
