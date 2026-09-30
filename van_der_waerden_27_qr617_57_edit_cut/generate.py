#!/usr/bin/env python3
"""Generate 24 exact QR617 budget-box exclusions using fixed integer guides.

Python 3.11+ standard library, one process/thread. Discovery uses square lists
and bit masks. verify.py independently uses Euler's criterion and sets.
A stall or timeout is an incomplete attempt, never an exclusion.
"""
import argparse
import hashlib
import json
import resource
import time
from pathlib import Path

P = 617
N = 3703
LAST = N - 1
SQUARES = {x * x % P for x in range(1, P)}
COLOR = [int(x % P not in SQUARES) for x in range(N)]
VERTICES = [x for x in range(N) if x % P]
FULL = sum(1 << x for x in VERTICES)
ROOTS = {0: [1, 618, 1235, 1852, 2469, 3086],
         1: [3421, 3468, 3515, 3562, 3609, 3656]}
BOXES = {0: [(28, 28), (29, 27)], 1: [(28, 28), (27, 29)]}


def critical_progressions():
    edges = [[] for _ in range(N)]
    for d in range(1, LAST // 6 + 1):
        for a in range(N - 6 * d):
            points = [a + j * d for j in range(7)]
            if any(x % P == 0 for x in points):
                continue
            values = [COLOR[x] for x in points]
            total = sum(values)
            if total in (1, 6):
                v = points[values.index(int(total == 1))]
                edges[v].append((sum(1 << x for x in points if x != v), a, d))
    return edges


def select_witness(edges, count):
    """Find an empty petal or a greedy disjoint packing, without completeness."""
    for mask, a, d in edges:
        if mask == 0:
            return [[a, d]]
    if len(edges) < count:
        return None
    m = len(edges)
    conflicts = [0] * m
    for i in range(m):
        for j in range(i):
            if edges[i][0] & edges[j][0]:
                conflicts[i] |= 1 << j
                conflicts[j] |= 1 << i
    available = (1 << m) - 1
    selected = []
    while available:
        indices = []
        bits = available
        while bits:
            bit = bits & -bits
            indices.append(bit.bit_length() - 1)
            bits ^= bit
        i = min(indices, key=lambda i: (
            (conflicts[i] & available).bit_count(),
            edges[i][0].bit_count(), edges[i][2], edges[i][1]))
        selected.append([edges[i][1], edges[i][2]])
        if len(selected) == count:
            return selected
        available &= ~(conflicts[i] | (1 << i))
    return None


def check_time(start, seconds):
    if time.monotonic() - start > seconds:
        raise RuntimeError("Time limit: incomplete proof attempt, no exclusion established")


def containing(v):
    for j in range(7):
        for d in range(1, LAST // 6 + 1):
            a = v - j * d
            if 0 <= a and a + 6 * d <= LAST:
                points = [a + k * d for k in range(7)]
                if all(x % P for x in points):
                    yield a, d, points


def compile_guides(data):
    """Compile the supplied guides and their reflected APs, without solving LPs.

    Reflection applies to necessary clauses of the fixed prefix. It never
    restricts a candidate coloring. All conditions are checked again at use.
    """
    compiled = {}
    for tag, v, scale, triples in data["weighted_forbidden_guides"]:
        if tag != "w" or type(v) is not int or v not in VERTICES:
            raise ValueError("Invalid guide target")
        if type(scale) is not int or scale <= 0 or not triples:
            raise ValueError("Invalid guide scale or AP list")
        for reflected in (False, True):
            target = LAST - v if reflected else v
            terms = []
            for a, d, weight in triples:
                if not all(type(z) is int for z in (a, d, weight)) or weight <= 0:
                    raise ValueError("Noninteger or nonpositive guide term")
                start = LAST - (a + 6 * d) if reflected else a
                if start < 0 or d <= 0 or start + 6 * d > LAST:
                    raise ValueError("Guide AP outside prefix")
                points = [start + j * d for j in range(7)]
                if target not in points or any(x % P == 0 for x in points):
                    raise ValueError("Guide AP touches a pole or omits its target")
                negative = sum(1 << x for x in points if COLOR[x] == COLOR[target])
                positive = sum(1 << x for x in points if COLOR[x] != COLOR[target])
                terms.append((negative, positive, start, d, weight))
            compiled.setdefault(target, []).append((scale, terms))
    return compiled


def guided_witness(v, choices, allowed, forced, remaining):
    for scale, terms in choices:
        if sum(weight for _, _, _, _, weight in terms) <= remaining * scale:
            continue
        loads = {}
        valid = True
        for negative, positive, a, d, weight in terms:
            if negative & ~(forced | (1 << v)) or positive & forced:
                valid = False
                break
            mask = positive & allowed
            while mask:
                bit = mask & -mask
                mask ^= bit
                loads[bit] = loads.get(bit, 0) + weight
                if loads[bit] > scale:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            return scale, [[a, d, weight] for _, _, a, d, weight in terms]
    return None


def conditional_certificate(endpoint, root, budgets, critical, guides, seconds):
    allowed = FULL
    forced = 1 << root
    edges = [row.copy() for row in critical]
    active_seen = set()
    processed = set()
    mandatory = []
    records = []
    start = time.monotonic()
    for d in range(1, 618):
        old = [N - j * d for j in range(1, 7)]
        if all(0 <= x < N and x % P and COLOR[x] == endpoint for x in old):
            mandatory.append((sum(1 << x for x in old), N - 6 * d, d))

    def activate_forced():
        # A subset of necessary implications suffices. The independent
        # checker derives every used clause from its AP and the current T.
        for v in [z for z in VERTICES if forced & (1 << z) and z not in processed]:
            processed.add(v)
            mandatory.extend(critical[v])
            for a, d, points in containing(v):
                for side in (0, 1):
                    negative = [x for x in points if COLOR[x] == side]
                    if len(negative) < 2:
                        continue
                    positive = sum(1 << x for x in points if COLOR[x] != side)
                    if positive & forced:
                        continue
                    missing = [x for x in negative if not (forced & (1 << x))]
                    key = (a, d, side)
                    if len(missing) <= 1 and key not in active_seen:
                        active_seen.add(key)
                        if missing:
                            edges[missing[0]].append((positive, a, d))
                        else:
                            mandatory.append((positive, a, d))

    def finish(contradiction):
        return {"format": "qr617-weighted-conditional-color-budget-v1",
                "budget": budgets, "endpoint": endpoint, "root": root,
                "status": "EXCLUDED", "records": records,
                "contradiction": contradiction}

    while True:
        check_time(start, seconds)
        activate_forced()
        counts = [sum(bool(forced & (1 << v)) for v in VERTICES if COLOR[v] == c)
                  for c in (0, 1)]
        remaining = [budgets[c] - counts[c] for c in (0, 1)]
        if min(remaining) < 0:
            return finish({"reason": "too_many_forced"})
        unforced = allowed & ~forced
        required = []
        new_forced = {}
        for mask, a, d in mandatory:
            if mask & forced:
                continue
            masked = mask & unforced
            if masked == 0:
                return finish({"reason": "empty_required", "ap": [a, d]})
            if masked.bit_count() == 1:
                v = masked.bit_length() - 1
                new_forced.setdefault(v, ["t", v, a, d])
            required.append((masked, a, d))
        if new_forced:
            records.extend(new_forced.values())
            forced |= sum(1 << v for v in new_forced)
            continue
        exhausted = [c for c in (0, 1) if remaining[c] == 0 and
                     any(unforced & (1 << v) for v in VERTICES if COLOR[v] == c)]
        if exhausted:
            for c in exhausted:
                allowed &= ~sum(1 << v for v in VERTICES if
                                COLOR[v] == c and unforced & (1 << v))
                records.append(["budget", c])
            continue
        for c in (0, 1):
            clauses = [(m, a, d) for m, a, d in required if
                       COLOR[m.bit_length() - 1] == c]
            witness = select_witness(clauses, remaining[c] + 1)
            if witness is not None:
                return finish({"reason": "required_packing", "color": c, "aps": witness})
        for v in VERTICES:
            if forced & (1 << v) and v in guides:
                weight = guided_witness(v, guides[v], allowed, forced, remaining[1 - COLOR[v]])
                if weight is not None:
                    return finish({"reason": "required_weighted", "color": 1 - COLOR[v],
                                   "scale": weight[0], "aps": weight[1]})
        removed = []
        for v in VERTICES:
            check_time(start, seconds)
            if not (unforced & (1 << v)):
                continue
            candidates = [(mask & unforced, a, d) for mask, a, d in edges[v]
                          if not (mask & forced)]
            witness = select_witness(candidates, remaining[1 - COLOR[v]] + 1)
            if witness is not None:
                removed.append(v)
                records.append(["f", v, witness])
            elif v in guides:
                weight = guided_witness(v, guides[v], allowed, forced, remaining[1 - COLOR[v]])
                if weight is not None:
                    removed.append(v)
                    records.append(["w", v, weight[0], weight[1]])
        if not removed:
            raise RuntimeError(f"Branch {endpoint}/{root}/{budgets} stalled; no exclusion established")
        allowed &= ~sum(1 << v for v in removed)


def write_certificate(directory, name, data):
    raw = (json.dumps(data, separators=(",", ":")) + "\n").encode()
    target = directory / name
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(target)
    return {"file": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("build"))
    parser.add_argument("--seconds-per-case", type=float, default=90)
    parser.add_argument("--resume", action="store_true",
                        help="Reuse existing completed files; verify.py must still check every file")
    args = parser.parse_args()
    if not 0 < args.seconds_per_case <= 90:
        parser.error("seconds-per-case must be positive and at most 90")
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    guide_raw = (Path(__file__).resolve().parent / "weight_guides.json").read_bytes()
    guides = compile_guides(json.loads(guide_raw))
    critical = critical_progressions()
    manifest = []
    for endpoint, roots in ROOTS.items():
        for a, b in BOXES[endpoint]:
            for root in roots:
                case_start = time.monotonic()
                name = f"branch-{endpoint}-{root}-{a}-{b}.json"
                if (args.output / name).exists():
                    if not args.resume:
                        raise RuntimeError(f"Refusing to overwrite {name}; choose a new output directory")
                    raw = (args.output / name).read_bytes()
                    cached = json.loads(raw)
                    if not (cached.get("status") == "EXCLUDED" and cached.get("budget") == [a, b]
                            and cached.get("endpoint") == endpoint and cached.get("root") == root):
                        raise RuntimeError(f"Incomplete or mismatched cache {name}")
                    item = {"file": name, "bytes": len(raw),
                            "sha256": hashlib.sha256(raw).hexdigest()}
                    manifest.append(item)
                    print(json.dumps({**item, "cached_unverified": True}, sort_keys=True), flush=True)
                    continue
                data = conditional_certificate(endpoint, root, [a, b], critical,
                                               guides, args.seconds_per_case)
                item = write_certificate(args.output, name, data)
                manifest.append(item)
                print(json.dumps({**item, "seconds": round(time.monotonic() - case_start, 3)},
                                 sort_keys=True), flush=True)
    write_certificate(args.output, "manifest.json", {"certificates": manifest})
    print(json.dumps({"generated": len(manifest), "seconds": round(time.monotonic() - start, 3),
                      "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      "guide_sha256": hashlib.sha256(guide_raw).hexdigest(),
                      "compiled_guides": sum(map(len, guides.values()))}, sort_keys=True))


if __name__ == "__main__":
    main()
