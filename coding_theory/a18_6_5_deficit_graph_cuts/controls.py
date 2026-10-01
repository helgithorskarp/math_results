"""Reject corrupted proof fixtures and retain visible incomplete guards."""
import copy
import json
import resource
import time
import carrier
import verify
from paths import BASE, WORK

def main():
    start = time.monotonic()
    truth = verify.facts()
    expected = json.loads((BASE / "expected.json").read_text())
    verify.audit(expected, truth)
    mutations = []
    for key in ("carrier_sha256", "classes"):
        d = copy.deepcopy(expected); d[key] = "wrong"; mutations.append(d)
    d = copy.deepcopy(expected); d["literal_coefficients"][0]["slack"] += 1; mutations.append(d)
    d = copy.deepcopy(expected); d["class_records"][0]["automorphism_order"] = 9; mutations.append(d)
    d = copy.deepcopy(expected); d["class_records"][0]["blocks"][0] = [0,0,1]; mutations.append(d)
    d = copy.deepcopy(expected); d["k6_original_word_composition"][0] = 5; mutations.append(d)
    for bad in mutations:
        try:
            verify.audit(bad, truth)
        except RuntimeError:
            pass
        else:
            raise RuntimeError("corrupted fixture was accepted")
    invalid = [dict(node_cap=0), dict(node_cap=-1), dict(node_cap=True), dict(node_cap=200001),
               dict(seconds_cap=0), dict(seconds_cap=float("nan")), dict(seconds_cap=float("inf")), dict(seconds_cap=11)]
    for options in invalid:
        try:
            carrier.primary(**options)
        except ValueError:
            pass
        else:
            raise RuntimeError("invalid or escalated guard was accepted")
    for engine in (carrier.primary, carrier.literal):
        try:
            engine(node_cap=1)
        except carrier.Incomplete:
            pass
        else:
            raise RuntimeError("small-cap incomplete control did not fail visibly")
    record = dict(agent="six-code-3", role="researcher", status="COMPLETE", corruptions_rejected=len(mutations),
                  invalid_guards_rejected=len(invalid), visible_incomplete_guards=2,
                  seconds=round(time.monotonic() - start, 6), maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (WORK / "controls.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))

if __name__ == "__main__":
    main()
