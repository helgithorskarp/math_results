"""Scalar and Huffman replay; imports neither profile.py nor anchors.py."""

from copy import deepcopy
import hashlib
import heapq
import importlib.util
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent
SIZES = (0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39)
ORDER = ("one_minimum", "one_maximum", "two_minima", "two_maxima", "mixed_pair")


def require(test, message):
    if not test:
        raise ValueError(message)


def check_certificate(expected, candidate):
    require(expected == candidate, "certificate differs from scalar/Huffman replay")


def digest(obj):
    raw = json.dumps(obj, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def integer_ceiling(x):
    power = 0
    while pow(2, power) < x:
        power += 1
    return power


def huffman(labels):
    heap = list(labels)
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, 1 + max(a, b))
    return heap[0]


def reconstruct_cuts(scalar, n, gates, final):
    cuts = [{} for _ in range(len(gates) + 1)]
    for name, data in final.items():
        histories = [[] for _ in cuts]
        for lm, hm, final_lo, final_hi, final_d, final_r, redundant in data["records"]:
            values = [0] * n
            lows = [i for i in range(n) if lm & pow(2, i)]
            highs = [i for i in range(n) if hm & pow(2, i)]
            for j, i in enumerate(lows):
                values[i] = j - len(lows)
            for j, i in enumerate(highs):
                values[i] = 2 + j
            d = r = rmask = 0
            for cut in range(len(gates) + 1):
                lo, hi = scalar.positions(values)
                histories[cut].append([lm, hm, lo, hi, d, r, rmask])
                if cut == len(gates):
                    require((lo, hi, d, r) == (final_lo, final_hi, final_d, final_r),
                            "prefix reconstruction differs from scalar enumeration")
                    break
                a, b = gates[cut]
                x, y = values[a], values[b]
                touched = x not in (0, 1) or y not in (0, 1)
                inactive = bool(redundant & pow(2, cut))
                require(not (touched and inactive), "one gate charged twice")
                d += int(touched)
                r += int(inactive)
                if inactive:
                    rmask += pow(2, cut)
                if x > y:
                    values[a], values[b] = y, x
        for cut, rows in enumerate(histories):
            rows.sort()
            summary, envelope = scalar.scalar_summary(rows)
            cuts[cut][name] = {"low_count": data["low_count"],
                               "high_count": data["high_count"],
                               "records": rows, "summary": summary, "envelope": envelope}
    return cuts


def independent_aggregate(n, data, side, semantic=True):
    pos = 0 if side == "low" else 1
    count = "low_count" if side == "low" else "high_count"
    unary = "one_minimum" if side == "low" else "one_maximum"
    live = sorted({row[2 + pos].bit_length() - 1 for row in data[unary]["records"]})
    selected = [(name, data[name]) for name in ORDER if data[name][count]]
    base = min(SIZES[n - item["low_count"] - item["high_count"]] for _, item in selected)
    labels, result = [], []
    for p in live:
        masses, options = {}, []
        for name, item in selected:
            classes = {}
            for row in item["records"]:
                if row[2 + pos] & pow(2, p):
                    pair = row[2], row[3]
                    cost = row[4] + row[5] if semantic else row[4]
                    classes[pair] = max(classes.get(pair, 0), cost)
            mass = sum(pow(2, cost) for cost in classes.values())
            masses[name] = mass
            if mass:
                options.append(SIZES[n - item["low_count"] - item["high_count"]]
                               + integer_ceiling(mass))
        label = max(options)
        labels.append(label)
        result.append({"port": p, "anchored_masses": masses,
                       "label": label, "units": pow(2, label - base)})
    return {"base": base, "normalized_mass": sum(x["units"] for x in result),
            "lower_bound": huffman(labels), "rows": result}


def boolean_replay(n, gates):
    activity = [None for _ in gates]
    failures, wrong = [], 0
    for mask in range(1 << n):
        values = [int(bool(mask & pow(2, i))) for i in range(n)]
        target = sorted(values)
        for j, (a, b) in enumerate(gates):
            if values[a] > values[b]:
                if activity[j] is None:
                    activity[j] = mask
                values[a], values[b] = values[b], values[a]
        if values != target:
            failures.append(mask)
        wrong += sum(x != y for x, y in zip(values, target))
    return {"failure_count": len(failures), "wrong_output_bits": wrong,
            "failures_sha256": digest(failures),
            "failures": failures if len(failures) <= 100 else None,
            "activity_witnesses": activity}


