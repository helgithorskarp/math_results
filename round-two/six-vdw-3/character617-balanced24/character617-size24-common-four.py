"""Complete private C4 branch: ten singleton columns, exactly two per row.

The fifth-smallest missing degree is2. When C has size4, a selected B14
requires all four common columns and ten other columns. Since the five row
capacities are2, each other column misses exactly one row and each row is
missed twice. The five added rows must each miss exactly2, or the total
missing-pair allowance20 is violated. Every actual column/row remains labeled.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path


def need(ok, why):
    if not ok:
        raise ValueError(why)


def canon(x):
    return json.dumps(x,sort_keys=True,separators=(",",":")).encode()


ap=argparse.ArgumentParser()
ap.add_argument("--capacity",type=Path,required=True)
ap.add_argument("--output",type=Path,required=True)
args=ap.parse_args()
need(not args.output.exists(),"preserve previous evidence")
capacity=json.loads(args.capacity.read_text())
sq=[q for q in range(1,617) if pow(q,308,617)==1]
ns=[t for t in range(1,617) if pow(t,308,617)==616]
v={t for d in range(1,617) if all(pow((1+j*d)%617,308,617)==616 for j in range(1,7))
   for t in [(1+j*d)%617 for j in range(1,7)]}
ratios=v|{pow(t,615,617) for t in v}
masks={q:sum(1<<(q*d%617) for d in ratios) for q in sq}
records=[]
hist=collections.Counter()
for item in capacity["records"]:
    if len(item["C"])!=4 or not item["surviving_core_sizes"]:
        continue
    a0,common=item["A0"],item["C"]
    singleton=[]
    for i in range(5):
        singleton.append([t for t in ns if sum(not masks[q]&(1<<t) for q in a0)==1 and not masks[a0[i]]&(1<<t)])
    need([len(s) for s in singleton]==item["singleton_counts"],"every singleton column")
    row_records=[]
    for choices in itertools.product(*(itertools.combinations(s,2) for s in singleton)):
        b=sorted(common+[t for group in choices for t in group])
        bm=sum(1<<t for t in b)
        need(len(set(b))==14 and all(14-(masks[q]&bm).bit_count()==2 for q in a0),"full B14 and exact five-row deficits")
        extra=[q for q in sq if q not in a0 and 14-(masks[q]&bm).bit_count()==2]
        row_records.append({"B":b,"cost_two_added_rows":extra})
        hist[len(extra)]+=1
    row_records.sort(key=lambda r:r["B"])
    records.append({"A0":a0,"C":common,"singleton_columns":singleton,"records":row_records})
candidate=[{"A0":r["A0"],**sub} for r in records for sub in r["records"] if len(sub["cost_two_added_rows"])>=5]
output={"schema":"private-character617-size24-common-four-v1","agent":"six-vdw-3","role":"researcher",
        "part_sizes":[10,14],"missing_budget":20,"first_five_common":4,"cores":len(records),
        "fourteen_column_sets":sum(len(r["records"]) for r in records),"extra_cost_two_histogram":sorted(hist.items()),
        "potential_support_cores":len(candidate),"potential_supports":candidate,
        "records_sha256":hashlib.sha256(canon(records)).hexdigest(),"records":records,
        "status":"COMPLETE_PRIVATE_COMMON_FOUR_PILOT_REQUIRES_INDEPENDENT_CHECK"}
args.output.write_text(json.dumps(output,sort_keys=True)+"\n")
print(json.dumps({k:v for k,v in output.items() if k not in ("records","potential_supports")}))
