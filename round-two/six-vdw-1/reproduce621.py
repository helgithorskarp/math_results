"""Complete finite audits for the period621 reduction (no solver required)."""
from collections import Counter
import json
import random
import resource
import sys
import time
from pathlib import Path
import fiber621 as enc
import audit621 as check


def main():
    began = time.monotonic()
    result = {"author": "six-vdw-1", "role": "researcher",
              "claim_status": "exact reduction and carry lemma", "period": 621}
    result["local"] = check.compare_local(enc.local_patterns)
    result["balance"] = check.balance_audit()
    result["controls"] = check.controls()
    squares = {x * x % 617 for x in range(1, 617)}
    baseline = "".join("1" if (x % 617 and x % 617 not in squares) or x == 3702 else "0"
                       for x in range(3703))
    result["baseline"] = check.check_coloring(baseline, 3703)
    results = []
    for name, tau in enc.skeletons():
        weighted = enc.edges(tau)
        direct = check.direct_edges(tau)
        check.require(weighted == direct, f"literal edge dictionary mismatch: {name}")
        check.require(sum(weighted.values()) == 190026, "static weight mismatch")
        check.require(len(weighted) >= 112608, "universal edge floor failed")
        orientation = [random.Random(1729 + i).randrange(2) for i in range(207)]
        word = enc.decode(tau, orientation)
        cost = enc.weighted_cost(weighted, orientation)
        pairs = check.cyclic_count(word)
        check.require(pairs == 2 * cost, "cost identity mismatch")
        entry = {"name": name, "edges": len(weighted),
                 "multiplicities": sorted(Counter(weighted.values()).items()),
                 "static_weight": sum(weighted.values()),
                 "dictionary_sha256": check.dictionary_digest(weighted),
                 "sample_weighted_cost": cost, "sample_cyclic_pairs": pairs}
        entry.update(check.support_and_carry_audit(tau))
        results.append(entry)
        print(json.dumps({"checked": name, "edges": len(weighted)}, sort_keys=True), flush=True)
    result["skeleton_checks"] = results
    result["elapsed_seconds"] = round(time.monotonic() - began, 6)
    result["max_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result["python_version"] = sys.version.split()[0]
    expected_path = Path(__file__).parent / "expected.json"
    if expected_path.exists():
        expected = json.loads(expected_path.read_text())
        stable = json.loads(json.dumps({key: value for key, value in result.items()
                                      if key not in ("elapsed_seconds", "max_rss_kib", "python_version")}))
        check.require(stable == expected, "compact expected results mismatch")
    output = Path(__file__).parent / "scratch" / "reproduction.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("VERIFIED_CARRY_REDUCTION_AND_FINITE_AUDITS", flush=True)


if __name__ == "__main__":
    main()
