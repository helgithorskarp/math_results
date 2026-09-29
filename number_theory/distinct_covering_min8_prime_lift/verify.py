"""Definition-level checker; independent of construct.py and any solver."""
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check_pairs(pairs, expected_minimum, expected_lcm):
    if not isinstance(pairs, list) or not pairs:
        raise ValueError("A nonempty congruence list is required")
    moduli = []
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("Each congruence must be [residue, modulus]")
        a, m = pair
        if type(a) is not int or type(m) is not int or m < 2 or not 0 <= a < m:
            raise ValueError("Invalid congruence")
        moduli.append(m)
    if len(set(moduli)) != len(moduli):
        raise ValueError("Repeated modulus")
    if min(moduli) != expected_minimum:
        raise ValueError("Incorrect exact minimum modulus")
    if math.lcm(*moduli) != expected_lcm:
        raise ValueError("Incorrect actual LCM")
    # Evaluate the congruence predicates directly, rather than mark progressions.
    multiplicities = [sum(x % m == a for a, m in pairs)
                      for x in range(expected_lcm)]
    if 0 in multiplicities:
        raise ValueError("An uncovered residue exists")
    return {
        "classes": len(pairs), "minimum_modulus": min(moduli),
        "lcm": expected_lcm, "uncovered": 0,
        "multiplicity_counts": {str(k): v for k, v in sorted(Counter(multiplicities).items())},
        "multiplicity_sha256": hashlib.sha256(bytes(multiplicities)).hexdigest(),
    }


def check_all():
    seed = json.loads((ROOT / "seed_m7.json").read_text())
    cover = json.loads((ROOT / "cover_m8.json").read_text())
    seed_result = check_pairs(seed["congruences"], 7, 10080)
    cover_result = check_pairs(cover["congruences"], 8, 70560)
    fixed = [pair for pair in seed["congruences"] if pair[1] != 7]
    if not all(pair in cover["congruences"] for pair in fixed):
        raise ValueError("The covering does not retain all designated classes")
    if math.lcm(*(m for a, m in fixed)) != 10080:
        raise ValueError("Wrong retained LCM")
    holes = [x for x in range(10080) if not any(x % m == a for a, m in fixed)]
    manifest = json.loads((ROOT / "capacity_manifest.json").read_text())
    if manifest["base_lcm"] != 10080 or manifest["base_holes"] != len(holes):
        raise ValueError("Wrong base-hole metadata")
    if [row["multiplier"] for row in manifest["rows"]] != list(range(1, 7)):
        raise ValueError("Incomplete multiplier enumeration")
    summaries = []
    used = {m for a, m in fixed}
    for row in manifest["rows"]:
        t, L = row["multiplier"], row["lcm"]
        if L != t * 10080:
            raise ValueError("Wrong proposed period")
        # A separate complete enumeration over integer d, not a divisor-pair generator.
        new_moduli = [d for d in range(8, L + 1) if L % d == 0 and d not in used]
        lifted = [h + k*10080 for k in range(t) for h in holes]
        capacities = []
        details = []
        for d in new_moduli:
            full_max = max(Counter(x % d for x in lifted).values())
            g = math.gcd(10080, d)
            w = max(Counter(x % g for x in holes).values())
            capacities.append(full_max)
            details.append([d, g, w, full_max])
        if details != row["capacities_d_g_w_C"]:
            raise ValueError("Entry-level capacity mismatch")
        if row["new_moduli"] != len(new_moduli) or row["hole_count"] != len(lifted):
            raise ValueError("Wrong row metadata")
        if row["capacity_sum"] != sum(capacities) or sum(capacities) >= len(lifted):
            raise ValueError("The strict capacity obstruction is not established")
        summaries.append({k: row[k] for k in
                          ["multiplier", "lcm", "new_moduli", "hole_count", "capacity_sum"]})
    return {"seed": seed_result, "cover": cover_result,
            "retained_classes": len(fixed), "retained_holes": len(holes),
            "fixed_seed_exclusions": summaries}


if __name__ == "__main__":
    result = check_all()
    expected = json.loads((ROOT / "expected.json").read_text())
    if result != expected:
        raise ValueError("Expected summary differs")
    print(json.dumps(result, sort_keys=True))
