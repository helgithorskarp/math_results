"""Rejection controls and an exhaustive small loss-rule check."""
import copy
import importlib.util
import itertools
import json
from pathlib import Path
import verify

HERE = Path(__file__).parent


def small_loss_rule():
    # Directly enumerate all subsets of three vertices that hit every AP
    # not covered by the removed point. These are the abstract triangle
    # petals {0,1},{1,2},{0,2}; the removed z is outside their screen.
    minima = []
    petals = [{0, 1}, {1, 2}, {0, 2}]
    for multiplicity in range(4):
        actual = [p | ({3} if i < multiplicity else set()) for i, p in enumerate(petals)]
        good = []
        for bits in range(8):
            h = {x for x in range(3) if bits >> x & 1}
            if all(3 in a or h & a for a in actual):
                good.append(len(h))
        minima.append(min(good))
    if minima != [2, 1, 1, 0]:
        raise ValueError("Direct loss-case minima disagree")
    return minima


def main():
    original = json.loads((HERE / "certificate.json").read_text())
    base, checker = HERE / "base/phase-269.json", HERE / "base/verify.py"
    good = verify.check(original, base, checker)
    mutations = []
    def add(name, mutate):
        changed = copy.deepcopy(original)
        mutate(changed)
        mutations.append((name, changed))
    add("missing_loss", lambda x: x.pop("worst_loss_numerator"))
    add("uncharged_AP_loss", lambda x: x.update(worst_loss_numerator=0))
    add("loss_understated", lambda x: x.update(worst_loss_numerator=x["worst_loss_numerator"]-1))
    add("loss_profile_not_complete", lambda x: x.update(loss_positions=[0]))
    add("hidden_chosen_edit", lambda x: x.update(chosen_z=0))
    add("supplied_partial_mask", lambda x: x.update(mask=[0]))
    add("wrong_phase", lambda x: x.update(phase=184))
    add("larger_class_cap", lambda x: x.update(class_cap=198))
    add("boolean_class_cap", lambda x: x.update(class_cap=True))
    add("wrong_fixed_base", lambda x: x.update(base_sha256="0"*64))
    add("negative_threshold", lambda x: x.update(threshold=-1))
    add("boolean_threshold", lambda x: x.update(threshold=True))
    add("screen_mask_overlap", lambda x: x.update(threshold=600000))
    add("zero_denominator", lambda x: x.update(denominator=0))
    add("invalid_capacity", lambda x: x.update(denominator=1))
    add("zero_AP_step", lambda x: x["AP_weights"][0].__setitem__(1, 0))
    add("out_of_range_AP", lambda x: x["AP_weights"][0].__setitem__(0, 3704))
    add("zero_AP_weight", lambda x: x["AP_weights"][0].__setitem__(2, 0))
    add("boolean_AP_weight", lambda x: x["AP_weights"][0].__setitem__(2, True))
    add("duplicated_AP", lambda x: x["AP_weights"].append(x["AP_weights"][0][:]))
    add("repeated_AP_in_triple", lambda x: x["cover2_weights"][0][0].__setitem__(1, x["cover2_weights"][0][0][0][:]))
    add("zero_triple_weight", lambda x: x["cover2_weights"][0].__setitem__(1, 0))
    add("duplicated_triple", lambda x: x["cover2_weights"].append(copy.deepcopy(x["cover2_weights"][0])))
    add("pole_or_wrong_color_AP", lambda x: x["AP_weights"].__setitem__(0, [349, 300, 1]))
    add("surcharge_outside_screen", lambda x: x["surcharges"].append([0, 1]))
    add("no_positive_proof", lambda x: x.update(AP_weights=[], cover2_weights=[], worst_loss_numerator=0))
    # Build an actual monochromatic triple with a shared screened position.
    raw = json.loads(base.read_text())
    loads = [0]*3704
    for a, d, w in raw["color0_APs"]:
        for j in range(7):
            loads[a+j*d] += w
    shared = {}
    for a, d, w in original["AP_weights"]:
        for j in range(7):
            xx = a+j*d
            if raw["denominator"]-loads[xx] <= good["other_edit_defect_slack_numerator"]:
                shared.setdefault(xx, []).append([a, d])
    paid_point, triple = next((x, row[:3]) for x, row in shared.items() if len(row) >= 3)
    add("unpaid_surcharge", lambda x: x["surcharges"].append([paid_point, 1000000]))
    add("nonempty_triple_common_intersection", lambda x: x["cover2_weights"][0].__setitem__(0, triple))
    rejected = []
    for name, changed in mutations:
        try:
            verify.check(changed, base, checker)
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
        else:
            raise ValueError("Accepted corrupted certificate: "+name)
    print(json.dumps({"agent": "six-vdw-3", "role": "researcher", "rejected_controls": len(rejected),
                      "names": rejected, "all_rejected": True, "small_loss_case_exact_minima": small_loss_rule()}))


if __name__ == "__main__":
    main()
