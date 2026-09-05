#!/usr/bin/env python3
"""Literal small-graph equivalence and malformed-input controls."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import tempfile
import analyze
import verify


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run():
    pairs, five_sets = list(combinations(range(4),2)), list(combinations(range(7),5))
    cases, clones = 0, 0
    for bits in range(63):  # The one excluded four-vertex core is the red K4.
        edges = {e for i,e in enumerate(pairs) if bits >> i & 1}
        rows = analyze.decode({"n":4,"red_edges":[list(e) for e in sorted(edges)]})
        blue_quads = analyze.cliques(rows,False,4)
        for first in range(16):
            for second in range(16):
                allowed = analyze.pair_colors(rows,first,second)
                unary = all(first & q and second & q for q in blue_quads)
                for color in (False,True):
                    actual = set(edges) | {(v,4) for v in range(4)}
                    actual |= {(v,5) for v in range(4) if first >> v & 1}
                    actual |= {(v,6) for v in range(4) if second >> v & 1}
                    if color:
                        actual.add((5,6))
                    ramsey = not any(len({e in actual for e in combinations(q,2)}) == 1 for q in five_sets)
                    require(ramsey == bool(unary and color in allowed), "literal pair-kernel equivalence")
                    cases += 1
        for footprint in range(16):
            cap = analyze.clone_capacity(rows,footprint)
            for copies in range(1,5):
                actual = set(edges) | {(v,4) for v in range(4)}
                actual |= {(v,w) for v in range(4) for w in range(5,5+copies) if footprint >> v & 1}
                ramsey = not any(len({e in actual for e in combinations(q,2)}) == 1
                                 for q in combinations(range(5+copies),5))
                require(ramsey == (copies <= cap), "literal blue-clone capacity")
                clones += 1
    invalid = [{"n":True,"red_edges":[]}, {"n":21,"red_edges":[]},
               {"n":3,"red_edges":[[0,0]]}, {"n":3,"red_edges":[[1,0]]},
               {"n":3,"red_edges":[[0,3]]}, {"n":3,"red_edges":[[0,1],[0,1]]},
               {"n":3,"red_edges":[[False,1]]}, {"n":3,"red_edges":[],"extra":0}]
    for doc in invalid:
        try:
            analyze.decode(doc)
        except ValueError:
            pass
        else:
            raise ValueError("bad graph accepted")
    for x,y in ((-1,0),(0,16),(True,0)):
        try:
            analyze.pair_colors([0]*4,x,y)
        except ValueError:
            pass
        else:
            raise ValueError("bad footprint accepted")
    with tempfile.TemporaryDirectory(prefix="r55-footprint-controls-") as temporary:
        path = Path(temporary) / "fixture.txt"
        for text in ("", "1 00002\n", "1 00001\n2 00002\n"):
            path.write_text(text)
            try:
                verify.compare_file(path,{1:[1]})
            except ValueError:
                pass
            else:
                raise ValueError("bad domain stream accepted")
        path.write_text("1 00001\n")
        verify.compare_file(path,{1:[1]})
    return {"literal_graph_cases":cases,"literal_blue_clone_cases":clones,"core_graphs":63,"malformed_graphs_rejected":len(invalid),
            "malformed_footprints_rejected":3,"malformed_domain_streams_rejected":3,
            "status":"PASS"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report",type=Path,required=True)
    args = parser.parse_args()
    result = run()
    args.report.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))


if __name__ == "__main__":
    main()
