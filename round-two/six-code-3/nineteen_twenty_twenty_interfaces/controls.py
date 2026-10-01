"""Literal exhaustive clique controls and malformed protocol checks."""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess

from native import Native
import verify_residual as r

HERE=Path(__file__).resolve().parent


def rejects(function):
    try:
        function()
    except (ValueError,TypeError,RuntimeError):
        return
    raise ValueError('malformed evidence was accepted')


def run(executable):
    labels=[0,63,64,127,255]
    edges=list(combinations(range(5),2))
    decisions=0
    for code in range(1 << len(edges)):
        adjacent=[set() for _ in range(256)]
        literal=[set() for _ in range(5)]
        for bit,(a,b) in enumerate(edges):
            if code & (1 << bit):
                adjacent[labels[a]].add(labels[b]);adjacent[labels[b]].add(labels[a])
                literal[a].add(b);literal[b].add(a)
        with Native(executable,[adjacent]) as engine:
            for target in range(1,6):
                expected=[[labels[i] for i in q] for q in combinations(range(5),target)
                          if all(b in literal[a] for a,b in combinations(q,2))]
                actual,nodes=engine.query(0,labels,target=target)
                r.check(actual==expected,'exhaustive small literal/native mismatch')
                decisions+=1
    bad_native=[
        '1\n257\n',
        '1\n2\n1 1\n0\n',
        '1\n2\n1 0\n0\n',
        '1\n3\n2 2 1\n0\n0\n',
        '1\n2\n0\n0\n0 1 2000000 20000 2 0 0\n',
        '1\n2\n0\n0\n0 0 2000000 20000 2 0 1\n',
        '1\n2\n0\n0\n0 1 0 20000 2 0 1\n',
        '1\n2\n0\n0\n0 1 2000000 20000 1 2\n',
        '1\n2\n1 1\n1 0\n0 2 1 20000 2 0 1\n',
    ]
    for data in bad_native:
        result=subprocess.run([str(executable.resolve())],input=data,text=True,capture_output=True,timeout=3)
        r.check(result.returncode!=0 and not result.stdout.strip(),'invalid/guarded native job reported completion')
    # This also tests subset extraction from a maximal clique larger than
    # the target, at the eleven-clique rank used by the actual census.
    graph=[set(range(12))-{i} for i in range(12)]
    with Native(executable,[graph]) as engine:
        for target in (1,2,5,11,12,13):
            got,nodes=engine.query(0,list(range(12)),target=target)
            r.check(got==[list(q) for q in combinations(range(12),target)],'complete-clique subset census')
            decisions+=1
    result={'status':'PASSED','small_graphs':1024,'clique_decisions':decisions,
            'vertex_labels':labels,'native_bad_or_guard_rejections':len(bad_native)}
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--executable',type=Path,required=True)
    args=ap.parse_args()
    run(args.executable)
