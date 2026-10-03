"""Small direct completeness fixtures and deliberate proof-transcript damage."""
import argparse
import itertools
import json
import tempfile
from pathlib import Path
from model import canon, require
from primary import selections
from verify_records import check, coefficient_count

def controls(stream):
    fixtures=0
    for weights in ((0,0,1,1,2,3,7), (0,1,1,1,2,2,8), (1,2,3,4,5,6,7)):
        weighted=sorted((w,q) for q,w in enumerate(weights))
        for k in (0,1,3,6):
            for cap in (0,3,6):
                expected={x for x in itertools.combinations(range(len(weights)),k)
                          if sum(weights[q] for q in x)<=cap}
                actual=set(selections(weighted,k,cap))
                require(actual==expected, "literal small subset coverage")
                require(coefficient_count(weights,k,cap)==len(expected), "coefficient fixture")
                fixtures+=1
    positive=check("balanced",0,8,stream)
    lines=stream.read_text().splitlines(keepends=True)
    r=json.loads(lines[0])
    damages={"omit_first":lines[1:], "omit_last":lines[:-1],
             "duplicate":lines[:1]+lines, "wrong_core":None,
             "wrong_cost":None,"wrong_best":None,"wrong_missing":None,
             "duplicated_row":None,"extra_field":None}
    for name in tuple(damages):
        if damages[name] is not None:
            continue
        x=json.loads(canon(r))
        if name=="wrong_core":x[0][0]=1
        elif name=="wrong_cost":x[3]+=1
        elif name=="wrong_best":x[4][0][1]=x[1][0]
        elif name=="wrong_missing":x[5]+=1
        elif name=="duplicated_row":x[2][1]=x[2][0]
        elif name=="extra_field":x.append(0)
        damages[name]=[canon(x)]+lines[1:]
    rejected=[]
    with tempfile.TemporaryDirectory() as d:
        for name,body in damages.items():
            p=Path(d)/"bad.jsonl";p.write_text("".join(body))
            try:check("balanced",0,8,p)
            except ValueError:rejected.append(name)
            else:raise ValueError("damage accepted: "+name)
    return dict(literal_subset_fixtures=fixtures,positive_records=positive["count"],
                semantic_damages_rejected=rejected)

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--stream",type=Path,required=True)
    x=ap.parse_args();print(canon(controls(x.stream)),end="")
