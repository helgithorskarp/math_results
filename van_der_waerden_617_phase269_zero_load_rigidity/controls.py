"""Test the support/cover hypotheses and exact weighted contradiction."""
from copy import deepcopy
import json
from pathlib import Path
import verify

HERE = Path(__file__).parent


def main():
    original = json.loads((HERE / "certificate.json").read_text())
    outcomes = []

    def reject(name, mutate, message):
        data = deepcopy(original)
        mutate(data)
        try:
            verify.check(data, HERE / "base/phase-269.json", HERE / "base/verify.py")
        except ValueError as exc:
            if message not in str(exc):
                raise AssertionError(f"{name}: unexpected rejection {exc}") from exc
            outcomes.append({"control": name, "reason": str(exc)})
        else:
            raise AssertionError(f"{name}: invalid certificate accepted")

    reject("larger class budget", lambda d: d.update({"class_cap": 198}), "frontier")
    reject("boolean class budget", lambda d: d.update({"class_cap": True}), "frontier")
    reject("wrong phase", lambda d: d.update({"phase": 205}), "frontier")
    reject("wrong base bytes", lambda d: d.update({"base_sha256": "0"*64}), "Base bytes")
    reject("supplied zero subset", lambda d: d.update({"zero_points": [50]}), "schema")
    reject("hidden forced-point condition", lambda d: d.update({"forced_zero": 50}), "schema")
    reject("zero denominator", lambda d: d.update({"denominator": 0}), "Positive integer denominator")
    reject("boolean denominator", lambda d: d.update({"denominator": True}), "Positive integer denominator")
    reject("zero AP difference", lambda d: d["AP_weights"][0].__setitem__(1, 0), "Actual AP integers")
    reject("out of range AP", lambda d: d["AP_weights"][0].__setitem__(0, -1), "Actual crossing coordinates")
    reject("boolean AP weight", lambda d: d["AP_weights"][0].__setitem__(2, True), "AP row")
    reject("negative AP weight", lambda d: d["AP_weights"][0].__setitem__(2, -1), "Positive unique AP")
    reject("duplicate AP", lambda d: d["AP_weights"].append(d["AP_weights"][0]), "Positive unique AP")
    reject("AP through a pole", lambda d: d["AP_weights"].append([349, 251, 1]), "Actual monochromatic nonpole AP")
    reject("unrepaired capacity overload", lambda d: d["AP_weights"][0].__setitem__(2, 100_000_000), "Exact screened point capacity")
    reject("missing cover-two rows", lambda d: d.update({"cover2_weights": []}), "No strict uniform")
    reject("duplicate triple AP", lambda d: d["cover2_weights"][0][0].__setitem__(1, d["cover2_weights"][0][0][0]), "Three distinct unique APs")
    reject("negative triple weight", lambda d: d["cover2_weights"][0].__setitem__(1, -1), "Positive triple weight")
    reject("duplicate cut", lambda d: d["cover2_weights"].append(d["cover2_weights"][0]), "Three distinct unique APs")

    base = json.loads((HERE / "base/phase-269.json").read_text())
    load = [0]*3704
    for a, step, w in base["color0_APs"]:
        for j in range(7):
            load[a+j*step] += w
    delta = 196*base["denominator"]-sum(w for a, step, w in base["color0_APs"])
    incidence = {}
    for a, step, w in original["AP_weights"]:
        for j in range(7):
            x = a+j*step
            if base["denominator"]-load[x] <= delta:
                incidence.setdefault(x, []).append([a, step])
    shared = next(x for x, aps in sorted(incidence.items()) if len(aps) >= 3)
    triple = incidence[shared][:3]
    reject("three petals with a common point", lambda d: d["cover2_weights"][0].__setitem__(0, triple), "Nonempty petals and empty common intersection")
    reject("surcharge outside screen", lambda d: d.update({"surcharges": [[-1, 1]]}), "Eligible unique positive surcharge")
    reject("negative surcharge", lambda d: d.update({"surcharges": [[shared, -1]]}), "Eligible unique positive surcharge")
    reject("surcharge penalty removes gap", lambda d: d.update({"surcharges": [[shared, 1_000_000_000]]}), "No strict uniform")

    # Find an actual original monochromatic AP meeting a zero-load point.
    # It cannot be used in the uniform H-cover, although it is a valid AP.
    squares = {r*r % 617 for r in range(1, 617)}
    colors = []
    for x in range(3704):
        r = (x-1852+(269 if x < 1852 else 349)) % 617
        colors.append(-1 if r == 0 else int(r not in squares) ^ int(x >= 1852))
    unsafe = next([a, step, 1] for step in range(1, 618)
                  for a in range(max(0, 1852-6*step), min(1852, 3704-6*step))
                  if all(colors[a+j*step] == 0 for j in range(7))
                  and any(load[a+j*step] == 0 for j in range(7)))
    reject("valid AP meets the zero-load set", lambda d: d["AP_weights"].insert(0, unsafe), "AP must avoid ALL base zero-load points")

    print(json.dumps({"agent": "six-vdw-3", "role": "researcher", "rejected_controls": len(outcomes),
                      "all_rejected": True, "outcomes": outcomes}))


if __name__ == "__main__":
    main()
