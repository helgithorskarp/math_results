#!/usr/bin/env python3
"""Generate exact QR617 edit-region certificates using mixed AP clauses.

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
BOXES = {0: [(27, 1848), (1848, 27), (29, 29)],
         1: [(27, 1848), (1848, 27), (29, 29)]}


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


def containing(v):
    for j in range(7):
        for d in range(1, LAST // 6 + 1):
            a = v - j * d
            if 0 <= a and a + 6 * d <= LAST:
                points = [a + k * d for k in range(7)]
                if all(x % P for x in points):
                    yield a, d, points


def conditional_certificate(endpoint, root, budgets, critical, seconds, initial=None):
    """Search for a proof, retaining valid records if the attempt is incomplete.

    This is not exhaustive search. Completeness is supplied only by the
    independently verified final contradiction and the endpoint/root cover.
    """
    allowed = FULL if initial is None else sum(1 << v for v in initial["allowed_positions"])
    forced = 1 << root if initial is None else sum(1 << v for v in initial["forced_positions"])
    records = [] if initial is None else initial["records"].copy()
    edges = [row.copy() for row in critical]
    active_seen = set()
    processed = set()
    mandatory = []
    start = time.monotonic()
    for d in range(1, 618):
        old = [N - j * d for j in range(1, 7)]
        if all(0 <= x < N and x % P and COLOR[x] == endpoint for x in old):
            mandatory.append((sum(1 << x for x in old), N - 6 * d, d))

    def activate_forced():
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

    def finish(status, contradiction=None):
        return {"format": "qr617-mixed-conditional-color-budget-v1", "budget": budgets,
                "endpoint": endpoint, "root": root, "status": status,
                "records": records, "contradiction": contradiction or {}}

    while True:
        if time.monotonic() - start > seconds:
            return finish("INCOMPLETE_TIME_LIMIT")
        activate_forced()
        counts = [sum(bool(forced & (1 << v)) for v in VERTICES if COLOR[v] == c)
                  for c in (0, 1)]
        remaining = [budgets[c] - counts[c] for c in (0, 1)]
        if min(remaining) < 0:
            return finish("EXCLUDED", {"reason": "too_many_forced"})
        unforced = allowed & ~forced
        required = []
        new_forced = {}
        for mask, a, d in mandatory:
            if mask & forced:
                continue
            masked = mask & unforced
            if masked == 0:
                return finish("EXCLUDED", {"reason": "empty_required", "ap": [a, d]})
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
        required_by_color = [[(m, a, d) for m, a, d in required
                              if COLOR[m.bit_length() - 1] == c] for c in (0, 1)]
        for c in (0, 1):
            witness = select_witness(required_by_color[c], remaining[c] + 1)
            if witness is not None:
                return finish("EXCLUDED", {"reason": "required_packing", "color": c,
                                           "aps": witness})
        removed = []
        for v in VERTICES:
            if time.monotonic() - start > seconds:
                return finish("INCOMPLETE_TIME_LIMIT")
            if not (unforced & (1 << v)):
                continue
            candidates = [(mask & unforced, a, d) for mask, a, d in edges[v]
                          if not (mask & forced)]
            opposite = 1 - COLOR[v]
            witness = select_witness(candidates, remaining[opposite] + 1)
            if witness is not None:
                removed.append(v)
                records.append(["f", v, witness])
            else:
                # Under v in S, already mandatory clauses are still required.
                # Their APs can omit v. They use the same opposite-color budget.
                witness = select_witness(candidates + required_by_color[opposite],
                                         remaining[opposite] + 1)
                if witness is not None:
                    removed.append(v)
                    records.append(["m", v, witness])
        if not removed:
            return finish("STALLED")
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
                        help="Independently recheck cached proofs or resume checked partial states")
    args = parser.parse_args()
    if not 0 < args.seconds_per_case <= 90:
        parser.error("seconds-per-case must be positive and at most90")
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    critical = critical_progressions()
    manifest = []
    branch_timings = []
    for endpoint, roots in ROOTS.items():
        for a, b in BOXES[endpoint]:
            for root in roots:
                name = f"branch-{endpoint}-{root}-{a}-{b}.json"
                initial = None
                target = args.output / name
                if target.exists():
                    if not args.resume:
                        raise RuntimeError(f"Refusing to overwrite {name}; use another output directory")
                    import verify
                    cached = json.loads(target.read_text())
                    if not (cached.get("budget") == [a, b] and cached.get("endpoint") == endpoint
                            and cached.get("root") == root):
                        raise ValueError(f"Mismatched cached branch {name}")
                    if cached.get("status") == "EXCLUDED":
                        verify.verify_branch(cached)
                        raw = target.read_bytes()
                        manifest.append({"file": name, "bytes": len(raw),
                                         "sha256": hashlib.sha256(raw).hexdigest()})
                        print(json.dumps({"file": name, "cached_and_verified": True}), flush=True)
                        continue
                    state = verify.verify_branch(cached, complete=False, include_state=True)
                    initial = {**state, "records": cached["records"]}
                case_start = time.monotonic()
                data = conditional_certificate(endpoint, root, [a, b], critical,
                                               args.seconds_per_case, initial)
                item = write_certificate(args.output, name, data)
                branch_timings.append({"file": name, "seconds": round(time.monotonic() - case_start, 3),
                                       "status": data["status"]})
                manifest.append(item)
                print(json.dumps({**item, **branch_timings[-1]}, sort_keys=True), flush=True)
                if data["status"] != "EXCLUDED":
                    write_certificate(args.output, "manifest.json", {"certificates": manifest,
                                      "incomplete": True})
                    print("Incomplete proof attempt; saved deductions establish no branch exclusion.", flush=True)
                    raise SystemExit(1)
    write_certificate(args.output, "manifest.json", {"certificates": manifest})
    summary = {"generated": len(manifest), "seconds": round(time.monotonic() - start, 3),
               "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "weight_guides": 0, "branch_timings": branch_timings}
    write_certificate(args.output, "generation-summary.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "branch_timings"}, sort_keys=True))


if __name__ == "__main__":
    main()