def local_anchor_audit():
    tested = 0
    for n in range(2, 7):
        words = list(product(range(3), repeat=n))
        for a in range(n):
            for b in range(n):
                if a == b:
                    continue
                for wanted in (0, 2):
                    for p in range(n):
                        target = (a if wanted == 0 else b) if p in (a, b) else p
                        fibres = {}
                        for word in words:
                            if word[p] != wanted:
                                continue
                            out = list(word)
                            out[a], out[b] = min(word[a], word[b]), max(word[a], word[b])
                            require(out[target] == wanted, "anchor absent after comparator")
                            charge = word[a] != 1 or word[b] != 1
                            fibres.setdefault(tuple(out), []).append(charge)
                            tested += 1
                        for charges in fibres.values():
                            if p in (a, b):
                                require(len(charges) == 1 and all(charges),
                                        "charged anchored map is not injective")
                            else:
                                require(len(charges) <= 2, "unanchored fibre too large")
                                if len(charges) == 2:
                                    require(all(charges), "uncharged double fibre")
    return tested


def main():
    start = time.monotonic()
    fixture = json.loads((ROOT / "anchor-fixture.json").read_text())
    require(hashlib.sha256((ROOT / "verify.py").read_bytes()).hexdigest() ==
            fixture["source_context"]["scalar_checker_sha256"], "scalar source changed")
    spec = importlib.util.spec_from_file_location("scalar_extreme_checker", ROOT / "verify.py")
    scalar = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scalar)
    raw = (ROOT / "anchor-certificate.json").read_bytes()
    certificate = json.loads(raw)
    expected = {"schema": "sorting-semantic-anchor-huffman-v1",
                "agent": "six-sorting-2", "role": "researcher", "cases": {}}
    assignments = evaluations = boolean_inputs = transported = 0
    for case in fixture["cases"]:
        n, gates, size = case["n"], case["gates"], case["profile_size"]
        require(2 <= n <= 13 and 0 <= size <= len(gates), "invalid dimensions")
        require(all(0 <= a < n and 0 <= b < n and a != b for a, b in gates), "invalid gate")
        final = {}
        for name, l, h in scalar.FAMILIES:
            data, counted, worked = scalar.scalar_family(n, gates[:size], l, h)
            final[name] = data
            assignments += counted
            evaluations += worked
        cuts = reconstruct_cuts(scalar, n, gates[:size], final)
        if case["name"] == "strict_semantic":
            sources = sum(pow(2, i) for i in (0, 6, 7))
            blocked_highs = pow(2, 10) + pow(2, 12)
            blocked_lows = pow(2, 4) + blocked_highs
            for name, item in final.items():
                for row in item["records"]:
                    lm, hm = row[:2]
                    if name == "one_maximum":
                        redundant = bool(hm & sources)
                    elif name == "two_maxima":
                        redundant = bool(hm & sources) and not bool(hm & blocked_highs)
                    elif name == "mixed_pair":
                        redundant = bool(hm & sources) and not bool(lm & blocked_lows)
                    else:
                        redundant = False
                    require(row[5] == int(redundant) and row[6] == (128 if redundant else 0),
                            "analytic redundancy characterization differs")
        semantic_profiles = [{side: independent_aggregate(n, cut, side)
                              for side in ("low", "high")} for cut in cuts]
        trace = [{"cut": i, "low": pair["low"]["normalized_mass"],
                  "high": pair["high"]["normalized_mass"], "base": pair["low"]["base"]}
                 for i, pair in enumerate(semantic_profiles)]
        first = previous = None
        for i, pair in enumerate(semantic_profiles):
            for side in ("low", "high"):
                value = pair[side]
                if value["lower_bound"] > case["budget"] and first is None:
                    first = {"cut": i, "direction": side, "normalized_mass": value["normalized_mass"],
                             "base": value["base"], "lower_bound": value["lower_bound"]}
                if i:
                    a, b = gates[i - 1]
                    old = semantic_profiles[i - 1][side]
                    label_at = {row["port"]: row["label"] for row in value["rows"]}
                    for row in old["rows"]:
                        p = row["port"]
                        hit = p in (a, b)
                        q = (a if side == "low" else b) if hit else p
                        require(label_at[q] >= row["label"] + int(hit), "anchor transport failed")
                        transported += 1
                    require(value["normalized_mass"] >= old["normalized_mass"], "aggregate decreased")
            for name in ORDER:
                item = cuts[i][name]
                mass = item["summary"]["semantic_mass"]
                lower = SIZES[n - item["low_count"] - item["high_count"]] + integer_ceiling(mass)
                require(lower <= max(x["lower_bound"] for x in pair.values()), "base profile not dominated")
                if lower > case["budget"] and previous is None:
                    previous = {"cut": i, "family": name, "mass": mass, "lower_bound": lower}
        families = {name: {"low_count": data["low_count"], "high_count": data["high_count"],
                           "envelope": data["envelope"], "summary": data["summary"],
                           "records_sha256": digest(data["records"]),
                           "mass_trace": [[x["ordinary_mass"], x["semantic_mass"]] for x in data["trace"]]}
                    for name, data in final.items()}
        boolean = boolean_replay(n, gates)
        boolean_inputs += 1 << n
        if case["kind"] == "active_prefix":
            require(all(x is not None for x in boolean["activity_witnesses"]), "inactive witness gate")
        if case["kind"] == "sorter":
            require(boolean["failure_count"] == 0 and first is None, "positive control rejected")
        if case["kind"] == "invalid_candidate":
            peer = case["peer_boolean"]
            require(boolean["failures"] == peer["failures"] and
                    boolean["wrong_output_bits"] == peer["wrong_output_bits"], "peer Boolean mismatch")
            require(previous == case["peer_previous_rejection"], "peer previous rejection mismatch")
        expected["cases"][case["name"]] = {
            "n": n, "size": len(gates), "profile_size": size, "families": families,
            "semantic_anchors": semantic_profiles[-1],
            "ordinary_anchors": {side: independent_aggregate(n, cuts[-1], side, False)
                                 for side in ("low", "high")},
            "anchor_trace": trace, "first_rejection": first,
            "previous_first_rejection": previous, "boolean": boolean}
    check_certificate(expected, certificate)
    witness = expected["cases"]["strict_semantic"]
    require(witness["first_rejection"]["cut"] == 8 and
            witness["semantic_anchors"]["high"]["normalized_mass"] == 544 and
            witness["ordinary_anchors"]["high"]["normalized_mass"] == 512 and
            witness["previous_first_rejection"] is None, "strict refinement lost")
    peer = expected["cases"]["peer_unweighted-fitness"]
    require(peer["first_rejection"]["cut"] == 15 and
            peer["first_rejection"]["normalized_mass"] == 640, "early peer rejection lost")
    relabeled = expected["cases"]["relabeled_strict_semantic"]
    require(witness["anchor_trace"] == relabeled["anchor_trace"], "oriented relabelling differs")
    corruptions = []
    bad = deepcopy(certificate)
    bad["cases"]["strict_semantic"]["semantic_anchors"]["high"]["rows"][5]["units"] = 32
    corruptions.append(bad)
    bad = deepcopy(certificate)
    bad["cases"]["strict_semantic"]["semantic_anchors"]["high"]["rows"].pop()
    corruptions.append(bad)
    bad = deepcopy(certificate)
    bad["cases"]["strict_semantic"]["first_rejection"]["lower_bound"] = 44
    corruptions.append(bad)
    for bad in corruptions:
        try:
            check_certificate(expected, bad)
        except ValueError:
            pass
        else:
            raise ValueError("altered certificate accepted")
    combinations_checked = 0
    for count in range(1, 9):
        for labels in combinations_with_replacement(range(6), count):
            require(huffman(labels) == integer_ceiling(sum(pow(2, x) for x in labels)),
                    "Huffman and dyadic capacity differ")
            combinations_checked += 1
    local_tests = local_anchor_audit()
    print(json.dumps({"status": "ALL_ANCHOR_CHECKS_PASSED", "agent": "six-sorting-2",
                      "role": "researcher", "python": sys.version.split()[0],
                      "scalar_free_assignments": assignments, "scalar_gate_evaluations": evaluations,
                      "full_boolean_inputs": boolean_inputs, "checked_anchor_transports": transported,
                      "local_anchor_configurations": local_tests, "huffman_multisets": combinations_checked,
                      "corruptions_rejected": len(corruptions),
                      "certificate_sha256": hashlib.sha256(raw).hexdigest(),
                      "seconds": round(time.monotonic() - start, 3),
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == "__main__":
    main()
