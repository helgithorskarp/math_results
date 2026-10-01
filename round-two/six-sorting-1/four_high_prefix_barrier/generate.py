#!/usr/bin/env python3
"""Generate a compact exact higher-extreme obstruction certificate."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
FAMILIES = [("one_minimum",1,0),("one_maximum",0,1),("two_minima",2,0),
            ("two_maxima",0,2),("mixed_pair",1,1),("four_maxima",0,4)]
PROFILE_SHA = "dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719"
ANCHORS_SHA = "0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902"


def canonical(value):
    return hashlib.sha256(json.dumps(value,separators=(",",":")).encode()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--profile-dir",type=Path,default=ROOT.parent.parent/"six-sorting-2/semantic-pruning")
    args=p.parse_args()
    for name,digest in [("profile.py",PROFILE_SHA),("anchors.py",ANCHORS_SHA)]:
        if hashlib.sha256((args.profile_dir/name).read_bytes()).hexdigest()!=digest:
            raise ValueError("pinned dependency differs: "+name)
    sys.path.insert(0,str(args.profile_dir.resolve()))
    import profile,anchors
    fixture=json.loads((ROOT/"fixture.json").read_text())
    prefix=fixture["prefix38"]
    data={name:profile.analyze_family(13,prefix,lo,hi) for name,lo,hi in FAMILIES}
    compact={name:{k:d[k] for k in ("low_count","high_count","records","envelope","summary")}
             for name,d in data.items()}
    control=profile.analyze_family(13,fixture["control45"],0,4)
    obj={"schema":"four-high-prefix38-v1","agent":"six-sorting-1","role":"researcher",
         "prefix_sha256":canonical(prefix),"prefix_size":38,"families":compact,
         "original_anchor_units":{side:r["normalized_mass"] for side,r in anchors.both(
             13,{name:data[name] for name,_,_ in FAMILIES[:-1]}).items()},
         "four_high_trace":[{k:v[k] for k in ("ordinary_mass","semantic_mass","port_classes")}
                            for v in data["four_maxima"]["trace"]],
         "control45_four_high":{k:control[k] for k in ("low_count","high_count","records","envelope","summary")}}
    (ROOT/"certificate.json").write_text(json.dumps(obj,sort_keys=True,separators=(",",":"))+"\n")
    print(json.dumps({"status":"EXACT_PRODUCER_COMPLETE","anchors":obj["original_anchor_units"],
                      "four_high":compact["four_maxima"]["summary"],
                      "prefix37":obj["four_high_trace"][37]},sort_keys=True))


if __name__=="__main__":
    main()
