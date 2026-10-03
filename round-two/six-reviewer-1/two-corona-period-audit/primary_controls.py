"""Controls written before producer code/certificate access."""
from pathlib import Path
import tempfile, json
from independent import *

def rejected(call):
    try:call()
    except (ValueError,KeyError,TypeError):return True
    raise ValueError("invalid control accepted")

def main():
    results=[]
    with tempfile.TemporaryDirectory() as temp:
        temp=Path(temp)
        for name,text in [
            ("missing-empty","1 0\n"),("post-zero","0 1\n"),("out-of-domain","644 0\n0\n"),
            ("duplicate","1 1 0\n0\n"),("deletion","d 1 0\n0\n"),("rat","1 x 0\n0\n"),
            ("early-empty","0\n1 0\n0\n"),("interior-zero","1 0 2 0\n0\n")]:
            f=temp/"damaged.rup";f.write_text(text)
            rejected(lambda:read_rup(f,643));results.append(name)
        for name,damage in [
            ("duplicate-source",lambda d:d["cells"].append(d["cells"][0])),
            ("noninteger-cell",lambda d:d["cells"][0].__setitem__(0,False)),
            ("wrong-depth",lambda d:d.__setitem__("depth",1)),
            ("wrong-margin",lambda d:d.__setitem__("margin",2)),
            ("lost-copy",lambda d:d["levels"][1].pop()),
            ("moved-root",lambda d:d["levels"][0][0].__setitem__(1,1))]:
            d=unique_json(BASE/"input.json");damage(d);f=temp/"input.json";f.write_text(json.dumps(d))
            rejected(lambda:build(f));results.append(name)
        for name,damage in [
            ("nonisometry",lambda d:d["representatives"][0].__setitem__("matrix",[1,1,0,1])),
            ("changed-period",lambda d:d["periods"][0].__setitem__(0,21)),
            ("missing-period-copy",lambda d:d["representatives"].pop())]:
            d=unique_json(BASE/"tiling.json");damage(d);f=temp/"tiling.json";f.write_text(json.dumps(d))
            rejected(lambda:build(tiling_path=f));results.append(name)
    m=build();n=build(row_order="adjugate")
    # Whole formula transport, including all 520 row names and each literal.
    rename={i+1:i+1 for i in range(123)}
    other={k:124+i for i,k in enumerate(n["order"])}
    rename.update({124+i:other[k] for i,k in enumerate(m["order"])})
    mapped=clean([[rename[abs(x)]*(1 if x>0 else -1) for x in c] for c in m["formula"]])
    require(mapped==n["formula"],"every formula clause under alternate exact quotient names")
    print(json.dumps({"rejected_controls":results,"whole_quotient_formula_bijection":True,
                      "local_exact_rows":local_controls()},sort_keys=True))

if __name__=="__main__":main()
