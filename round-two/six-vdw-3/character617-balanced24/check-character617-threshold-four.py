"""Independent increasing-tuple coverage and literal-ratio state checks.

Square-set character and Euclidean inverses; columns use compact class indices.
Never imports the queue producer. The tuple algorithm independently covers every
anchored five-row set with at least four common neighbors by prefix monotonicity.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def inverse(x):
    a, b, u, v = 617, x, 0, 1
    while b:
        k = a//b
        a, b, u, v = b, a-k*b, v, u-k*v
    need(a == 1, "nonzero field inverse")
    return u % 617


ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=Path)
ap.add_argument("--output", required=True, type=Path)
ap.add_argument("--mode", required=True, choices=("tuples", "states", "merge"))
ap.add_argument("--start", type=int, default=0)
ap.add_argument("--stop", type=int)
ap.add_argument("--pieces", type=Path)
args = ap.parse_args()
need(not args.output.exists(), "preserve existing check")
data = json.loads(args.input.read_text())
square_set = {q*q % 617 for q in range(1, 617)}
sq = sorted(square_set)
ns = sorted(set(range(1, 617))-square_set)
nsset = set(ns)
supports = []
for step in range(1, 617):
    now, points = 1, []
    for j in range(6):
        now = (now+step) % 617
        points.append(now)
    if set(points) <= nsset:
        supports.append(points)
v = set().union(*(set(s) for s in supports))
ratios = v | {inverse(t) for t in v}
rows = []
for q in sq:
    iq = inverse(q)
    rows.append(sum(1 << i for i, t in enumerate(ns) if t*iq % 617 in ratios))
need(len(supports) == 6 and len(v) == 33 and not v & {inverse(t) for t in v}, "literal endpoint graph")
need(all(m.bit_count() == 66 for m in rows), "whole square adjacency")

if args.mode == "tuples":
    start, stop = args.start, args.stop
    need(1 <= start < stop <= 308, "second-row range")
    records, retained, trials = [], collections.Counter(), collections.Counter()

    def visit(indices, common):
        retained[len(indices)] += 1
        if len(indices) == 5:
            records.append({"A0": [sq[i] for i in indices], "C": [t for j, t in enumerate(ns) if common & (1 << j)]})
            return
        for index in range(indices[-1]+1, len(sq)):
            trials[len(indices)+1] += 1
            sub = common & rows[index]
            if sub.bit_count() >= 4:
                visit((*indices, index), sub)

    for index in range(start, stop):
        trials[2] += 1
        sub = rows[0] & rows[index]
        if sub.bit_count() >= 4:
            visit((0, index), sub)
    result = {"mode": "tuples", "start": start, "stop": stop,
              "retained_counts": sorted(retained.items()), "trial_counts": sorted(trials.items()),
              "records": records, "records_sha256": hashlib.sha256(canon(records)).hexdigest()}

elif args.mode == "states":
    start, stop = args.start, args.stop
    need(0 <= start < stop <= len(data["records"]), "closed-state range")
    state_set = {tuple(r["B"]) for r in data["records"]}
    need(len(state_set) == len(data["records"]), "state uniqueness")
    positions = {t:i for i,t in enumerate(ns)}
    state_masks = {sum(1 << positions[t] for t in b) for b in state_set}
    retained = 0
    for record in data["records"][start:stop]:
        b = sum(1 << positions[t] for t in record["B"])
        aa = [q for q, m in zip(sq, rows) if m & b == b]
        need(aa == record["A"] and 1 in aa, "every full literal square closure")
        common = rows[0]
        for q in aa:
            common &= rows[sq.index(q)]
        need(common == b and b.bit_count() >= 4, "every full literal column closure")
        for m in rows:
            cc = b & m
            if cc.bit_count() >= 4:
                retained += 1
                need(cc in state_masks, "every retained transition in full family")
    result = {"mode": "states", "start": start, "stop": stop, "checked_states": stop-start,
              "tested_transitions": (stop-start)*308, "retained_transitions": retained}

else:
    need(args.pieces is not None, "pieces directory")
    records, retained, trials = [], collections.Counter(), collections.Counter()
    pieces = sorted(args.pieces.glob("tuples-*.json"))
    cursor = 1
    for path in pieces:
        part = json.loads(path.read_text())
        need(part["start"] == cursor and part["mode"] == "tuples", "entire second-row partition")
        need(part["records_sha256"] == hashlib.sha256(canon(part["records"])).hexdigest(), "whole tuple-piece digest")
        cursor = part["stop"]
        records.extend(part["records"])
        retained.update(dict(part["retained_counts"]))
        trials.update(dict(part["trial_counts"]))
    need(cursor == 308, "all307 second rows covered")
    need(records == data["five_records"], "every complete anchored five-set, not just aggregate counts")
    need(data["five_records_sha256"] == hashlib.sha256(canon(records)).hexdigest(), "canonical five-record digest")
    states = sorted(args.pieces.glob("states-*.json"))
    cursor = kept = 0
    for path in states:
        part = json.loads(path.read_text())
        need(part["start"] == cursor and part["mode"] == "states", "entire closed-state partition")
        cursor = part["stop"]
        kept += part["retained_transitions"]
    need(cursor == len(data["records"]) == data["states"] and kept == data["retained_transitions"], "whole state/transition counters")
    need(data["records_sha256"] == hashlib.sha256(canon(data["records"])).hexdigest(), "whole literal state digest")
    result = {"mode": "merge", "agent": "six-vdw-3", "role": "researcher",
              "status": "COMPLETE_PRIVATE_THRESHOLD_FOUR_COVERAGE_CHECKED",
              "states": cursor, "retained_transitions": kept,
              "five_set_count": len(records), "retained_tuple_counts": [[1, 1], *sorted(retained.items())],
              "trial_counts": sorted(trials.items()), "maximum_five_common": max(len(r["C"]) for r in records),
              "records_sha256": data["records_sha256"], "five_records_sha256": data["five_records_sha256"]}
args.output.write_text(json.dumps(result, sort_keys=True) + "\n")
print(json.dumps({k:v for k,v in result.items() if k != "records"}))
