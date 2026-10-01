"""Literal, producer-free certificate and six-point carrier verification."""
from collections import Counter
import hashlib
import itertools
import json
import resource
import time
from paths import BASE, WORK

def facts():
    start = time.monotonic()
    rows = []
    small_pairs = tuple(itertools.combinations(range(3), 2))
    for graph in range(8):
        edges = {frozenset(p) for i, p in enumerate(small_pairs) if graph >> i & 1}
        for subset in range(8):
            s = {x for x in range(3) if subset >> x & 1}
            pairs = {frozenset(p) for p in itertools.combinations(sorted(s), 2)}
            a = len(pairs & edges)
            b = len(pairs - edges)
            h = sum(all(frozenset((x, y)) in edges for y in range(3) if y != x) for x in s)
            low = sum(all(frozenset((x, y)) not in edges for y in range(3) if y != x) for x in set(range(3)) - s)
            slack = h + low - a + b
            if slack < 0:
                raise RuntimeError("false literal cut certificate")
            rows.append(dict(graph=graph, subset=subset, a=a, b=b, h=h, low=low, slack=slack))
    triples = tuple(itertools.combinations(range(6), 3))
    triple_index = {t: i for i, t in enumerate(triples)}
    pairs = tuple(itertools.combinations(range(6), 2))
    carrier = set()
    carrier_start = time.monotonic()
    for count, ids in enumerate(itertools.combinations(range(20), 8), 1):
        if count > 200000 or time.monotonic() - carrier_start > 10:
            raise RuntimeError("INCOMPLETE literal verifier carrier")
        blocks = tuple(triples[i] for i in ids)
        incidence = Counter(x for b in blocks for x in b)
        if any(incidence[x] != 4 for x in range(6)):
            continue
        pair_incidence = Counter(p for b in blocks for p in itertools.combinations(b, 2))
        if any(pair_incidence[p] > 3 for p in pairs):
            continue
        carrier.add(blocks)
    if count != 125970:
        raise RuntimeError("literal subset domain incomplete")
    permutations = tuple(itertools.permutations(range(6)))
    remaining = set(carrier)
    records = []
    compositions = 0
    def code(blocks):
        return sum(1 << triple_index[b] for b in blocks)
    pairs5 = tuple(itertools.combinations(range(5), 2))
    p5_index = {p: i for i, p in enumerate(pairs5)}
    while remaining:
        orbit_start = time.monotonic()
        blocks = min(remaining, key=code)
        orbit = set()
        automorphisms = set()
        for pi in permutations:
            image = tuple(sorted(tuple(sorted(pi[x] for x in b)) for b in blocks))
            orbit.add(image)
            if image == blocks:
                automorphisms.add(pi)
        if time.monotonic() - orbit_start > 10:
            raise RuntimeError("INCOMPLETE literal point-action case")
        if not orbit <= remaining or len(orbit) * len(automorphisms) != 720:
            raise RuntimeError("literal point-orbit or mass check failed")
        for a in automorphisms:
            for b in automorphisms:
                if tuple(a[b[x]] for x in range(6)) not in automorphisms:
                    raise RuntimeError("literal automorphism group is not closed")
                compositions += 1
        remaining -= orbit
        core_profile = []
        for x in range(6):
            others = sorted(set(range(6)) - {x})
            covered = {frozenset(set(b) - {x}) for b in blocks if x in b}
            missing = {frozenset(p) for p in itertools.combinations(others, 2)} - covered
            if len(missing) != 6 or any(all(frozenset(p) in missing for p in itertools.combinations(q, 2)) for q in itertools.combinations(others, 4)):
                raise RuntimeError("invalid six-edge literal link core")
            codes = []
            for images in itertools.permutations(range(5)):
                pi = dict(zip(others, images))
                codes.append(sum(1 << p5_index[tuple(sorted(pi[y] for y in edge))] for edge in missing))
            core_profile.append(min(codes))
        pair_count = Counter(p for b in blocks for p in itertools.combinations(b, 2))
        records.append(dict(family_code=code(blocks), blocks=blocks, orbit_size=len(orbit),
                            automorphism_order=len(automorphisms), pair_profile=sorted(pair_count[p] for p in pairs),
                            six_core_profile=sorted(core_profile)))
    records = json.loads(json.dumps(records))
    stream = "".join(str(c) + "\n" for c in sorted(map(code, carrier))).encode()
    return dict(literal_coefficients=rows, carrier_count=len(carrier), carrier_sha256=hashlib.sha256(stream).hexdigest(),
                classes=len(records), class_records=records, group_compositions=compositions,
                seconds=round(time.monotonic() - start, 6))

def audit(expected, truth):
    for key in ("literal_coefficients", "carrier_count", "carrier_sha256", "classes", "class_records"):
        if expected[key] != truth[key]:
            raise RuntimeError("certificate or complete carrier mismatch: " + key)
    if (expected["cut_inequality"] != "5q >= (s-6)(12-s)"
            or expected["k6_uncovered_triple_composition"] != [12,24,12,48]
            or expected["k6_original_word_composition"] != [4,24,36,8,0,0]
            or expected["global_interval"] != [69,72]
            or expected["code_realization_claimed"] or expected["ordinary_bridges_formalized"]
            or expected["independent_peer_review"]):
        raise RuntimeError("incorrect ordinary bridge summary or scope")

def main():
    truth = facts()
    expected = json.loads((BASE / "expected.json").read_text())
    audit(expected, truth)
    production = json.loads((WORK / "carrier_record.json").read_text())
    cut = json.loads((WORK / "cut_record.json").read_text())
    if (production["status"] != "COMPLETE" or cut["status"] != "COMPLETE"
            or production["carrier_sha256"] != truth["carrier_sha256"]
            or production["classification"]["records"] != truth["class_records"]
            or production["classification"]["labeled_carrier"] != truth["carrier_count"]
            or cut["literal_coefficients"] != truth["literal_coefficients"]):
        raise RuntimeError("producer records incomplete or inconsistent with independent literal facts")
    record = dict(agent="six-code-3", role="researcher", status="COMPLETE", literal_triple_cases=64,
                  complete_labeled_families=truth["carrier_count"], point_isomorphism_classes=truth["classes"],
                  literal_group_compositions=truth["group_compositions"], carrier_sha256=truth["carrier_sha256"],
                  seconds=truth["seconds"], maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  cut_inequality="5q >= (s-6)(12-s)", global_interval=[69,72], independent_peer_review=False)
    (WORK / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))

if __name__ == "__main__":
    main()
