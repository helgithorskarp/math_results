"""Meaningful mathematical and malformed-input negative controls."""
from independent import *
from reproduce import fixture_check
import tempfile

def reject(call):
    try:call()
    except ValueError:return
    raise ValueError("damaged mathematical control accepted")

def main():
    m=build();proof=read_rup(BASE/"proof.rup",643);names=[]
    for name,formula in [
        ("removed-nonempty",[c for c in m["formula"] if c!=m["nonempty"]]),
        ("removed-period-failure",[c for c in m["formula"] if c!=m["failed"]])]:
        reject(lambda:verify_rup(formula,proof));names.append(name)
    reject(lambda:verify_rup(m["formula"],[()]));names.append("unsupported-immediate-empty")
    # The independent actual 64-cell witness proves first-only satisfiable.
    fixture_check(m,BASE/"counterexample.json")
    physical_first=[]
    for i,j in combinations(range(7),2):
        inv={v:p for p,v in m["images"][j].items()}
        for p,v in m["images"][i].items():
            if v in inv:
                physical_first.append((-(m["u"].index(p)+1),-(m["u"].index(inv[v])+1)))
    first=clean(physical_first+m["groups"]["halo0"]+
                m["groups"]["nonempty"]+m["groups"]["failure"])
    reject(lambda:verify_rup(first,proof));names.append("second-stage-wholly-removed")
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        no_empty=td/"missing-empty.rup"
        no_empty.write_text("".join(" ".join(map(str,c))+" 0\n"for c in proof[:-1])+ "643 0\n")
        reject(lambda:read_rup(no_empty,643));names.append("lost-final-empty-obligation")
        for name,mutate in [
            ("moved-period-representative",lambda t:t["representatives"][1]["translation"].__setitem__(0,6)),
            ("duplicated-period-representative",lambda t:t["representatives"].__setitem__(1,t["representatives"][0]))]:
            t=unique_json(BASE/"tiling.json");mutate(t);f=td/"tiling.json";f.write_text(json.dumps(t))
            reject(lambda:build_record(build(tiling_path=f)));names.append(name)
        for name,mutate in [
            ("deleted-counter-cell",lambda t:t["raw_cells"].pop()),
            ("changed-counter-origin",lambda t:t["raw_cells"][0].__setitem__(0,0)),
            ("moved-first-counter-copy",lambda t:t["fixture"]["levels"][1][0].__setitem__(1,10)),
            ("missing-first-counter-copy",lambda t:t["fixture"]["levels"][1].pop())]:
            t=unique_json(BASE/"counterexample.json");mutate(t);f=td/"counterexample.json";f.write_text(json.dumps(t))
            reject(lambda:fixture_check(m,f));names.append(name)
    print(json.dumps({"mathematical_damages_rejected":names,"count":len(names)},sort_keys=True))

if __name__=="__main__":main()
