"""Complete necessary covered-triple carrier on a six-point deficit component."""
from pathlib import Path
import hashlib
import itertools
import json
import math
import resource
import time

from paths import WORK
ROOT = WORK
TRIPLES = tuple(itertools.combinations(range(6), 3))
INDEX = {t: i for i, t in enumerate(TRIPLES)}
MASKS = tuple(sum(1 << x for x in t) for t in TRIPLES)
PAIRS = tuple(itertools.combinations(range(6), 2))
P_INDEX = {p: i for i, p in enumerate(PAIRS)}
TRIPLE_PAIRS = tuple(tuple(P_INDEX[p] for p in itertools.combinations(t, 2)) for t in TRIPLES)
NODE_CAP = 200000
SECONDS_CAP = 10

class Incomplete(RuntimeError):
    pass

def primary(node_cap=NODE_CAP, seconds_cap=SECONDS_CAP):
    if type(node_cap) is not int or not 0 < node_cap <= NODE_CAP or type(seconds_cap) not in (int, float) or not math.isfinite(seconds_cap) or not 0 < seconds_cap <= SECONDS_CAP:
        raise ValueError("invalid carrier guard")
    start = time.monotonic()
    nodes = 0
    output = set()
    def visit(need, pair_count, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap or time.monotonic() - start > seconds_cap:
            raise Incomplete("primary covered-triple carrier exceeded its fixed guard")
        active = [x for x in range(6) if need[x]]
        if not active:
            if len(chosen) != 8:
                raise RuntimeError("wrong block count at a full degree cover")
            family = sum(1 << i for i in chosen)
            if family in output:
                raise RuntimeError("point-star recursion repeated a family")
            output.add(family)
            return
        point = active[0]
        candidates = [i for i, t in enumerate(TRIPLES) if point in t and all(need[x] for x in t)]
        for star in itertools.combinations(candidates, need[point]):
            after = list(need)
            pairs = list(pair_count)
            for i in star:
                for x in TRIPLES[i]:
                    after[x] -= 1
                for j in TRIPLE_PAIRS[i]:
                    pairs[j] += 1
            if min(after) < 0 or max(pairs) > 3:
                continue
            if after[point] != 0:
                raise RuntimeError("the chosen whole point-star is not complete")
            visit(tuple(after), tuple(pairs), chosen + star)
    visit((4,) * 6, (0,) * 15, ())
    return output, {"status": "COMPLETE", "nodes": nodes, "seconds": round(time.monotonic() - start, 6)}

def literal(node_cap=NODE_CAP, seconds_cap=SECONDS_CAP):
    if type(node_cap) is not int or not 0 < node_cap <= NODE_CAP or type(seconds_cap) not in (int, float) or not math.isfinite(seconds_cap) or not 0 < seconds_cap <= SECONDS_CAP:
        raise ValueError("invalid carrier guard")
    start = time.monotonic()
    output = set()
    nodes = 0
    for chosen in itertools.combinations(range(20), 8):
        nodes += 1
        if nodes > node_cap or time.monotonic() - start > seconds_cap:
            raise Incomplete("literal eight-subset carrier exceeded its fixed guard")
        blocks = [set(TRIPLES[i]) for i in chosen]
        if any(sum(x in b for b in blocks) != 4 for x in range(6)):
            continue
        if any(sum(set(p) <= b for b in blocks) > 3 for p in PAIRS):
            continue
        output.add(sum(1 << i for i in chosen))
    return output, {"status": "COMPLETE", "subsets_checked": nodes, "seconds": round(time.monotonic() - start, 6)}

def permute(family, point_map):
    result = 0
    for i, t in enumerate(TRIPLES):
        if family >> i & 1:
            result |= 1 << INDEX[tuple(sorted(point_map[x] for x in t))]
    return result

def core_code(family, center):
    others = tuple(x for x in range(6) if x != center)
    edges = tuple(p for p in itertools.combinations(others, 2) if not (family >> INDEX[tuple(sorted((center,) + p))] & 1))
    edge_index = {p: i for i, p in enumerate(itertools.combinations(range(5), 2))}
    code = min(sum(1 << edge_index[tuple(sorted((mapping[others.index(a)], mapping[others.index(b)])))] for a, b in edges)
               for mapping in itertools.permutations(range(5)))
    if len(edges) != 6 or any(all(p in edges for p in itertools.combinations(q, 2)) for q in itertools.combinations(others, 4)):
        raise RuntimeError("a necessary six-edge high core is invalid")
    return code

def classify(carrier):
    start = time.monotonic()
    group = tuple(itertools.permutations(range(6)))
    generators = []
    for i in range(5):
        m = list(range(6)); m[i], m[i + 1] = m[i + 1], m[i]; generators.append(tuple(m))
    remaining = set(carrier)
    cases = []
    while remaining:
        case_start = time.monotonic()
        representative = min(remaining)
        orbit = {representative}
        todo = [representative]
        while todo:
            if len(orbit) > NODE_CAP or time.monotonic() - case_start > SECONDS_CAP:
                raise Incomplete("joint triple orbit exceeded its fixed guard")
            f = todo.pop()
            for g in generators:
                image = permute(f, g)
                if image not in carrier:
                    raise RuntimeError("point action left the literal carrier")
                if image not in orbit:
                    orbit.add(image); todo.append(image)
        full = {permute(representative, g) for g in group}
        automorphisms = [g for g in group if permute(representative, g) == representative]
        if orbit != full or not orbit <= remaining or len(orbit) * len(automorphisms) != 720:
            raise RuntimeError("full literal map and generator orbit checks disagree")
        remaining -= orbit
        blocks = [TRIPLES[i] for i in range(20) if representative >> i & 1]
        pair_profile = sorted(sum(set(p) <= set(t) for t in blocks) for p in PAIRS)
        core_profile = sorted(core_code(representative, x) for x in range(6))
        cases.append({"family_code": representative, "blocks": blocks, "orbit_size": len(orbit),
                      "automorphism_order": len(automorphisms), "pair_profile": pair_profile,
                      "six_core_profile": core_profile})
    return {"status": "COMPLETE", "classes": len(cases), "labeled_carrier": len(carrier),
            "records": cases, "seconds": round(time.monotonic() - start, 6)}

def main():
    start = time.monotonic()
    output = ROOT / "carrier_record.json"
    output.write_text(json.dumps({"agent": "six-code-3", "role": "researcher", "status": "INCOMPLETE"}) + "\n")
    a, a_record = primary()
    b, b_record = literal()
    if a != b:
        raise RuntimeError("complete actual necessary carriers differ entry by entry")
    classes = classify(a)
    stream = "".join(str(x) + "\n" for x in sorted(a)).encode()
    record = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE",
              "scope": "Necessary six-point covered-triple family only; no code realization or global72 exclusion implied",
              "primary": a_record, "literal": b_record, "classification": classes,
              "carrier_sha256": hashlib.sha256(stream).hexdigest(), "guards": [NODE_CAP, SECONDS_CAP],
              "seconds": round(time.monotonic() - start, 6), "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "ordinary_bridge_formalized": False, "independent_peer_review": False}
    output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))

if __name__ == "__main__":
    main()
