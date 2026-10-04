"""Canonical serialization and exact partition coverage only.
Mathematical engines compute before optional fixture or whole-record checks.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from itertools import product
from math import prod
import argparse,json

def require(ok,label):
    if not ok:raise ValueError(label)

def rows(poly):
    return [{"powers":list(m),"coefficient":str(F(c.numerator,c.denominator))}
            for m,c in sorted(poly.items(),reverse=True)if c]

def canonical(record):return(json.dumps(record,sort_keys=True,separators=(",",":"))+"\n").encode()

def partitions():
    p=json.loads((Path(__file__).resolve().parent/"PARTITION.json").read_text())
    root=[[F(v)for v in r]for r in p["root"]]
    require(root==[[F(0),F(1,5)],[F(1,4),F(1,2)]],"exact original quartic root rectangle")
    require(len(p["leaves"])==10,"ten-leaf quartic coverage")
    boxes=[]
    for i,l in enumerate(p["leaves"]):
        require(l["label"]==f"quartic-{i+1:02d}","canonical quartic leaf order")
        b=[[F(v)for v in r]for r in l["bounds"]]
        require(len(b)==2 and all(len(r)==2 for r in b),"two-dimensional partition shape")
        require(all(root[k][0]<=b[k][0]<b[k][1]<=root[k][1]for k in range(2)),"strict paid quartic boxes")
        boxes.append({"label":l["label"],"bounds":b})
    cuts=[sorted({root[k][0],root[k][1],*[v for b in boxes for v in b["bounds"][k]]})for k in range(2)]
    for i,j in product(range(len(cuts[0])-1),range(len(cuts[1])-1)):
        cell=[(cuts[0][i],cuts[0][i+1]),(cuts[1][j],cuts[1][j+1])]
        count=sum(all(b["bounds"][k][0]<=cell[k][0] and cell[k][1]<=b["bounds"][k][1]for k in range(2))for b in boxes)
        require(count==1,"whole quartic partition cell coverage")
    return boxes

def summarize(record):
    boxes=[]
    labels=[f"quartic-{i+1:02d}"for i in range(10)]+["positive","negative"]
    require([b["label"]for b in record["leaves"]]==labels,"complete two-cap and quartic coverage")
    for b in record["leaves"]:
        d={tuple(t["powers"]):F(t["coefficient"])for t in b["controls"]};deg=b["degrees"]
        indices=product(*(range(n+1)for n in deg));values=[d.get(m,F(0))for m in indices]
        require(len(values)==len(d)==prod(n+1 for n in deg),"complete exact tensor entries")
        require(min(values)>0,"entire Bernstein tensor strictly positive")
        boxes.append({"label":b["label"],"kind":b["kind"],"bounds":b["bounds"],"degrees":deg,
                      "entries":len(values),"minimum":str(min(values)),"whole_leaf_sha256":sha256(canonical(b)).hexdigest()})
    require(sum(b["entries"]for b in boxes)==3706,"all new exact controls counted")
    require(all(F(x)>0 for x in record["scalar_margins"].values()),"strict original-strip constants")
    return {"actual_agent":"six-sendov-2","role":"researcher",
            "claim":"every normalized odd-moment-zero real8 exact-one-double has C<47/2; new positive-q0 closure",
            "domain":record["domain"],"whole_math_bytes":len(canonical(record)),
            "whole_math_sha256":sha256(canonical(record)).hexdigest(),
            "maps":{k:{"terms":len(record[k])}for k in ["Delta","N","P"]},
            "scalar_margins":record["scalar_margins"],"boxes":boxes,
            "all_3706_controls_strictly_positive":True,"entire_models_and_coefficients_checked":True,
            "removed_positive_factor":"h^10; cleared denominator (kappa*A*J)^8",
            "ordinary_bridges_unformalized":True,"independent_peer_review_claimed":False,
            "full_complex_first_power_claimed":False}

def emit(record):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--whole",type=Path)
    p.add_argument("--expected",type=Path);p.add_argument("--check",type=Path);a=p.parse_args()
    summary=summarize(record);data=canonical(record)
    if a.check:require(a.check.read_bytes()==data,"entire external mathematical record mismatch")
    if a.expected:require(json.loads(a.expected.read_text())==summary,"complete expected record mismatch")
    if a.whole:
        require(not a.whole.resolve().is_relative_to(Path(__file__).resolve().parent),"keep bulky output outside source")
        a.whole.write_bytes(data)
    print(json.dumps(summary,sort_keys=True,indent=2))
