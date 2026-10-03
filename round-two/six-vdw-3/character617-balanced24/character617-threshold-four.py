"""Resumable private exact threshold-four intersection exploration.

No exclusion follows until the queue is exhausted and separately checked.
Rows are squares, columns are nonsquares, vertex1 is the anchored square.
Each atomic step takes an explicit number of queued states, then checkpoints.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path


def require(ok, why):
    if not ok:
        raise ValueError(why)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


ap = argparse.ArgumentParser()
ap.add_argument("--checkpoint", type=Path, required=True)
ap.add_argument("--states-per-step", type=int, default=1000)
ap.add_argument("--final", type=Path)
args = ap.parse_args()
require(args.states_per_step > 0, "positive bounded batch")
p = 617
sq = [q for q in range(1, p) if pow(q, (p-1)//2, p) == 1]
ns = [q for q in range(1, p) if pow(q, (p-1)//2, p) == p-1]
nsset = set(ns)
supports = [[(1+j*d) % p for j in range(1, 7)] for d in range(1, p)
            if all((1+j*d) % p in nsset for j in range(1, 7))]
v = {q for support in supports for q in support}
dset = v | {pow(q, p-2, p) for q in v}
require(len(sq) == len(ns) == 308 and len(supports) == 6 and len(v) == 33 and len(dset) == 66,
        "complete endpoint graph")
masks = {q: sum(1 << (q*t % p) for t in dset) for q in sq}
schema = "private-character617-threshold-four-resumable-v1"
if args.checkpoint.exists():
    c = json.loads(args.checkpoint.read_text())
    require(c["schema"] == schema and c["threshold"] == 4 and (not c["complete"] or args.final), "unfinished own checkpoint or final extraction")
    values = [int(s, 16) for s in c["states"]]
    processed = c["processed"]
    retained = c["retained_transitions"]
    require(c["states_sha256"] == digest(c["states"]) and len(set(values)) == len(values), "whole unique checkpoint states")
else:
    values = [masks[1]]
    processed = retained = 0
seen = set(values)
stop = processed if args.final else min(processed + args.states_per_step, len(values))
start = processed
while processed < stop:
    b = values[processed]
    for q in sq:
        cc = b & masks[q]
        if cc.bit_count() >= 4:
            retained += 1
            if cc not in seen:
                seen.add(cc)
                values.append(cc)
    processed += 1
c = {"schema": schema, "agent": "six-vdw-3", "role": "researcher", "threshold": 4,
     "processed": processed, "tested_transitions": processed*308, "retained_transitions": retained,
     "states": [hex(s) for s in values], "complete": processed == len(values)}
c["states_sha256"] = digest(c["states"])
temporary = args.checkpoint.with_suffix(".next.json")
temporary.write_text(json.dumps(c, sort_keys=True) + "\n")
temporary.replace(args.checkpoint)
if args.final:
    require(c["complete"], "final requires every state and every transition")
    require(not args.final.exists(), "preserve existing final evidence")
    records = []
    fives = {}
    for b in values:
        a = [q for q in sq if b & masks[q] == b]
        bs = [t for t in ns if b & (1 << t)]
        records.append({"A": a, "B": bs})
        if len(a) >= 5:
            require(1 in a, "anchor in whole closure")
            for others in itertools.combinations(a[1:], 4):
                common = masks[1]
                for q in others:
                    common &= masks[q]
                fives[(1, *others)] = [t for t in ns if common & (1 << t)]
    records.sort(key=lambda r: r["B"])
    five_records = [{"A0": list(a), "C": bs} for a, bs in sorted(fives.items())]
    output = {"schema": "private-character617-threshold-four-complete-v1",
              "agent": "six-vdw-3", "role": "researcher", "threshold": 4,
              "states": len(records), "tested_transitions": c["tested_transitions"],
              "retained_transitions": retained, "maximum_A": max(len(r["A"]) for r in records),
              "A_B_histogram": [[a, b, n] for (a,b), n in sorted(collections.Counter((len(r["A"]), len(r["B"])) for r in records).items())],
              "five_set_count": len(five_records),
              "five_common_histogram": sorted(collections.Counter(len(r["C"]) for r in five_records).items()),
              "records_sha256": digest(records), "five_records_sha256": digest(five_records),
              "records": records, "five_records": five_records,
              "status": "COMPLETE_PRIVATE_PILOT_REQUIRES_INDEPENDENT_CHECK"}
    args.final.write_text(json.dumps(output, sort_keys=True) + "\n")
    print(json.dumps({k:v for k,v in output.items() if k not in ("records", "five_records")}))
else:
    print(json.dumps({k:v for k,v in c.items() if k != "states"} | {"state_count": len(values), "batch_start": start}))
