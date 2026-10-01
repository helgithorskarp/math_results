"""Affine-ratio classification and complete entry-level literal-bitmap audit."""
import argparse
import hashlib
from itertools import permutations
import json
from math import comb, isqrt
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def ratios(p):
    return {(v-u)*pow((w-u) % p,-1,p) % p for u,v,w in permutations(range(7),3)}


def affine_bitmap(p, s, allowed):
    total = comb(p-s,3) if p-s >= 3 else 0
    result = bytearray((total+7)//8)
    c2 = [comb(r,2) if r>=2 else 0 for r in range(p-s)]
    c3 = [comb(r,3) if r>=3 else 0 for r in range(p-s)]
    for a in range(s,p):
        for b in range(s,p):
            if a == b:
                continue
            delta = b-a
            for ratio in allowed:
                c = (a+delta*ratio) % p
                if c<s:
                    continue
                x,y,z = sorted((a-s,b-s,c-s))
                rank = x+c2[y]+c3[z]
                require(0<=rank<total, "affine colex rank outside domain")
                result[rank//8] |= 1 << (rank%8)
    return bytes(result)


def verify(metadata_path, bitmap_path):
    data = json.loads(metadata_path.read_text()); p,s = data["p"],data["s"]
    fields={"p","s","N","literal_APs","ordinary_triples","AP_triple_occurrences",
            "realized_triples","unrealized_triples","bitmap_bytes"}
    require(set(data)==fields and all(type(v) is int and v>=0 for v in data.values()), "wrong metadata fields or types")
    require(type(p) is int and 7<=p<=617 and all(p%d for d in range(2,isqrt(p)+1)), "wrong prime")
    require(type(s) is int and 1<=s<=6 and data["N"]==6*p+s, "wrong interval")
    allowed = ratios(p)
    require(0 not in allowed and 1 not in allowed, "degenerate normalized triple")
    for r in allowed:
        orbit = {r,(1-r)%p,pow(r,-1,p),pow((1-r)%p,-1,p),
                 (r-1)*pow(r,-1,p)%p,r*pow((r-1)%p,-1,p)%p}
        require(orbit<=allowed,"slot ratios not closed under triple relabeling")
    require(p*(p-1)*len(allowed)%6 == 0, "ordered-triple division invalid")
    all_triples = p*(p-1)*len(allowed)//6
    degree = (p-1)*len(allowed)//2
    prediction = all_triples-s*degree+comb(s,2)*len(allowed)-(comb(s,3) if s>=3 else 0)
    total = comb(p-s,3) if p-s>=3 else 0
    require(prediction==data["realized_triples"] and total==data["ordinary_triples"] and
            total-prediction==data["unrealized_triples"] and (total+7)//8==data["bitmap_bytes"],
            "analytic classification counts disagree")
    require(data["literal_APs"] == p*(3*(p-1)+s), "literal AP coverage mismatch")
    require(prediction<=data["AP_triple_occurrences"]<=35*data["literal_APs"], "wrong occurrence diagnostic")
    actual = bitmap_path.read_bytes()
    require(len(actual)==(total+7)//8,"wrong support bitmap length")
    expected = affine_bitmap(p,s,allowed)
    require(actual == expected,"literal AP supports and affine ratio classification differ")
    realized = sum(byte.bit_count() for byte in actual)
    require(realized==prediction==data["realized_triples"] and total==data["ordinary_triples"] and
            total-realized==data["unrealized_triples"] and len(actual)==data["bitmap_bytes"], "classification counts disagree")
    orbits = []; unseen = set(allowed)
    while unseen:
        r=min(unseen)
        orbit={r,(1-r)%p,pow(r,-1,p),pow((1-r)%p,-1,p),
               (r-1)*pow(r,-1,p)%p,r*pow((r-1)%p,-1,p)%p}
        unseen-=orbit; orbits.append(sorted(orbit))
    if p==617:
        require(len(allowed)==33 and sorted(map(len,orbits))==[3,6,6,6,6,6], "wrong617 ratio orbit census")
    return {"status":"EXACT_LITERAL_AFFINE_SUPPORT_BITMAPS_MATCH",**data,
            "normalized_ratios":sorted(allowed),"ratio_orbits":orbits,
            "classification_entries_checked":total,"bitmap_sha256":hashlib.sha256(actual).hexdigest()}


if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("metadata",type=Path); parser.add_argument("bitmap",type=Path)
    parser.add_argument("--output",type=Path); args=parser.parse_args()
    result=verify(args.metadata,args.bitmap); text=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text,end="")
