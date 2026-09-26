#!/usr/bin/env python3
"""Replay the complete obstructions; optionally run the slower direct layer census."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess
import tempfile

from model import build, decode, normalizations, write_instance

HERE = Path(__file__).resolve().parent
CASES = [(71,28,-1,"23401"),(71,1,495,"10234"),(71,1,943,"10234"),
         (72,0,495,"01234"),(72,0,943,"01234")]


def geometry():
    pts = list(product(range(5), repeat=3))
    index = {p:i for i,p in enumerate(pts)}
    directions = [v for v in pts if any(v) and next(x for x in v if x) == 1]
    lines = sorted({tuple(sorted(index[tuple((a[j]+t*v[j])%5 for j in range(3))]
                                 for t in range(5))) for a in pts for v in directions})
    if len(lines) != 775:
        raise ValueError("incorrect three-dimensional geometry")
    return pts,index,lines


def check(points, lines, size):
    chosen = set(points)
    if len(chosen) != len(points) or len(chosen) != size or not chosen <= set(range(125)):
        raise ValueError("bad witness coordinates")
    if any(set(line) <= chosen for line in lines):
        raise ValueError("full line in control")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path)
    parser.add_argument("--full",action="store_true",help="all five slower direct layer enumerations")
    parser.add_argument("--sanitize",action="store_true")
    parser.add_argument("--check-expected",action="store_true")
    args = parser.parse_args()
    out = args.out.resolve() if args.out else Path(tempfile.mkdtemp(prefix="reflection-rigidity-"))
    out.mkdir(parents=True,exist_ok=True)
    flags = ["-std=c++20","-Wall","-Wextra","-Wconversion","-Werror"]
    flags += ["-O1","-g","-fsanitize=address,undefined"] if args.sanitize else ["-O2"]
    binaries = {}
    for name in ["reflection_constraints","reflection_direct","order4_probe","order4_gray"]:
        binary = out/name
        subprocess.run(["g++",*flags,str(HERE/(name+".cpp")),"-o",str(binary)],check=True)
        binaries[name] = str(binary)
    model = build()
    normalized = normalizations(model)
    if [r["first"] for r in normalized] != [495,943]:
        raise ValueError("unexpected full-layer normal forms")
    instance = out/"instance.txt"
    write_instance(instance,model)
    second_files = {}
    for row in normalized:
        path = out/("second"+str(row["first"])+".txt")
        path.write_text(" ".join(str(c["representative"]) for c in row["classes"])+"\n")
        second_files[row["first"]] = str(path)
    records = []
    for size,center,first,order in CASES:
        command = [binaries["reflection_constraints"],str(instance),str(size),str(center),str(first),order]
        if size == 72:
            command.append(second_files[first])
        result = json.loads(subprocess.check_output(command,text=True))
        if result["solutions"] != 0:
            raise ValueError(("obstruction failed",result))
        records.append(result)
    def direct(case):
        size,center,first,order = case
        command = [binaries["reflection_direct"],str(size),str(center),str(first),order]
        if size == 72:
            command.append(second_files[first])
        return json.loads(subprocess.check_output(command,text=True))
    direct_cases = CASES if args.full else CASES[:1]
    # The case partition is fixed; each process completes its own full domain.
    with ThreadPoolExecutor(max_workers=2) as pool:
        direct_records = list(pool.map(direct,direct_cases))
    if direct_records != records[:len(direct_cases)]:
        raise ValueError("direct and constraint layer representations disagree")

    cube_instance = out/"cube_instance.txt"
    write_instance(cube_instance,model,cube=True)
    common = out/"cube_masks.txt"
    common.write_text("0 943\n")
    controls = []
    pts,index,lines = geometry()
    for size,count in [(64,5),(80,0)]:
        first = json.loads(subprocess.check_output(
            [binaries["reflection_constraints"],str(cube_instance),str(size),"0","-1","01234"],text=True))
        second = json.loads(subprocess.check_output(
            [binaries["reflection_direct"],str(size),"0","-1","01234","-",str(common)],text=True))
        if first != second or first["solutions"] != count:
            raise ValueError(("positive/negative control failed",first,second))
        controls.append(first)
    for hole in range(5):
        witness = decode(0,[0 if x == hole else 943 for x in range(5)],model)
        check(witness,lines,64)
        if {index[(x,-y%5,-z%5)] for x,y,z in (pts[p] for p in witness)} != set(witness):
            raise ValueError("line-reflection control is not invariant")

    order4 = [json.loads(line) for line in subprocess.check_output(
        [binaries["order4_probe"]],text=True).splitlines()]
    gray = [json.loads(line) for line in subprocess.check_output(
        [binaries["order4_gray"]],text=True).splitlines()]
    stripped = [{k:v for k,v in row.items() if k not in {"example_b","example_allowed"}} for row in order4]
    if stripped != gray or len(order4) != 9:
        raise ValueError("order-four histograms disagree")
    for row in order4:
        bsize,kind = row["bsize"],row["kind"]
        if 4*bsize+row["max_allowed"] > 68 or row["relaxation_survivors71"]:
            raise ValueError("order-four bound failed")
        b,a = row["example_b"],row["example_allowed"]
        tb = sum(1 << (5*((5-p//5)%5 if kind == 2 else p//5)
                       +((5-p%5)%5 if kind else p%5)) for p in range(25) if b >> p & 1)
        witness = [25*x+p for x,mask in enumerate([a,b,tb,tb,b]) for p in range(25) if mask >> p & 1]
        check(witness,lines,4*bsize+row["max_allowed"])
        transformed = {
            index[(2*x%5,-y%5 if kind == 2 else y,-z%5 if kind else z)]
            for x,y,z in (pts[p] for p in witness)
        }
        if transformed != set(witness):
            raise ValueError("order-four boundary control is not invariant")

    for count,representative in [(1,1),(3,28)]:
        masks = {sum(1<<((a*x+b)%5) for x in range(5) if representative >> x & 1)
                 for a in range(1,5) for b in range(5)}
        if masks != {m for m in range(32) if m.bit_count() == count}:
            raise ValueError("fixed-line normalization incomplete")
    summary = {
        "status":"LARGER_CANDIDATES_HAVE_AT_MOST_ONE_REFLECTION",
        "layer_spectra":[dict(sorted(Counter(m.bit_count() for m in menu).items())) for menu in model["menus"]],
        "maximal_layer_classes":[r for r in model["classes"][0] if r["weight"] == 8],
        "normalization_counts":[{"first":r["first"],"stabilizer_order":r["stabilizer_order"],
                                 "second_classes":dict(sorted(Counter(c["weight"] for c in r["classes"]).items())),
                                 "covered_masks":sum(c["multiplicity"] for c in r["classes"])} for r in normalized],
        "transverse_patterns":len(model["constraints"]),"line_count":len(lines),
        "line_reflection_cases":records,"cube_controls":controls,
        "order4_cases":order4,
        "normalization_sha256":sha256(json.dumps(normalized,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
        "verified_geometric_controls":14,
    }
    summary = json.loads(json.dumps(summary))
    if args.check_expected and summary != json.loads((HERE/"EXPECTED.json").read_text()):
        raise ValueError("expected-output mismatch")
    print(json.dumps(summary,sort_keys=True,indent=2))


if __name__ == "__main__":
    main()
